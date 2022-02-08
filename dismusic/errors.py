from discord.ext.commands.errors import CheckFailure


class NotConnectedToVoice(CheckFailure):
    """User not connected to any voice channel"""

    pass


class PlayerNotConnected(CheckFailure):
    """Player not connected"""

    pass


class MustBeSameChannel(CheckFailure):
    """Player and user not in same channel"""

    pass


class NothingIsPlaying(CheckFailure):
    """Nothing is playing"""

    pass


class NotEnoughSong(CheckFailure):
    """Not enough songs in queue"""

    pass


class InvalidLoopMode(CheckFailure):
    """Invalid loop mode"""

    pass
