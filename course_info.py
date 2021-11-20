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

def title_body(soup):
    full_class_name = soup.find(class_="course_title").get_text()
    full_class_descr = soup.find(class_="default_body course_body").get_text().strip()

    return full_class_name, full_class_descr

def embed_builder(course, url):
    page = requests.get(url)
    content = page.content
    soup = BeautifulSoup(content, 'lxml')

    full_class_name, full_class_descr = title_body(soup)

    # get course details
    details_dict = {}
    for data in soup.find_all("strong"):
        details_value = str(data.next_sibling)
        details_value = details_value.strip()
        details_key = str(data)
        details_key = re.sub('<*.?strong>','',details_key, flags=re.DOTALL)
        details_dict[details_key] = details_value

    # Requisites can get pretty long, let's make sure it wont break things
    reqs = (details_dict['Requisites:'])
    groups = reqs.split(';')
    if len(groups) > 4:
        reqs = "List too long, [go to the page](" + str(url) +")."
    else:
        reqs_list = ''
        for x in groups:
            reqs_list += x + "\n"
        reqs = reqs_list

    credit_num = (details_dict['Total Class Credits:'])
    selfserv_url = "[Click here](https://selfserve.waketech.edu/Student/Courses/Search?keyword=" + course + ")"

    # get program overview url, if it exists
    prog_href = soup.find_all(href=re.compile("programs-courses/credit/"))
    if prog_href is not None:
        program_url = None
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
    if program_url is not None:
        embed.add_field(name="Program Overview", value=program_url, inline=True)


    return embed
