# coding: UTF-8
import re
import logging

class User(object):

    def __init__(self, json_user):
        self.__json_user = json_user
    
    def get_user_str(self):
        return ''
    
    @property
    def id(self):
        return self.__json_user['id']
    
    @property
    def name(self):
        return self.__json_user['name']

    @property
    def is_bot(self):
        return self.__json_user['is_bot']


class BotControlBehavior(object):

    def execute(self, event, slack_client, **params):

        subcommand = re.search(r'^\s*(\S+)', event.text)

        result = {}

        if subcommand is None:
            text = 'Can''t find subcommand.'
            logging.warn(text)
            result['text'] = text
        elif subcommand.group(1) == 'list':
            logging.debug('List command.')
            # Botリスト取得
            response = slack_client.api_call('users.list')

            if not response['ok']:
                text = 'Unable to get user list. {}'.format(response['error'])
                logging.error(text)
                result['text'] = text
            else:
                logging.debug('Response payload: %s', response)
                # 成功時の処理
                bot_users = []

                for user in [User(x) for x in response['members']]:
                    logging.debug('Find user: %s / is_bot=%s', (user.name, user.is_bot))
                    if user.is_bot:
                        bot_users.append({
                            'title': user.name,
                            'value': 'id: <@{}>'.format(user.id)
                        })
                
                result['text'] = 'Search bot users.'
                result['attachments'] = [{
                    'text': 'Found {} bot users.'.format(len(bot_users)),
                    'fields': bot_users
                }]
        else:
            text = 'Subcommand [{}] is not defined.'.format(subcommand.group(1))
            logging.warn(text)
            result['text'] = text
        
        return result
