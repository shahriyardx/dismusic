from copyreg import constructor
from typing import List, Optional
from .models import LavalinkConfig, SpotifyCredentials


def init_dismusic(
    bot,
    lavalink_nodes: List[LavalinkConfig],
    spotify_credentials: Optional[SpotifyCredentials],
):
    bot.lavalink_nodes = [
        (node.asdict() if isinstance(node, LavalinkConfig) else node)
        for node in lavalink_nodes
    ]

    bot.spotify_credentials = (
        (
            spotify_credentials.asdict()
            if isinstance(spotify_credentials, SpotifyCredentials)
            else spotify_credentials
        )
        if spotify_credentials
        else SpotifyCredentials.default()
    )
