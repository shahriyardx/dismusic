import asyncio
import math

from discord import (Color, Embed, Forbidden, HTTPException, InvalidArgument,
                     NotFound)

from ._classes import Emojis


class Paginator:
    def __init__(self, ctx, player) -> None:
        self.ctx = ctx
        self.player = player

    @staticmethod
    def get_length(queue):
        length = sum([track.length for track in queue._queue])
        if length > 3600:
            length = f"{int(length // 3600)}h {int(length % 3600 // 60)}m {int(length % 60)}s"
        elif length > 60:
            length = f"{int(length // 60)}m {int(length % 60)}s"
        else:
            length = f"{int(length)}s"

        return length

    def create_embed(self, tracks, current_page, total_pages):
        embed = Embed(color=Color(0x2F3136))
        embed.set_author(
            name="Queue",
            icon_url="https://cdn.discordapp.com/attachments/776345413132877854/940247400046542948/list.png",
        )

        if self.player.loop == "CURRENT":
            next_song = (
                f"Next > [{self.player.source.title}]({self.player.source.uri}) \n\n"
            )
        else:
            next_song = ""

        description = next_song
        queue_length = self.get_length(self.player.queue)

        for index, track in enumerate(tracks):
            description += (
                f"{current_page * 10 + index + 1}. [{track.title}]({track.uri}) \n"
            )

        embed.description = description

        if total_pages == 1:
            embed.set_footer(
                text=f"{len(self.player.queue._queue)} tracks, {queue_length}"
            )
        else:
            embed.set_footer(
                text=f"Page {current_page + 1}/{total_pages}, {len(self.player.queue._queue)} tracks, {queue_length}"
            )

        return embed

    async def start(self):
        per_page = 10
        current_page = 0
        track_list = list(self.player.queue._queue)

        total_pages = math.ceil(len(track_list) / per_page)

        msg = None

        while True:
            tracks = track_list[current_page * per_page : (current_page + 1) * per_page]
            embed = self.create_embed(tracks, current_page, total_pages)

            if not msg:
                msg = await self.ctx.send(embed=embed)
            else:
                await msg.edit(embed=embed)

            if total_pages > 1:
                try:
                    await msg.add_reaction(Emojis.FIRST)
                    await msg.add_reaction(Emojis.PREV)
                    await msg.add_reaction(Emojis.NEXT)
                    await msg.add_reaction(Emojis.LAST)
                except (HTTPException, Forbidden, NotFound, InvalidArgument) as e:
                    print(e)
                    pass
            else:
                break

            def check(reaction, user):
                valid_reactions = [Emojis.FIRST, Emojis.PREV, Emojis.NEXT, Emojis.LAST]
                return (
                    user == self.ctx.author
                    and str(reaction.emoji) in valid_reactions
                    and reaction.message.id == msg.id
                )

            try:
                reaction, user = await self.ctx.bot.wait_for(
                    "reaction_add", timeout=60.0, check=check
                )
            except asyncio.TimeoutError:
                break

            if str(reaction.emoji) == Emojis.PREV:
                current_page = max(0, current_page - 1)
            elif str(reaction.emoji) == Emojis.NEXT:
                current_page = min(total_pages - 1, current_page + 1)
            elif str(reaction.emoji) == Emojis.FIRST:
                current_page = 0
            elif str(reaction.emoji) == Emojis.LAST:
                current_page = total_pages - 1

            await msg.remove_reaction(reaction.emoji, user)
