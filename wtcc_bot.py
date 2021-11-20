#!/usr/bin/env python3

from os import environ
import discord
from discord.commands import Option
import rmp_info
import course_info
from bs4 import BeautifulSoup
import requests
import transfer_info


# Set your own server's guild id and bot token
# for security reasons, this is being done using enviornmental variables
token = environ.get("TOKEN")
guild = int(environ.get("GUILD"))
guild_id = []
guild_id.append(guild)

# embed message color
WAKETECH_BLUE = 0x005480

# bot initilization
bot = discord.Bot()

### DEBUG OPTIONS ###
DEBUG = False

if DEBUG:
    import logging

    logging.basicConfig(level=logging.WARNING)

    # token & guild ID used for debugging; must be in order and on separate lines
    f = open("debug.txt")
    lines = f.readlines()
    token = lines[0]
    guild = int(lines[1])
    guild_id = []
    guild_id.append(guild)
    f.close()

    @bot.command(guild_ids=guild_id, description="Verify response and latency")
    async def ping(ctx):
        await ctx.respond(f"Pong! ({bot.latency*1000}ms)")

    @bot.command(guild_ids=guild_id, description="Graceful shutdown")
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
@bot.command(guild_ids=guild_id, description="Get more info about the bot and commands")
async def help(ctx):
    embed = discord.Embed(
        title="WTCC Bot Help",
        description="""WTCC bot is a Discord bot which pulls information from Wake Tech's course descriptions and RateMyProfessors.com.
        
        **Course Descriptions**
        Use `/course` to find out more information about a course.
        
        **Rate My Professors**
        Use `/professor` to get ratings on a professor from ratemyprofessors.com

        **Transfer Options** (coming soon)
        Use `/transfer` to see transfer information and options based on a program/degree or the university you want to transfer to.
        
        **Source Code**
        [Click here](https://github.com/dfuentes87/wtcc_bot/)
        """,
        color=WAKETECH_BLUE,
    )
    embed.set_footer(
        text="Questions, suggestions, or problems regarding the bot? Send a message to netdragon#3288"
    )
    await ctx.respond(embed=embed)


# ratemyprofessors
@bot.command(guild_ids=guild_id, description="Get ratings on a professor from ratemyprofessors.com")
async def professor(ctx,
    name: Option(str, "Professor's first and last name, e.g. Karen Klein", required=True)
):
    # Discord will only wait up to 3 seconds for a response, so we need to defer
    await ctx.defer()
    await ctx.followup.send(embed=rmp_info.embed_builder(name))


# course info
@bot.command(guild_ids=guild_id, description="Get information on a course.")
async def course(ctx,
    id: Option(str, "Enter a course, for example: NET-125", required=True)
):
    # add hyphen if missing, needed for url
    course = str(id)
    if '-' not in course:
        course = course.replace(' ','-',1)

    url = (
        "https://waketech.edu/course/" + f"{course}"
    )
    r = requests.get(url)

    if r.status_code == 404:
        embed = discord.Embed(
            title="404: Course not found",
            description="That doesn't seem to be a real course or it may no longer be offered.",
            color=WAKETECH_BLUE,
        )
        embed.set_footer(
            text="Questions, suggestions, or problems regarding the bot? Send a message to netdragon#3288"
        )
        await ctx.respond(embed=embed)
    else:
        await ctx.defer()
        await ctx.followup.send(embed=course_info.embed_builder(course, url))


# transfer info
@bot.command(guild_ids=guild_id, description="Find your transfer options by Program/Degree or NC University (pick only ONE option).")
async def transfer(ctx,
    program: Option(str, "Enter program or degree name, e.g. 'Simulation and Game Development' or 'Associate in Engineering'", required=False),
    university: Option(str, "Enter a NC university name, e.g. 'East Carolina University'", required=False)
):
    # fancy xor usage to force only one option
    if bool(program) ^ bool(university):
        await ctx.defer()
        #await ctx.followup.send(embed=transfer_info.embed_builder_prog(Program))
        await ctx.followup.send("Work in progress, keep an eye on #server-announcements for when this functionality is ready!")
    else:
        embed = discord.Embed(
            title="400: Bad Request",
            description="You can only do one type of a search at a time, either for a Program/Degree OR a University.",
            color=WAKETECH_BLUE,
        )
        embed.set_footer(
            text="Questions, suggestions, or problems regarding the bot? Send a message to netdragon#3288"
        )
        await ctx.respond(embed=embed)


bot.run(token)
