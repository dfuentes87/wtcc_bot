#!/usr/bin/env python3

import discord
from bs4 import BeautifulSoup
import requests
import re

WAKETECH_BLUE = 0x005480

# https://waketech.edu/course/net-126

def get_descriptions(soup):
    """Returns the Full Class Name and Full Class Description from a site.
    Args:
        soup (BeautifulSoup Object): represents the webpage in bs4
    """
    full_class_name = soup.find(class_="title-coursedescr").get_text()

    full_class_descr = soup.find(class_="catalog-descr").get_text().strip()

    return full_class_name, full_class_descr

def course_embed_builder(dep, num, url):
    semester = re.search("([SF][A-Z]*[0-9]+)", url).group(1)
    em = requests.get(url)
    content = em.content

    soup = BeautifulSoup(content, "lxml")

    full_class_name, full_class_descr = get_descriptions(soup)

    credit_num = safe_get_data(
        soup, "credit-val", "For some reason, the number of credits is not listed."
    )

    prereq = safe_get_data(
        soup,
        "catalog-prereq",
        "N/A: This class does not have any prerequisites, or none are listed.",
    ).replace("Prerequisites/Corequisites", "")

    # create the embed
    embed = discord.Embed(
        title=dep.upper() + " " + num + ": " + full_class_name,
        url=url,
        description=full_class_descr,
        color=WAKETECH_BLUE,
    )
    embed.add_field(name="Credits", value=credit_num, inline=True)
    embed.add_field(name="Prerequisites/Corequisites", value=prereq, inline=True)
    embed.add_field(name="Self-Service", value="[Click here](course_url)", inline=True)

    embed.set_footer(text="Questions, suggestions, problems? Send a message to netdragon#3288")

    return embed
