import random
import string


def nonce_str():
    terms = string.letters + string.digits
    return ''.join([random.choice(terms) for _ in xrange(16)])


def new_validate_code():
    terms = string.digits
    return ''.join([random.choice(terms) for _ in xrange(6)])
