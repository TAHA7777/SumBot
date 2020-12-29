import discord
from discord.ext import commands
import aiohttp


class random(commands.Cog):
    """
    All commands are based on random value
    """
    def __init__(self, client):
        self.client = client

    @commands.command(help='to show random img cat')
    @commands.guild_only()
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://some-random-api.ml/img/cat') as r:
                res = await r.json()
                embed = discord.Embed(
                    color=ctx.author.color,
                    description=f"[Random Cat]({res['link']})",
                    timestamp=ctx.message.created_at
                )
                embed.set_image(url=res['link'])
                embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
                embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)

    @commands.command(help='to show random img panda')
    @commands.guild_only()
    async def panda(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/panda") as r:
                res = await r.json()
                embed = discord.Embed(
                    color=ctx.author.color,
                    description=f"[Random Panda]({res['link']})",
                    timestamp=ctx.message.created_at
                )
                embed.set_image(url=res['link'])
                embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
                embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)

    @commands.command(help='to show random img coffee')
    @commands.guild_only()
    async def coffee(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://coffee.alexflipnote.dev/random.json") as r:
                res = await r.json()
                embed = discord.Embed(
                    color=ctx.author.color,
                    description=f"Daily Coffee, [link Img]({res['file']})",
                    timestamp=ctx.message.created_at
                )
                embed.set_image(url=res["file"])
                embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
                embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)

    @commands.command(help='to show random img dog')
    @commands.guild_only()
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://dog.ceo/api/breeds/image/random') as r:
                res = await r.json()
                embed = discord.Embed(
                    color=ctx.author.color,
                    description=f"Random Dog, [Link img]({res['message']})",
                    timestamp=ctx.message.created_at
                )
                embed.set_image(url=res['message'])
                embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
                embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)

    @commands.command(help='to show random img fox')
    @commands.guild_only()
    async def fox(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://randomfox.ca/floof/') as r:
                res = await r.json()
                embed = discord.Embed(
                    color=ctx.author.color,
                    description=f"Random Fox, [link Img]({res['image']})",
                    timestamp=ctx.message.created_at
                )
                embed.set_image(url=res['image'])
                embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
                embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)

    @commands.command(help='to show random img redpanda')
    @commands.guild_only()
    async def redpanda(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/red_panda") as r:
                res = await r.json()
                embed = discord.Embed(
                    color=ctx.author.color,
                    description=f"Random Panda, [Link Img]({res['link']})",
                    timestamp=ctx.message.created_at
                )
                embed.set_image(url=res['link'])
                embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
                embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(random(client))
