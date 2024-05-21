from dto.channel import Channel as ChannelDto

from models.channel import Channel
from models.user import User
from models.video import Video
from repository.manager import RepositoryManager


class ParsedDataSaver:
    def __init__(self, repo: RepositoryManager):
        self.__repo = repo

    def save_channel(self, user: User, channel_dto: ChannelDto):
        channel = self.__repo.channel_repository.get_by_user_id_and_url(
            user_id=user.id,
            channel_url=channel_dto.channel_url
        )

        if not channel:
            self.__new_channel(user=user, dto=channel_dto)
        else:
            self.__update_channel(channel=channel, dto=channel_dto)

    def __new_channel(self, user: User, dto: ChannelDto):
        channel = Channel(
            title=dto.title,
            channel_url=dto.channel_url,
            user_id=user.id,
        )
        self.__repo.channel_repository.save(channel)
        self.__repo.flush()

        for video_dto in dto.videos:
            video = Video(
                title=video_dto.title,
                description=video_dto.description,
                video_url=video_dto.video_url,
                views_count=video_dto.views_count,
                channel_id=channel.id,
            )

            self.__repo.video_repository.save(video)

        self.__repo.flush()
        self.__repo.commit()

    def __update_channel(self, channel: Channel, dto: ChannelDto):
        channel.title = dto.title
        self.__repo.channel_repository.save(channel)

        video_urls = [video.video_url for video in dto.videos]
        already_exist_video_urls = self.__repo.video_repository.get_list_of_duplicate_urls(
            channel_id=channel.id,
            urls=video_urls
        )
        for video_dto in dto.videos:
            if video_dto.video_url in already_exist_video_urls:
                continue
            video = Video(
                title=video_dto.title,
                description=video_dto.description,
                video_url=video_dto.video_url,
                views_count=video_dto.views_count,
                channel_id=channel.id,
            )

            self.__repo.video_repository.save(video)
        self.__repo.flush()
        self.__repo.commit()
