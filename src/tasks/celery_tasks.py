import asyncio
import os
import sys

from aiogram import Bot

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from celery import Celery  # noqa
from config import settings  # noqa
from config.db import get_db  # noqa
from repository.manager import RepositoryManager  # noqa
from repository.user_repository import UserRepository  # noqa
from service.data_saver import ParsedDataSaver  # noqa
from service.parser import ChannelParser  # noqa

celery = Celery('celery_tasks', broker=settings.redis.redis_url)


@celery.task(name='tasks.celery_tasks.parse_data')
def parse_data(telegram_user_id: int, channel_url: str, video_amount: int):
    asyncio.run(wrapped(telegram_user_id, channel_url, video_amount))


async def wrapped(telegram_user_id: int, channel_url: str, video_amount: int):
    bot: Bot = Bot(token=settings.bot.token)

    channel_dto = await ChannelParser(channel_url=channel_url,
                                      parse_video_amount=video_amount).parse()

    if not channel_dto:
        await bot.send_message(chat_id=telegram_user_id, text='Произошла ошибка при парсинге.')

    with get_db() as session:
        repo = RepositoryManager(session)

        user = UserRepository(session=session).get_by_telegram_id(telegram_id=str(telegram_user_id))

        ParsedDataSaver(repo=repo).save_channel(user=user,
                                                channel_dto=channel_dto)

    await bot.send_message(chat_id=telegram_user_id,
                           text=f'Видео спарсились. Количество: {len(channel_dto.videos)}')
