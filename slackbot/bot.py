import logging
import os
import json
from slack import WebClient
from .managers.event import SlackEventManager
from .managers.plugins import PluginManager
from .managers.udp import UdpManager
from .managers.users import UserManager
from .managers.mqtt import MqttManager
from .web import create_app


class SlackBot():
    def __init__(self, config_path=None):
        self.package = __loader__.name
        self.version = 'v0.1.0'
        logging.basicConfig(level=logging.DEBUG)
        self.log = logging.getLogger(__name__)
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.plugins_path = os.path.join(self.base_path, 'plugins')
        self.state_file_base = os.path.join(self.base_path, 'data')

        if config_path:
            self.state_file_base = os.path.join(config_path, 'data')

        if not os.path.exists(self.state_file_base):
            os.makedirs(self.state_file_base)

        self.state = {
            'log_level': 'DEBUG',

            'udp_pass': 'mekker',
            'udp_port': 47774,
            'udp_ip': '0.0.0.0',

            'mqtt_host': '127.0.0.1',
            'mqtt_port': 1883,

            'bot_base': self.base_path,
            'bot_token': '',
            'bot_user': '',
            'bot_prefix': '!',
            'bot_plugins': ['plugins', 'echo']
        }

        self.load_state()
        self.save_state()

        self.slack = WebClient(token=self.state['bot_token'])

        self.plugins = PluginManager(self)
        self.plugins.load_plugin(self.state['bot_plugins'])

        self.events = SlackEventManager(self)
        self.users = UserManager(self)

        self.udp = UdpManager(self, self.udp_event)
        self.mqtt = MqttManager(self, self.mqtt_event)

        self.web = create_app(self)
        self.web.run(port=3000, host='0.0.0.0')

    def load_state(self):
        self.log.info("Loading state file")
        state_file = os.path.join(self.state_file_base, 'state.json')
        if os.path.isfile(state_file):
            with open(state_file) as f:
                self.state = {**self.state, **json.load(f)}

    def save_state(self):
        self.log.info("Saving state file")
        state_file = os.path.join(self.state_file_base, 'state.json')
        with open(state_file, 'w') as f:
            json.dump(self.state, f)

    def mqtt_event(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload

        try:
            payload = json.loads(payload)
        except (json.JSONDecodeError, TypeError):
            pass

        return self.plugins.handle_mqtt(topic, payload)

    def udp_event(self, msg):
        args = msg.split(' ', 2)
        if len(args) < 3:
            return

        if args[0] != self.state['udp_pass']:
            return
        channel = args[1]
        text = args[2]

        self.slack.chat_postMessage(channel=channel, text=text)
