import os
from unittest import TestCase
from unittest import mock

import functions.otp.create_auth_challenge.lambda_function as create_auth_challenge


class Test(TestCase):

    def setUp(self):
        os.environ["LOG_ENABLED"] = "true"

    @mock.patch.dict(os.environ, {
        "SMS_MESSAGE_CODE": "MyApp: Tu codigo secreto es: ####",
        "SEND_CODE_TO_ALTERNATIVE_VERIFIED_EMAIL": "FALSE"
    })
    def test_create_auth_challenge_handler_send_sms(self):
        event = {"request": {"userAttributes": {"phone_number": "+51999999999"},
                             "session": []},
                 "response": {"privateChallengeParameters": {}}}

        create_auth_challenge.handler(event, None)
        self.assertRegex(
            event['response']['privateChallengeParameters']['secretLoginCode'], r"(\d*)")

    def test_create_auth_challenge_handler_previous_challenge(self):
        event = {"request": {"userAttributes": {"phone_number": "+51999999999"},
                             "session": [
                                 {"test1": "value1"},
                                 {"test2": "value2"},
                                 {"challengeMetadata": "CODE-1234"}]},
                 "response": {"privateChallengeParameters": {}}}

        create_auth_challenge.handler(event, None)
        print(event['response']['privateChallengeParameters']
              ['secretLoginCode'])
        self.assertRegex(
            event['response']['privateChallengeParameters']['secretLoginCode'], r"(\d*)")
