import asyncio
from datetime import datetime

import httpx

from bs4 import BeautifulSoup

from config import settings
from dto.channel import Channel
from dto.video import Video


class VideoParser:
    def __init__(self, url):
        self.url = url

    async def parse(self) -> Video:
        async with httpx.AsyncClient(
                headers={},
                follow_redirects=True
        ) as client:
            result: httpx.Response = await client.get(url=self.url)

        markup_data = await result.aread()

        if result.status_code != 200:
            raise Exception(f'Статус запроса: {result.status_code}')

        return Video(**self.__parse_html(markup_data),
                     video_url=self.url)

    def __parse_html(self, markup_data) -> dict[str, str]:
        soup: BeautifulSoup = BeautifulSoup(markup=markup_data, features="lxml")
        title = soup.find(
            name='section',
            attrs={'aria-label': 'название'}
        ).find('h1').text.replace('\xa0', ' ')

        try:
            description = soup.find(
                name='section',
                attrs={'aria-label': 'описание видео'}
            ).findChild('div').findChild('div').text.replace('\xa0', ' ')
        except AttributeError:
            description = ''

        views_count = soup.find(
            name='div',
            attrs={'role': 'region'}
        ).text.replace('\xa0', ' ')

        return {
            'title': title,
            'description': description[:99],
            'views_count': views_count
        }


class ChannelParser:
    def __init__(self, url):
        self.url = url

    async def parse(self) -> Channel:
        async with httpx.AsyncClient(
                headers={},
                follow_redirects=True
        ) as client:
            result: httpx.Response = await client.get(url=self.url)

        markup_data = await result.aread()

        if result.status_code != 200:
            raise Exception(f'Статус запроса: {result.status_code}')

        channel_info = self.__parse_html(markup_data, 100)

        tasks = []
        for video_url in channel_info['video_urls']:
            tasks.append(VideoParser(video_url).parse())

        videos = await asyncio.gather(*tasks)

        return Channel(
            title=channel_info['title'],
            channel_url=self.url,
            videos=list(videos),
        )

    def __parse_html(self, markup_data, limit) -> dict[str, str | list[str]]:
        soup: BeautifulSoup = BeautifulSoup(markup=markup_data, features="lxml")
        title = soup.findChild('div', {'class': 'wdp-feed-banner-module__wdp-feed-banner__title-wrapper'}).text
        videos = soup.find_all('a', {'class': 'wdp-link-module__link wdp-card-poster-module__posterWrapper'},
                               limit=limit)
        urls = []
        for video in videos:
            url = settings.rutube.url + video['href']
            urls.append(url)

        return {
            'title': title,
            'video_urls': urls
        }
