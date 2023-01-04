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
					children = children.strip()
					if children == "":
						continue
					uni_name=children.split("\n")[0]
					prog_name=children.split("\n")[1]
					program_details += "**"+uni_name+"**\n" +prog_name+ "\n\n"
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
	url = 'https://www.waketech.edu/programs-courses/credit/transfer-choices/search-college'
	page = requests.get(url)
	# get rid of everything but the universities
	uni_list = SoupStrainer(class_="paragraph--view-mode--default panel-heading faq")
	soup = BeautifulSoup(page.content, "lxml", parse_only=uni_list)
	
	university_name=None
	
	for uni in soup.find_all("div",class_="paragraph--view-mode--default panel-heading faq"):
		
		# '^' will make regex do a 'starts with' search
		university = "^" + university
		university_name = uni.find(string=re.compile(university, re.IGNORECASE))
		if university_name is None:
			continue
		
		degree_plan=None
		advisor_link=None
		aas_link=None
		transfer_link=None
		
		degrees_list = uni.find('ul', class_='wt-bullets')
		degrees = []
		for li in degrees_list.find_all('li'):
			degrees.append(li.text)
		degree_list="\n\n".join(degrees)
		
		buttons = uni.find_all("div", attrs={'class': re.compile('^wt-btn*')})
		for button in buttons:
			if button.a.text == "Transfer link":
				transfer_link = button.a['href']
			
			if button.a.text == "AAS transfer link":
				aas_link = button.a['href']
			
			if button.a.text == "Transfer degree plans":
				degree_plan = button.a['href']
			
			if button.a.text == "Talk with an advisor":
				advisor_link = button.a['href']
			
			if button.a.text == "Talk with UNCW advisor":
				advisor_link = button.a['href']
				
		if not university_name is None:
			break

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
		embed.add_field(name="Transfer Link", value=transfer_link, inline=True)
	if aas_link is not None:
		embed.add_field(name="AAS Transfer Link", value=aas_link, inline=True)
	if degree_plan is not None:
		embed.add_field(name="Transfer Degree Plans", value=degree_plan, inline=True)
	if advisor_link is not None:
		embed.add_field(name="Talk with a University Advisor", value=advisor_link, inline=True)

	return embed
