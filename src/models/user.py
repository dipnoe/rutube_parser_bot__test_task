from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    telegram_id = Column(String, index=True, nullable=False, unique=True)
    channels = relationship("Channel", back_populates="user")
