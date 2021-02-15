import logging
import os

import boto3

from common.base import EventBase, ResultBase, Response

LOGGER = logging.getLogger(__name__)


def handler(e, c):
    event = Event(e, c)
    event.handle()
    return event.response()


class Result(ResultBase):
    REFRESH_TOKEN_SUCCEEDED = (
        200, "REFRESH_TOKEN_SUCCEEDED", "Refresh Token succeeded")
    REFRESH_TOKEN_WRONG_CODE = (401, "WRONG_CODE", "Wrong code")
    REFRESH_TOKEN_NOT_AUTHORIZED = (403, "NOT_AUTHORIZED", "Not Authorized")
    REFRESH_TOKEN_EXPIRED_CODE = (410, "EXPIRED_CODE", "Code has expired")
    UNKNOWN = (500, "SERVER_ERROR", "Server Error")


class Event(EventBase):
    def __init__(self, event, context):
        EventBase.__init__(self, event, context)
        self.__cognito_idp_client = boto3.client('cognito-idp')
        self.__client_id = os.environ['COGNITO_POOL_CLIENT_ID']
        self.__refresh_token = self._body['refresh_token']
        self.__device_key = self._body['device_key']

    def handle(self):
        result, data = self.__initiate_auth()
        self._response = Response(result, data).to_json()

    def __initiate_auth(self):
        try:
            data = self.__cognito_idp_client.initiate_auth(
                ClientId=self.__client_id,
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters={
                    'REFRESH_TOKEN': self.__refresh_token,
                    'DEVICE_KEY': self.__device_key
                }
            )
            return Result.REFRESH_TOKEN_SUCCEEDED, data
        except self.__cognito_idp_client.exceptions.NotAuthorizedException as e:
            LOGGER.error(e)
            return Result.REFRESH_TOKEN_NOT_AUTHORIZED, {}
        except self.__cognito_idp_client.exceptions.PasswordResetRequiredException as e:
            LOGGER.error(e)
            return Result.REFRESH_TOKEN_NOT_AUTHORIZED, {}
        except self.__cognito_idp_client.exceptions.UserNotConfirmedException as e:
            LOGGER.error(e)
            return Result.REFRESH_TOKEN_NOT_AUTHORIZED, {}
        except Exception as e:
            LOGGER.error(str(e))
            return Result.UNKNOWN, {}
