import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO
from PIL import ImageFont, ImageDraw
import arabic_reshaper


class info(commands.Cog):
    """
    Informations commands
    """

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, no_pm=True, help='Shows list roles in the server')
    @commands.guild_only()
    async def roles(self, ctx):
        roles = [r.mention for r in ctx.guild.roles]
        embed = discord.Embed(
            title="Roles",
            description="the current roles are \n{}".format(" | ".join(roles)),
            colour=ctx.author.color)
        await ctx.send(embed=embed)

    @roles.error
    async def roles_error(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(aliases=['bot'], help='show bot info')
    @commands.guild_only()
    async def botinfo(self, ctx):
        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            color=ctx.author.color,
            description=f"""
`SumBot`: It is an easy-to-use bot made in history {self.client.user.created_at.strftime("%d/%m/%Y")}
`length server`: {len(self.client.guilds)}
`length channel`: {sum(1 for g in self.client.guilds for _ in g.channels)}
`language`: python
`library`: discord.py
`invite bot`: [click here](https://discord.com/oauth2/authorize?client_id={self.client.user.id}&scope=bot&permissions=8)
`ping bot`: {self.client.ws.latency * 1000:.0f}ms
""")
        await ctx.send(embed=embed)

    @botinfo.error
    async def botinfo_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("🙄 I don't have permissions")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(aliases=['s'], pass_context=True, help='show server info')
    @commands.guild_only()
    async def server(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(
            title='server info',
            timestamp=ctx.message.created_at)
        embed.add_field(name='📛 | Name', value=guild.name)
        embed.add_field(name='🆔 | guild id', value=guild.id)
        embed.add_field(name='👑 | Owner', value='<@' + str(guild.owner_id) + ">")
        embed.add_field(name='👥 | Members', value=guild.member_count)
        embed.add_field(
            name=f'channels({len(guild.channels)})',
            value=f'''
📣 Categories: {len(guild.categories)}
💬 text: {len(ctx.guild.text_channels)} 
🔊 voice: {len(ctx.guild.voice_channels)}''')
        embed.add_field(name='🕍 | created at', value=guild.created_at.strftime("%m/%d/%Y, %H:%M:%S %p"))
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text='Requested by {}'.format(ctx.author.display_name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @server.error
    async def server_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("🙄 I don't have permissions")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(aliases=['id', 'userinfo'], help='show user info')
    @commands.guild_only()
    async def user(self, ctx, member: discord.Member = None):
        member = member if member else ctx.author

        embed = discord.Embed(colour=ctx.author.color, timestamp=ctx.message.created_at)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="👤 | user", value=member.display_name + "#" + member.discriminator, inline=True)
        embed.add_field(name='🆔 | id', value=member.id, inline=False)
        embed.add_field(name='👏 | created at', value=member.created_at.strftime("%Y/%m/%d"), inline=True)
        embed.add_field(name='😍 | joined at', value=member.joined_at.strftime("%Y/%m/%d"), inline=False)
        await ctx.send(embed=embed)

    @user.error
    async def user_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send('🙄 I could not find this member')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("🙄 I don't have permissions")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    # @commands.command(help='show the profile')
    # @commands.guild_only()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    # async def profile(self, ctx, user: discord.Member = None):
    #     if user == None:
    #         user = ctx.author
    #
    #     img = Image.open("./img/SumBot.png")
    #     ava = user.avatar_url_as(size=128)
    #     data = BytesIO(await ava.read())
    #     pfp = Image.open(data)
    #     pfp = pfp.resize((123, 98))
    #     img.paste(pfp, (83, 28))
    #     username = user.name
    #     reshaped_text = arabic_reshaper.reshape(username)
    #     draw = ImageDraw.Draw(img)
    #     font = ImageFont.truetype("arial.ttf", size=24)
    #     draw.text((52, 173), reshaped_text, font=font)
    #     img.save(f'./img/profile.png')
    #     await ctx.send(file=discord.File(f"./img/profile.png"))
    #
    # @profile.error
    # async def profile_error(self, ctx, error):
    #
    #     if isinstance(error, commands.errors.MemberNotFound):
    #         await ctx.send('🙄 I could not find this member')
    #
    #     elif isinstance(ctx.channel, discord.channel.DMChannel):
    #         pass
    #     else:
    #         await ctx.send(error)
    #
    # @commands.group(name='devs', help='Information all developers')
    # @commands.guild_only()
    # def info_devs(self, ctx):
    #     embed = discord.Embed(
    #         title='info developers',
    #         color=ctx.author.color,
    #         timestamp=ctx.message.created_at
    #     )
    #     embed.add_field(
    #         name="hazem",)
    #
    #
    #     embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
    #     embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
    @commands.command(help='show the profile')
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def profile(self, ctx, user: discord.Member = None):

        if user == None:
            user = ctx.author
        img = Image.open("./img/profile_sorce.png")  # import img

        ava = user.avatar_url_as(size=128)  # save avatar user
        data = BytesIO(await ava.read())  # None

        pfp = Image.open(data)  # open img

        pfp = pfp.resize((230, 230))  # resize avatar url
        img.paste(pfp, (593, 21))  # None

        draw = ImageDraw.Draw(img)  # draw img
        font = ImageFont.truetype("./fonts/Sukar_Black.ttf", size=40)  # font all text
        shadow_color = "yellow"  # shadow color all text
        stroke_width = 2  # stroke width
        color_stroke = "black"  # color stroke

        username = user.name  # get user name
        user_tag = "#" + user.discriminator  # get user tag
        join_at = user.created_at.strftime("%Y/%m/%d")  # get join at
        user_id = user.id  # get user id

        # fonts and size name
        draw.text(
            [180, 67],
            arabic_reshaper.reshape(username),  # add arabic
            font=font,
            fill=shadow_color,
            stroke_width=stroke_width,
            stroke_fill=color_stroke)

        # fonts and size tag
        draw.text(
            [124, 169],
            user_tag,
            font=font,
            fill=shadow_color,
            stroke_width=stroke_width,
            stroke_fill=color_stroke)

        # fonts and size join at
        draw.text(
            [185, 269],
            join_at,
            font=font,
            fill=shadow_color,
            stroke_width=stroke_width,
            stroke_fill=color_stroke)

        # fonts and size user id
        draw.text(
            [115, 375],
            str(user_id),
            font=font,
            fill=shadow_color,
            stroke_width=stroke_width,
            stroke_fill=color_stroke)

        # copy rights SumBot
        draw.text(
            [580, 375],
            "© SumBot",
            font=font,
            fill="black",
            stroke_width=2,
            stroke_fill="white")

        img.save(f'./img/profile.png')  # save img

        await ctx.send(file=discord.File(f"./img/profile.png"))  # send profile img

    @profile.error
    async def profile_error(self, ctx, error):

        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send('🙄 I could not find this member')

        elif isinstance(ctx.channel, discord.channel.DMChannel):
            pass
        else:
            await ctx.send(error)


def setup(client):
    client.add_cog(info(client))
