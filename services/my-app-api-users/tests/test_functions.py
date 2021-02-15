import unittest

from requests import get


class TestStringMethods(unittest.TestCase):

    def test_get(self):
        assert get("http://www.google.com/").status_code == 200


if __name__ == '__main__':
    unittest.main()
