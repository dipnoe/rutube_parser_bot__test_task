import asyncio

from celery import Celery
from config import settings
from config.db import get_db
from repository.manager import RepositoryManager
from repository.user_repository import UserRepository
from service.data_saver import ParsedDataSaver
from service.parser import ChannelParser

celery = Celery('celery_tasks', broker=settings.redis.redis_url)


@celery.task
def parse_data(telegram_user_id: int, channel_url: str, video_amount: int):
    asyncio.run(wrapped(telegram_user_id, channel_url, video_amount))


async def wrapped(telegram_user_id: int, channel_url: str, video_amount: int):
    channel_dto = await ChannelParser(
        channel_url=channel_url,
        parse_video_amount=video_amount
    ).parse()

    with get_db() as session:
        repo = RepositoryManager(session)

        user = UserRepository(session=session).get_by_telegram_id(telegram_id=str(telegram_user_id))

        ParsedDataSaver(repo=repo).save_channel(
            user=user,
            channel_dto=channel_dto
        )
