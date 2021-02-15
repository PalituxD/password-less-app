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
    LOGON_SUCCEEDED = (200, "LOGON_SUCCEEDED", "Logon succeeded")
    WRONG_CODE = (401, "WRONG_CODE", "Wrong code")
    NOT_AUTHORIZED = (403, "NOT_AUTHORIZED", "Not Authorized")
    EXPIRED_CODE = (410, "EXPIRED_CODE", "Code has expired")
    UNKNOWN = (500, "SERVER_ERROR", "Server Error")


class Event(EventBase):
    def __init__(self, event, context):
        EventBase.__init__(self, event, context)
        self.__cognito_idp_client = boto3.client('cognito-idp')
        self.__client_id = os.environ['COGNITO_POOL_CLIENT_ID']

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
            if data.get('AuthenticationResult') and data.get('AuthenticationResult').get('AccessToken'):
                return Result.LOGON_SUCCEEDED, data
            else:
                return Result.NOT_AUTHORIZED, {}

        except self.__cognito_idp_client.exceptions.NotAuthorizedException as e:
            LOGGER.error(e)
            return Result.NOT_AUTHORIZED, {}
        except self.__cognito_idp_client.exceptions.CodeMismatchException as e:
            LOGGER.error(e)
            return Result.WRONG_CODE, {}
        except self.__cognito_idp_client.exceptions.ExpiredCodeException as e:
            LOGGER.error(e)
            return Result.EXPIRED_CODE, {}
        except Exception as e:
            LOGGER.error(str(e))
            return Result.UNKNOWN, {}
