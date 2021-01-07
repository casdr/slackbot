from slackbot import SlackBot
import sys

state_path = None

if len(sys.argv) > 1:
    state_path = sys.argv[1]

bot = SlackBot(state_path)
