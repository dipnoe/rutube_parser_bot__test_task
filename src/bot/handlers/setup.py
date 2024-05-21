from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand


class Setups:
    def __init__(self, dp: Dispatcher, bot: Bot):
        self.__dp = dp
        self.__bot = bot

    async def set_commands(self):
        commands = [
            BotCommand(
                command='parse_channel',
                description='Парсинг rutube канала'
            ),
            BotCommand(
                command='show_channels',
                description='Показать мои каналы'
            )

        ]

        await self.__bot.set_my_commands(commands=commands)

    def register_setup(self):
        self.__dp.startup.register(self.set_commands)
