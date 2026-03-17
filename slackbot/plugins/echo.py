def config(bot):
    return {
        'commands': ['echo'],
        'events': [],
        'mqtt': ['slackbot/echo'],
        'help': 'tools for echoing'
    }

def run(bot, event):
    event.reply(text=event.rest)

def mqtt(bot, topic, payload):
    if isinstance(payload, dict):
        bot.slack.chat_postMessage(**payload)
    else:
        bot.slack.chat_postMessage(channel='#general', text=str(payload))
