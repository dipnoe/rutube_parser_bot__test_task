from dataclasses import dataclass

from dto.video import Video


@dataclass
class Channel:
    title: str
    videos: list[Video]
    channel_url: str
