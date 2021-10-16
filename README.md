# WTCC-bot

The WTCC bot is a Discord bot which pulls information from Wake Tech's course descriptions and RateMyProfessors.com.

## Commands

The bot takes two slash commands, one for course information and another for ratemyprofessors.com.

#### Examples

`/professor Harry Truman` will return results for the professor "Harry Truman" on RateMyProfessors.com 

`/course NET-125` will return results for the class known as "NET-125 - Introduction to Networks"

![Screenshot](screenshot.jpg?raw=true "Screenshot")

## Adding the Bot

Bot is currently in Beta, no link to add it directly will be provided at this time. If you decide to use it in this stage, I won't be providing any support and you'll be using it at your own risk. Code is constantly being changed!

## ToDo

- Implement cooldown on commands (once Pycord implements it to slash commands)
- Look into adding other features

## Acknowledgements and License

This project is a loose fork of [Cornell ClassRoster Discord Bot](https://github.com/aw632/cornellclassrosterbot_pub), which serves as an inspiration for this project, while adding on a web scraper "API" for [RateMyProfessor](ratemyprofessors.com/) which you can [find here](https://github.com/Nobelz/RateMyProfessorAPI/).

The bot is written using [PyCord](https://github.com/Pycord-Development/pycord).

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html). See LICENSE for more details.