import os
from unittest import mock
from unittest.mock import patch
from unittest import TestCase
from functions.otp import pre_sign_up
from functions.otp import define_auth_challenge
from functions.otp import verify_auth_challenge_response
from functions.otp import create_auth_challenge


class Test(TestCase):

    def setUp(self):
        os.environ["LOG_ENABLED"] = "true"

    def test_pre_sign_up_handler(self):

        event = {"request": {}, "response": {}}

        result = pre_sign_up.handler(event, None)

        self.assertTrue(result['response']['autoConfirmUser'])
        self.assertTrue(result['response']['autoVerifyPhone'])

    def test_define_auth_challenge_handler_user_not_found(self):

        event = {"request": {"userNotFound": True}, "response": {}}

        with self.assertRaises(Exception) as context:
            define_auth_challenge.handler(event, None)

        self.assertIsInstance(
            context.exception, define_auth_challenge.UserNotFound)

        self.assertFalse(event['response']['issueTokens'])
        self.assertTrue(event['response']['failAuthentication'])

    def test_define_auth_challenge_handler_invalid_challenge(self):

        event = {"request": {"userNotFound": False,
                             "session": [
                                 {'challengeName': 'SMS_MFA',
                                     'challengeResult': False},
                                 {'challengeName': 'PASSWORD_VERIFIER',
                                     'challengeResult': False},
                                 {'challengeName': 'CUSTOM_CHALLENGE',
                                  'challengeResult': False, 'challengeMetadata': {}},
                             ]}, "response": {}}

        with self.assertRaises(Exception) as context:
            define_auth_challenge.handler(event, None)

        self.assertIsInstance(
            context.exception, define_auth_challenge.InvalidChallenge)

        self.assertFalse(event['response']['issueTokens'])
        self.assertTrue(event['response']['failAuthentication'])

    def test_define_auth_challenge_handler_already_verified(self):

        event = {"request": {"userNotFound": False,
                             "session": [
                                 {'challengeName': 'SMS_MFA',
                                     'challengeResult': False},
                                 {'challengeName': 'PASSWORD_VERIFIER',
                                     'challengeResult': False},
                                 {'challengeName': 'CUSTOM_CHALLENGE',
                                  'challengeResult': True, 'challengeMetadata': {}},
                             ]}, "response": {}}

        define_auth_challenge.handler(event, None)

        self.assertTrue(event['response']['issueTokens'])
        self.assertFalse(event['response']['failAuthentication'])

    def test_define_auth_challenge_handler_define_custom_challenge(self):

        event = {"request": {"userNotFound": False,
                             "session": [
                             ]}, "response": {}}

        define_auth_challenge.handler(event, None)

        self.assertFalse(event['response']['issueTokens'])
        self.assertFalse(event['response']['failAuthentication'])
        self.assertEqual("CUSTOM_CHALLENGE",
                         event['response']['challengeName'])

    def test_verify_auth_challenge_response_handler_valid_answer(self):

        event = {"request": {"privateChallengeParameters": {"secretLoginCode": "1234"},
                             "challengeAnswer": "1234"}, "response": {}}

        verify_auth_challenge_response.handler(event, None)

        self.assertTrue(event['response']['answerCorrect'])

    def test_verify_auth_challenge_response_handler_wrong_answer(self):

        event = {"request": {"privateChallengeParameters": {"secretLoginCode": "1234"},
                             "challengeAnswer": "4578"}, "response": {}}

        verify_auth_challenge_response.handler(event, None)

        self.assertFalse(event['response']['answerCorrect'])

    @mock.patch.dict(os.environ, {
        "SMS_MESSAGE_CODE": "PasswordLess: Tu codigo secreto es: ####",
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
