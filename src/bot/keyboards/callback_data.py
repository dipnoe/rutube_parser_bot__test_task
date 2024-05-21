from aiogram.filters.callback_data import CallbackData


class ChannelCallback(CallbackData, prefix="channel"):
    channel_id: int


class VideoCallback(CallbackData, prefix='video'):
    video_id: int


class VideoPaginationCallback(CallbackData, prefix='video_pagination'):
    page: int
    channel_id: int


class ChannelPaginationCallback(CallbackData, prefix='channel_pagination'):
    page: int
    user_id: int
