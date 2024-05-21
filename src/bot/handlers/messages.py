from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from celery_tasks.tasks import save_parsed_data
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
        video_amount = message.text
        if video_amount.isdigit():
            video_amount = int(video_amount)
        else:
            await message.reply('Это не число!')
            return
        data = await state.get_data()
        link = data.get('link')
        result = f"Ссылка: {link}\nКоличество видео для парсинга: {video_amount}"

        save_parsed_data.delay(
            telegram_user_id=message.from_user.id,
            channel_url=link,
            video_amount=video_amount
        )

        await message.answer(f"Спасибо! Сейчас пришлю видео:\n{result}")

        await state.clear()

    def register_messages(self):
        self.__dp.message.register(self.process_link, Form.waiting_for_link)
        self.__dp.message.register(self.process_videos_amount, Form.waiting_for_videos_amount)
