import unittest
from utils import str_value, int_value, list_value, bool_value


class UtilsTest(unittest.TestCase):
    def test_config_values(self):
        pid = str_value('project', 'id')
        self.assertEquals(pid, 'solutions-2023-mar-107')

    def test_int(self):
        depth = int_value('category', 'depth')
        self.assertEquals(depth, 4)

    def test_list(self):
        filter = list_value('category', 'filter')
        self.assertEquals(len(filter), 4)

    def test_bool(self):
        allow_nulls = bool_value(key='allow_trailing_nulls')
        self.assertFalse(allow_nulls)
