# WTCC-bot

The WTCC bot is a Discord bot which pulls information from Wake Tech's course descriptions and RateMyProfessors.com.

## Commands

The bot currently takes two slash commands, one for course information and another for ratemyprofessors.com.

#### Examples

`/professor Harry Truman` will return results for the professor "Harry Truman" on RateMyProfessors.com 

`/course NET-125` will return results for the class known as "NET-125 - Introduction to Networks"

![Screenshot](screenshot.jpg?raw=true "Screenshot")

## Adding the Bot

The WTCC Bot is currently in Beta but stable enough for use. To deploy the bot for your Discord server:

1. Clone the repo on the hosting server that will be running the bot
2. Install the requirements: `python3 -m pip install -r requirements`
3. Create a [bot token](https://www.writebots.com/discord-bot-token/) and add it along with your [guild ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-) to wtcc_bot.py
4. Run the bot: `python3 wtcc_bot.py`

Keep in mind this repo will continue to be updated as needed so you'll want to keep an eye on it and update your bot as well.

## Notes

The bot was written in Python3 (tested on Python 3.9) for macOS and Linux distros. YMMV on Windows and older versions of Python3.

The bot uses [PyCord](https://github.com/Pycord-Development/pycord) on the currently in alpha "Slash Commands" branch.

## ToDo

- Implement cooldown on commands (once Pycord implements it to slash commands)
- Look into adding other features

## Acknowledgements and License

This project is a loose fork of [Cornell ClassRoster Discord Bot](https://github.com/aw632/cornellclassrosterbot_pub), which serves as an inspiration, while adding on a web scraper "API" for [RateMyProfessor](ratemyprofessors.com/) which you can [find here](https://github.com/Nobelz/RateMyProfessorAPI/).

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html). See LICENSE for more details.