import discord
from discord.ext import commands
import secrets
import aiohttp

class Bot:

    def __init__(self):
        self.bot = commands.Bot(command_prefix="yeet ", description="Yeetmeister9000 is here to help!")
        self.bot.secrets = secrets.Secrets()
        self.token = self.bot.secrets.BOT_TOKEN
        self.bot.case_insensitive = True
        self.bot._voice_clients = {}
        self.bot._queue = {}
        self.bot._playing = {}
        self.bot._debug = False
        self.extensions = [ 'cogs.admin', 'cogs.mc', 'cogs.pils', 'cogs.text', 'cogs.fun', 'cogs.dromendans'] #,'cogs.youtube', 'cogs.cleverbot']


    def load_extensions(self):
        try:
            for ext in self.extensions:
                self.bot.load_extension(ext)
        except Exception as e:
            print(e)


    def reload_extensions(self):
        try:
            for ext in self.extensions:
                self.bot.reload_extension(ext)
        except Exception as e:
            print(e)


    def run(self):
        self.load_extensions()
        @self.bot.event
        async def on_ready():
            self.bot._session = aiohttp.ClientSession()
            headers = {}
            headers['Authorization'] = 'Bearer HzEnNuHDAYJOCIjqLI4kIHzhWIM4nZrkyjgsqLxezhF9DaKQY0ZvqVsMlkT2Zebp'
            self.bot._genius_session = aiohttp.ClientSession(headers=headers)
            print(self.bot.user.name)
            print(self.bot.user.id)
            print(discord.utils.oauth_url(self.bot.user.id))
        self.bot.run(self.token)


if __name__ == "__main__":
    bot = Bot()
    bot.run()