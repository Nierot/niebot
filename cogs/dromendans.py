from discord.ext import commands
import discord
import asyncio

class Dromendans(commands.Cog, name="dromendans"):

    def __init__(self, bot):
        self.bot = bot
        self.voice_client = self.bot._voice_clients
        self.stopped = {}


    @commands.command(name="dromendans")
    async def dromendans(self, ctx):
        """
        Plays dromendans on repeat
        """
        await ctx.send("Dromendans Xdddddd")
        self.stopped[ctx.message.guild.id] = False
        await self._dromendans(ctx, 'music/dromendans.mp3')


    @commands.command(name="putin")
    async def putin(self, ctx):
        """
        putin xd
        """
        await ctx.send("PUTIN HAHAHAHAHA")
        self.stopped[ctx.messgage.guild.id] = False
        await self._dromendans(ctx, 'music/putin.mp3')


    @commands.command(name="geen_dromendans_meer_pls", aliases=["geen_putin_meer_pls"])
    async def _stop_dromendans(self, ctx):
        """
        For people who are laf
        """
        guild = ctx.message.author.guild.id
        self.stopped[guild] = True
        await ctx.send("laf")
        await self.voice_client[guild].disconnect()


    async def _dromendans(self, ctx, music):
        channel = ctx.message.author.voice.channel
        guild = ctx.message.author.guild.id
        source = discord.FFmpegPCMAudio(music)
        try:
            self.voice_client[guild] = await channel.connect()
        except Exception as e:
            pass

        try:
            self.voice_client[guild].play(source, after=lambda: print("Playing dromendans"))
        except Exception as e:
            print(e)

        while self.voice_client[guild].is_playing():
            await asyncio.sleep(1)
            if self.stopped[guild]:
                break
            if not self.voice_client[guild].is_playing():
                await self._dromendans(ctx)
        

def setup(bot):
    bot.add_cog(Dromendans(bot))