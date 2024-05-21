from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from config.db import Base


class Channel(Base):
    __tablename__ = "channels"
    __table_args__ = (
        UniqueConstraint('user_id', 'channel_url', name='uix_user_channel'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=False)
    channel_url = Column(String, nullable=False, unique=False)
    videos = relationship("Video", back_populates="channel")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=False)
    user = relationship("User", back_populates="channels")
