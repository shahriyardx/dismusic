import os

from discord.ext import commands
from discord.ext.commands.context import Context
from dotenv import load_dotenv

load_dotenv(".env")
bot = commands.Bot(command_prefix="?")

bot.lavalink_nodes = [
    {"host": "losingtime.dpaste.org", "port": 2124, "password": "SleepingOnTrains"},
    # Can have multiple nodes here
]

# If you want to use spotify search
bot.spotify_credentials = {
    "client_id": "CLIENT_ID_HERE",
    "client_secret": "CLIENT_SECRET_HERE",
}


@bot.event
async def on_ready():
    print(f"{bot.user} is ready")


@bot.command()
async def rickroll(ctx: Context):
    """Never gonna give you up"""
    await ctx.invoke(
        bot.get_command("play"), query="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )
    await ctx.send("Never gonna give you up")


@bot.command()
async def kids(ctx: Context):
    """Test playlist playing"""
    await ctx.invoke(
        bot.get_command("play"),
        query="https://www.youtube.com/playlist?list=PL2MHGlY_k-FG_Wc83QiOWj1-P5aXv-Tsm",
    )
    await ctx.send("Some kids song added for you")


bot.load_extension("dismusic")
bot.load_extension("jishaku")
bot.run(os.getenv("TOKEN"))
