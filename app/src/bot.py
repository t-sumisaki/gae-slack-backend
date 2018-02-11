# coding: UTF-8
import logging


class Bot(object):
    """ SlackBotクラス """

    __behaviors = {}

    def __init__(self, slack_client, user_id=None):
        """ 初期化

            :parameters:  
            slack_client - SlackClient インスタンス  
            user_id - BotのユーザID
        """
        self.slack_client = slack_client
        self.user_id = user_id

    def assign_behavior(self, name='', behavior=None):
        """ Bot用コマンドクラスのアサイン

            :parameters:  
            name - コマンドの定義名
            behavior - Behaviorインスタンス
        
        """
        if name not in self.__behaviors:
            self.__behaviors[name] = behavior

    def get_user_id(self):
        response = self.slack_client.api_call('auth.test')
        if not response['ok']:
            logging.error('Unable to retrieve bot id due to %s',
                          response['error'])
            pass
        else:
            user_id = response['user_id']
            logging.info('Retrieved user_id: %s', user_id)
            return user_id

    def handle_event(self, event):
        """ イベントを受け入れる
        
            :parameters:  
            event - Slack Event API イベント構造体
        """
        if event.type == 'message':
            self.__handle_message_event(event)
        else:
            logging.debug('Ignoring unknown event type')

    def __handle_message_event(self, event):
        """ メッセージイベントの処理を行う

            :parameters:  
            event -　Slack Event API イベント構造体
        """
        if not self.user_id:
            self.user_id = self.get_user_id()

        # 送信元が自分だった場合は処理しない（セルフフィードバックループの防止）
        if event.user_id == self.user_id:
            logging.debug('Ignoring own message')
            return

        # BotCommand処理
        for name, command in self.__commands.items():
            logging.debug('Call command. %s', name)
            command.call(event, self.slack_client)
