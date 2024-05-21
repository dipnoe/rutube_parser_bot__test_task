from models.user import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    def save(self, user: User):
        self.session.add(user)

    def get_by_id(self, user_id) -> User | None:
        return self.session.query(User).filter_by(id=user_id).first()

    def get_by_telegram_id(self, telegram_id) -> User | None:
        return self.session.query(User).filter_by(telegram_id=telegram_id).first()
