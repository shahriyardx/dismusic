import os

from discord import Intents
from discord.ext import commands
from discord.ext.commands.context import Context
from dotenv import load_dotenv
from dismusic import init_dismusic
from dismusic.models import LavalinkConfig, SpotifyCredentials

load_dotenv(".env")

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents=intents)

init_dismusic(
    bot,
    lavalink_nodes=[
        LavalinkConfig(
            host="lavalink.oops.wtf", port=2000, password="www.freelavalink.ga"
        )
        # Can have multiple nodes here
    ],
    spotify_credentials=SpotifyCredentials.default(),
)


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


bot.load_extension("dismusic.cogs.prefix")
bot.run(os.getenv("TOKEN"))
