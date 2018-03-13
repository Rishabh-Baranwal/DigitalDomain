import unittest
import shutil
import os
from pm import CLI


class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.args = Namespace(name=None, type=None, path=None, SUBCMD=None)
        self.args1 = Namespace(name='abc', type='maya',
                               path=os.path.join(os.path.dirname(__file__),
                                                 'ddtest'), SUBCMD='create')
        self.args2 = Namespace(name='abc', type=None,
                               path=os.path.join(os.path.dirname(__file__),
                                                 'ddtest'), SUBCMD='delete')

    def test_cli_negative(self):
        self.cli = CLI(self.args)
        with self.assertRaises(SystemExit) as cm:
            self.cli.run()
        self.assertEqual(cm.exception.code, 4)

    def test_cli_positive(self):
        self.cli1 = CLI(self.args1)
        result1 = self.cli1.run()
        self.assertTrue(result1 is None)

        self.cli2 = CLI(self.args2)
        result2 = self.cli2.run()
        self.assertTrue(result2 is None)

    def tearDown(self):
        del self.args
        del self.args1
        del self.args2
        shutil.rmtree(os.path.join(os.path.dirname(__file__),
                                                 'ddtest'), ignore_errors=True)


if __name__ == "__main__":
    unittest.main()