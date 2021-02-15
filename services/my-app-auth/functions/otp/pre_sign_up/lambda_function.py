from common.base import EventBase


def handler(e, c):
    event = Event(e, c)
    event.handle()
    return event.event()


class Event(EventBase):
    def __init__(self, event, context):
        EventBase.__init__(self, event, context)

    def handle(self):
        self._event['response']['autoConfirmUser'] = True
        self._event['response']['autoVerifyPhone'] = True
