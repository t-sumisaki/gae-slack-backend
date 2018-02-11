# coding: UTF-8
import os
import sys

rootdir = os.path.dirname(__file__)

sys.path.append(rootdir)
sys.path.append(os.path.join(rootdir, 'behaviors'))
import logging
from flask import Flask, request, jsonify, abort

import settings

from bot import Bot
from command_manager import CommandManager
from command import Command
from event import Event
from slackclient import SlackClient

from bot_control_behavior import BotControlBehavior


app = Flask(__name__)

verification_token = settings.VERIFICATION_TOKEN
access_token = settings.ACCESS_TOKEN
slack_client = SlackClient(access_token)
bot = Bot(slack_client)
command_manager = CommandManager(slack_client)

# 将来的にはyamlからプラグイン形式でAssign出来るようにする?
bot.assign_behavior('botctl', BotControlBehavior())

command_manager.assign_behavior('/botctl', BotControlBehavior())


@app.route('/')
def root():
    text = 'Hello from Google App Engine!'
    slack_client.api_call(
        'chat.postMessage', channel='#general', text=text
    )
    return text

@app.route('/healthcheck')
def healthcheck():
    return 'It works.'

@app.route('/slack/commands', methods=['POST'])
def slack_command():
    """ Slack Slash Command Hook 受信用

        :document:  
    """
    logging.debug('Request payload: %s', request.form)
    event = request.form

    if 'token' not in event:
        logging.error('There is not verification token in JSON, discarding event')
        abort(401)
    elif event['token'] != verification_token:
        logging.error('Wrong verification token in JSON, discarding event')
        abort(403)
    else:
        # イベント開始
        result = command_manager.execute_command(Command(event.to_dict()))

        return jsonify(result)
    



@app.route('/slack/event', methods=['POST'])
def slack_event():
    """ Slack Events API 受信用

        :document:
        https://api.slack.com/events-api
    """
    logging.debug('Request payload: %s', request.data)
    event = request.get_json()

    if 'token' not in event:
        logging.error('There is no verification token in JSON, discarding event')
        abort(401)
    elif event['token'] != verification_token:
        logging.error('Wrong verification token in JSON, discarding event')
        abort(403)
    elif 'challenge' in event:
        return jsonify({'challenge': event['challenge']})
    else:
        # イベント開始

        # slackにはOKの応答を返しておく
        return jsonify({})


@app.errorhandler(500)
def server_error(e):
    """ Internal Server Error エラーハンドラ """
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == '__main__':
    app.run()