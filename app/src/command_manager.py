# coding: UTF-8
import logging

class CommandManager(object):

    __behaviors = {}

    def __init__(self, slack_client):
        self.slack_client = slack_client

    def assign_behavior(self, cmd, behavior):

        if cmd not in self.__behaviors:
            self.__behaviors[cmd] = behavior
    
    def execute_command(self, command):
        """ コマンド実行
        """
        cmd = command.command
        if cmd in self.__behaviors:
            return self.__behaviors[cmd].execute(command, self.slack_client)
        else:
            text = 'Command {} is not defined.'.format(cmd)
            logging.info(text)
            return {
                'text': text
            }
