import asyncio
import random

from config.db import get_db
from models.user import User
from repository.manager import RepositoryManager
from service.data_saver import ParsedDataSaver
from service.parser import ChannelParser

CHANNEL_URL = 'https://rutube.ru/u/goblin/'


async def main():
    with get_db() as session:
        repo = RepositoryManager(session)

        user = User(
            id=3,
            telegram_id=random.randint(1, 1000000)
        )

        channel = await ChannelParser(
            channel_url=CHANNEL_URL,
            parse_video_amount=1002
        ).parse()

        print(f'Name: {channel.title}')
        print(f'Url: {channel.channel_url}')
        print(f'Videos parsed: {len(channel.videos)}')

        ParsedDataSaver(repo=repo).save_channel(user=user, channel_dto=channel)


if __name__ == '__main__':
    asyncio.run(main())
