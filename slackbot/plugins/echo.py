def config(bot):
    return {
        'commands': ['echo'],
        'events': [],
        'mqtt': ['slackbot/echo'],
        'help': 'tools for echoing'
    }

def run(bot, event):
    event.reply(text="%s" % event.rest)

def mqtt(bot, topic, payload):
    bot.slack.chat_postMessage(payload)