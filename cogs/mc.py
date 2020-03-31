import discord
from discord.ext import commands
import aiohttp
import json

class Mc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="fish", aliases=["fish_leaderboard", "vissers", "vissen"])
    async def fish(self, ctx):
        """
            Hoeveel vissen heeft iedereen gevangen?
        """
        board = self._sort_leaderboard(json.loads(await self._query(ctx, "fish")))
        player = ""
        fish = ""
        place = ""
        i = 1
        for x in board:
            player += x['player'] + "\n"
            fish += str(x['fish']) + "\n"
            place += str(i) +"\n"
            i += 1
        embed: discord.Embed = discord.Embed(
            color = discord.Color.blue()
        )
        embed.add_field(name = "Place", value =place, inline=True)
        embed.add_field(name = "Player", value=player, inline=True)
        embed.add_field(name = "Fish", value=fish, inline=True)
        await ctx.send(embed = embed)


    @commands.command(name="size", aliases=["time"])
    async def size(self, ctx):
        """
            Stuurt hoe groot de border is en hoe lang het nog duurt tot het volgende blok.
        """
        size = json.loads(await self._query(ctx, "size"))
        time = json.loads(await self._query(ctx, "time"))
        await ctx.send("De border is nu {} blokken groot! Volgende blok in {} seconden.".format(size['size'], time['time']))


    async def _query(self, ctx, endpoint):
        url = "https://api.nierot.com/v1/mc/" + endpoint
        try:
            async with ctx.channel.typing():
                session = self.bot._session
                async with session.get(url) as resp:
                    webpage = await resp.text()
            return webpage
        except aiohttp.ClientConnectorError as e:
            raise e


    def _sort_leaderboard(self, board):
        return sorted(board, key=lambda k: k.get('fish', 0), reverse=True)
