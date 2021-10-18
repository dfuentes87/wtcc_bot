#!/usr/bin/env python3

import discord
import ratemyprofessor

WAKETECH_BLUE = 0x005480

def embed_builder(prof_name):
    professor = ratemyprofessor.get_professor_by_school_and_name(
        ratemyprofessor.get_school_by_name("Wake Technical Community College"), prof_name)
    if professor is not None:
        prof_name = professor.name
        prof_dept = professor.department
        prof_rating = str(professor.rating) + " / 5.0"
        prof_diff = str(professor.difficulty) + " / 5.0"
        prof_total = professor.num_ratings
        if professor.would_take_again is not None:
            prof_again = str(round(professor.would_take_again, 1)) + "%"
        else:
            prof_again = "0% or no rating"

        embed = discord.Embed(
            title=prof_name,
            color=WAKETECH_BLUE
        )
        embed.add_field(name="Department", value=prof_dept, inline=True)
        embed.add_field(name="Rating", value=prof_rating, inline=True)
        embed.add_field(name="Difficuty", value=prof_diff, inline=True)
        embed.add_field(name="Total Ratings", value=prof_total, inline=True)
        embed.add_field(name="Would Take Again:", value=prof_again, inline=True)
    else:
        embed = discord.Embed(
            title="404: Professor not found",
            description="Double check your spelling and make sure you are typing only the first and last name. Otherwise, they do not have an entry in ratemyprofessor.com.",
            color=WAKETECH_BLUE,
        )

    return embed
