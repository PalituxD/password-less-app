import os
from unittest import TestCase

import functions.otp.verify_auth_challenge_response.lambda_function as verify_auth_challenge_response


class Test(TestCase):

    def setUp(self):
        os.environ["LOG_ENABLED"] = "true"

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
