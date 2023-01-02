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
    institution_table = SoupStrainer(class_="wt-table")
    soup = BeautifulSoup(page.content, "lxml", parse_only=institution_table)

    # find the program and format the results
    program_details = ""
    program_title = None
    for item in soup.find_all("strong"):
        #print(item)
        # standardizes capitzalition for comparison
        user_entry = program.title()
        item_program = (re.sub('<.*?>', '', str(item), flags=re.DOTALL)).title()
        item_program = item_program.replace('Amp;', '')
        if user_entry in str(item_program):
            #print(item_program)
            program_title = (re.sub('<.*?>', '', str(item), flags=re.DOTALL)).title()
            program_title = program_title.replace('Amp;', '')
            for children in item.parent.parent.next_siblings:
                # this will stop it from continuing to the next program/degree
                if "strong" not in str(children):
                    children=children.text
                    children = str(children)
                    
                    # remove annoying HTML 'amp;'
                    children = children.replace('amp;','')
                    program_details += children.strip() + "\n"
                else:
                    break
            # prevents duplicates
            break

    short_url = "[Click here](https://www.waketech.edu/programs-courses/credit/transfer-choices/by-degree)"

    if program_title is not None:
        # create the successful embed
        embed = discord.Embed(
            title="TRANSFER OPTIONS FOR: \n" + program_title,
            # url=url,
            description=program_details,
            color=WAKETECH_BLUE,
        )
        embed.add_field(name="Full List of Transfer Options by Degree:", value=short_url, inline=True)

        return embed
    else:
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


def embed_builder_uni(university, transfer_link=None):
    url = 'https://www.waketech.edu/programs-courses/credit/transfer-choices/by-degree'
    page = requests.get(url)
    institution_table = SoupStrainer(class_="wt-table")
    soup = BeautifulSoup(page.content, "lxml", parse_only=institution_table)
    print(soup)
    
    universities = {}

    for row in soup.find_all("div", {"class": "wt-row"}):
      cells = row.select('.wt-cell')
      if len(cells) == 2:
        uni = cells[0].text
        program = cells[1].text
        if uni not in universities:
          universities[uni] = []
        universities[uni].append(program)
        
    
    print(universities)
    if university in universities:

        # create the embed
        embed = discord.Embed(
            title="TRANSFER OPTIONS FOR: \n" + university,
            # url=url,
            description="\n".join(universities[university]),
            color=WAKETECH_BLUE,
        )
        
        '''
        if transfer_link is not None:
            embed.add_field(name="Transfer Link", value=reqs, inline=True)
        if aas_link is not None:
            embed.add_field(name="AAS Transfer Link", value=reqs, inline=True)
        if degree_plan is not None:
            embed.add_field(name="Transfer Degree Plans", value=reqs, inline=True)
        if advisor_link is not None:
            embed.add_field(name="Talk with a University Advisor", value=advisor_link, inline=True)
        '''

        return embed
    else:
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
