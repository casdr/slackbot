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
        loaded = []
        for name in names:
            self.bot.log.info(f"loading plugin '{name}'")
            if name.endswith('.py'):
                name = name[:-3]
            plugin_path = os.path.join(self.bot.plugins_path, f'{name}.py')
            if not os.path.isfile(plugin_path):
                self.bot.log.warning(f"plugin '{name}' not found at '{plugin_path}'")
                continue

            plugin_object = ''
            try:
                spec = importlib.util.spec_from_file_location(f'{self.bot.package}.plugins.{name}', plugin_path)
                plugin_object = importlib.util.module_from_spec(spec)
                sys.modules[name] = plugin_object
                spec.loader.exec_module(plugin_object)
            except Exception as e:
                self.bot.log.warning(f"loading plugin '{name}' failed")
                self.bot.log.warning(e)
                continue

            if not hasattr(plugin_object, 'config'):
                self.bot.log.warning(f"no config for plugin '{name}'")
                continue

            plugin_config = plugin_object.config(self.bot)
            missing_keys = [k for k in ['events', 'commands', 'help'] if k not in plugin_config]
            if missing_keys:
                self.bot.log.warning(f"missing config keys {missing_keys} for plugin '{name}'")
                continue

            plugin_config['object'] = plugin_object
            self.plugins[name] = plugin_config

            if name not in self.bot.state['bot_plugins']:
                self.bot.state['bot_plugins'].append(name)

            loaded.append(name)
            self.bot.log.info(f"enabled plugin '{name}'")
        self.bot.save_state()
        return loaded

    def unload_plugin(self, names):
        if isinstance(names, str):
            names = [names]
        unloaded = []
        for name in names:
            self.bot.log.info(f"unloading plugin '{name}'")
            if name.endswith('.py'):
                name = name[:-3]

            if name not in self.plugins:
                self.bot.log.warning(f"plugin '{name}' is not loaded")
                continue

            del self.plugins[name]

            if name in self.bot.state['bot_plugins']:
                self.bot.state['bot_plugins'].remove(name)

            unloaded.append(name)
            self.bot.log.info(f"unloaded plugin '{name}'")
        self.bot.save_state()
        return unloaded
    
    def handle_command(self, event):
        for name, plugin in self.plugins.items():
            if event.command not in plugin['commands']:
                continue
            self.bot.log.info(f"using plugin '{name}' to handle '{event.command}' command")
            try:
                plugin['object'].run(self.bot, event)
                return True
            except Exception as e:
                self.bot.log.error(f"error from plugin '{name}'", exc_info=e)
                return False
        return None

    def handle_mqtt(self, topic, payload):
        for name, plugin in self.plugins.items():
            if 'mqtt' not in plugin:
                continue
            for ptopic in plugin['mqtt']:
                if not topic.startswith(ptopic):
                    continue
                self.bot.log.info(f"using plugin '{name}' to handle '{topic}' topic")
                try:
                    plugin['object'].mqtt(self.bot, topic, payload)
                except Exception as e:
                    self.bot.log.error(f"error from plugin '{name}'", exc_info=e)
                    return False