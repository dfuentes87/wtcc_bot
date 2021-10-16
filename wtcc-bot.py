#!/usr/bin/env python3

from os import environ
import discord
from discord.app import Option
import rmp_info
import course_info
from bs4 import BeautifulSoup
import requests

# Set your own server's guild id and bot token
guild_id = environ.get("GUILD")
token = environ.get("TOKEN")

bot = discord.Bot()

WAKETECH_BLUE = 0x005480

### DEBUG OPTIONS ###
DEBUG = True

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

    @bot.event
    async def on_ready():
        print("Ready!")

    # Verify response and latency
    @bot.command(guild_ids=guild_id,
                description="Verify response and latency")
    async def ping(ctx):
        await ctx.respond(f"Pong! ({bot.latency*1000}ms)")

    # Clean quit
    @bot.command(guild_ids=guild_id,
                description="Graceful shutdown")
    async def logout(ctx):
        await ctx.respond("Shutting down...")
        await bot.close()
### END DEBUG OPTIONS ###

# ratemyprofessor
@bot.command(guild_ids=guild_id,
            description="Check RateMyProfessors")
async def professor(ctx,
    name: Option(str, "Professor's first and last name, e.g. Karen Klein", required=True)
):
    # Discord will only wait up to 3 seconds for a response, so we need to defer
    await ctx.defer()
    await ctx.followup.send(embed=rmp_info.embed_builder(name))


# course info
@bot.command(guild_ids=guild_id,
             description="Get info on a course")
async def course(ctx,
    course: Option(str, "Enter a course (no hyphen), e.g. NET 125", required=True)
):
    ## dep = department, num = course number
    
    dep, num = str(course).split()

    url = (
        "https://waketech.edu/course/" + f"{dep}-{num}"
    )
    r = requests.get(url)

    if r.status_code == 404:
        embed = discord.Embed(
            title="404: Course not found",
            description="That doesn't seem to be a real course, or it may no longer be offered. You may also want to check the spelling of your command; remember that courses are formatted like this (no hyphen): CTI 110",
            color=WAKETECH_BLUE,
        )
        embed.set_footer(
            text="Questions, suggestions, problems? Send a message to netdragon#3288"
        )
        await ctx.respond(embed=embed)
    else:
        await ctx.defer()
        await ctx.followup.send(embed=course_info.course_embed_builder(dep, num, url))

bot.run(token)
