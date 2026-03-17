import json
from flask import Flask, request


def create_app(bot):
    app = Flask(__name__)

    @app.route('/slack/event', methods=['GET', 'POST'])
    def slack_event():
        return bot.events.event(request)

    return app
