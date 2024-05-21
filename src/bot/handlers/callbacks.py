from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery

from bot.keyboards.callback_data import ChannelCallback, VideoCallback, VideoPaginationCallback, \
    ChannelPaginationCallback
from bot.keyboards.inline import InlineKeyboard
from config.settings import AppSettings
from repository.manager import RepositoryManager


class Callbacks:
    def __init__(self, dp: Dispatcher, settings: AppSettings, repo: RepositoryManager):
        self.__dp = dp
        self.__repo = repo
        self.__settings = settings
        self.__inline = InlineKeyboard(settings=settings, repo=repo)

    async def handler_channel_callback(self, query: CallbackQuery, callback_data: ChannelCallback):
        channel_id: int = callback_data.channel_id
        keyboard = self.__inline.create_videos_keyboard(channel_id)
        channel = self.__repo.channel_repository.get_by_id(channel_id=channel_id)

        await query.message.answer(f"Видео канала {channel.title}:", reply_markup=keyboard)

    async def handle_video_callback(self, call: CallbackQuery, callback_data: VideoCallback):
        video_id: int = callback_data.video_id
        video = self.__repo.video_repository.get_by_id(video_id=video_id)
        if video:
            await call.message.answer(f"📺 <b>{video.title}</b>\n\n"
                                      f"{video.description}\n\n"
                                      f"Просмотры: <b>{video.views_count}</b>\n\n"
                                      f"Ссылка:\n{video.video_url}")

    async def handle_channel_pagination_callback(self, call: CallbackQuery, callback_data: ChannelPaginationCallback):
        user_id: int = callback_data.user_id
        page: int = callback_data.page
        keyboard = self.__inline.create_channels_keyboard(user_tg_id=user_id, page=page)

        await call.message.edit_reply_markup(reply_markup=keyboard)

    async def handle_video_pagination_callback(self, call: CallbackQuery, callback_data: VideoPaginationCallback):
        channel_id: int = callback_data.channel_id
        page: int = callback_data.page
        keyboard = self.__inline.create_videos_keyboard(channel_id=channel_id, page=page)

        await call.message.edit_reply_markup(reply_markup=keyboard)

    def register_callbacks(self):
        self.__dp.callback_query.register(self.handler_channel_callback, ChannelCallback.filter())
        self.__dp.callback_query.register(self.handle_video_callback, VideoCallback.filter())
        self.__dp.callback_query.register(self.handle_channel_pagination_callback, ChannelPaginationCallback.filter())
        self.__dp.callback_query.register(self.handle_video_pagination_callback, VideoPaginationCallback.filter())
