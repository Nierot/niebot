from discord.ext import commands
import secrets

class Admin(commands.Cog, name='Helper'):

    def __init__(self, bot):
        self.bot = bot
        self.extensions = bot.extensions

    @commands.command(name='debug', hidden=True)
    async def _toggle_debug(self, ctx):
        if str(ctx.message.author.id) == str(secrets.OWNER_ID):
            self.bot._debug = not self.bot._debug

    @commands.command(name='reload', hidden=True)
    async def _reload(self, ctx):
        if self.bot._debug:
            print("reloading")
            if str(ctx.message.author.id) == str(secrets.OWNER_ID):
                await self.reload(ctx)


    async def reload(self, ctx):
        print("Reloading")
        try:
            for ext in self.extensions:
                self.bot.reload_extension(ext)
                await ctx.send("Reloading... {}".format(ext.replace('cogs.', '')))
                print("--------- {}".format(ext.replace('cogs.', '')))
                print()
        except Exception as e:
            print(e)

    
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot._debug:
            if message.content.lower() == 'r':
                await self.reload(message.channel)


def setup(bot):
    bot.add_cog(Admin(bot))