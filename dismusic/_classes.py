from dataclasses import asdict, dataclass
from typing import Union

from wavelink import SoundCloudTrack, YouTubeMusicTrack, YouTubePlaylist, YouTubeTrack
from wavelink.ext.spotify import SpotifyTrack

Provider = Union[
    YouTubeTrack, YouTubePlaylist, YouTubeMusicTrack, SoundCloudTrack, SpotifyTrack
]


@dataclass
class Emojis:
    PREV = "⬅️"
    NEXT = "➡️"
    FIRST = "⏮️"
    LAST = "⏭️"


@dataclass
class Loop:
    NONE = "NONE"
    CURRENT = "CURRENT"
    PLAYLIST = "PLAYLIST"

    TYPES = [NONE, CURRENT, PLAYLIST]


@dataclass
class LavalinkConfig:
    host: str
    port: Union[int, str]
    password: str

    def asdict(self):
        return asdict(self)


@dataclass
class SpotifyCredeentials:
    client_id: str
    client_secret: str

    def asdict(self):
        return asdict(self)

    @staticmethod
    def default():
        return {"client_id": "", "client_secret": ""}
