import json
import threading

class SlackEventManager():
    def __init__(self, bot):
        self.bot = bot
    
    def event(self, request):
        if request.data:
            request.data = json.loads(request.data)
        
        handlers = {
            'url_verification': self.url_verification,
            'event_callback': self.event_callback
        }

        if request.data['type'] in handlers:
            return handlers[request.data['type']](request)
        else:
            self.bot.log.error("no handler for '%s' request" % request.data['type'])
            return "meh"

    def url_verification(self, request):
        self.bot.log.info("received url_verification, replying with challenge")
        return request.data['challenge']

    def event_callback(self, request):
        self.bot.log.info("received '%s' event" % request.data['event']['type'])
        data = request.data['event']
        if data['type'] == 'message' and 'user' in data and data['user'] != self.bot.state['bot_user']:
            if data['text'][0:len(self.bot.state['bot_prefix'])] == self.bot.state['bot_prefix']:
                message = SlackMessage(self.bot, data)
                thr = threading.Thread(target=self.bot.plugins.handle_command, args=(message,))
                thr.start()
        return data

class SlackMessage():
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.text = data['text']
        self.args = data['text'][len(self.bot.state['bot_prefix']):len(data['text'])].split()
        self.command = self.args[0]
        self.rest = ' '.join(self.args[1:len(self.args)])
        self.user_id = data['user']
        self.user = self.bot.users.get_user(self.user_id)
        self.team = data['team']
        self.blocks = []

        if 'blocks' in data:
            self.blocks = data['blocks']
        
        self.channel = data['channel']

        self.bot.log.debug(self.__dict__)
    
    def dotted(self, items):
        return ' .. '.join(items)

    def reply(self, *args, **kwargs):
        if 'items'in kwargs.keys():
            items = kwargs.pop('items')
            kwargs['text'] = self.dotted(items)
        self.bot.slack.chat_postMessage(channel=self.channel, *args, **kwargs)