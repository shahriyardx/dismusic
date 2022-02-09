from discord.ext import commands

from .errors import MustBeSameChannel, NotConnectedToVoice, PlayerNotConnected


def voice_connected():
    def predicate(ctx: commands.Context):
        if not ctx.author.voice:
            raise NotConnectedToVoice("You are not connected to any voice channel.")

        return True

    return commands.check(predicate)


def player_connected():
    def predicate(ctx: commands.Context):
        if not ctx.voice_client:
            raise PlayerNotConnected("Player is not connected to any voice channel.")

        return True

    return commands.check(predicate)


def in_same_channel():
    def predicate(ctx: commands.Context):
        if not ctx.voice_client:
            raise PlayerNotConnected("Player is not connected to any voice channel.")

        if ctx.voice_client.channel.id != ctx.author.voice.channel.id:
            raise MustBeSameChannel("You must be in the same voice channel as the player.")

        return True

    return commands.check(predicate)


def voice_channel_player():
    def predicate(ctx: commands.Context):
        if not ctx.author.voice:
            raise NotConnectedToVoice("You are not connected to any voice channel.")

        if not ctx.voice_client:
            raise PlayerNotConnected("Player is not connected to any voice channel.")

        if ctx.voice_client.channel.id != ctx.author.voice.channel.id:
            raise MustBeSameChannel("You must be in the same voice channel as the player.")

        return True

    return commands.check(predicate)
