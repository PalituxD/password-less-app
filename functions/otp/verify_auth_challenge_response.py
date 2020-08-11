from functions.otp.base import EventBase


def handler(e, c):
    event = Event(e, c)
    event.handle()
    return event._event


class Event(EventBase):
    def __init__(self, event, context):
        EventBase.__init__(self, event, context)

    def handle(self):
        if self.__check_answer():
            self._event['response']['answerCorrect'] = True
        else:
            self._event['response']['answerCorrect'] = False

    def __check_answer(self):
        return self._event['request']['privateChallengeParameters']['secretLoginCode'] == self._event['request']['challengeAnswer']
