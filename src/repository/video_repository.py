from models.video import Video


class VideoRepository:
    def __init__(self, session):
        self.session = session

    def save(self, video: Video):
        self.session.add(video)

    def get_by_id(self, video_id) -> Video | None:
        return self.session.query(Video).filter_by(id=video_id).first()

    def list_for_channel_id(self, channel_id, page=1, per_page=10) -> dict[str, int | list[Video]]:
        query = self.session.query(Video).filter_by(channel_id=channel_id)
        total = query.count()  # Общее количество записей
        videos = query.offset((page - 1) * per_page).limit(per_page).all()
        return {
            'total': total,
            'page': page,
            'per_page': per_page,
            'videos': videos
        }

    def get_list_of_duplicate_urls(self, channel_id, urls: list[str]) -> list[str]:
        result = self.session.query(Video.video_url).filter_by(
            channel_id=channel_id
        ).filter(Video.video_url.in_(urls)).all()

        return [url[0] for url in result]
