#!/usr/bin/env python3

import discord
from bs4 import BeautifulSoup
import requests
import re

WAKETECH_BLUE = 0x005480

"""
We're going to be using BeautifulSoup (https://beautiful-soup-4.readthedocs.io) to render the page in HTML to easily pullout the items we need to created the embeded response.
"""

def title_body(soup):
    full_class_name = soup.find(class_="course_title").get_text()
    full_class_descr = soup.find(class_="default_body course_body").get_text().strip()

    return full_class_name, full_class_descr

def embed_builder(dep, url):
    page = requests.get(url)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')

    full_class_name, full_class_descr = title_body(soup)

    # get course credits
    details_dict = {}
    for data in soup.find_all("strong"):
        details_value = str(data.next_sibling)
        details_value = details_value.strip()
        details_key = str(data)
        details_key = re.sub('<*.?strong>','',details_key, flags=re.DOTALL)
        details_dict[details_key] = details_value

    reqs = (details_dict['Requisites:'])
    credit_num = (details_dict['Total Class Credits:'])
    selfserv_url = "[Click here](https://selfserve.waketech.edu/Student/Courses/Search?subjects=" + str(dep) + ")"
    
    # get program overview url
    prog_href = soup.find_all(href=re.compile("programs-courses/credit/"))
    for tag in prog_href:
        prog_rel = tag.get('href')
    program_url = "[Click here](https://waketech.edu" + str(prog_rel) + ")"

    # create the embed
    embed = discord.Embed(
        title=full_class_name,
        url=url,
        description=full_class_descr,
        color=WAKETECH_BLUE,
    )   
    embed.add_field(name="Prerequisites/Corequisites", value=reqs, inline=True)
    embed.add_field(name="Credits", value=credit_num, inline=True)
    embed.add_field(name="Self-Service", value=selfserv_url, inline=True)
    embed.add_field(name="Program Overview", value=program_url, inline=True)

    embed.set_footer(text="Questions, suggestions, problems? Send a message to netdragon#3288")

    return embed
