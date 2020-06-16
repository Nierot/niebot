import cleverbotfree.cbfree
from discord.ext import commands

class Cleverbot(commands.Cog, name="Cleverbot"):

    def __init__(self, bot):
        self.bot = bot
        geckodriver_autoinstaller.install()
        self.cb = cleverbotfree.cbfree.Cleverbot()


    @commands.command(name="cleverbot")
    async def command(self, ctx, *args):
        await ctx.send(self.chat(args[0]))


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.bot.user:
            if str(self.bot.user.id) in message.content:
                x = await self.chat(message.content, str(message.author))
                await message.channel.send(x)


    async def chat(self, message, username):
        response = self.cb.single_exchange(message[23:])
        return response


def setup(bot):
    bot.add_cog(Cleverbot(bot))