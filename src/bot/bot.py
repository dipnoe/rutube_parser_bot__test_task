from aiogram import Dispatcher, Bot as BaseBot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.handlers.callbacks import Callbacks
from bot.handlers.commands import Commands
from bot.handlers.messages import Messages
from bot.handlers.setup import Setups
from config import logger
from config.settings import AppSettings
from repository.manager import RepositoryManager


class Bot:
    def __init__(self, settings: AppSettings, repo: RepositoryManager) -> None:
        self.__settings = settings
        self.__repo = repo
        self.__dp = Dispatcher()
        self.__bot = BaseBot(
            token=settings.bot.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

    async def start(self) -> None:
        Commands(dp=self.__dp, settings=self.__settings, repo=self.__repo).register_commands()
        Messages(dp=self.__dp, settings=self.__settings, repo=self.__repo).register_messages()
        Callbacks(dp=self.__dp, settings=self.__settings, repo=self.__repo).register_callbacks()
        await Setups(self.__dp, self.__bot).set_commands()

        logger.info("Bot starting...")
        await self.__dp.start_polling(self.__bot)
