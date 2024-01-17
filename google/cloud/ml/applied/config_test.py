import unittest

from config import Config

class UtilsTest(unittest.TestCase):

    def setUp(self) -> None:
        self.config = Config()

    def test_config_values(self):
        pid = self.config.value('project', 'id')
        self.assertEquals(pid, 'solutions-2023-mar-107')

    def test_int(self):
        depth = self.config.value('category', 'depth')
        self.assertEquals(depth, 4)

    def test_list(self):
        filter = self.config.value('category', 'filter')
        self.assertEquals(len(filter), 4)

    def test_bool(self):
        allow_nulls = self.config.value(key='allow_trailing_nulls')
        self.assertFalse(allow_nulls)
