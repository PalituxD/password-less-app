import json
import logging
import os
from datetime import datetime, timezone

import boto3

from common.base import EventBase

LOGGER = logging.getLogger(__name__)


def handler(e, c):
    event = Event(e, c)
    event.handle()
    return event.event()


class Event(EventBase):
    def __init__(self, event, context):
        EventBase.__init__(self, event, context)
        self.__events_client = boto3.client("events")
        self.__cognito_idp_client = boto3.client('cognito-idp')
        self.__user_pool_id = event['userPoolId']
        self.__username = event['request']['userAttributes']['sub']
        self.__py_events_bus_name = os.getenv("PY_EVENTS_BUS_NAME", "default")

    def handle(self):
        self.__update_cognito_user()
        self.__save_user()

    def __update_cognito_user(self):
        self.__cognito_idp_client.admin_update_user_attributes(
            UserPoolId=self.__user_pool_id,
            Username=self.__username,
            UserAttributes=[
                {'Name': 'phone_number_verified', 'Value': 'true'}
            ]
        )

    def __save_user(self):
        self.__create_py_user()

    def __user_data(self):
        return {
            'username': self.__username
        }

    def __create_py_user(self):
        ret = self.__events_client.put_events(
            Entries=[{
                "Time": datetime.now(tz=timezone.utc),
                "Source": "py.auth",
                "DetailType": "py.api.user.creation",
                "Detail": json.dumps(self.__user_data()),
                "EventBusName": self.__py_events_bus_name,
            }])
        LOGGER.info(ret)
