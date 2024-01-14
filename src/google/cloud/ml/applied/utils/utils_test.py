
import unittest
from utils import str_value
class UtilsTest(unittest.TestCase):
    def test_config_values(self):
        pid = str_value('project', 'id')
        self.assertEquals(pid, 'solutions-2023-mar-107')
