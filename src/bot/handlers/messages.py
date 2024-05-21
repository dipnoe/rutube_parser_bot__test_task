from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import settings
from bot.states import Form
from config.settings import AppSettings
from repository.manager import RepositoryManager


class Messages:
    def __init__(self, dp: Dispatcher, settings: AppSettings, repo: RepositoryManager):
        self.__dp = dp
        self.__repo = repo
        self.__settings = settings

    async def process_link(self, message: Message, state: FSMContext):
        link: str = message.text
        if not link.startswith(settings.rutube.url):
            await message.reply('Эта ссылка не с Rutube`a')
            return
        await state.update_data(link=link)
        await message.answer("Спасибо! Теперь укажите количество видео для парсинга.")
        await state.set_state(Form.waiting_for_videos_amount)

    async def process_videos_amount(self, message: Message, state: FSMContext):
        number = message.text
        if number.isdigit():
            num_number = int(number)
        else:
            await message.reply('Это не число!')
            return
        data = await state.get_data()
        link = data.get('link')
        result = f"Ссылка: {link}\nКоличество видео для парсинга: {num_number}"

        await message.answer(f"Спасибо! Сейчас пришлю видео:\n{result}")

        await state.clear()

    def register_messages(self):
        self.__dp.message.register(Form.waiting_for_link)
        self.__dp.message.register(Form.waiting_for_videos_amount)
