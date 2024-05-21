import asyncio
import re

import demjson3
import httpx

from bs4 import BeautifulSoup

from config import settings
from config import logger
from dto.channel import Channel
from dto.video import Video
from models.video import DESCRIPTION_MAX_LENGTH


class ChannelParser:
    def __init__(self, channel_url, parse_video_amount):
        self.url = channel_url
        self.parse_video_amount = parse_video_amount

    async def parse(self) -> Channel | None:
        try:
            async with httpx.AsyncClient(
                    headers={},
                    follow_redirects=True,
                    timeout=settings.rutube.timeout,
            ) as client:
                result: httpx.Response = await client.get(url=self.url)

            markup_data = await result.aread()
        except Exception as e:
            logger.error(f'exception: {e}, url: {self.url}')
            return None

        if result.status_code != 200:
            logger.error(f'status_code: {result.status_code}, url: {self.url}')
            return None

        soup: BeautifulSoup = BeautifulSoup(markup=markup_data, features="lxml")
        data: str = soup.find(name='script',
                              type='text/javascript',
                              string=re.compile(r'window\.version')
                              ).text

        s_index = data.find('{')
        f_index = data.rfind('}')
        js_obj_string = data[s_index:f_index + 1]

        information = demjson3.decode(js_obj_string)

        channel_id = information['userChannel']['info']['id']
        channel_title = information['userChannel']['info']['name']
        channel_videos_count = information['userChannel']['info']['video_count']

        pagination_urls = self.__prepare_pagination_urls(channel_id, channel_videos_count)

        tasks = []
        videos_to_get = (channel_videos_count
                         if self.parse_video_amount >= channel_videos_count
                         else self.parse_video_amount)

        for i, pagination_url in enumerate(pagination_urls):
            tasks.append(self.__process_page(pagination_url, i + 1, videos_to_get))
            videos_to_get -= settings.rutube.videos_per_page

        video_batches = sorted(await asyncio.gather(*tasks), key=lambda x: x['num'])

        videos = []
        for video_batch in video_batches:
            videos += video_batch['videos']

        return Channel(title=channel_title,
                       videos=videos,
                       channel_url=self.url
                       )

    def __prepare_pagination_urls(self, channel_id: int, channel_videos_count: int) -> list[str]:
        if channel_videos_count >= self.parse_video_amount:
            urls_amount = self.parse_video_amount // settings.rutube.videos_per_page
            if self.parse_video_amount % settings.rutube.videos_per_page != 0:
                urls_amount += 1
        else:
            urls_amount = channel_videos_count // settings.rutube.videos_per_page
            if channel_videos_count % settings.rutube.videos_per_page != 0:
                urls_amount += 1

        result = []
        for i in range(urls_amount):
            result.append(f'{settings.rutube.video_pagination_url}{i + 1}' % channel_id)

        return result

    async def __process_page(self, pagination_url: str, page: int, videos_to_get: int) -> dict:
        try:
            async with httpx.AsyncClient(
                    headers={
                        'Accept': 'application/json',
                    },
                    follow_redirects=True,
                    timeout=settings.rutube.timeout,
            ) as client:
                result: httpx.Response = await client.get(url=pagination_url)

            page_json = await result.aread()
        except Exception as e:  # rutube can cause ConnectTimeout
            logger.error(f'exception: {e}, url: {pagination_url}')
            return {
                "num": page,
                "videos": []
            }

        # 404 is possible if there are hidden or deleted videos on this channel
        # 503 is possible if there are too many requests
        # So this is a temporary solution
        if result.status_code != 200:
            logger.error(f'status_code: {result.status_code}, url: {pagination_url}')
            return {
                "num": page,
                "videos": []
            }

        page_info = demjson3.decode(page_json)

        videos = []
        for video in page_info['results']:
            if len(videos) == videos_to_get:
                break

            videos.append(Video(
                title=video['title'] if video["title"] else "",
                description=(video['description'][:DESCRIPTION_MAX_LENGTH]
                             if video['description'] else ""),
                views_count=video['hits'] if video['hits'] else 0,
                video_url=video['video_url'] if video['video_url'] else "",
            ))

        return {
            'num': page,
            'videos': videos
        }
