from dataclasses import dataclass
from typing import Union

from wavelink import (SoundCloudTrack, YouTubeMusicTrack, YouTubePlaylist,
                      YouTubeTrack)
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
