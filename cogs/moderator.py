import discord
import asyncio
from discord.ext import commands


class mod(commands.Cog):
    """
    moderator commands
    """
    def __init__(self, client):
        self.client = client

    @commands.command(help='to re-send the your message')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, *, arg):
        await ctx.message.delete()
        await ctx.send(arg)

    @commands.has_permissions(manage_messages=True)
    @say.error
    async def say_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description='**Used:** `{}say <messgae>`\n**Type:** Mod'.format(self.client.command_prefix),
                color=ctx.author.color,
                timestamp=ctx.message.created_at)
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_image(url='http://g.recordit.co/ImNnlcwSYy.gif')
            await ctx.send(embed=embed)
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🙄 You don't have permissions")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(help='to re-send the your message in embed')
    @commands.guild_only()
    @commands.has_permissions(embed_links=True)
    async def embed(self, ctx, *, arg):
        embed = discord.Embed(
            description=arg,
            color=ctx.author.color,
            timestamp=ctx.message.created_at)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.has_permissions(embed_links=True)
    @embed.error
    async def embed_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description='**Used:** `{}embed <messgae>`\n**Type:** Mod'.format(self.client.command_prefix),
                color=ctx.author.color,
                timestamp=ctx.message.created_at)
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_image(url='http://g.recordit.co/NbrwofkvLJ.gif')
            await ctx.send(embed=embed)
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('I do not have permissions `embed_links`')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permissions `embed_links`")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(help="to remove the namber message")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):

        if amount > 200:
            await ctx.send('You cannot delete more than 200 messages.')
        elif amount <= 0:
            await ctx.send('You cannot delete less than one message.')
        else:
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount)
            await ctx.send(f"`{amount}` Message has been clear")
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=1)

    @commands.has_permissions(manage_messages=True)
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description='**Used:** `{}clear <namber>`\n**Type:** Mod'.format(self.client.command_prefix),
                color=ctx.author.color,
                timestamp=ctx.message.created_at)
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_image(url='http://g.recordit.co/E0OVM1nbKs.gif')
            await ctx.send(embed=embed)
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('🙄 I do not have permissions `manage messages`')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🙄 You don't have permissions `manage messages`")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(help='to hide the channel in everyone')
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def hide(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.read_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send('👤 | channel has been Hide {}'.format(channel.mention))

    @commands.has_permissions(manage_channels=True)
    @hide.error
    async def hide_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('🙄 I do not have permissions `manage channels`')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🙄 You don't have permissions `manage channels`")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(help="to unhide the channel in everyone")
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def unhide(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.read_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send('👥 | channel has been unHide {}'.format(channel.mention))

    @commands.has_permissions(manage_channels=True)
    @unhide.error
    async def unhide_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('🙄 I do not have permissions `manage channels`')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🙄 You don't have permissions `manage channels`")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(help='to lock the channel in everyone')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send('🔒 | channel locked {}'.format(channel.mention))

    @commands.has_permissions(manage_messages=True)
    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('🙄 I do not have permissions `manage messages`')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🙄 You don't have permissions `manage messages`")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(help='to unlock the channel in everyone')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send('🔓 | channel unlock {}'.format(channel.mention))

    @commands.has_permissions(manage_messages=True)
    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('🙄 I do not have permissions `manage messages`')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🙄 You don't have permissions `manage messages`")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(invoke_without_command=True, help='to send the message in channel')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def echo(self, ctx, channel: discord.TextChannel, *, arg):
        await channel.send(arg)
        await ctx.send('Message was sent in {}'.format(channel.mention))

    @commands.has_permissions(manage_messages=True)
    @echo.error
    async def channel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description='**Used:** `{0}echo(channel, message)`\n**Type:** Mod\n**description:** To add the bot to your server'.format(self.client.command_prefix),
                color=ctx.author.color,
                timestamp=ctx.message.created_at)
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_image(url='http://g.recordit.co/03NiBJC2i9.gif')
            await ctx.send(embed=embed)   
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send('🙄 I could not find this channel') 
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send('🙄 You don\'t have permissions `manage messages`')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🙄 I don't have permissions")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

    @commands.command(help='to make the poll')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def poll(self, ctx, *, arg):

        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            description=arg,
            color=ctx.author.color)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        msg = await ctx.send("📢 poll 📢", embed=embed)
        await ctx.message.delete()
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

    @commands.has_permissions(manage_messages=True)
    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description='**Used:** `{}poll <messgae>`\n**Type:** Mod'.format(self.client.command_prefix),
                color=ctx.author.color,
                timestamp=ctx.message.created_at)
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_image(url='http://g.recordit.co/I5jL3Ibolt.gif')
            await ctx.send(embed=embed)
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send('🙄 You don\'t have permissions `manage messages`')
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass
    #
    # @commands.command(no_pm=True, pass_context=True)
    # @commands.has_permissions(manage_nicknames=True)
    # async def rename(self, ctx, user : discord.Member, *, nickname=""):
    #     """Changes user's nickname
    #
    #     Leaving the nickname empty will remove it."""
    #     nickname = nickname.strip()
    #     if nickname == "":
    #         nickname = None
    #     try:
    #         await self.client.change_nickname(user, nickname)
    #         await self.client.say("Done.")
    #     except discord.Forbidden:
    #         await self.client.say("I cannot do that, I lack the "
    #                            "\"Manage Nicknames\" permission.")

def setup(client):
    client.add_cog(mod(client))
