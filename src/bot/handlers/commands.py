from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram import html, Dispatcher

from bot.keyboards.inline import InlineKeyboard
from bot.states import Form
from config import logger
from config.settings import AppSettings
from models.user import User
from repository.manager import RepositoryManager


class Commands:
    def __init__(self, dp: Dispatcher, settings: AppSettings, repo: RepositoryManager):
        self.__dp = dp
        self.__repo = repo
        self.__settings = settings
        self.__inline = InlineKeyboard(settings=settings, repo=repo)

    async def start(self, message: Message):
        user = self.__repo.user_repository.get_by_telegram_id(message.from_user.id)
        if not user:
            user = User(telegram_id=str(message.from_user.id))
            self.__repo.user_repository.save(user=user)
            self.__repo.flush()
            self.__repo.commit()

            logger.info(f"new user created: id: {user.id}, telegram_id: {user.telegram_id}")

        await message.answer(f'Привет, {html.bold(message.from_user.full_name)}!\n'
                             f'В прошлой жизни я рвал цветы и ел детей. А сейчас я паршу видео с  Rutube!')

    async def parse_channel(self, message: Message, state: FSMContext):
        await message.answer('Пришлите ссылку на канал, который нужно спарсить.')
        await state.set_state(Form.waiting_for_link)

    async def show_channels(self, message: Message):
        await message.answer(
            'Каналы, которые вы парсили.',
            reply_markup=self.__inline.create_channels_keyboard(message.from_user.id)
        )

    def register_commands(self):
        self.__dp.message.register(self.start, CommandStart())
        self.__dp.message.register(self.parse_channel, Command('parse_channel'))
        self.__dp.message.register(self.show_channels, Command('show_channels'))
