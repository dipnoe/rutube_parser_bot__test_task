import asyncio
import functools

from bot.bot import Bot
from config import settings, logger
from config.db import get_db
from repository.manager import RepositoryManager


def retry_on_exception_async(max_retries=2, delay=1, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    logger.error(f"Attempt {attempts} failed "
                                 f"with exception: {e}. "
                                 f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
            logger.fatal(f"All {max_retries} attempts failed.")
            raise  # pylint: disable=misplaced-bare-raise

        return wrapper

    return decorator


@retry_on_exception_async(10, 5)
async def run() -> None:
    with get_db() as session:
        repo = RepositoryManager(session)
        bot = Bot(settings=settings, repo=repo)
        await bot.start()
