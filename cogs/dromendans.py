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
        await self._dromendans(ctx)


    @commands.command(name="geen_dromendans_meer_pls")
    async def _stop_dromendans(self, ctx):
        """
        For people who are laf
        """
        guild = ctx.message.author.guild.id
        self.stopped[guild] = True
        await ctx.send("laf")
        await self.voice_client[guild].disconnect()


    async def _dromendans(self, ctx):
        channel = ctx.message.author.voice.channel
        guild = ctx.message.author.guild.id
        source = discord.FFmpegPCMAudio('music\\dromendans.mp3')
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