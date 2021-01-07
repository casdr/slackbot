import importlib
import os
import sys

class PluginManager:
    def __init__(self, bot):
        self.bot = bot
        self.plugins = {}

    def load_plugin(self, names):
        if isinstance(names, str):
            names = [names]
        for name in names:
            self.bot.log.info("loading plugin '%s'" % name)
            if name[-3:] == '.py':
                name = name[:-3]
            plugin_path = os.path.join(self.bot.plugins_path, '%s.py' % name)
            if not os.path.isfile(plugin_path):
                self.bot.log.warning("plugin '%s' not found at '%s'" % (name, plugin_path))
                continue
            
            plugin_object = ''
            try:
                spec = importlib.util.spec_from_file_location('%s.plugins.%s' % (self.bot.package, name), plugin_path)
                plugin_object = importlib.util.module_from_spec(spec)
                sys.modules[name] = plugin_object
                spec.loader.exec_module(plugin_object)
            except Exception as e:
                self.bot.log.warning("loading plugin '%s' failed" % name)
                self.bot.log.warning(e)
                continue
            
            if not hasattr(plugin_object, 'config'):
                self.bot.log.warning("no config for plugin '%s'" % name)
                continue
            
            plugin_config = plugin_object.config(self.bot)
            for test in ['events', 'commands', 'help']:
                if test not in plugin_config:
                    self.bot.log.warning("missing config key '%s' for plugin '%s'" % (test, name))
                    continue
            
            plugin_config['object'] = plugin_object
            self.plugins[name] = plugin_config

            if name not in self.bot.state['bot_plugins']:
                self.bot.state['bot_plugins'].append(name)

            self.bot.log.info("enabled plugin '%s'" % name)
        self.bot.save_state()
 
    def unload_plugin(self, names):
        if isinstance(names, str):
            names = [names]
        for name in names:
            self.bot.log.info("unloading plugin '%s'" % name)
            if name[-3:] == '.py':
                name = name[:-3]
            
            if name not in self.plugins:
                self.bot.log.warning("plugin '%s' is not loaded" % name)
                continue
        
            del self.plugins[name]

            if name in self.bot.state['bot_plugins']:
                self.bot.state['bot_plugins'].remove(name)

            self.bot.log.info("unloaded plugin '%s'" % name)
        self.bot.save_state()
    
    def handle_command(self, event):
        for name, plugin in self.plugins.items():
            if event.command not in plugin['commands']:
                continue
            self.bot.log.info("using plugin '%s' to handle '%s' command" % (name, event.command))
            try:
                plugin['object'].run(self.bot, event)
            except Exception as e:
                self.bot.log.error("error from plugin '%s'" % name)
                self.bot.log.error(e)
                return False
        
    def handle_mqtt(self, topic, payload):
        for name, plugin in self.plugins.items():
            if 'mqtt' not in plugin:
                continue
            for ptopic in plugin['mqtt']:
                if not topic.startswith(ptopic):
                    continue
            self.bot.log.info("using plugin '%s' to handle '%s' topic" % (name, topic))
            try:
                plugin['object'].mqtt(self.bot, topic, payload)
            except Exception as e:
                self.bot.log.error("error from plugin '%s'" % name)
                self.bot.log.error(e)
                return False