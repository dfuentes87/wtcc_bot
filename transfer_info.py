#!/usr/bin/env python3

import discord
from bs4 import BeautifulSoup
import requests
import re

WAKETECH_BLUE = 0x005480

"""
We're going to be using BeautifulSoup (https://beautiful-soup-4.readthedocs.io) to 
render the page in HTML to easily pullout the items we need to created the embeded response.
"""

def embed_builder_prog(program):
    url = 'https://www.waketech.edu/programs-courses/credit/transfer-choices/by-degree'
    page = requests.get(url)
    content = page.content
    soup = BeautifulSoup(content, 'lxml')

    # program/degree title
    # PROGRAM/DEGREE

    # title url (tbd)

    # description
    # **Institution**
    # "College or Program Transfers To"

    short_url = "[Click here](https://www.waketech.edu/programs-courses/credit/transfer-choices/by-degree)"

    # create the embed
    embed = discord.Embed(
        title=program_title,
        #url=url,
        description=program_description,
        color=WAKETECH_BLUE,
    )
    embed.add_field(name="Comprehensive List of Transfer Options", value=short_url, inline=True)


    return embed


def embed_builder_uni(university):
    url = 'https://www.waketech.edu/programs-courses/credit/transfer-choices/search-college'
    page = requests.get(url)
    content = page.content
    soup = BeautifulSoup(content, 'lxml')

    # university name
    ## UNIVERSITYNAME

    # url (tbd..anchor?)

    # description
    ## affiliation & list of degrees/programs

    # transfer link


    # aas transfer link


    # transfer degree plans link (including AE)


    # talk with advisor url


    # create the embed
    embed = discord.Embed(
        title=university_name,
        #url=url,
        description=program_description,
        color=WAKETECH_BLUE,
    )
    embed.add_field(name="Transfer Link", value=reqs, inline=True)
    embed.add_field(name="AAS Transfer Link", value=reqs, inline=True)
    embed.add_field(name="Transfer Degree Plans", value=reqs, inline=True)
    if advisor_url is not None:
        embed.add_field(name="Talk with a University Advisor", value=advisor_url, inline=True)


    return embed