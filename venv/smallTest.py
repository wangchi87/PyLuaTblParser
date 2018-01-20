import unittest
from PyLuaTblParser import *


class TestPyLuaTblParser(unittest.TestCase):

    def test_parse_sstr_key_with_other_characters_in_the_key_and_throw_exception2(self):
        lua_table_str = '{$name = "Python"}'

        lua_table_parser = PyLuaTblParser()
        self.assertRaises(Exception, lua_table_parser.dumpDict, lua_table_str)


unittest.main()