from functions.otp.base import EventBase


def handler(e, c):
    event = Event(e, c)
    event.handle()
    return event._event


class Event(EventBase):
    def __init__(self, event, context):
        EventBase.__init__(self, event, context)

    def handle(self):
        if self.__user_not_found():
            self._event['response']['issueTokens'] = False
            self._event['response']['failAuthentication'] = True
            raise UserNotFound

        if self.__is_invalid_challenge():
            self._event['response']['issueTokens'] = False
            self._event['response']['failAuthentication'] = True
            raise InvalidChallenge

        elif self.__user_already_verified():
            self._event['response']['issueTokens'] = True
            self._event['response']['failAuthentication'] = False

        else:
            self._event['response']['issueTokens'] = False
            self._event['response']['failAuthentication'] = False
            self._event['response']['challengeName'] = 'CUSTOM_CHALLENGE'

    def __user_not_found(self):
        return self._event['request']['userNotFound']

    def __is_invalid_challenge(self):
        return len(self._event['request']['session']) >= 3 and self._event['request']['session'][-1]['challengeResult'] == False

    def __user_already_verified(self):
        return len(self._event['request']['session']) > 0 and self._event['request']['session'][-1]['challengeResult'] == True


class UserNotFound(Exception):
    """User does not exist"""


class InvalidChallenge(Exception):
    """Invalid Challenge"""
