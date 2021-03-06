import discord
from discord.ext import commands
import aiohttp
from pyquery import PyQuery
import re
import urllib.parse

"""
credits naar Davvos11
"""

class Pils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(name="beer", aliases=["pils", "biernet", "bier"])
    async def biernet(self, ctx, *args):
        """ 
        Beste prijs voor pils
        Compleet gejat van Davvos11
        """
        text = ''.join(args[i] + ' ' for i in range(0, len(args)))
        text = text.strip()

        if text == "":
            message = await ctx.send("Usage: .bier [beer brand]")
            return

        async with ctx.channel.typing():
            try:
                # Search biernet for the provided beer
                result = await self.search(text)
                # Create an embed with the results
                embed: discord.Embed = discord.Embed(
                    title='Beste aanbieding van ' + result['brand'], url=result['url'],
                    colour=discord.colour.Colour.green(),
                    description=result['name'])
                embed.add_field(name=result['product'],  inline=True,
                                value="~~" + result['original_price'] + "~~ **" + result['sale_price'] + "**")
                embed.add_field(name=result['PPL'], inline=True, value=result['sale'])
                embed.set_author(name=result['shop_name'], url=result['biernet_shop_url'], icon_url=result['shop_img'])
                embed.set_thumbnail(url=result['img'])
                embed.set_footer(text="Aanbieding duurt tot " + result['end_date'],
                                 icon_url="https://biernet.nl/site/images/general_site_specific/logo-klein.png")
                message = await ctx.send(embed=embed)
                await message.add_reaction(emoji="\U0001F37B")
            except aiohttp.ClientConnectorError:
                await ctx.send("Doet biernet het niet?")
            except ValueError as e:
                await ctx.send(str(e))


    async def get_search(self, args):
        biernet_url = "https://www.biernet.nl/site/php/data/aanbiedingen.php"
        try:
            session = self.bot._session
            # Send a post request with the provided arguments
            async with session.post(biernet_url, data=args) as resp:
                # Return the webpage
                return await resp.text()
        except aiohttp.ClientConnectorError as e:
            raise e


    async def search(self, search_term):
        # First try finding crates with the search term as brand name
        webpage = await self.get_search({'zoeken': 'true', 'merk': search_term.replace(" ", "-"), 'kratten': 'krat-alle',
                                        'sorteer': 'prijs-oplopend'})
        url = PyQuery(webpage)('a.merkenUrl').attr('href')
        if url is None:
            # Try finding crates with the search term as search term
            webpage = await self.get_search({'zoeken': 'true', 'zoek': search_term.replace(" ", "+"),
                                            'kratten': 'krat-alle', 'sorteer': 'prijs-oplopend'})
            url = PyQuery(webpage)('a.merkenUrl').attr('href')
            if url is None:
                # Try finding other offers (not crates) with the search term as brand name
                webpage = await get_search(self, {'zoeken': 'true', 'merk': search_term.replace(" ", "-"),
                                                'sorteer': 'prijs-oplopend'})
                url = PyQuery(webpage)('a.merkenUrl').attr('href')
                if url is None:
                    # Try finding other offers with the search term as search term
                    webpage = await get_search(self, {'zoeken': 'true', 'zoek': search_term.replace(" ", "+"),
                                                    'sorteer': 'prijs-oplopend'})
                    url = PyQuery(webpage)('a.merkenUrl').attr('href')
                    if url is None:
                        # If nothing is found, we throw an exception
                        raise ValueError(search_term + ' not found, or not on sale')

        host = "https://www.biernet.nl"

        first_result = PyQuery(PyQuery(webpage)('li.cardStyle')[0])
        # Get all the various information from the HTML page
        biernet_url = host + first_result('div.item_image')('a').attr('href')
        image = host + first_result('div.item_image')('a')('img').attr('data-src')
        brand = first_result('h3.merkenH3')('a')[0].text

        product = first_result('p.artikel')('a')[0].text
        product_name = first_result('div.item_image')('a')('img').attr('title')
        original_price = first_result('p.prijs')('span.van_prijs')[0].text
        sale_price = first_result('p.prijs')('span.voor_prijs')[0].text
        sale = PyQuery(first_result('div.informatie')('li.item')[0]).text()
        sale = sale.replace('korting', 'off')
        sale_price_liter = PyQuery(first_result('div.informatie')('li.item')[1]).text()
        end_date = first_result('div.footer-item')('span')[0].text
        end_date = end_date.replace("t/m ", "").strip()

        biernet_shop_url = host + first_result('div.logo_image')('a').attr('href')
        shop_name = biernet_shop_url.split('winkel:')[-1]
        shop_name = shop_name.replace('-', ' ').title()
        shop_image = host + first_result('div.logo_image')('a')('img').attr('data-src')

        shop_url = first_result('a.bestelknop').attr('href')
        if shop_url is None:
            shop_url = biernet_shop_url

        biernet_url = urllib.parse.quote(biernet_url, safe=':/%')
        image = urllib.parse.quote(image, safe=':/%')
        shop_url = urllib.parse.quote(shop_url, safe=':/%')
        shop_image = urllib.parse.quote(shop_image, safe=':/%')

        return {'url': biernet_url, 'brand': brand, 'name': product_name, 'img': image, 'product': product,
                'shop_name': shop_name, 'shop_url': shop_url, 'biernet_shop_url': biernet_shop_url, 'shop_img': shop_image,
                'original_price': original_price, 'sale_price': sale_price, 'sale': sale, 'PPL': sale_price_liter,
                'end_date': end_date}

def setup(bot):
    bot.add_cog(Pils(bot))