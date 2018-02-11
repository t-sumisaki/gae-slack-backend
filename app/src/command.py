class Command(object):

    def __init__(self, form_command):
        self.__form_command = form_command
    
    @property
    def command(self):
        return self.__form_command['command']
    
    @property
    def text(self):
        return self.__form_command['text']
    
    @property
    def channel_id(self):
        return self.__form_command['channel_id']
    

    @property
    def user_id(self):
        return self.__form_command['user_id']
    
