__all__ = ["helper"]

import asyncio
from random import randint
from typing import List, Union

import discord
from discord.ext import commands
from discord.ext.commands.cog import Cog
from discord.ext.commands.help import HelpCommand

from .navigation import Navigation


class Paginator:

    def __init__(
        self,
        color=0,
    ):
        self.ending_note = None
        self.color = color
        self.char_limit = 6000
        self.field_limit = 26
        self.prefix = "```"
        self.suffix = "```"
        self.clear()

    def clear(self):
        self._pages = []

    def _check_embed(self, embed: discord.Embed, *chars: str):
        check = (
            len(embed) + sum(len(char) for char in chars if char) < self.char_limit
            or len(embed.fields) < self.field_limit
        )
        return check

    def _new_page(self, title: str):
        return discord.Embed(
            title=title,
            color=self.color,
            description='**[invite bot](https://discord.com/oauth2/authorize?client_id=738120633430573176&scope=bot&permissions=8) | [support bot](https://discord.gg/BZKJfqZ) | [Vote](https://top.gg/bot/738120633430573176)**')

    def _add_page(self, page: discord.Embed):
        page.set_footer(text=self.ending_note)
        self._pages.append(page)

    def add_cog(
        self, title: Union[str, commands.Cog], commands_list: List[commands.Command]
    ):
        cog = isinstance(title, commands.Cog)
        if not commands_list:
            return

        page_title = title.qualified_name if cog else title
        embed = self._new_page(page_title)
        embed.description = (title.description or "") if cog else ""

        self._add_command_fields(embed, page_title, commands_list)

    def _add_command_fields(
        self, embed: discord.Embed, page_title: str, commands: List[commands.Command]):

        for command in commands:
            if not self._check_embed(
                embed,
                self.ending_note,
                command.name,
                command.short_doc,
                self.prefix,
                self.suffix,
            ):
                self._add_page(embed)
                embed = self._new_page(page_title)

            embed.add_field(
                name=command.name,
                value=f'{self.prefix}{command.short_doc or "No Description"}{self.suffix}',
                inline=False,
            )

        self._add_page(embed)

    def add_command(self, command: commands.Command, signature: str):

        page = self._new_page(command.qualified_name)
        page.description = f"{self.prefix}{command.help}{self.suffix}" or ""
        if command.aliases:
            aliases = ", ".join(command.aliases)
            page.add_field(
                name="Aliases",
                value=f"{self.prefix}{aliases}{self.suffix}",
                inline=False,
            )
        page.add_field(
            name="Usage", value=f"{self.prefix}{signature}{self.suffix}", inline=False
        )
        page.add_field(name = 'Info', value='**[vote](https://top.gg/bot/738120633430573176) | [invite bot](https://discord.com/oauth2/authorize?client_id=738120633430573176&scope=bot&permissions=8) | [support](<https://discord.gg/WGEbtCuFbj>)**')

        self._add_page(page)

    def add_group(self, group: commands.Group, commands_list: List[commands.Command]):

        page = self._new_page(group.name)
        page.description = f"{self.prefix}{group.help}{self.suffix}" or ""
        self._add_command_fields(page, group.name, commands_list)

    def add_index(self, include: bool, title: str, bot: commands.Bot):
        if include:
            index = self._new_page(title)
            index.description = bot.description or ""
            for page_no, page in enumerate(self._pages, 2):
                index.add_field(
                    name=f"{page_no}) {page.title}",
                    value=f'{self.prefix}{page.description or "No Description"}{self.suffix}',
                    inline=False,
                )
            index.set_footer(text=self.ending_note)
            self._pages.insert(0, index)
        else:
            self._pages[0].description = bot.description

    @property
    def pages(self):
        if len(self._pages) == 1:
            return self._pages
        lst = []
        for page_no, page in enumerate(self._pages, start=1):
            page: discord.Embed
            page.description = (
                f"`Page: {page_no}/{len(self._pages)}`\n{page.description}")

            lst.append(page)
            page.add_field(name='Info', value='**[invite bot](https://discord.com/oauth2/authorize?client_id=738120633430573176&scope=bot&permissions=8) | [support bot](https://discord.gg/BZKJfqZ) | [Vote](https://top.gg/bot/738120633430573176)**')
        return lst


class help_command(HelpCommand):

    def __init__(self, **options):

        self.active_time = options.pop("active_time", 30)
        self.color = options.pop(
            "color",
            discord.Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)),
        )
        self.dm_help = options.pop("dm_help", False)
        self.index_title = options.pop("index_title", "Categories")
        self.navigation = options.pop("navigation", Navigation())
        self.no_category = options.pop("no_category", "No Category")
        self.sort_commands = options.pop("sort_commands", True)
        self.show_index = options.pop("show_index", True)
        self.paginator = Paginator(color=self.color)

        super().__init__(**options)

    async def prepare_help_command(self, ctx: commands.Context, command: commands.Command):
        if ctx.guild is not None:
            perms = ctx.channel.permissions_for(ctx.guild.me)
            if not perms.embed_links:
                raise commands.BotMissingPermissions(("embed links",))
            if not perms.read_message_history:
                raise commands.BotMissingPermissions(("read message history",))
            if not perms.add_reactions:
                raise commands.BotMissingPermissions(("add reactions permission",))

        self.paginator.clear()
        self.paginator.ending_note = self.get_ending_note()
        await super().prepare_help_command(ctx, command)

    def get_ending_note(self):
        command_name = self.invoked_with
        return (
            "Type {0}{1} command for more info on a command.\n"
            "You can also type {0}{1} category for more info on a category.".format(
                self.clean_prefix, command_name
            )
        )

    async def send_pages(self):

        pages = self.paginator.pages
        total = len(pages)
        destination = self.get_destination()

        message: discord.Message = await destination.send(embed=pages[0])

        if total > 1:
            bot: commands.Bot = self.context.bot
            navigating = True
            index = 0

            for reaction in self.navigation:
                await message.add_reaction(reaction)

            while navigating:
                try:

                    def check(payload: discord.RawReactionActionEvent):

                        if (
                            payload.user_id != bot.user.id
                            and message.id == payload.message_id
                        ):
                            return True

                    payload: discord.RawReactionActionEvent = await bot.wait_for(
                        "raw_reaction_add", timeout=self.active_time, check=check
                    )

                    emoji_name = (
                        payload.emoji.name
                        if payload.emoji.id is None
                        else f":{payload.emoji.name}:{payload.emoji.id}"
                    )
                    if (
                        emoji_name in self.navigation
                        and payload.user_id == self.context.author.id
                    ):
                        nav = self.navigation.get(emoji_name)
                        if not nav:

                            navigating = False
                            return await message.delete()
                        else:
                            index += nav
                            embed: discord.Embed = pages[index % total]

                            await message.edit(embed=embed)

                    try:
                        await message.remove_reaction(
                            payload.emoji, discord.Object(id=payload.user_id)
                        )
                    except discord.errors.Forbidden:
                        pass

                except asyncio.TimeoutError:
                    navigating = False
                    for emoji in self.navigation:
                        try:
                            await message.remove_reaction(emoji, bot.user)
                        except Exception:
                            pass

    def get_destination(self):
        ctx = self.context
        if self.dm_help is True:
            return ctx.author
        else:
            return ctx.channel

    async def send_bot_help(self, mapping: dict):
        bot = self.context.bot
        channel = self.get_destination()
        async with channel.typing():
            mapping = dict((name, []) for name in mapping)
            help_filtered = (
                filter(lambda c: c.name != "help", bot.commands)
                if len(bot.commands) > 1
                else bot.commands
            )
            for cmd in await self.filter_commands(
                help_filtered,
                sort=self.sort_commands,
            ):
                mapping[cmd.cog].append(cmd)
            self.paginator.add_cog(self.no_category, mapping.pop(None))
            sorted_map = sorted(
                mapping.items(),
                key=lambda cg: cg[0].qualified_name
                if isinstance(cg[0], commands.Cog)
                else str(cg[0]),
            )
            for cog, command_list in sorted_map:
                self.paginator.add_cog(cog, command_list)
            self.paginator.add_index(self.show_index, self.index_title, bot)
        await self.send_pages()

    async def send_command_help(self, command: commands.Command):
        filtered = await self.filter_commands([command])
        if filtered:
            self.paginator.add_command(command, self.get_command_signature(command))
            await self.send_pages()

    async def send_group_help(self, group: commands.Group):
        async with self.get_destination().typing():
            filtered = await self.filter_commands(
                group.commands, sort=self.sort_commands
            )
            if filtered:
                self.paginator.add_group(group, filtered)
        await self.send_pages()

    async def send_cog_help(self, cog: commands.Cog):
        async with self.get_destination().typing():
            filtered = await self.filter_commands(
                cog.get_commands(), sort=self.sort_commands
            )
            self.paginator.add_cog(cog, filtered)
        await self.send_pages()
