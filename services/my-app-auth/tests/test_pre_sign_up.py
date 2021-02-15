import os
from unittest import TestCase

import functions.otp.pre_sign_up.lambda_function as pre_sign_up


class Test(TestCase):

    def setUp(self):
        os.environ["LOG_ENABLED"] = "true"

    def test_pre_sign_up_handler(self):
        event = {"request": {}, "response": {}}

        result = pre_sign_up.handler(event, None)

        self.assertTrue(result['response']['autoConfirmUser'])
        self.assertTrue(result['response']['autoVerifyPhone'])
