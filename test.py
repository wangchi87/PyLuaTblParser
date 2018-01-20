import unittest
from PyLuaTblParser import *


class TestPyLuaTblParser(unittest.TestCase):

    def test_parse_empty_lua_table(self):
        lua_table_str = '{}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertTrue(len(dumped_dict) == 0)

    def test_parse_empty_invalid_lua_table(self):
        lua_table_str = '}'

        lua_table_parser = PyLuaTblParser()
        self.assertRaises(InvalidLuaTableError, lua_table_parser.load, lua_table_str)

    # *******************************************************
    # Test simplified string key(sstr_key):
    def test_parse_sstr_key(self):
        lua_table_str = '{_na_m4ef5 = 1, move_name = 2, myname50 = 3, _temp = 4, a23b9 = 5}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict['_na_m4ef5'], 1)
        self.assertEqual(dumped_dict['move_name'], 2)
        self.assertEqual(dumped_dict['myname50'], 3)
        self.assertEqual(dumped_dict['_temp'], 4)
        self.assertEqual(dumped_dict['a23b9'], 5)

    def test_parse_sstr_key_with_extra_blanks(self):
        lua_table_str = '{   _na_m4ef5    = 1,   move_name   = 2, myname50     =  3   ,   _temp =    4,   a23b9 = 5}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict['_na_m4ef5'], 1)
        self.assertEqual(dumped_dict['move_name'], 2)
        self.assertEqual(dumped_dict['myname50'], 3)
        self.assertEqual(dumped_dict['_temp'], 4)
        self.assertEqual(dumped_dict['a23b9'], 5)

    def test_parse_sstr_key_with_blanks_in_the_key_and_throw_exception(self):
        lua_table_str = '{    n ame     = 1}'

        lua_table_parser = PyLuaTblParser()
        self.assertRaises(InvalidLuaTableError, lua_table_parser.load, lua_table_str)

    def test_parse_sstr_key_start_with_num_and_throw_exception(self):
        lua_table_str = '{4name = 1}'

        lua_table_parser = PyLuaTblParser()
        self.assertRaises(Exception, lua_table_parser.load, lua_table_str)

    def test_parse_sstr_key_with_other_characters_in_the_key_and_throw_exception1(self):
        lua_table_str = '{n*ame = 1}'

        lua_table_parser = PyLuaTblParser()
        self.assertRaises(InvalidLuaTableError, lua_table_parser.load, lua_table_str)

    def test_parse_sstr_key_with_other_characters_in_the_key_and_throw_exception2(self):
        lua_table_str = '{$name = "Python"}'

        lua_table_parser = PyLuaTblParser()
        self.assertRaises(Exception, lua_table_parser.load, lua_table_str)

    # *******************************************************
    # Test string value
    def test_parse_string_value(self):
        lua_table_str = '{empty = "", str = "a string."}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict['empty'], '')
        self.assertEqual(dumped_dict['str'], 'a string.')

    def test_parse_string_value_with_backslash(self):
        lua_table_str = '{backslash = "\\\\", controls = "\\b\\f\\n\\r\\t",}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict['backslash'], '\\')
        self.assertEqual(dumped_dict['controls'], '\b\f\n\r\t')

    def test_parse_string_value_with_escape_character(self):
        lua_table_str = '{empty = "\\"", str = "a string."}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict['empty'], '\"')
        self.assertEqual(dumped_dict['str'], 'a string.')

    def test_parse_string_value_with_escape_character(self):
        lua_table_str = '{empty = "]\\"=", str = "a string."}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict['empty'], ']\"=')
        self.assertEqual(dumped_dict['str'], 'a string.')

    def test_parse_string_value_with_any_character(self):
        lua_table_str = '{empty = "\\\\\\"\\b\\f\\n\\r\\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?", str = "a string."}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict['empty'], '\\\"\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?')
        self.assertEqual(dumped_dict['str'], 'a string.')

    # *******************************************************
    # Test string key
    def test_parse_str_key(self):
        lua_table_str = '{["key"] = 1}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict['key'], 1)

    def test_parse_str_key_with_empty_str_key(self):
        lua_table_str = '{[""] = 1, [" "] = 2}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict[''], 1)
        self.assertEqual(dumped_dict[' '], 2)

    def test_parse_str_key_with_blanks(self):
        lua_table_str = '{[    "   ke y   "  ]   = 1}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict['   ke y   '], 1)

    def test_parse_str_key_with_other_str_after_the_key1(self):
        lua_table_str = '{["key" xxx] = 1}'

        lua_table_parser = PyLuaTblParser()
        self.assertRaises(InvalidLuaTableError, lua_table_parser.load, lua_table_str)

    def test_parse_str_key_with_other_str_after_the_key1(self):
        lua_table_str = '{["key"] xxx = 1}'

        lua_table_parser = PyLuaTblParser()
        self.assertRaises(InvalidLuaTableError, lua_table_parser.load, lua_table_str)

    def test_parse_str_key_with_special_str1(self):
        lua_table_str = '{["\\""] = 1}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()

        self.assertEqual(dumped_dict['\"'], 1)

    def test_parse_str_key_with_special_str2(self):
        lua_table_str = '{["]\\"="] = 1}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict[']\"='], 1)

    def test_parse_str_key_with_special_str3(self):
        lua_table_str = '{["ke\\"]y"] = 1}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict['ke\"]y'], 1)

    def test_parse_str_key_with_any_charactors(self):
        lua_table_str = '{["\\"\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?"] = 1}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict['"\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?'], 1)

    # *******************************************************
    # Test number key
    def test_parse_num_key(self):
        lua_table_str = '{[1] = "Python", [2] = "C++", [99] = "PHP"}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict[1], 'Python')
        self.assertEqual(dumped_dict[2], 'C++')
        self.assertEqual(dumped_dict[99], 'PHP')

    def test_parse_num_key_with_extra_blanks(self):
        lua_table_str = '{[ 1  ] = "Python", [    2    ] = "C++", [ 99   ] = "PHP"}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict[1], 'Python')
        self.assertEqual(dumped_dict[2], 'C++')
        self.assertEqual(dumped_dict[99], 'PHP')

    def test_parse_float_num_key(self):
        lua_table_str = '{[1.1] = "Python", [2.2] = "C++", [99.99] = "PHP"}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict[1.1], 'Python')
        self.assertEqual(dumped_dict[2.2], 'C++')
        self.assertEqual(dumped_dict[99.99], 'PHP')

    def test_parse_num_key_with_more_than_one_dot_in_the_key_throw_exception(self):
        lua_table_str = '{[1.1] = "Python", [2.2] = "C++", [99.9.9] = "PHP"}'

        lua_table_parser = PyLuaTblParser()
        self.assertRaises(Exception, lua_table_parser.load, lua_table_str)

    def test_parse_num_key_with_blanks_in_the_key_throw_exception(self):
        lua_table_str = '{[1] = "Python", [2] = "C++", [9 9] = "PHP"}'

        lua_table_parser = PyLuaTblParser()
        self.assertRaises(Exception, lua_table_parser.load, lua_table_str)

    def test_parse_num_key(self):
        lua_table_str = '{[-1] = "Python", [2] = "C++", [-99] = "PHP"}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict[-1], 'Python')
        self.assertEqual(dumped_dict[2], 'C++')
        self.assertEqual(dumped_dict[-99], 'PHP')

    # *******************************************************
    # Test number
    def test_parse_num(self):
        lua_table_str = '{num = 100}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict['num'], 100)

    def test_parse_signed_num(self):
        lua_table_str = '{positive_num = +100, negative_num = -100, positive_float_num = +100.55, negative_float_num = -100.0}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict['positive_num'], 100)
        self.assertEqual(dumped_dict['negative_num'], -100)
        self.assertEqual(dumped_dict['positive_float_num'], 100.55)
        self.assertEqual(dumped_dict['negative_float_num'], -100.0)

    # Parse 170. to 170.0
    def test_parse_float_number(self):
        lua_table_str = '{weight = 60.55, height = 170.}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict['weight'], 60.55)
        self.assertEqual(dumped_dict['height'], 170.0)

    def test_parse_scientific_notation(self):
        lua_table_str = '{num = 12.34e5}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertEqual(dumped_dict['num'], 12.34e5)

    # *******************************************************
    # Test list
    def test_parse_list(self):
        lua_table_str = '{80, 90, 100}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertTrue(type(dumped_dict) == list)
        self.assertEqual(dumped_dict[0], 80)
        self.assertEqual(dumped_dict[1], 90)
        self.assertEqual(dumped_dict[2], 100)

    def test_parse_list_end_with_comma(self):
        lua_table_str = '{80, 90, 100,}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertTrue(type(dumped_dict) == list)
        self.assertEqual(dumped_dict[0], 80)
        self.assertEqual(dumped_dict[1], 90)
        self.assertEqual(dumped_dict[2], 100)

    def test_parse_list_with_extra_blank(self):
        lua_table_str = '{   80   ,   90,    100   }'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertTrue(type(dumped_dict) == list)
        self.assertEqual(dumped_dict[0], 80)
        self.assertEqual(dumped_dict[1], 90)
        self.assertEqual(dumped_dict[2], 100)

    def test_parse_list_with_extra_blank_and_semicolon_fieldsep(self):
        lua_table_str = '{80, 90;    100}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertTrue(type(dumped_dict) == list)
        self.assertEqual(dumped_dict[0], 80)
        self.assertEqual(dumped_dict[1], 90)
        self.assertEqual(dumped_dict[2], 100)

    def test_parse_list_with_nested_dict(self):
        lua_table_str = '{{}}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertTrue(type(dumped_dict) == list)
        self.assertTrue(type(dumped_dict[0]) == list)
        self.assertTrue(len(dumped_dict[0]) == 0)

    def test_parse_complicated_list(self):
        lua_table_str = '{80, 89.5, false, 72.5, "math", nil, nil, 99, true, 86.55, nil, "error", {}}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()
        self.assertTrue(type(dumped_dict) == list)
        self.assertEqual(dumped_dict[0], 80)
        self.assertEqual(dumped_dict[1], 89.5)
        self.assertEqual(dumped_dict[2], False)
        self.assertEqual(dumped_dict[3], 72.5)
        self.assertEqual(dumped_dict[4], "math")
        self.assertEqual(dumped_dict[5], None)
        self.assertEqual(dumped_dict[6], None)
        self.assertEqual(dumped_dict[7], 99)
        self.assertEqual(dumped_dict[8], True)
        self.assertEqual(dumped_dict[9], 86.55)
        self.assertEqual(dumped_dict[10], None)
        self.assertEqual(dumped_dict[11], "error")
        print type(dumped_dict[12])
        self.assertTrue(type(dumped_dict[12]) == list)  # {} to []?
        self.assertTrue(len(dumped_dict[12]) == 0)

    # *******************************************************
    # Test nested lua table
    def test_parse_nested_list(self):
        lua_table_str = '{name = "Python", nested = {80, 89.5, false, 72.5, 99, true, 86.55}, weight = 60.55, height = 170., location = "sichuan"}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()

        nested = dumped_dict['nested']
        print nested
        self.assertTrue(type(nested) == list)
        self.assertEqual(nested[0], 80)
        self.assertEqual(nested[1], 89.5)
        self.assertEqual(nested[2], False)
        self.assertEqual(nested[3], 72.5)
        self.assertEqual(nested[4], 99)
        self.assertEqual(nested[5], True)
        self.assertEqual(nested[6], 86.55)

        self.assertEqual(dumped_dict['name'], 'Python')
        self.assertEqual(dumped_dict['weight'], 60.55)
        self.assertEqual(dumped_dict['height'], 170.0)
        self.assertEqual(dumped_dict['location'], 'sichuan')

    def test_parse_nil_dict_and_remove_the_nil_item(self):
        lua_table_str = '{scores = {80, Math = 89.5, 72.5, nil, English = 99, 86.55, computer = nil}}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()

        scores = dumped_dict['scores']
        self.assertTrue(type(scores) == dict)
        self.assertEqual(scores[1], 80)
        self.assertEqual(scores['Math'], 89.5)
        self.assertEqual(scores[2], 72.5)
        self.assertEqual(scores['English'], 99)
        # !!!!!! score[3] = 86.55????
        #self.assertEqual(scores[4], 86.55)
        self.assertFalse('computer' in scores.keys())

    def test_parse_nested_lua_table(self):
        lua_table_str = '{array = {65,23,5},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'

        lua_table_parser = PyLuaTblParser()
        lua_table_parser.load(lua_table_str)

        dumped_dict = lua_table_parser.dumpDict()

        # list1
        list1 = dumped_dict['array']
        self.assertTrue(type(list1) == list)
        self.assertEqual(list1[0], 65)
        self.assertEqual(list1[1], 23)
        self.assertEqual(list1[2], 5)

        # dict1
        dict1 = dumped_dict['dict']
        self.assertTrue(type(dict1) == dict)

        # dict2 in dict1
        dict2 = dict1['mixed']
        self.assertTrue(type(dict2) == dict)
        self.assertEqual(dict2[1], 43)
        self.assertEqual(dict2[2], 54.33)
        self.assertEqual(dict2[3], False)
        self.assertEqual(dict2['string'], 'value')

        # list2 in dict1
        list2 = dict1['array']
        self.assertTrue(type(list2) == list)
        self.assertEqual(list2[0], 3)
        self.assertEqual(list2[1], 6)
        self.assertEqual(list2[2], 4)

        self.assertEqual(dict1['string'], 'value')


unittest.main()