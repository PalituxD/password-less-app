import boto3
import os
from functions.otp.base import EventBase, ResultBase, Response


def handler(e, c):

    event = Event(e, c)
    event.handle()
    return event._response


class Result(ResultBase):
    SIGN_UP_USER_CREATED = (200, "LOGON_SUCCEEDED", "User was created")
    SIGN_UP_USER_ALREADY_EXISTS = (
        200, "LOGON_SUCCEEDED", "User already exists")
    SIGN_UP_INVALID_PASSWORD = (401, "LOGON_SUCCEEDED", "Invalid password")


class Event(EventBase):
    def __init__(self, event, context):
        EventBase.__init__(self, event, context)
        self.__cognito_idp_client = boto3.client('cognito-idp')
        self.__client_id = os.environ['COGNITO_POOL_CLIENT_ID']
        self.__user_pool_id = os.environ['COGNITO_POOL_USER_POOL_ID']
        self.__username = self._body['phone_number']
        self.__device_key = self._body['device_key']
        self._response = {}

    def handle(self):

        result = self.__sign_up()
        data = {}
        if result in [Result.SIGN_UP_USER_CREATED, Result.SIGN_UP_USER_ALREADY_EXISTS]:
            if result == Result.SIGN_UP_USER_CREATED:
                self.__update_user_data()
            data = self.__initiate_auth()

        self._response = Response(result, data).to_json()

    def __sign_up(self) -> Result:
        try:
            self.__cognito_idp_client.sign_up(
                ClientId=self.__client_id,
                Username=self.__username,
                Password=self.__username,
                UserAttributes=[
                    {'Name': 'phone_number', 'Value': self.__username}],
                ValidationData=[{'Name': 'phone_number', 'Value': 'string'}]
            )
            return Result.SIGN_UP_USER_CREATED

        except self.__cognito_idp_client.exceptions.UsernameExistsException as e:
            print(e)
            return Result.SIGN_UP_USER_ALREADY_EXISTS

        except self.__cognito_idp_client.exceptions.InvalidPasswordException as e:
            print(e)
            return Result.SIGN_UP_INVALID_PASSWORD

        except Exception as e:
            print(e)
            return Result.UNKNOWN

    def __update_user_data(self):
        self.__cognito_idp_client.admin_update_user_attributes(
            UserPoolId=self.__user_pool_id,
            Username=self.__username,
            UserAttributes=[
                {'Name': 'phone_number_verified', 'Value': 'false'},
                {'Name': 'custom:custom_attribute', 'Value': self.__device_key}
            ]
        )

    def __initiate_auth(self):
        return self.__cognito_idp_client.initiate_auth(
            ClientId=self.__client_id,
            AuthFlow='CUSTOM_AUTH',
            AuthParameters={
                'USERNAME': self.__username,
                'DEVICE_KEY': self.__device_key
            }
        )
