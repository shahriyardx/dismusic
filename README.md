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
    {"host": "losingtime.dpaste.org", "port": 2124, "password": "SleepingOnTrains"},
    # Can have multiple nodes here
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
{"host": "lavalink.eu", "port": 2333, "password": "Raccoon"} # Does not work sometimes
{"host": "losingtime.dpaste.org", "port": 2124, "password": "SleepingOnTrains"}
{"host": "lava.link", "port": 80, "password": "dismusic"}
{"host": "lavalink.islantay.tk", "port": 8880, "password": "waifufufufu"}

# SSL
{"host": "lavalink.devz.cloud", "port": 443, "password": "mathiscool", "https": True},
{"host": "lavalink2.devz.cloud", "port": 443, "password": "mathiscool", "https": True},
{"host": "disbotlistlavalink.ml", "port": 443, "password": "LAVA", "https": True},
{"host": "lavalink.scpcl.site", "port": 443, "password": "lvserver", "https": True},
{"host": "lavalink.mariliun.ml", "port": 443, "password": "lavaliun", "https": True},
{"host": "lavalinkinc.ml", "port": 443, "password": "incognito", "https": True},
{"host": "node1.lavalink.trgop.gq", "port": 443, "password": "onionispro", "https": True},
{"host": "node3.lavalink.trgop.gq", "port": 443, "password": "onionop", "https": True},
{"host": "node5.lavalink.trgop.gq", "port": 443, "password": "htandsm", "https": True},
{"host": "www.lavalinknodepublic.ml", "port": 443, "password": "mrextinctcodes", "https": True},
{"host": "www.lavalinknodepublic2.ml", "port": 443, "password": "mrextinctcodes", "https": True},
{"host": "lavalink.cobaltonline.net", "port": 443, "password":"cobaltlavanode23@", "https": True},
```

[Join Discord](https://discord.gg/7SaE8v2) For any kind of help