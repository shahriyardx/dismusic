from typing import Union
from wavelink import (SoundCloudTrack,
                      YouTubeMusicTrack, YouTubeTrack)
from wavelink.ext.spotify import SpotifyTrack

Provider = Union[YouTubeTrack, YouTubeMusicTrack, SoundCloudTrack, SpotifyTrack]
