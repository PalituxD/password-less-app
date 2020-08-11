import os
import enum
import json
from distutils.util import strtobool


class EventBase:
    def __init__(self, event, context):
        self._event = event
        self._body = self.__get_body()
        self._query = self.__get_query()
        self._context = context
        self._log()

    def _log(self):
        if _is_log_enabled():
            print('{\'event\':' + str(self._event))

    def __get_body(self):
        body = {}
        raw_body = self._event.get('body')
        if raw_body:
            body = json.loads(raw_body)
        return body

    def __get_query(self):
        query = {}
        raw_query = self._event.get('queryStringParameters')
        if raw_query:
            query = raw_query
        return query


def _is_log_enabled():
    log_enabled = os.environ["LOG_ENABLED"]
    return log_enabled is not None and bool(strtobool(log_enabled)) == True


class Response:
    def __init__(self, result, data={}):
        self.__status_code = result.status_code
        self.__data = data
        self.__data['message'] = result.message
        self.__data['code'] = result.code

    def to_json(self):
        return {
            'statusCode': self.__status_code,
            'body': json.dumps(self.__data)
        }


class ResultBase(enum.Enum):

    def __init__(self, status_code, code, message):
        self.__status_code = status_code
        self.__code = code
        self.__message = message

    @ property
    def status_code(self):
        return self.__status_code

    @ property
    def code(self):
        return self.__code

    @ property
    def message(self):
        return self.__message
