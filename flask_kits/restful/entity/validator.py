from decimal import Decimal


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
