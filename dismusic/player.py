import asyncio

import async_timeout
import discord
import wavelink
from discord.ext import commands
from wavelink import Player

from .errors import InvalidLoopMode, NotEnoughSong, NothingIsPlaying


class DisPlayer(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.queue = asyncio.Queue()
        self.loop = "NONE"  # CURRENT, PLAYLIST
        self.currently_playing: wavelink.Track = None
        self.bound_channel = None
        self.player_is_invoking = False
        self.track_provider = "yt"

    async def destroy(self, player_id, force: bool = False) -> None:
        self.client.players.pop(player_id)

        await super().stop()
        await super().disconnect()

    async def do_next(self, force=False) -> None:
        if self.is_playing():
            return

        try:
            with async_timeout.timeout(300):
                track = await self.queue.get()
        except asyncio.TimeoutError:
            return await self.destroy()

        self.currently_playing = track
        await self.play(track)
        await self.invoke_player()

    async def set_loop(self, loop_type: str) -> None:
        valid_types = ["NONE", "CURRENT", "PLAYLIST"]

        if not self.is_playing() or not self.currently_playing:
            raise NothingIsPlaying("Player is not playing any track. Can't loop")

        if not loop_type:
            if valid_types.index(self.loop) >= 2:
                loop_type = "NONE"
            else:
                loop_type = valid_types[valid_types.index(self.loop) + 1]

            if loop_type == "PLAYLIST" and len(self.queue._queue) < 1:
                loop_type = "NONE"

        if loop_type.upper() == "PLAYLIST" and len(self.queue._queue) < 1:
            raise NotEnoughSong("There must be 2 songs in the queue in order to use the PLAYLIST loop")

        if loop_type.upper() not in valid_types:
            raise InvalidLoopMode("Loop type must be `NONE`, `CURRENT` or `PLAYLIST`.")

        self.loop = loop_type.upper()

        return self.loop

    async def invoke_player(self, ctx: commands.Context = None) -> None:
        track = self.currently_playing

        if not track:
            raise NothingIsPlaying("Player is not playing anything.")

        embed = discord.Embed(title=track.title, url=track.uri, color=discord.Color(0x2F3136))
        embed.set_author(name=track.author, url=track.uri, icon_url=self.client.user.display_avatar.url)
        try:
            embed.set_thumbnail(url=track.thumb)
        except AttributeError:
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/776345413132877854/940540758442795028/unknown.png"
            )
        embed.add_field(
            name="Length",
            value=f"{int(track.length // 60)}:{int(track.length % 60)}",
        )
        embed.add_field(name="Looping", value=self.loop)
        embed.add_field(name="Volume", value=self.volume)

        next_song = ""

        if self.loop == "CURRENT":
            next_song = self.currently_playing.title
        else:
            if len(self.queue._queue) > 0:
                next_song = self.queue._queue[0].title

        if next_song:
            embed.add_field(name="Next Song", value=next_song, inline=False)

        if not ctx:
            return await self.bound_channel.send(embed=embed)

        await ctx.send(embed=embed)
