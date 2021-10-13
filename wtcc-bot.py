#!/usr/bin/env python3

from os import environ
import discord
import discord_slash
from discord_slash.utils import manage_commands
from discord_slash.utils.manage_commands import create_option
import rmp_info
import course_info
from bs4 import BeautifulSoup
import requests

# make sure to set your guild id and token
guild_id = environ.get("GUILD")
token = environ.get("TOKEN")

bot = discord.Bot()
client = discord.Client(intents=discord.Intents.default())
slash = discord_slash.SlashCommand(client, sync_commands=True)

WAKETECH_BLUE = 0x005480

### DEBUG OPTIONS ###
DEBUG = True

if DEBUG:
    import logging

    logging.basicConfig(level=logging.WARNING)

    # Discord bot token & guild ID
    f = open("debug.txt")
    lines = f.readlines()
    token = lines[0]
    guild = int(lines[1])
    guild_id = []
    guild_id.append(guild)

    @bot.event
    async def on_ready():
        print("Ready!")

    # Verify response and latency
    @bot.slash_command(name="ping", guild_ids=guild_id)
    async def ping(ctx):
        await ctx.send(f"Pong! ({bot.latency*1000}ms)")

    # clean quit
    @bot.slash_command(name="logout", guild_ids=guild_id,
                description="Graceful shutdown")
    async def logout(ctx):
        await ctx.send("Shutting down...")
        await bot.close()
### END DEBUG OPTIONS ###

# ratemyprofessor
@bot.slash_command(name="professor", guild_ids=guild_id,
             description="Check RateMyProfessors: Enter first and last name only!",
             options=[
               create_option(
                 name="Professor Name",
                 description="Professor's first and last name",
                 option_type=3,
                 required=True
               )
             ])
async def professor(ctx, name):
    # Discord will only wait up to 3 seconds for a response, so we need to defer
    await ctx.defer()
    await ctx.followup.send(embed=rmp_info.embed_builder(name))


# course info
@bot.slash_command(name="course", guild_ids=guild_id,
             description="Get info on a course, e.g. NET 125",
             options=[
               create_option(
                 name="Course Info",
                 description="Course number",
                 option_type=3,
                 required=True
               )
             ])
# dep = department, num = course number. space is required 
async def get(ctx, dep, num):
    url = (
        "https://waketech.edu/course/"
        + f"{dep}-{num}"
    )
    r = requests.get(url)

    if r.status_code == 404:
        embed = discord.Embed(
            title="404: Course not found",
            description="That doesn't seem to be a real course, or it may no longer be offered. You may also want to check the spelling of your command; remember that courses are formatted like this: CTI 110.",
            color=WAKETECH_BLUE,
        )
        embed.set_footer(
            text="Questions, suggestions, problems? Send a message to netdragon#3288"
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=course_info.embed_builder(dep, num, url))

bot.run(token)
