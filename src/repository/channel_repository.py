from models.channel import Channel


class ChannelRepository:
    def __init__(self, session):
        self.session = session

    def save(self, channel: Channel):
        self.session.add(channel)

    def get_by_id(self, channel_id) -> Channel | None:
        return self.session.query(Channel).filter_by(id=channel_id).first()

    def get_by_user_id_and_url(self, user_id, channel_url) -> Channel | None:
        return self.session.query(Channel).filter_by(
            user_id=user_id,
            channel_url=channel_url
        ).first()

    def list_for_user_id(self, user_id, page=1, per_page=10) -> dict[str, int | list[Channel]]:
        query = self.session.query(Channel).filter_by(user_id=user_id)
        total = query.count()  # Общее количество записей
        channels = query.offset((page - 1) * per_page).limit(per_page).all()
        return {
            'total': total,
            'page': page,
            'per_page': per_page,
            'channels': channels
        }
