import asyncio
from pprint import pprint

from service.parser import ChannelParser

CHANNEL_URL = 'https://rutube.ru/u/goblin/'


async def main():
    channel = await ChannelParser(
        channel_url=CHANNEL_URL,
        parse_video_amount=1000
    ).parse()

    pprint(channel)
    print(f'Name: {channel.title}')
    print(f'Url: {channel.channel_url}')
    print(f'Videos parsed: {len(channel.videos)}')


if __name__ == '__main__':
    asyncio.run(main())
