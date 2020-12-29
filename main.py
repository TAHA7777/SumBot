import discord
from discord.ext import commands
import os
import json
from datetime import datetime
import pyfiglet
from prettytable import PrettyTable
# import sqlite3
from Lib.help.help_SumBot import help_command

with open('./config.json', 'r') as f:
    config = json.load(f)

EXTENSIONS = [
    "commands",
    "fun",
    "giveaway",
    "info",
    "moderator",
    "random"
    # "mis"
]


# db = sqlite3.connect('app.db')
#
# cr = db.cursor()
#
#
# def close_and_save():
#    db.commit()
#
#    db.close()


class SumBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=config["prefix"],
            case_insensitive=True,
            allowed_mentions=discord.AllowedMentions(
                everyone=config["mention"]["everyone"],
                users=config["mention"]["users"],
                roles=config["mention"]["roles"]),
            help_command=help_command())
        self.client_id = config["client_id"]
        self.owner_id = config["owner_id"]

#        self.remove_command('help')

        if config["token"] == "" or config["token"] == "token":
            self.token = os.environ['token']
        else:
            self.token = config["token"]

        for filename in EXTENSIONS:
            try:
                self.load_extension(f'cogs.{filename}')
                print('lode {}'.format(filename))
            except:
                print('error in {}'.format(filename))

    async def on_ready(self):
        activity = discord.Game(name="{}help | server {}".format(self.command_prefix, len(self.guilds)), type=3)
        await self.change_presence(status=discord.Status.online, activity=activity)
        tap = PrettyTable(
            ['Name Bot', 'Tag', 'Id', 'prefix', 'guilds', 'commands', 'Usage'])
        tap.add_row([ 
            self.user.name,
            '#' + self.user.discriminator,
            self.user.id,
            self.command_prefix,
            len(self.guilds),
            len(self.commands),
            len(self.users),
            
        ])
        print(tap)
        print(pyfiglet.figlet_format(self.user.name), end=" ")

#        async for guild in self.fetch_guilds(limit=2):
#            print(guild.name, end=" ,")

    async def on_guild_join(self, guild):
        channel = self.get_channel(config["channel"]["join"])
        now = datetime.now()
        try:
            embed = discord.Embed(title="add guild", color=0x46FF00)

            embed.add_field(name='name guild: ', value=guild.name, inline=False)
            embed.add_field(name='id guild: ', value=guild.id, inline=False)
            embed.add_field(name='owner guild: ', value='<@' + str(guild.owner_id) + ">", inline=False)
            embed.add_field(name='owner id: ', value=str(guild.owner_id), inline=False)
            embed.add_field(name='member guild: ', value=guild.member_count, inline=False)
            embed.add_field(name='bot server: ', value=self.guilds, inline=False)
            embed.set_footer(text=guild.name, icon_url=guild.icon_url)
            embed.set_author(name=self.user.name, icon_url=self.user.avatar_url)
            await channel.send(now.strftime("%d/%m/%Y, %H:%M"), embed=embed)
        except:
            print('error')

    async def on_guild_remove(self, guild):
        channel = self.get_channel(config['channel']["remove"])
        now = datetime.now()
        try:
            embed = discord.Embed(title="remove guild", color=0xFF0000)

            embed.add_field(name='name guild: ', value=guild.name, inline=False)
            embed.add_field(name='id guild: ', value=guild.id, inline=False)
            embed.add_field(name='owner guild: ', value='<@' + str(guild.owner_id) + ">", inline=False)
            embed.add_field(name='owner id: ', value=str(guild.owner_id), inline=False)
            embed.add_field(name='member guild: ', value=guild.member_count, inline=False)
            embed.add_field(name='bot server: ', value=self.guilds, inline=False)
            embed.set_footer(text=guild.name, icon_url=guild.icon_url)
            embed.set_author(name=self.user.name, icon_url=self.user.avatar_url)
            await channel.send(now.strftime("%d/%m/%Y, %H:%M"), embed=embed)
        except:
            print('error')

    def run(self):
        super().run(self.token, reconnect=True)


if __name__ == '__main__':
    client = SumBot()
    client.run()
