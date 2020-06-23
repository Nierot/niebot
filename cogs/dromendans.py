from discord.ext import commands
import discord
import random
import asyncio
from os import listdir
import aiohttp
from bs4 import BeautifulSoup
import re
import os

class Dromendans(commands.Cog, name="dromendans"):
    """
    Elke update heeft dit minder met dromendans te maken, het blijft wel dromendans heten want dat is handig.
    """


    def __init__(self, bot):
        self.bot = bot
        self.voice_client = self.bot._voice_clients
        self.stopped = {}
        self.troep = ["Dit wordt kut", "Hier heb ik nou geen zin in", "jesus wat slecht", "ik heb deathmetal gehoord dat beter is dan dit"]
        self.json = {}


    """
    TODO Add a progress bar
    TODO Add a auto leave
    TODO Add geniusApi to get lyrics
    TODO Add same reaction as other people
    TODO anime character randomizer
    """

    # Plays dromendans in the current voicechannel
    @commands.command(name="dromendans")
    async def dromendans(self, ctx):
        """
        Plays dromendans on repeat
        """
        await ctx.send("Dromendans Xdddddd")
        self.stopped[ctx.message.guild.id] = False
        await self._dromendans(ctx, 'music/dromendans.mp3', 1.0)


    # Plays the putin walking song
    @DeprecationWarning
    @commands.command(name="putin")
    async def putin(self, ctx):
        """
        putin xd
        """
        await ctx.send("Gebruik de troep command pls") # kinda deprecated
        self.stopped[ctx.message.guild.id] = False
        await self._dromendans(ctx, 'music/putin.mp3', 1.0)


    # Returns the upload url
    @commands.command(name="upload")
    async def upload(self, ctx):
        await ctx.send("https://6ix9ine.nierot.com/")


    # Plays a mp3 from the /music folder
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
            volume = 1.0
            if (len(args) == 2):
                volume = float(args[1])

            await ctx.send("Het volgende nummer is: " + music)
            await ctx.send(random.choice(self.troep))
            self.stopped[ctx.message.guild.id] = False
            await self._dromendans(ctx, 'music/' + music + '.mp3', volume)


    # List off all available music
    @commands.command(name="shitlist")
    async def shitlist(self, ctx):
        """
        Alle troep mogelijk
        """
        embed: discord.Embed = discord.Embed(
            color = discord.Color.blue()
        )
        values = ''
        for x in listdir('music'):
            values += x.split('.')[0] + '\n'
        embed.add_field(name="Kut muziek", value=values)
        await ctx.send(embed=embed)
            

    # Stop command for the music
    @commands.command(name="geen_dromendans_meer_pls", aliases=["geen_putin_meer_pls", "nee"])
    async def _stop_dromendans(self, ctx):
        """
        For people who are laf
        """
        guild = ctx.message.author.guild.id
        if (random.randint(0,10) > 3):
            self.stopped[guild] = True
            await ctx.send("laf")
            await self.voice_client[guild].disconnect()
        else:
            await ctx.send("Lol nee")


    @commands.command(name="lyrics")
    async def genius(self, ctx, *args):
        """
        Voor als je toch maar wil weten wat Steen zegt
        """
        query = '%20'.join(args)
        if query == '':
            await ctx.send("doe ff normaal man")
        else:
            await self._genius_search(ctx, query)


    # The music player, repeats itself if not stopped
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
            self.voice_client[guild].play(source)
        except Exception as e:
            print(e)

        while self.voice_client[guild].is_playing():
            await asyncio.sleep(1)
            if self.stopped[guild]:
                break
            if not self.voice_client[guild].is_playing():
                await self._dromendans(ctx, music, volume)

    
    async def _genius_json(self, ctx, song_id):
        url = 'https://api.genius.com/songs/' + str(song_id)
        headers = {}
        headers['Authorization'] = 'Bearer HzEnNuHDAYJOCIjqLI4kIHzhWIM4nZrkyjgsqLxezhF9DaKQY0ZvqVsMlkT2Zebp'
        try:
            async with self.bot._genius_session.get(url=url, headers=headers) as r:
                return await r.json()
        except Exception as e:
            print(e)
            await ctx.send(e)

    
    async def _genius_lyrics(self, ctx, song_id):
        json = await self._genius_json(ctx, song_id)
        url = 'https://genius.com' + json['response']['song']['path']
        name = json['response']['song']['full_title']

        async with self.bot._genius_session.get(url=url) as r:
            html = BeautifulSoup(await r.text(), 'html.parser')

            # source: https://github.com/johnwmillr/LyricsGenius/blob/master/lyricsgenius/api.py
            # Determine the class of the div
            old_div = html.find("div", class_="lyrics")
            new_div = html.find("div", class_="SongPageGrid-sc-1vi6xda-0 DGVcp Lyrics__Root-sc-1ynbvzw-0 jvlKWy")
            if old_div:
                lyrics = old_div.get_text()
            elif new_div:
                # Clean the lyrics since get_text() fails to convert "</br/>"
                lyrics = str(new_div)
                lyrics = lyrics.replace('<br/>', '\n')
                lyrics = re.sub(r'(\<.*?\>)', '', lyrics)
            else:
                return None # In case the lyrics section isn't found
            lyrics = re.sub('(\[.*?\])*', '', lyrics)
            #lyrics = re.sub('\n{2}', '\n', lyrics)  # Gaps between verses
            if (len(lyrics) > 1900):
                await self.split_lyrics(name + lyrics, ctx)
            else:
                await ctx.send(name + lyrics)


    async def split_lyrics(self, lyrics, ctx):
        arr = lyrics.split('\n')
        i = 0
        first = []
        prev = ''
        for line in arr:
            if line == prev:
                prev = line
                continue
            prev = line
            i += len(line)
            first.append(line)
            if i > 1500:
                i = 0
                await ctx.send('\n'.join(first))
                first = []
        await ctx.send('\n'.join(first))


    async def _genius_search(self, ctx, search):
        url = 'https://api.genius.com/search'
        try:
            async with self.bot._genius_session.get(url=url + "?q=" + search) as r:
                json = await r.json()
                i = 1
                ids = []
                msg = 'Songs\n'
                for song in json['response']['hits']:
                    if i == 4:
                        break
                    ids.append(song['result']['id'])
                    msg += str(i) + ": " + song['result']['full_title'] + "\n"
                    i += 1
                msg = await ctx.send(msg)
                print(ids)
            await msg.add_reaction(emoji='1️⃣')
            await msg.add_reaction(emoji='2️⃣')
            await msg.add_reaction(emoji='3️⃣')

            try:
                def check(reaction, user):
                    return user != self.bot.user

                reaction, user = await self.bot.wait_for('reaction_add', check=check)
            except asyncio.TimeoutError as e:
                print(e)
                await ctx.send(e)
            else:
                print(str(reaction.emoji))
                if str(reaction.emoji) == '1️⃣':
                    return await ctx.send(await self._genius_lyrics(ctx, ids[0]))
                elif str(reaction.emoji) == '2️⃣':
                    print("yeet")
                    return await ctx.send(await self._genius_lyrics(ctx, ids[1]))
                elif str(reaction.emoji) == '3️⃣':
                    return await ctx.send(await self._genius_lyrics(ctx, ids[2]))
                else:
                    await ctx.send("mogool")
        except Exception as e:
            print(e)


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        msg = reaction.message
        if msg.author == self.bot.user and reaction.count >= 2 and not self.count_reactions(msg.reactions) > 4:
            pass
            #msg.reactions)
            # print("yeet")
            # await self._genius_search(self, reaction=True)

        
    def count_reactions(self, reactions):
        i = 0
        for r in reactions:
            i += r.count
        return i

def setup(bot):
    bot.add_cog(Dromendans(bot))