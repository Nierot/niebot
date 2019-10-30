import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix=".")
client = discord.Client()

@bot.command(name="tyfus")
async def bloxquote(ctx):
    bloxquotes = [
        "OOF",
        "oof",
        "OOOF!",
        "of!",
        "oef!",
        "REEEEEEE"
    ]
    response = random.choice(bloxquotes)
    await ctx.send(response)


# @client.event
# async def on_ready():
#     guild = discord.utils.get(client.guilds, name=GUILD)
#     print(
#         f'{client.user} is connected to the following guild:\n'
#         f'{guild.name}(id: {guild.id})'
#     )
#     members = '\n - '.join([member.name for member in guild.members])
#     print(f'Guild Members:\n - {members}')

# class CustomClient(discord.Client):
#     async def on_ready(self):
#         print(f'{self.user} has connected to Discord!')


# @client.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to my Discord server!'
#     )

@bot.command(name="rblx")
async def rlbx(ctx):
    if message.author == client.user:
        return
    quotes = [
        "Oof",
        "yeet",
        "reee",
        "autism",
        "iets"
    ]
    robloxquotes = [
        "Tycoon > obby",
        "Counter-Blox is better than Counter-Strike",
        "Oof",
        "OOOOF",
        "Go commit die!"
    ]
    if message.content == "autism":
        response = random.choice(quotes)
        await message.channel.send(response)
    elif message.content == "roblox":
        response = random.choice(robloxquotes)
        await message.channel.send(response)

bot.run(token)
#client.run(token)
