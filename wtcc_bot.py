#!/usr/bin/env python3

from os import environ
import discord
from discord.app import Option
import rmp_info
import course_info
from bs4 import BeautifulSoup
import requests


## currently broken in conjunction with pycord, set manually instead ##
# Set your own server's guild id and bot token
#guild_id = environ.get("GUILD")
#token = environ.get("TOKEN")
guild_id = [] # must be a list
token = ""

# embed message color
WAKETECH_BLUE = 0x005480

# bot initilization
bot = discord.Bot()

### DEBUG OPTIONS ###
DEBUG = False

if DEBUG:
    import logging

    logging.basicConfig(level=logging.WARNING)

    # Discord bot token & guild ID. must be in order on separate lines
    f = open("debug.txt")
    lines = f.readlines()
    token = lines[0]
    guild = int(lines[1])
    guild_id = []
    guild_id.append(guild)

    @bot.command(guild_ids=guild_id,
                description="Verify response and latency")
    async def ping(ctx):
        await ctx.respond(f"Pong! ({bot.latency*1000}ms)")

    @bot.command(guild_ids=guild_id,
                description="Graceful shutdown")
    async def logout(ctx):
        await ctx.respond("Shutting down...")
        await bot.close()
### END DEBUG OPTIONS ###

@bot.event
async def on_ready():
    print("Ready!")
    await bot.change_presence(status=discord.Status.online,
                    activity=discord.Game('Use /help for more info!'))

# help/usage
@bot.command(guild_ids=guild_id,
            description="Get more info about the bot and commands")
async def help(ctx):
    embed = discord.Embed(
        title="WTCC Bot Help",
        description="""WTCC bot is a Discord bot which pulls information from Wake Tech's course descriptions and RateMyProfessors.com.
        
        **Course Descriptions**
        Use `/course` to find out more information about a course.
        
        **RateMyProfessor**
        Use `/professor` to get ratings on a professor from ratemyprofessor.com
        
        **Source Code**
        [Click here](https://github.com/dfuentes87/wtcc_bot/)
        """,
        color=WAKETECH_BLUE,
    )
    embed.set_footer(
        text="Questions, suggestions, problems? Send a message to netdragon#3288"
    )
    await ctx.respond(embed=embed)


# ratemyprofessor
@bot.command(guild_ids=guild_id,
            description="Get ratings on a professor from ratemyprofessor.com")
async def professor(ctx,
    name: Option(str, "Professor's first and last name, e.g. Karen Klein", required=True)
):
    # Discord will only wait up to 3 seconds for a response, so we need to defer
    await ctx.defer()
    await ctx.followup.send(embed=rmp_info.embed_builder(name))


# course info
@bot.command(guild_ids=guild_id,
             description="Get information on a course.")
async def course(ctx,
    course: Option(str, "Enter a course (with hyphen), e.g. NET-125", required=True)
):
    ## dep = department, num = course number
    dep, num = str(course).split('-')

    url = (
        "https://waketech.edu/course/" + f"{course}"
    )
    r = requests.get(url)

    if r.status_code == 404:
        embed = discord.Embed(
            title="404: Course not found",
            description="That doesn't seem to be a real course, or it may no longer be offered. Also, keep in mind that you need to format the course with a hyphen: CTI-110",
            color=WAKETECH_BLUE,
        )
        embed.set_footer(
            text="Questions, suggestions, problems? Send a message to netdragon#3288"
        )
        await ctx.respond(embed=embed)
    else:
        await ctx.defer()
        await ctx.followup.send(embed=course_info.embed_builder(dep, url))


bot.run(token)
