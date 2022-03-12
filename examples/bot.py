import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv(".env")
bot = commands.Bot(command_prefix='?')

bot.lavalink_nodes = [
    {"host": "losingtime.dpaste.org", "port": 2124, "password": "SleepingOnTrains"},
    # Can have multiple nodes here
]

# If you want to use spotify search
bot.spotify_credentials = {
    'client_id': 'CLIENT_ID_HERE',
    'client_secret': 'CLIENT_SECRET_HERE'
}

@bot.event
async def on_ready():
    print(f"{bot.user} is ready")

bot.load_extension('dismusic')
bot.load_extension('jishaku')
bot.run(os.getenv("TOKEN"))