import os
from unittest import TestCase

import functions.otp.define_auth_challenge.lambda_function as define_auth_challenge


class Test(TestCase):

    def setUp(self):
        os.environ["LOG_ENABLED"] = "true"

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
