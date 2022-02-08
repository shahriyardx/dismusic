import asyncio
import wavelink
from discord import Color, Embed, ClientException
from discord.ext import commands
from wavelink.ext import spotify

from .checks import voice_channel_player, voice_connected
from .errors import MustBeSameChannel
from .player import DisPlayer


class Music(commands.Cog):
    """Music commands"""

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.bot.players = dict()
        self.bot.nodes = list()
        self.bot.loop.create_task(self.start_nodes())

    async def play_track(self, ctx: commands.Context, query: str, provider=None):
        player: DisPlayer = self.bot.players[ctx.guild.id]

        if ctx.author.voice.channel.id != player.channel.id:
            raise MustBeSameChannel("You must be in the same voice channel as the player.")

        track_provider = {
            "yt": wavelink.YouTubeTrack,
            "ytmusic": wavelink.YouTubeMusicTrack,
            "soundcloud": wavelink.SoundCloudTrack,
            "spotify": spotify.SpotifyTrack,
        }

        msg = await ctx.send(f"Searching for `{query}` :mag_right:")

        provider = track_provider.get(provider) if provider else track_provider.get(player.track_provider)

        try:
            track = await provider.search(query, return_first=True)
        except:
            track = None

        if not track:
            return await msg.edit("No song/track found with given query.")

        await msg.edit(content=f"Added `{track.title}` to queue. ")
        await player.queue.put(track)

        await player.do_next()

    async def start_nodes(self):
        await self.bot.wait_until_ready()
        spotify_credential = getattr(self.bot, "spotify_credentials", {"client_id": "", "client_secret": ""})

        for config in self.bot.lavalink_nodes:
            try:
                node: wavelink.Node = await wavelink.NodePool.create_node(
                    bot=self.bot, **config, spotify_client=spotify.SpotifyClient(**spotify_credential)
                )
                print(f"[dismusic] INFO - Created node: {node.identifier}")
            except Exception:
                print(f"[dismusic] ERROR - Failed to create node {config['host']}:{config['port']}")

    @commands.command(aliases=["con"])
    @voice_connected()
    async def connect(self, ctx: commands.Context):
        """Connect the player"""
        if ctx.guild.id in self.bot.players:
            return

        msg = await ctx.send(f"Connecting to **`{ctx.author.voice.channel}`**")

        try:
            player: DisPlayer = await ctx.author.voice.channel.connect(cls=DisPlayer)
        except (asyncio.TimeoutError, ClientException):
            return await msg.edit(content="Failed to connect to voice channel.")

        player.bound_channel = ctx.channel
        player.bot = self.bot

        self.bot.players[ctx.guild.id] = player

        await msg.edit(content=f"Connected to **`{player.channel.name}`**")

    @commands.group(aliases=["p"], invoke_without_command=True)
    @voice_connected()
    async def play(self, ctx: commands.Context, *, query: str):
        """Play or add song to queue (Defaults to YouTube)"""
        await ctx.invoke(self.connect)
        await self.play_track(ctx, query)

    @play.command(aliases=["yt"])
    async def youtube(self, ctx: commands.Context, *, query: str):
        """Play a YouTube track"""
        await ctx.invoke(self.connect)
        await self.play_track(ctx, query, "yt")

    @play.command(aliases=["ytmusic"])
    async def youtubemusic(self, ctx: commands.Context, *, query: str):
        """Play a YouTubeMusic track"""
        await ctx.invoke(self.connect)
        await self.play_track(ctx, query, "ytmusic")

    @play.command(aliases=["sc"])
    async def soundcloud(self, ctx: commands.Context, *, query: str):
        """Play a SoundCloud track"""
        await ctx.invoke(self.connect)
        await self.play_track(ctx, query, "soundcloud")

    @play.command(aliases=["sp"])
    async def spotify(self, ctx: commands.Context, *, query: str):
        """play a spotify track"""
        await ctx.invoke(self.connect)
        await self.play_track(ctx, query, "spotify")

    @commands.command(aliases=["vol"])
    @voice_channel_player()
    async def volume(self, ctx: commands.Context, vol: int, forced=False):
        """Set volume"""
        player: DisPlayer = self.bot.players[ctx.guild.id]

        if vol < 0:
            return await ctx.send("Volume can't be less than 0")

        if vol > 100 and not forced:
            return await ctx.send("Volume can't greater than 100")

        await player.set_volume(vol)
        await ctx.send(f"Volume set to {vol} :loud_sound:")

    @commands.command(aliases=["disconnect", "dc"])
    @voice_channel_player()
    async def stop(self, ctx: commands.Context):
        """Stop the player"""
        player: DisPlayer = self.bot.players[ctx.guild.id]

        await player.destroy(ctx.guild.id)
        await ctx.send("Stopped the player :stop_button: ")

    @commands.command()
    @voice_channel_player()
    async def pause(self, ctx: commands.Context):
        """Pause the player"""
        player: DisPlayer = self.bot.players[ctx.guild.id]

        if player.is_playing():
            if player.is_paused():
                return await ctx.send("Player is already paused.")

            await player.set_pause(pause=True)
            return await ctx.send("Paused :pause_button: ")

        await ctx.send("Player is not playing anything.")

    @commands.command()
    @voice_channel_player()
    async def resume(self, ctx: commands.Context):
        """Resume the player"""
        player: DisPlayer = self.bot.players[ctx.guild.id]

        if player.is_playing():
            if not player.is_paused():
                return await ctx.send("Player is already playing.")

            await player.set_pause(pause=False)
            return await ctx.send("Resumed :musical_note: ")

        await ctx.send("Player is not playing anything.")

    @commands.command()
    @voice_channel_player()
    async def skip(self, ctx: commands.Context):
        """Skip to next song in the queue."""
        player: DisPlayer = self.bot.players[ctx.guild.id]

        if player.loop == "CURRENT":
            player.loop = "NONE"

        await player.stop()

        await ctx.send("Skipped :track_next:")

    @commands.command()
    @voice_channel_player()
    async def seek(self, ctx: commands.Context, seconds: int):
        """Seek the player backward or forward"""
        player: DisPlayer = self.bot.players[ctx.guild.id]

        if player.is_playing():
            position = player.position + seconds
            if position > player.currently_playing.length:
                return await ctx.send("Can't seek past the end of the track.")

            if position < 0:
                position = 0

            await player.seek(position * 1000)
            return await ctx.send(f"Seeked to {seconds} seconds :fast_forward: ")

        await ctx.send("Player is not playing anything.")

    @commands.command()
    @voice_channel_player()
    async def loop(self, ctx: commands.Context, loop_type: str = None):
        """Set loop to `NONE`, `CURRENT` or `PLAYLIST`"""
        player: DisPlayer = self.bot.players[ctx.guild.id]

        result = await player.set_loop(loop_type)
        await ctx.send(f"Loop has been set to {result} :repeat: ")

    @commands.command(aliases=["q"])
    @voice_channel_player()
    async def queue(self, ctx: commands.Context):
        """Player queue"""
        player: DisPlayer = self.bot.players[ctx.guild.id]

        if len(player.queue._queue) < 1:
            return await ctx.send("Nothing is in the queue.")

        embed = Embed(color=Color(0x2F3136))
        embed.set_author(
            name="Queue",
            icon_url="https://cdn.discordapp.com/attachments/776345413132877854/940247400046542948/list.png",
        )

        tracks = ""
        if player.loop == "CURRENT":
            next_song = f"Next > [{player.currently_playing.title}]({player.currently_playing.uri}) \n\n"
        else:
            next_song = ""

        if next_song:
            tracks += next_song

        for index, track in enumerate(player.queue._queue):
            tracks += f"{index + 1}. [{track.title}]({track.uri}) \n"

        embed.description = tracks

        await ctx.send(embed=embed)

    @commands.command(aliases=["np"])
    @voice_channel_player()
    async def nowplaying(self, ctx: commands.Context):
        """Currently playing song information"""
        player: DisPlayer = self.bot.players[ctx.guild.id]
        await player.invoke_player(ctx)
