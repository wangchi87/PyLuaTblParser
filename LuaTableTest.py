# -*- coding:utf-8 -*-

import unittest

from PyLuaTblParser import *


if __name__ == '__main__':

    ut = unittest.TestCase
    path = r'LuaTable1.txt'
    test_str0 = '{1,4,dsa,abc=1,false,true}'
    test_str1 = '{array = {65;23,5,a={1,3;4,b=23}};bb = {65,23,5,}}'
    test_str2 = '{array = {65,23;5,},dict = {mixed = {43;54.33,false,9,string = "VALue",};array = {3,6;4,},string = "value",},}'
    test_str3 = '{dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
    test_str4 = '{  sd,r\\t     \\n, {12, false; nil}, a = false; [1] = 123}'
    test_str5 = '{ a=2, a{sda}; sd,\t     \n \rroot = sadd, s=true}'
    test_str6 = '{dict = {mixed = {43,54.33,false,nil,string = nil,};array = {3,6,4,},string = "value",}}'
    test_str7 = '{ "x";[4] = "y"; x = 1;"sd", [30] = 23; 45 }'


    test_str9 = '{ [  \t"\\ abc"  ] = 123,[123]=2,[abcd]="abcd", xx =1}'

    test_str = [test_str1, test_str2, test_str3, test_str4, test_str5, test_str6,test_str0, ]
    s1 = "\\\"\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:',./<>?"
    s2 = '\\"'


    test_str10 = '{["\\"--asd"] = 1 --asd\n 123}'

    test_str = [test_str10]


    #bug1= '{special = "`1~!@#$%^&*()_+-={':[,]}|;.</>?",hex = "a",}'

    lua_table_str ='{scores = {80, Math = 89.5, 72.5, nil, English = 99, 86.55, computer = nil}}'

    lua_table_parser = PyLuaTblParser()
    lua_table_parser.load(lua_table_str)

    #lua_table_parser.loadLuaTable('lua2.lua')
    #lua_table_parser.loadLuaTable('rawluatable.lua')
    print lua_table_parser.dumpDict()


