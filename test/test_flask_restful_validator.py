import unittest

from flask_kits.restful.entity.validator import RegexValidator


class HelloWorldTestCase(unittest.TestCase):
    def test_regex_validator(self):
        validator = RegexValidator("^[A-Za-z0-9\-_]+$")
        self.assertTrue(validator.validate("abcd"))
        result = validator.validate("a/bcd")
        self.assertTrue(isinstance(result, ValueError))
