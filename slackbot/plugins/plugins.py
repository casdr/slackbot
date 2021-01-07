
def config(bot):
    return {
        'commands': ['plugins'],
        'events': [],
        'help': 'control plugins'
    }

def run(bot, event):
    if event.args[1] == 'load':
        if bot.plugins.load_plugin(event.args[2]) == False:
            return event.reply(text="couldn't load plugin '%s'" % event.args[2])
        event.reply(text="reloaded plugin '%s'" % event.args[2])
    
    if event.args[1] == 'unload':
        if bot.plugins.unload_plugin(event.args[2]) == False:
            return event.reply(text="couldn't unload plugin '%s'" % event.args[2])
        event.reply(text="unloaded plugin '%s'" % event.args[2])
    
    if event.args[1] == 'list':
        return event.reply(text="enabled plugins: " + " .. ".join(bot.plugins.plugins.keys()))
