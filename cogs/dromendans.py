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
        self.skip = {}
        self.troep = ["Dit wordt kut", "Hier heb ik nou geen zin in", "jesus wat slecht", "ik heb deathmetal gehoord dat beter is dan dit", "moet dit nou"]
        self.json = {}
        self.last = {}


    """
    TODO Add a progress bar
    DONE Add a auto leave
    DONE Add geniusApi to get lyrics
    DONE Add same reaction as other people
    TODO anime character randomizer
    TODO Use genius api Youtube links to download and play music
    TODO Instead of repeating a song, add an option to randomize
    TODO add database with song mp3, name, artist and (genius id optional)
    TODO a good queuing system
    DONE/TODO A seperate channel with a constantly updating message with the current song/progress maybe a leaderboard
    DONE Send song title + newline seperately
    TODO add a command to change your color
    TODO use member.move_to to put people in the same channel with dromendans bot
    DONE count how many times the bot rejected someone
    TODO automatically send lyrics in status channel when a known song is being played
    """

    # Plays dromendans in the current voicechannel
    @commands.command(name="dromendans")
    async def dromendans(self, ctx):
        """
        Plays dromendans on repeat
        """
        await ctx.send("Dromendans Xdddddd")
        self.stopped[ctx.message.guild.id] = False
        self.skip[ctx.message.guild.id] = False
        await self._dromendans(ctx, 'music/dromendans.mp3', 1.0, False)


    # Plays the putin walking song
    @DeprecationWarning
    @commands.command(name="putin")
    async def putin(self, ctx):
        """
        putin xd
        """
        await ctx.send("Gebruik de troep command pls") # kinda deprecated
        self.stopped[ctx.message.guild.id] = False
        self.skip[ctx.message.guild.id] = False
        await self._dromendans(ctx, 'music/putin.mp3', 1.0, False)


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
            await self.increment_rejection(ctx.message.author)
        else:
            if (len(args) < 1 or len(args) > 2):
                await ctx.send("doe het dan wel goed")
                return
            music = args[0]
            volume = 1.0
            if (len(args) == 2):
                volume = float(args[1])

            await ctx.send("Het volgende nummer is: " + music)
            await self.set_playing_status(ctx, music)
            await ctx.send(random.choice(self.troep))
            self.stopped[ctx.message.guild.id] = False
            self.skip[ctx.message.guild.id] = False
            await self._dromendans(ctx, 'music/' + music + '.mp3', volume, False)


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
            self.skip[guild] = False
            await ctx.send("laf")
            await self.voice_client[guild].disconnect()
        else:
            await self.increment_rejection(ctx.message.author)
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


    @commands.command(name="set_channel")
    async def set_channel(self, ctx, *args):
        author = ctx.message.author
        channel = ctx.message.channel
        if ctx.message.author.guild_permissions.administrator:
            msg = await ctx.send('Reageer met "Y" om dit kanaal het Niebot kanaal te maken')
            
            def check(message):
                return message.author == author and message.content == 'Y'

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=10.0)
                if not await self._is_niebot_channel(channel.id):
                    self.bot.cursor.execute("INSERT INTO niebot_channels (guild, channel_name, channel_id) VALUES (?,?,?)", [str(channel.guild.id), channel.name, str(channel.id)])
                    self.bot.db.commit()
                else:
                    await ctx.send("Dit is al mijn kanaal")

                role = await self._get_NiebotChannel_rank(ctx.guild)

                if role == -1:
                    role_obj = await self._make_niebot_rank(ctx, msg.guild.me)
                    role = role_obj.id

                msg = await ctx.send("Status")
                self.insert_status(msg)
                await self._set_permissions(ctx, role)
                print(role)
            except asyncio.TimeoutError:
                await ctx.send("Oke dan niet")


    @commands.command(name="loserscoreboard")
    async def rejection_scoreboard(self, ctx):
        rejected = ""
        amount = ""
        for row in self.bot.db.execute("SELECT * FROM rejection"):
            rejected += f"{row[0]}\n"
            amount += f"{row[1]}\n"
        embed = discord.Embed()
        embed.add_field(name='Loser', value=rejected)
        embed.add_field(name='Loserheid', value=amount)
        await ctx.send(embed=embed)


    @commands.command(name="shuffle")
    async def shuffle(self, ctx, *args):
        if (random.randint(0,10) < 4):
            await ctx.send("Nee ga ik niet doen")
            await self.increment_rejection(ctx.message.author)
        else:
            print(args)
            if (len(args) == 1 or len(args) == 2):
                if (len(args) > 2):
                    await ctx.send("doe het dan wel goed")
                    return
                music = args[0]
                volume = 1.0
                if (len(args) == 2):
                    volume = float(args[1])
                await ctx.send("Het volgende nummer is: " + music)
                await self.set_playing_status(ctx, music)
                await ctx.send(random.choice(self.troep))
                self.stopped[ctx.message.guild.id] = False
                self.skip[ctx.message.guild.id] = False
                await self._dromendans(ctx, 'music/' + music + '.mp3', volume, True)
            else:
                await ctx.send("Slechte keus")
                self.stopped[ctx.message.guild.id] = False
                self.skip[ctx.message.guild.id] = False
                await self._dromendans(ctx, self.random_song(), 1.0, True)


    @commands.command(name="skip")
    async def skip(self, ctx):
        if (random.randint(0,10) < 1):
            await ctx.send("lmao")
            await self.increment_rejection(ctx.message.author)
        else:
            await ctx.send("miet")
            self.skip[ctx.message.guild.id] = True


    def random_song(self):
        return 'music/' + random.choice(listdir('music'))


    async def set_status(self, ctx, *args):
        channel = await self._get_status_channel(ctx)
        status = await self._get_status(channel)
        await status.edit(content=' '.join(args))
        

    async def _get_status_channel(self, ctx):
        for row in self.bot.cursor.execute("SELECT * FROM niebot_channels WHERE guild = ?", (str(ctx.guild.id),)):
            channel = ctx.guild.get_channel(int(row[2]))
            return channel


    async def _set_permissions(self, ctx, niebot_role):
        print(f"Niebot role {niebot_role}")
        channel = await self._get_status_channel(ctx)
        for role in ctx.guild.roles:
            if role.id != niebot_role:
                await channel.set_permissions(role, send_messages=False)



    def insert_status(self, msg):
        self.bot.cursor.execute("DELETE FROM niebotchannel_msg WHERE guild = ?", (str(msg.guild.id),))
        self.bot.db.commit()
        self.bot.cursor.execute("INSERT INTO niebotchannel_msg(guild, msg, channel) VALUES(?, ?, ?)", (str(msg.guild.id), str(msg.id), str(msg.channel.id)))
        self.bot.db.commit()


    async def _get_status(self, channel):
        for row in self.bot.cursor.execute("SELECT msg FROM niebotchannel_msg WHERE guild = ?", (str(channel.guild.id),)):
            return await channel.fetch_message(row[0])


    async def _get_NiebotChannel_rank(self, guild):
        for row in self.bot.cursor.execute("SELECT role_id FROM niebotchannel_role WHERE guild = ?", (str(guild.id),)):
            return row[0]
        return -1

    async def _make_niebot_rank(self, ctx, member):
        guild = ctx.guild
        await ctx.send("Creating the role")
        role = await guild.create_role(name="NiebotChannel")
        self.bot.cursor.execute("INSERT INTO niebotchannel_role(guild, role_id) VALUES(?,?)", (str(guild.id), str(role.id)))
        self.bot.db.commit()
        await member.add_roles(discord.utils.get(ctx.guild.roles, name="NiebotChannel")) # Add role to this user
        return role


    # Checks if the given channel is the niebot channel
    async def _is_niebot_channel(self, channel_id):
        for row in self.bot.cursor.execute("SELECT * FROM niebot_channels WHERE channel_id = ?", (str(channel_id),)):
            #print(row)
            return True


    async def _get_niebot_channel(self, guild):
        for row in self.bot.cursor.execute("SELECT guild FROM niebot_channels WHERE guild = ? ", (str(guild),)):
            print(row)
            return row[0]


    async def set_playing_status(self, ctx, song):
        await self.set_status(ctx, f"Ik ben nu {song} aan het spelen!")

    async def set_idle_status(self, ctx):
        await self.set_status(ctx, f"Ik doe nu evenveel als ken")


    async def increment_rejection(self, person):
        self.bot.cursor.execute("INSERT OR IGNORE INTO rejection (person, reject) VALUES (?, ?)", (str(person), 0))
        self.bot.cursor.execute("UPDATE rejection SET reject = reject + 1 WHERE person = ?", (str(person), ))
        self.bot.db.commit()


    # The music player, repeats itself
    async def _dromendans(self, ctx, music, volume, shuffle) -> None:
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
            if (len(channel.members) == 1 or len(channel.members) == 0): # Lmao niebot is met al zn vrienden
                await ctx.send("Laten jullie mij hier nou achter?")
                self.stopped[guild] = True
            if self.stopped[guild]:
                await self.set_idle_status(ctx)
                await self.voice_client[guild].disconnect()
                break
            if self.skip[guild]:
                self.skip[guild] = False
                self.voice_client[guild].stop()
                await self._dromendans(ctx, self.random_song(), volume, True)
            if not self.voice_client[guild].is_playing():
                if shuffle:
                    await self._dromendans(ctx, self.random_song(), volume, True)
                else:
                    await self._dromendans(ctx, music, volume, False)
    

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
            await ctx.send(name + '\n')
            if (len(lyrics) > 1900):
                await self.split_lyrics(lyrics, ctx)
            else:
                await ctx.send(lyrics)


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


def setup(bot):
    bot.add_cog(Dromendans(bot))