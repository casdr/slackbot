class SlackMessage():
    def __init__(self, bot, data):
        self.bot = bot
        self.data = data
        self.text = data['text']
        self.args = data['text'][len(self.bot.state['bot_prefix']):].split()
        self.command = self.args[0]
        self.rest = ' '.join(self.args[1:])
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
        if 'items' in kwargs:
            items = kwargs.pop('items')
            kwargs['text'] = self.dotted(items)
        self.bot.slack.chat_postMessage(channel=self.channel, *args, **kwargs)
