# Discord-Posture-Bot
A bot that will record your favourite quotes and remind you to sit up straight.

## Dependencies
Last tested on:

discord-1.7.3 library documentation here: https://discordpy.readthedocs.io/en/stable/intro.html#installing

PyNaCl-1.4.0 (voice module)

ffmpeg library install and documentation here guide here: https://www.ffmpeg.org/


To install the necessary dependencies:

For Python:

```
pip install discord
pip install discord.py[voice]
```

For the ffmpeg:

There is a useful video here on getting started for windows and rasberry pi.

https://www.youtube.com/watch?v=M_6_GbDc39Q

## Running the Bot.

First set up an application from here: https://discord.com/developers/applications

then make a Token.txt file in the Files folder and put the token in it.

To run the bot from your computer run the main.py python script.

Then invite the bot to your server using the OAuth2 Link Generator section of the application.

The bot needs the following permissions to function:

1. **Text Permissions**
  - Send Messages
  - Read Message History
2. **Voice Permissions**
  - Connect
  - Speak
  - Use Voice Activty

