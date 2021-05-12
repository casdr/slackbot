# slackbot

Slackbot is a bot for Slack ;) Inspired by gozerbot.

A few features:

- UDP to Slack messages
- MQTT pub and sub
- Permissions for users
- Modular using plugins

## Starting the bot

Start the bot once by running ./bot.py. Stop it and edit the state in slackbot/data/state.json.

Set the following keys to match your Slack instance: 

- `bot_token`: The token for the Slack app
- `bot_user`: Nickname for the bot
- `udp_pass`: Password for sending messages through the UDP gateway

Run the bot again, it should answer your commands :)
