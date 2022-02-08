from discord.ext import commands

from .errors import (
    InvalidLoopMode,
    MustBeSameChannel,
    NotConnectedToVoice,
    NotEnoughSong,
    NothingIsPlaying,
    PlayerNotConnected,
)
from .player import DisPlayer


class MusicEvents(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def handle_end_stuck_exception(self, player: DisPlayer):
        if player.loop == "CURRENT":
            return await player.play(player.currently_playing)

        if player.loop == "PLAYLIST":
            await player.queue.put(player.currently_playing)

        player.currently_playing = None
        player._source = None
        await player.do_next()

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player, *args, **kwargs):
        await self.handle_end_stuck_exception(player)

    @commands.Cog.listener()
    async def on_wavelink_track_exception(self, player, *args, **kwargs):
        await self.handle_end_stuck_exception(player)

    @commands.Cog.listener()
    async def on_wavelink_track_stuck(self, player, *args, **kwargs):
        await self.handle_end_stuck_exception(player)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        errors = (
            InvalidLoopMode,
            MustBeSameChannel,
            NotConnectedToVoice,
            PlayerNotConnected,
            NothingIsPlaying,
            NotEnoughSong,
        )

        if isinstance(error, errors):
            await ctx.send(error)
        else:
            return
