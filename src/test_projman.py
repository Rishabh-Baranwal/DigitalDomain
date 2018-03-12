import unittest
import os
import shutil
import projman


class TestProjman(unittest.TestCase):

    def setUp(self):
        self.create_args = {'name': None, 'dcc_type': None, 'path': '/abc',
                            'template_path': '/def'}
        self.create_args1 = {'name': 'xyz', 'dcc_type': 'maya',
                             'path': os.path.join(os.path.dirname(__file__),
                                                 'ddtest'),
                             'template_path': os.path.join(os.path.relpath(
                                 os.getcwd(), 'projman'),'templates')}
        self.list_args = {'template_path': '/pqr'}
        self.types_args = {'dcc_type': None, 'path': '/ghi'}
        self.delete_args = {'name': None, 'dcc_type': None, 'path': '/jkl',
                            'force': None}
        self.describe_args = {'name': None, 'path': '/mno'}

    def test_create_negative(self):
        with self.assertRaises(SystemExit) as cm:
            projman.create(**self.create_args)
        self.assertEqual(cm.exception.code, 4)

    def test_list_negative(self):
        with self.assertRaises(SystemExit) as cm:
            projman.list_types(**self.list_args)
        self.assertEqual(cm.exception.code, 4)

    def test_types_negative(self):
        with self.assertRaises(SystemExit) as cm:
            projman.list_projects(**self.types_args)
        self.assertEqual(cm.exception.code, 4)

    def test_delete_negative(self):
        with self.assertRaises(SystemExit) as cm:
            projman.delete(**self.delete_args)
        self.assertEqual(cm.exception.code, 4)

    def test_describe_negative(self):
        with self.assertRaises(SystemExit) as cm:
            projman.describe(**self.describe_args)
        self.assertEqual(cm.exception.code, 4)

    def test_all_positive(self):
        result = projman.create(**self.create_args1)
        self.assertTrue(result is None)
        result1 = projman.list_types(self.create_args1['template_path'])
        self.assertTrue(result1 is None)
        result2 = projman.list_projects(self.create_args1['dcc_type'],
                                          self.create_args1['path'])
        self.assertTrue(result2 is None)
        result3 = projman.describe(self.create_args1['name'],
                                   self.create_args1['path'])
        self.assertTrue(result3 is None)
        result4 = projman.delete(self.create_args1['name'],
                                 self.create_args1['dcc_type'],
                                 self.create_args1['path'], True)
        self.assertTrue(result4 is None)

    def tearDown(self):
        del self.create_args
        del self.create_args1
        del self.list_args
        del self.types_args
        del self.delete_args
        del self.describe_args
        shutil.rmtree(os.path.join(os.path.dirname(__file__),
                                   'ddtest'), ignore_errors=True)

if __name__ == "__main__":
    unittest.main()