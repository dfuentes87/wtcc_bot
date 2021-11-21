#!/usr/bin/env python3

import discord
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
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
    # get rid of everything but the table data
    institution_table = SoupStrainer(class_="table table-striped table-responsive")
    soup = BeautifulSoup(page.content, "lxml", parse_only=institution_table)

    # '^' will make regex do a 'starts with' search
    program = "^" + program
    program_title = soup.find(string=re.compile(program, re.IGNORECASE))

    # title url (tbd?)

    if program_title is None:
        embed = discord.Embed(
            title="404: Degree/Program not found",
            description="Check your spelling, otherwise that program/degree may not be transferable.\n[Click here](https://www.waketech.edu/programs-courses/credit/transfer-choices/by-degree) to check the full degree transfer list.",
            color=WAKETECH_BLUE,
        )
        embed.set_footer(
            text="Questions, suggestions, or problems regarding the bot? Send a message to netdragon#3288")

        return embed

    # program transfer options
    program_details = ""
    for item in soup.find_all("strong"):
        if program_title in str(item):
            for next in item.find_all_next("tr"):
                if "strong" not in str(next):
                    next = str(next)
                    next = re.sub('<.*?>','',next, flags=re.DOTALL)
                    details = next.replace('\n','** : ',1)
                    details = "**" + details
                    # remove annoying HTML 'amp;'
                    details = details.replace('amp;','')
                    program_details += details + "\n"
                else:
                    break

    short_url = "[Click here](https://www.waketech.edu/programs-courses/credit/transfer-choices/by-degree)"

    # create the embed
    embed = discord.Embed(
        title="TRANSFER OPTIONS FOR: \n" + program_title,
        #url=url,
        description=program_details,
        color=WAKETECH_BLUE,
    )
    embed.add_field(name="Full List of Transfer Options by Degree:", value=short_url, inline=True)

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