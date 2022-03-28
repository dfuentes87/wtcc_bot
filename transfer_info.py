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

    if program_title is None:
        embed = discord.Embed(
            title="404: Degree/Program not found",
            description="Check your spelling, otherwise that program/degree may not be transferable.\n \
            [Click here](https://www.waketech.edu/programs-courses/credit/transfer-choices/by-degree) \
            to check the full degree transfer list.",
            color=WAKETECH_BLUE,
        )
        embed.set_footer(
            text="Questions, suggestions, or problems regarding the bot? Send a message to netdragon#3288")

        return embed

    # title url (tbd?)

    # program transfer options
    program_details = ""
    for item in soup.find_all("strong"):
        if program_title in str(item):
            for children in item.find_all_next("tr"):
                if "strong" not in str(children):
                    children = str(children)
                    children = re.sub('<.?tr>','',children)
                    children = re.sub('<.?td>', '**', children, 2)
                    children = re.sub('<.?td>', '', children, 2)
                    children = re.sub('\n', '', children, 1)
                    # remove annoying HTML 'amp;'
                    children = children.replace('amp;','')
                    program_details += children + "\n"
                else:
                    break

    short_url = "[Click here](https://www.waketech.edu/programs-courses/credit/transfer-choices/by-degree)"

    # create the embed
    embed = discord.Embed(
        title="TRANSFER OPTIONS FOR: \n" + program_title,
        # url=url,
        description=program_details,
        color=WAKETECH_BLUE,
    )
    embed.add_field(name="Full List of Transfer Options by Degree:", value=short_url, inline=True)

    return embed


def embed_builder_uni(university, transfer_link=None):
    url = 'https://www.waketech.edu/programs-courses/credit/transfer-choices/search-college'
    page = requests.get(url)
    # get rid of everything but the universities
    uni_list = SoupStrainer(class_="paragraph--view-mode--default panel-heading faq")
    soup = BeautifulSoup(page.content, "lxml", parse_only=uni_list)

    # '^' will make regex do a 'starts with' search
    university = "^" + university
    university_name = soup.find(string=re.compile(university, re.IGNORECASE))

    if university_name is None:
        embed = discord.Embed(
            title="404: University not found",
            description="Keep in mind only NC universities are listed. You may want to double check your spelling?\n \
            [Click here](https://www.waketech.edu/programs-courses/credit/transfer-choices/search-college#) \
            to see the full list of NC universities.",
            color=WAKETECH_BLUE,
        )
        embed.set_footer(
            text="Questions, suggestions, or problems regarding the bot? Send a message to netdragon#3288")

        return embed

    # title url (tbd..anchor?)

    # list of degrees

    # transfer link

    # aas transfer link

    # transfer degree plans link (including AE)

    # talk with advisor url

    # create the embed
    embed = discord.Embed(
        title="TRANSFER OPTIONS FOR: \n" + university_name,
        # url=url,
        description=degree_list,
        color=WAKETECH_BLUE,
    )
    if transfer_link is not None:
        embed.add_field(name="Transfer Link", value=reqs, inline=True)
    if aas_link is not None:
        embed.add_field(name="AAS Transfer Link", value=reqs, inline=True)
    if degree_plan is not None:
        embed.add_field(name="Transfer Degree Plans", value=reqs, inline=True)
    if advisor_link is not None:
        embed.add_field(name="Talk with a University Advisor", value=advisor_link, inline=True)

    return embed
