import re
from decimal import Decimal

import six


class Validator(object):
    help = ""

    def __call__(self, value):
        """
        validate param
        :param value: 
        :rtype: bool 
        """
        return self.validate(value)

    def validate(self, value):
        """
        :rtype: (None|ValueError)
        """
        raise NotImplementedError()

    def handle_error(self, *args):
        return ValueError(self.help.format(*args))


class CompareValidator(Validator):
    def __init__(self, threshold):
        self.threshold = threshold

    def validate(self, value):
        if value is None or self.illegal(value):
            return self.handle_error(self.threshold)

    def illegal(self, value):
        raise NotImplementedError()


class LetterValidator(CompareValidator):
    help = "Must be less than {0}"

    def illegal(self, value):
        return value > self.threshold


class MoreValidator(CompareValidator):
    help = "Must be more than {0}"

    def illegal(self, value):
        return value < self.threshold


class MinLengthValidator(CompareValidator):
    help = "String length must be more than {0}"

    def illegal(self, value):
        return len(value) < self.threshold


class MaxLengthValidator(CompareValidator):
    help = "String length must be less than {0}"

    def illegal(self, value):
        return len(value) > self.threshold


class PrecisionValidator(CompareValidator):
    help = "Must be less than {0} precision bit"

    def illegal(self, value):
        """
        :param Decimal value:
        """
        return value.quantize(Decimal('1.' + (self.threshold * '0'))) != value


class PasswordValidator(Validator):
    def validate(self, value):
        return True


class RegexValidator(Validator):
    help = "String length must be match the regex {0}"

    def __init__(self, line):
        self.conditions = []
        if isinstance(line, six.string_types):
            self.conditions = [re.compile(line, re.MULTILINE)]
        elif isinstance(line, (list, tuple)):
            self.conditions = [re.compile(x, re.MULTILINE) for x in line if x]
        else:
            self.conditions = [line]

    def validate(self, value):
        for condition in self.conditions:
            if not re.match(condition, value):
                return self.handle_error(condition.pattern)
        return True
