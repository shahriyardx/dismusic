# dismusic
Music cog for discord bots. Supports YouTube, YoutubeMusic, SoundCloud and Spotify.

# Installation
```sh
python3 -m pip install dismusic
```

# Usage

```python
from discord.ext import commands

bot = commands.Bot(command_prefix='..')

bot.lavalink_nodes = [
    {"host": "lavalink.eu", "port": 2333, "password": "Raccoon"}
]

# If you want to use spotify search
bot.spotify_credentials = {
    'client_id': 'CLIENT_ID_HERE', 
    'client_secret': 'CLIENT_SECRET_HERE'
}

bot.load_extension('dismusic')
bot.run('TOKEN')
```

# Commands

**connect** - `Connect to vc` \
**disconnect** - `Disconnect from vc` 

**play** - `Play a song or playlist` \
**pause** - `Pause player` \
**resume** - `Resume player`

**seek** - `Seek player` \
**nowplaying** - `Now playing` \
**queue** - `See queue` \
**volume** - `Set volume` \
**loop** - `Loop song/playlist`

> Filter commands coming soon.

# Lavalink Configs
```py
# No SSL/HTTPS
{"host": "lavalink.eu", "port": 2333, "password": "Raccoon"}
{"host": "losingtime.dpaste.org", "port": 2124, "password": "SleepingOnTrains"}
{"host": "lava.link", "port": 80, "password": "dismusic"}
{"host": "lavalink.islantay.tk", "port": 8880, "password": "waifufufufu"}
```

[Join Discord](https://discord.gg/7SaE8v2) For any kind of help