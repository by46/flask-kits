import unittest


class HelloWorldTestCase(unittest.TestCase):
    def test_hello_world(self):
        self.assertEqual('hello world', 'hello world')
