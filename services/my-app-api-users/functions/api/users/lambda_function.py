import json
import logging
import os

from pynamodb.exceptions import PutError

from common.base import EventBase, ResultBase, Response
from functions.api.users.models import UserModel

LOGGER = logging.getLogger(__name__)


class Result(ResultBase):
    SUCCEEDED = (200, "FOUND", "User found")
    NOT_FOUND = (404, "NOT FOUND", "User not found")


class Event(EventBase):
    def __init__(self, event, context):
        EventBase.__init__(self, event, context)
        self.__table_users = os.getenv("PY_TABLE_USERS")

    def put(self):
        username = self._event['detail']['username']
        try:
            UserModel(username=username).save(UserModel.username.does_not_exist())
        except PutError:
            pass
        return self.response()

    def get(self):
        username = self.__get_requested_username()
        user = UserModel.find_by_hash_key(username)
        if user:
            response_data = user.get_json()
            self._response = Response(Result.SUCCEEDED, response_data, False).to_json()
        else:
            self._response = Response(Result.NOT_FOUND).to_json()
        return self.response()

    def post(self):
        new_data = json.loads(self._event['body'])
        username = self.__get_requested_username()
        user = UserModel.find_by_hash_key(username)
        if user:
            updated_user = user.update(new_data)
            if updated_user:
                user = updated_user
            self._response = Response(Result.SUCCEEDED, user.get_json(), False).to_json()
        else:
            self._response = Response(Result.NOT_FOUND).to_json()
        return self.response()

    def __get_requested_username(self):
        if self._event['pathParameters']:
            return self._event['pathParameters']['userId']
        else:
            return self._event['requestContext']['authorizer']['claims']['sub']


def handler_put(e, c):
    event = Event(e, c)
    return event.put()


def handler_post(e, c):
    event = Event(e, c)
    return event.post()


def handler_get(e, c):
    event = Event(e, c)
    return event.get()
