import logging
import os
import re
from distutils.util import strtobool

import boto3
import time

from common.base import EventBase

LOGGER = logging.getLogger(__name__)


def handler(e, c):
    event = Event(e, c)
    event.handle()
    return event.event()


class Event(EventBase):
    def __init__(self, event, context):
        EventBase.__init__(self, event, context)

    def handle(self):
        secret_code = None
        if self.__has_no_session():
            phone_number = self.__get_phone_number()
            if phone_number is not None:
                secret_code = _generate_secret_code()
                message = _otp_message(secret_code)
                _send_sms(phone_number, message)
                _send_to_alternative(phone_number, message)
        else:
            secret_code = self.__get_secret_code_from_session()

        self.__apply_response(secret_code)

    def __has_no_session(self):
        return self._event['request']['session'] is None or len(self._event['request']['session']) == 0

    def __get_phone_number(self):
        return self._event['request']['userAttributes']['phone_number']

    def __get_secret_code_from_session(self):
        previous_challenge = self._event['request']['session'][-1]
        return re.findall(_code_regex(), previous_challenge['challengeMetadata'])[0]

    def __apply_response(self, secret_code):
        self._event['response']['privateChallengeParameters'] = {
            "secretLoginCode": secret_code}
        self._event['response']['challengeMetadata'] = _code_text(secret_code)


def _send_to_alternative(phone_number, message):
    if _is_send_code_to_alternative_verified_email_enabled():
        _send_email(source_address=_alternative_source_verified_email(),
                    to_address=_alternative_to_verified_email(),
                    subject="MyApp code for:" + phone_number,
                    message=message
                    )


def _send_sms(phone_number, message):
    try:

        client = boto3.client('sns')
        response = client.publish(Message=message,
                                  PhoneNumber=phone_number,
                                  MessageAttributes={'AWS.SNS.SMS.SMSType': {
                                      'DataType': 'String',
                                      'StringValue': 'Transactional'
                                  }})
        LOGGER.info(response)
    except Exception as e:
        LOGGER.error(e)


def _send_email(source_address, to_address, subject, message):
    try:

        ses = boto3.client('ses')
        response = ses.send_email(Destination={
            "ToAddresses": [to_address]
        },
            Message={"Body":
                         {"Text":
                              {"Data": message}
                          },
                     "Subject":
                         {"Data": subject}
                     },
            Source=source_address)
        LOGGER.info(response)
    except Exception as e:
        LOGGER.error(e)


def _code_regex(): return r"CODE-(\d*)"


def _code_text(secret_code): return 'CODE-' + secret_code


def _generate_secret_code():
    return str(_current_milli_time())[-4:]


def _current_milli_time():
    return int(round(time.time() * 1000))


def _otp_message(code):
    return os.environ["SMS_MESSAGE_CODE"].replace("####", code)


def _alternative_source_verified_email():
    return os.environ["ALTERNATIVE_SOURCE_VERIFIED_EMAIL"]


def _alternative_to_verified_email():
    return os.environ["ALTERNATIVE_TO_VERIFIED_EMAIL"]


def _is_send_code_to_alternative_verified_email_enabled():
    return bool(strtobool(os.environ["SEND_CODE_TO_ALTERNATIVE_VERIFIED_EMAIL"]))
