# coding: UTF-8
class Event(object):
    """ Slack Event API イベントメッセージ構造体

        :Document:
        https://api.slack.com/events-api
    """

    def __init__(self, json_event):
        self.__json_event = json_event


    def is_private_message(self):
        """ メッセージがDM（プライベートメッセージ）であるか？ """
        return self.__json_event['event']['channel'].startswith('D')
    
    @property
    def user_id(self):
        """ メッセージ送信元ユーザID """
        return self.__json_event['event'].get('user', None)
    
    @property
    def text(self):
        """ Slackのメッセージに入力したテキスト """
        return self.__json_event['event']['text']

    @property
    def type(self):
        """ メッセージタイプ """
        return self.__json_event['event']['type']

    @property
    def channel(self):
        """ 送信先チャンネル """
        return self.__json_event['event']['channel']
    
