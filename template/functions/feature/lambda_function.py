import os

from common.base import EventBase, ResultBase, Response


def handler(e, c):
    event = Event(e, c)
    return event.get()


class Result(ResultBase):
    SUCCEEDED = (200, "SUCCEEDED", ":)")


class Event(EventBase):
    def __init__(self, event, context):
        EventBase.__init__(self, event, context)
        self.__id = self._event['pathParameters']['id']
        self.__current_stage = os.getenv("CURRENT_STAGE", "local")

    def get(self):
        body = {'id': self.__id, 'current_stage': self.__current_stage}
        self._response = Response(Result.SUCCEEDED, body, False).to_json()
        return self.response()
