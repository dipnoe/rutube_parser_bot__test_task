from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from config.db import Base

DESCRIPTION_MAX_LENGTH = 100

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String(DESCRIPTION_MAX_LENGTH), nullable=False)
    video_url = Column(String, nullable=False, unique=True)
    views_count = Column(Integer, nullable=False)

    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    channel = relationship("Channel", back_populates="videos")
