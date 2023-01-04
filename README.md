# WTCC-bot

The WTCC bot is a Discord bot which pulls information from Wake Tech's course descriptions, NC university transfer information, and RateMyProfessors.com.

## Commands

`/course` will return information about the Wake Tech course specified.

`/professor` will return the ratings from ratemyprofessors.com for the professor specified. The bot only searches for professors at Wake Tech Community College in North Carolina.

`/transfer` is used to see transfer information based on a Wake Tech program/degree OR a North Carolina university, depending on which suboption you choose.

![Screenshot](screenshot1.jpeg?raw=true "Screenshot")

![Screenshot](screenshot2.jpeg?raw=true "Screenshot")

## Adding the Bot

The WTCC Bot is currently in Beta but stable enough for use. To deploy the bot for your Discord server:

1. Clone the repo on the hosting server that will be running the bot
2. Install the requirements: `python3 -m pip install -r requirements.txt`
3. Create a [bot token](https://www.writebots.com/discord-bot-token/) and add it along with your [guild ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-) to an .env file placed in the same directory
4. Run the bot: `python3 wtcc_bot.py`

## Notes

The bot was written in Python3 (tested on Python 3.9) for macOS and Linux distros. YMMV on Windows and older versions of Python3.

## Acknowledgements and License

This project is a loose fork of [Cornell ClassRoster Discord Bot](https://github.com/aw632/cornellclassrosterbot_pub), which serves as an inspiration, while adding on a web scraper "API" for [RateMyProfessor](https://www.ratemyprofessors.com/) which you can [find here](https://github.com/Nobelz/RateMyProfessorAPI/).

This project uses [Pycord](https://pycord.dev/).

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html). See LICENSE for more details.