def config(bot):
    return {
        'commands': ['plugins'],
        'events': [],
        'help': 'control plugins'
    }

def run(bot, event):
    if len(event.args) < 2:
        return event.reply(text="usage: plugins <load|unload|list> [name]")

    if event.args[1] == 'load':
        if len(event.args) < 3:
            return event.reply(text="usage: plugins load <name>")
        loaded = bot.plugins.load_plugin(event.args[2])
        if not loaded:
            return event.reply(text=f"couldn't load plugin '{event.args[2]}'")
        event.reply(text=f"reloaded plugin '{event.args[2]}'")

    elif event.args[1] == 'unload':
        if len(event.args) < 3:
            return event.reply(text="usage: plugins unload <name>")
        unloaded = bot.plugins.unload_plugin(event.args[2])
        if not unloaded:
            return event.reply(text=f"couldn't unload plugin '{event.args[2]}'")
        event.reply(text=f"unloaded plugin '{event.args[2]}'")

    elif event.args[1] == 'list':
        return event.reply(text="enabled plugins: " + " .. ".join(bot.plugins.plugins.keys()))
