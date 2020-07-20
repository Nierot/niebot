import discord
from discord.ext import commands
from bs4 import BeautifulSoup

class Anime(commands.Cog, name="Anime"):

    def __init__(self, bot):
        self.bot = bot


    # @commands.command(name="sauce")
    # async def saucenao(self, ctx, *args):
    #     """
    #     Ik weet ook niet wat ik hier nou van vind
    #     """
    #     if (len(args) != 1):
    #         return await ctx.send("USAGE: yeet sauce [LINK]")
        
    #     url = f'https://saucenao.com/search.php?url={args[0]}' # Words cannot describe how stupid this is
    #     await ctx.send(url)

    #     try:
    #         async with ctx.typing():
    #             async with self.bot._session.get(url=url) as r:
    #                 soup = BeautifulSoup(await r.text())
    #                 for result in soup.find_all('div', class_='result'):
    #                     if result.get('id') == 'result-hidden-notification':
    #                         continue
    #                     img = result.table.tr.td.img.get('data-src')
    #                     print(img)
    #                     await ctx.send(img)
    #     except Exception as e:
    #         await ctx.send(e)


    @commands.command(name='sauce')
    async def iqdb(self, ctx, *args):
        if (len(args) != 1):
            return await ctx.send("USAGE: yeet iqdb [LINK]")

        url = f'https://iqdb.org/?url={args[0]}'

        try:
            async with ctx.typing():
                async with self.bot._session.get(url=url) as r:
                    html = BeautifulSoup(await r.text(), 'lxml')
                    div = html.find_all('div', class_='pages')[0]
                    div = div.find_all('div')[2]
                    #print(div)
                    #await ctx.send(div)
                    result = ''
                    result += f'Tags: {div.table.img["alt"].split(":")[2]} \n'
                    result += f'*{str(div.table.find_all("tr")[4]).split("<")[2][3:]}* \n'
                    result += f'https://{div.table.a["href"][2:]} \n'
                    await ctx.send(result)
        except Exception as e:
            print(e)
            await ctx.send(e)

def setup(bot):
    bot.add_cog(Anime(bot))