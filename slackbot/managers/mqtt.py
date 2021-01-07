import paho.mqtt.client as mqtt
import threading
import json

class MqttManager:
    def __init__(self, bot, event_handler):
        self.bot = bot
        self.mqtt_open = False
        self.event_handler = event_handler

        self.client = mqtt.Client()
        self.client.on_message = self.event_handler

        self.client.connect(self.bot.state['mqtt_host'], self.bot.state['mqtt_port'])

        self.open()
    
    def open(self):
        if self.mqtt_open:
            self.close()
        self.bot.log.info('opening mqtt connection')
        self.client.loop_start()
        self.client.subscribe('#')
        self.mqtt_open = True
        self.bot.log.info('opened mqtt connection')
    
    def close(self):
        self.bot.log.info('closing mqtt connection')
        self.client.loop_stop()
        self.mqtt_open = False
        self.bot.log.info('closed mqtt connection')
        
    def publish(self, topic, payload):
        try:
            payload = json.dumps(payload)
        except:
            pass
        return self.client.publish(topic, payload)