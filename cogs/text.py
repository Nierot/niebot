import discord
from discord.ext import commands 

class Text(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send("Welkom {0.mention}.".format(member))


    @commands.command(name="hoegaathet", aliases=["hoe_gaat_het", "hoeishet"])
    async def hoegaathet(self, ctx, *, member: discord.Member = None):
        """Vraagt hoe het gaat"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hoi {0.name}, hoe gaat het?'.format(member))
        else:
            await ctx.send('HALLO {0.name}, HOE GAAT HET?!?!?!?!?!?.'.format(member))
        self._last_member = member