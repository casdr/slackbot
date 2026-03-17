import json
import threading
from ..models.message import SlackMessage


class SlackEventManager():
    def __init__(self, bot):
        self.bot = bot

    def event(self, request):
        data = request.get_json(force=True)

        handlers = {
            'url_verification': self.url_verification,
            'event_callback': self.event_callback
        }

        if data['type'] in handlers:
            return handlers[data['type']](data)
        else:
            self.bot.log.error(f"no handler for '{data['type']}' request")
            return "meh"

    def url_verification(self, data):
        self.bot.log.info("received url_verification, replying with challenge")
        return data['challenge']

    def event_callback(self, data):
        self.bot.log.info(f"received '{data['event']['type']}' event")
        data = data['event']
        if data['type'] == 'message' and 'user' in data and data['user'] != self.bot.state['bot_user']:
            if data['text'].startswith(self.bot.state['bot_prefix']):
                message = SlackMessage(self.bot, data)
                thr = threading.Thread(target=self.bot.plugins.handle_command, args=(message,))
                thr.start()
        return data
