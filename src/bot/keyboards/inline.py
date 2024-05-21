from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import settings
from bot.keyboards.callback_data import ChannelCallback, VideoCallback, VideoPaginationCallback, \
    ChannelPaginationCallback
from config.settings import AppSettings
from repository.manager import RepositoryManager


class InlineKeyboard:
    def __init__(self, settings: AppSettings, repo: RepositoryManager):
        self.__settings = settings
        self.__repo = repo

    def create_channels_keyboard(self, user_tg_id, page: int = 0):
        page_size = self.__settings.bot.page_size
        user = self.__repo.user_repository.get_by_telegram_id(telegram_id=user_tg_id)

        builder = InlineKeyboardBuilder()

        channels = self.__repo.channel_repository.list_for_user_id(
            user_id=user.id,
            page=page + 1,
            per_page=page_size
        )

        for channel in channels["channels"]:
            builder.button(
                text=channel.title,
                callback_data=ChannelCallback(channel_id=channel.id)
            )

        if page > 0:
            builder.button(
                text=self.__settings.bot.backwards,
                callback_data=ChannelPaginationCallback(page=page - 1, user_id=user.id)
            )

        if (page + 1) * page_size < channels['total']:
            builder.button(
                text=self.__settings.bot.forwards,
                callback_data=ChannelPaginationCallback(page=page + 1, user_id=user.id)
            )

        total_pages = channels['total'] // page_size
        if channels['total'] % page_size > 0:
            total_pages += 1

        builder.button(
            text=f'{page + 1}/{total_pages}',
            callback_data="noop"
        )

        builder.adjust(1, 1)

        return builder.as_markup()

    def create_videos_keyboard(self, channel_id, page=0) -> InlineKeyboardMarkup:
        page_size = self.__settings.bot.page_size
        channel_videos = self.__repo.video_repository.list_for_channel_id(
            channel_id=channel_id,
            page=page + 1,
            per_page=page_size
        )

        builder = InlineKeyboardBuilder()

        for video in channel_videos["videos"]:
            builder.button(
                text=video.title,
                callback_data=VideoCallback(video_id=video.id)
            )

        if page > 0:
            builder.button(
                text=self.__settings.bot.backwards,
                callback_data=VideoPaginationCallback(page=page - 1, channel_id=channel_id)
            )

        if (page + 1) * page_size < channel_videos['total']:
            builder.button(
                text=self.__settings.bot.forwards,
                callback_data=VideoPaginationCallback(page=page + 1, channel_id=channel_id)
            )

        total_pages = channel_videos['total'] // page_size
        if channel_videos['total'] % page_size > 0:
            total_pages += 1

        builder.button(
            text=f'{page + 1}/{total_pages}',
            callback_data="noop"
        )

        builder.adjust(1, 1)

        return builder.as_markup()
