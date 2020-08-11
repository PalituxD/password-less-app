import boto3
import os
from functions.otp.base import EventBase, ResultBase, Response


def handler(e, c):
    event = Event(e, c)
    event.handle()
    return event._response


class Result(ResultBase):
    SIGN_IN_LOGON_SUCCEEDED = (200, "LOGON_SUCCEEDED", "Logon succeeded")
    SIGN_IN_WRONG_CODE = (401, "WRONG_CODE", "Wrong code")
    SIGN_IN_NOT_AUTHORIZED = (403, "NOT_AUTHORIZED", "Not Authorized")
    SIGN_IN_EXPIRED_CODE = (410, "EXPIRED_CODE", "Code has expired")


class Event(EventBase):
    def __init__(self, event, context):
        EventBase.__init__(self, event, context)
        self.__cognito_idp_client = boto3.client('cognito-idp')
        self.__client_id = os.environ['COGNITO_POOL_CLIENT_ID']
        self._response = {}

    def handle(self):
        result, data = self.__sign_in()
        self._response = Response(result, data).to_json()

    def __sign_in(self):
        try:
            data = self.__cognito_idp_client.respond_to_auth_challenge(
                ClientId=self.__client_id,
                ChallengeName='CUSTOM_CHALLENGE',
                ChallengeResponses={
                    'USERNAME': self._body['username'],
                    "ANSWER": self._body['answer']
                },
                Session=self._body['session']
            )
            print(data)
            return Result.SIGN_IN_LOGON_SUCCEEDED, data
        except self.__cognito_idp_client.exceptions.NotAuthorizedException as e:
            print(e)
            return Result.SIGN_IN_NOT_AUTHORIZED, {}
        except self.__cognito_idp_client.exceptions.CodeMismatchException as e:
            print(e)
            return Result.SIGN_IN_WRONG_CODE, {}
        except self.__cognito_idp_client.exceptions.ExpiredCodeException as e:
            print(e)
            return Result.SIGN_IN_EXPIRED_CODE, {}
        except Exception as e:
            print(str(e))
            return Result.UNKNOWN, {}
