import discord
from discord.ext import commands
import time


class command(commands.Cog):
    """
    General commands
    """
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['inv'], help='invite bot', description='To invite the bot in your server')
    @commands.guild_only()
    async def invite(self, ctx):
        """
        To invite the bot in your server
        """
        embed = discord.Embed(
            description='''
**Invite bot => [Click here](https://discord.com/oauth2/authorize?client_id={}&scope=bot&permissions=8)**
**Support bot => [Click here]({})**'''.format(self.client.user.id, 'https://discord.gg/MJmzZ62qv2'),
            color=ctx.author.color,
            timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @invite.error
    async def inv_error(self, ctx, error):       
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("🙄 I don't have permissions `embed_links`")

    @commands.command(invoke_without_command=True, help='To know the connection speed of the bot on the server')
    @commands.guild_only()
    async def ping(self, ctx):

        before = time.monotonic()

        embed = discord.Embed(
            description='!pong',
            timestamp=ctx.message.created_at,
            color=ctx.author.color)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        msg = await ctx.send(embed=embed)
        ping = (time.monotonic() - before) * 1000
        embed = discord.Embed(
            description='''Time taken: `{} ms`
Discord API: `{} ms`
            '''.format(int(ping), round(self.client.latency * 1000)),
            timestamp=ctx.message.created_at,
            color=ctx.author.color)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        await msg.edit(content="pong!", embed=embed)

    @ping.error
    async def ping_error(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.group(invoke_without_command=True, help='To know the personal avatar')
    @commands.guild_only()
    async def avatar(self, ctx, member: discord.Member = None):
        member = member if member else ctx.author
        embed = discord.Embed(
            title='avatar',
            description='**[png]({}) | [jpg]({}) | [jpeg]({}) **'.format(
                member.avatar_url_as(format="png"),
                member.avatar_url_as(format="jpg"),
                member.avatar_url_as(format="jpeg")), timestamp=ctx.message.created_at)
        embed.set_image(url=member.avatar_url_as(size=1024))
        await ctx.send(embed=embed)

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send('🙄 I could not find this member')        
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("🙄 I don't have permissions `embed_links`")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass
        if isinstance(ctx.channel, commands.errors.CommandOnCooldown):
            await ctx.send(error)
    
    @avatar.command()
    @commands.guild_only()
    async def server(self, ctx):
        """Shows the server icon."""
        embed = discord.Embed(
            title="Server icon",
            description="[Server Icon]({}).".format(ctx.guild.icon_url),
            colour=0X008CFF)
        embed.set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @server.error
    async def icon_error(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @avatar.command()
    @commands.guild_only()
    async def bot(self, ctx):
        """Shows the avatar bot."""
        embed = discord.Embed(
            title="Bot avatar",
            description="[Bot avatar]({}).".format(self.client.user.avatar_url),
            colour=0X008CFF)
        embed.set_image(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @bot.error
    async def bot_error(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass


'''
    @commands.command()
    async def msgg(self, ctx, *, arg):


        img = Image.open("./img/text.png")

        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype("arial.ttf", size=24)

        draw.text((0, 400), arg, font=font)

        img.save('./img/text.png')

        await ctx.send(file = discord.File("./img/text.png"))

    @commands.command()
    async def length(self, ctx, *, arg):
        await ctx.send('Your message is `{}` characters long.'.format(len(arg)))
    @length.error
    async def length_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("error")
'''


def setup(client):
    client.add_cog(command(client))
