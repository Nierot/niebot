from discord.ext import commands
import discord
import random
import asyncio

class Dromendans(commands.Cog, name="dromendans"):
    """
    Elke update heeft dit minder met dromendans te maken, het blijft wel dromendans heten want dat is handig.
    """

    def __init__(self, bot):
        self.bot = bot
        self.voice_client = self.bot._voice_clients
        self.stopped = {}
        self.troep = ["Dit wordt kut", "Hier heb ik nou geen zin in", "jesus wat slecht", "ik heb deathmetal gehoord dat beter is dan dit"]
        self.root = ''


    @commands.command(name="dromendans")
    async def dromendans(self, ctx):
        """
        Plays dromendans on repeat
        """
        await ctx.send("Dromendans Xdddddd")
        self.stopped[ctx.message.guild.id] = False
        await self._dromendans(ctx, 'music/dromendans.mp3', 0.5)


    @commands.command(name="putin")
    async def putin(self, ctx):
        """
        putin xd
        """
        await ctx.send("PUTIN HAHAHAHAHA")
        self.stopped[ctx.message.guild.id] = False
        await self._dromendans(ctx, 'music/putin.mp3', 0.5)


    @commands.command(name="troep")
    async def troep(self, ctx, *args):
        """
        speelt die troep af van jullie
        gebruik: yeet troep nummer
        """
        if (random.randint(0,10) < 4):
            await ctx.send("Nee ga ik niet doen")
        else:
            if (len(args) < 1 or len(args) > 2):
                await ctx.send("doe het dan wel goed")
                return
            music = args[0]
            volume = 0.5
            if (len(args) == 2):
                volume = float(args[1])

            await ctx.send("Het volgende nummer is: " + music)
            await ctx.send(random.choice(self.troep))
            self.stopped[ctx.message.guild.id] = False
            await self._dromendans(ctx, 'music/' + music + '.mp3', volume)


    @commands.command(name="geen_dromendans_meer_pls", aliases=["geen_putin_meer_pls", "nee"])
    async def _stop_dromendans(self, ctx):
        """
        For people who are laf
        """
        guild = ctx.message.author.guild.id
        self.stopped[guild] = True
        await ctx.send("laf")
        await self.voice_client[guild].disconnect()


    async def _dromendans(self, ctx, music, volume) -> None:
        channel = ctx.message.author.voice.channel
        guild = ctx.message.author.guild.id
        try:
            source = discord.FFmpegPCMAudio(music)
            source = discord.PCMVolumeTransformer(source, volume)
        except Exception as e:
            print(e)
            await ctx.send("weet je zeker dat je kan spellen?")
            return
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
                await self._dromendans(ctx, music, volume)
        

def setup(bot):
    bot.add_cog(Dromendans(bot))