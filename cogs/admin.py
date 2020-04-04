from discord.ext import commands
import secrets

class Admin(commands.Cog, name='Helper'):

    extensions = ['cogs.youtube', 'cogs.admin', 'cogs.mc', 'cogs.pils', 'cogs.text', 'cogs.fun']

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='reload', hidden=True)
    async def _reload(self, ctx):
        if ctx.message.author.id == secrets.OWNER_ID:
            self.reload(ctx)


    async def reload(self, ctx):
        try:
            for ext in self.extensions:
                self.bot.reload_extension(ext)
                await ctx.send("Reloading... {}".format(ext.replace('cogs.', '')))
                print("--------- {}".format(ext.replace('cogs.', '')))
                print()
        except Exception as e:
            await ctx.send(e)

    
    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if message.content.lower() == 'r':
    #         await self.reload(message.channel)


def setup(bot):
    bot.add_cog(Admin(bot))