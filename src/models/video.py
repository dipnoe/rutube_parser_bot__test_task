from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from config.db import Base

DESCRIPTION_MAX_LENGTH = 100

class Video(Base):
    __tablename__ = "videos"
    __table_args__ = (
        UniqueConstraint('channel_id', 'video_url', name='uix_channel_video'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=False)
    description = Column(String(DESCRIPTION_MAX_LENGTH), nullable=False, unique=False)
    video_url = Column(String, nullable=False, unique=False)
    views_count = Column(Integer, nullable=False, unique=False)

    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False, unique=False)
    channel = relationship("Channel", back_populates="videos")
