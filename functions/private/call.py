from functions.otp.base import EventBase, ResultBase, Response


def handler(e, c):
    event = Event(e, c)
    event.handle()
    return event._response


class Result(ResultBase):
    SUCCESSED = (200, "SUCCESSED", "PasswordLess works!")


class Event(EventBase):
    def __init__(self, event, context):
        EventBase.__init__(self, event, context)

    def handle(self):
        data = self._query
        result = Result.SUCCESSED
        self._response = Response(result, data).to_json()
