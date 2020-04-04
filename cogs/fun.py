import discord
from discord.ext import commands
import aiohttp
import random
from pyquery.pyquery import PyQuery
import html

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Made by Davvos11
    @commands.command(name="avatar",aliases=['pf'])
    async def avatar(self, ctx, user: discord.User):
        """
            Laat de profielfoto van iemand zien.
        """
        member = ctx.guild.get_member(user.id)

        embed: discord.Embed = discord.Embed(title=user.name+"'s avatar:",
                                             colour=member.colour)
        embed.set_image(url=user.avatar_url)
        embed.set_author(name=user.display_name, icon_url=user.avatar_url)
        await ctx.send(embed=embed)
    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Wie?")
            raise error
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Wie?')
            raise error


    @commands.command(name="playing", hidden=True)
    async def playing(self, ctx, *args):
        if len(args) == 0:
            args = "Aardappel"
        else:
            temp = ''
            for i in args:
                temp = temp + " " + i
            args = temp
        await self.bot.change_presence(activity=discord.Game(name=args))


    @commands.command(name="meme")
    async def meme(self, ctx, args):
        """
        Stuurt een willekeurige meme van de gegeven subreddit
        """
        async with ctx.channel.typing():
            session = self.bot._session
            url = 'https://www.reddit.com/r/' + args + '.json?&limit=100'
            try:
                async with session.get(url, headers={'User-agent': 'oofyeet '}) as resp:
                    data = await resp.json()
            except aiohttp.ClientConnectorError as e:
                await ctx.send("Error: "+str(e))
                return
            memes = data['data']['children']

            if len(memes) == 0:
                await ctx.send("/r/"+args+" does not exist")
                return

            meme = memes[random.randint(0, 99)]['data']
            meme_title = meme['title']
            meme_url = meme['url']
            meme_reddit_url = 'https://reddit.com'+meme['permalink']
            meme_author = meme['author']
            meme_thumbnail = meme['thumbnail']

            if 'post_hint' in meme:
                meme_type = meme['post_hint']
            else:
                meme_type = 'text'

            if meme_type == 'image':
                embed: discord.Embed = discord.Embed(colour=0x00ffff, title=meme_title, url=meme_reddit_url)
                embed.set_image(url=meme_url)
            elif meme_type == 'text':
                url = meme_reddit_url+'.json'
                try:
                    async with session.get(url, headers={'User-agent': 'oofyeet '}) as resp:
                        data = await resp.json()
                    meme_text_html = data[0]['data']['children'][0]['data']['selftext_html']
                    meme_text_html = html.unescape(meme_text_html)
                    html_root = PyQuery(meme_text_html)
                    meme_text = html_root('div.md').html()
                    meme_text = meme_text.replace("<p>", "").replace("</p>","\n")
                    if len(meme_text) >= 1024:
                        meme_text = meme_text[0:1020]+"..."
                except aiohttp.ClientConnectorError:
                    meme_text = ""
                embed: discord.Embed = discord.Embed(description=meme_text, colour=0x00ffff,
                                                     url=meme_reddit_url, title=meme_title)
            else:
                embed: discord.Embed = discord.Embed(colour=0x00ffff, url=meme_reddit_url, title=meme_title)
                embed.set_thumbnail(url=meme_thumbnail)
            embed.set_author(name="/u/"+meme_author, url='https://reddit.com/u/' + meme_author)
            await ctx.send(embed=embed)


    async def on_message_lmao(self, message: discord.Message):
        if "lmao" in message.content.lower():
            response = ("<:lol:646089960792916018>""<:lol:646089960792916018>""<:lol:646089960792916018>"
                    "WHO DID THIS"
                    "<:lol:646089960792916018>""<:lol:646089960792916018>""<:lol:646089960792916018>")
            await message.channel.send(response)

    async def on_message_alexa(self, message: discord.Message):
        if "this is so sad" in message.content.lower():
            await message.channel.send("Alexa, play Despacito")


    async def on_message_best(self, message: discord.Message):
        if "best" in message.content.lower():
            await message.channel.send("[REACTIE]")


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        await self.on_message_alexa(message)
        await self.on_message_lmao(message)
        await self.on_message_best(message)


def setup(bot):
    bot.add_cog(Fun(bot))