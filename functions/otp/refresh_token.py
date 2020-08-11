import boto3
import os
from functions.otp.base import EventBase, ResultBase, Response


def handler(e, c):
    event = Event(e, c)
    event.handle()
    return event._response


class Result(ResultBase):
    REFRESH_TOKEN_LOGON_SUCCEEDED = (200, "LOGON_SUCCEEDED", "Logon succeeded")
    REFRESH_TOKEN_WRONG_CODE = (401, "WRONG_CODE", "Wrong code")
    REFRESH_TOKEN_NOT_AUTHORIZED = (403, "NOT_AUTHORIZED", "Not Authorized")
    REFRESH_TOKEN_EXPIRED_CODE = (410, "EXPIRED_CODE", "Code has expired")


class Event(EventBase):
    def __init__(self, event, context):
        EventBase.__init__(self, event, context)
        self.__cognito_idp_client = boto3.client('cognito-idp')
        self.__client_id = os.environ['COGNITO_POOL_CLIENT_ID']
        self.__REFRESH_TOKEN_ = self._body['REFRESH_TOKEN_']
        self.__device_key = self._body['device_key']
        self._response = {}

    def handle(self):
        result, data = self.__initiate_auth()
        self._response = Response(result, data).to_json()

    def __initiate_auth(self):
        try:
            data = self.__cognito_idp_client.initiate_auth(
                ClientId=self.__client_id,
                AuthFlow='REFRESH_TOKEN__AUTH',
                AuthParameters={
                    'REFRESH_TOKEN_': self.__REFRESH_TOKEN_,
                    'DEVICE_KEY': self.__device_key
                }
            )
            return Result.REFRESH_TOKEN_LOGON_SUCCEEDED, data
        except self.__cognito_idp_client.exceptions.NotAuthorizedException as e:
            print(e)
            return Result.REFRESH_TOKEN_NOT_AUTHORIZED, {}
        except self.__cognito_idp_client.exceptions.PasswordResetRequiredException as e:
            print(e)
            return Result.REFRESH_TOKEN_NOT_AUTHORIZED, {}
        except self.__cognito_idp_client.exceptions.UserNotConfirmedException as e:
            print(e)
            return Result.REFRESH_TOKEN_NOT_AUTHORIZED, {}
        except Exception as e:
            print(str(e))
            return Result.UNKNOWN, {}
