from typing import List, Optional
from ._classes import LavalinkConfig, SpotifyCredeentials


def init_dismusic(
    bot,
    lavalink_nodes: List[LavalinkConfig],
    spotify_credentials: Optional[SpotifyCredeentials],
):
    bot.lavalink_nodes = [node.asdict() for node in lavalink_nodes]
    bot.spotify_credentials = (
        spotify_credentials.asdict()
        if spotify_credentials
        else SpotifyCredeentials.default()
    )
