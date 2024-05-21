from repository.channel_repository import ChannelRepository
from repository.user_repository import UserRepository
from repository.video_repository import VideoRepository


class RepositoryManager:
    def __init__(self, session):
        self.session = session
        self.user_repository: UserRepository = UserRepository(self.session)
        self.channel_repository: ChannelRepository = ChannelRepository(self.session)
        self.video_repository: VideoRepository = VideoRepository(self.session)

    def commit(self):
        self.session.commit()

    def flush(self):
        self.session.flush()
