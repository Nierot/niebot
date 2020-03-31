import discord
from discord.ext import commands
import secrets
import cogs.fun as fun
import cogs.text as text
import cogs.pils as pils
import cogs.mc as mc
import aiohttp

bot = commands.Bot(command_prefix="!")

class Bot:

    def __init__(self):
        self.token = secrets.BOT_TOKEN
        self.bot = commands.Bot(command_prefix="yeet ", description="Yeetmeister9000 is here to help!")


    def load_cogs(self):
        self.bot.add_cog(fun.Fun(self.bot))
        self.bot.add_cog(text.Text(self.bot))
        self.bot.add_cog(pils.Pils(self.bot))
        self.bot.add_cog(mc.Mc(self.bot))


    def run(self):
        self.load_cogs()
        @self.bot.event
        async def on_ready():
            self.bot._session = aiohttp.ClientSession()
            print('Logged in as')
            print(self.bot.user.name)
            print(self.bot.user.id)
            print('------')
            print(discord.utils.oauth_url(self.bot.user.id))
        self.bot.run(self.token)


if __name__ == "__main__":
    bot = Bot()
    bot.run()