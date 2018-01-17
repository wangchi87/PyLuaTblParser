# -*- coding: gbk -*-

from PyLuaTblParser import *


if __name__ == '__main__':
    path = r'LuaTable1.txt'

    test_str1 = '{array = {65,23,5,},bb = {65,23,5,}}'
    test_str2 = '{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
    test_str3 = '{dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
    test_str4 = '{ nil , string = nil}'
    test_str5 = '{ a=2,string = nil, s=true}'
    test_str6 = '{dict = {mixed = {43,54.33,false,nil,string = nil,},array = {3,6,4,},string = "value",}}'

    test_str = {test_str1, test_str2, test_str3, test_str4, test_str5, test_str6}

    # test_str = {test_str5}

    for s in test_str:
        a1 = PyLuaTblParser()
        a2 = PyLuaTblParser()
        a3 = PyLuaTblParser()

        a1.load(s)
        d1 = a1.dumpDict()
        # print 'a1 list: ', a1.dumpList()
        # print 'a1 dict: ', a1.dumpDict()

        a2.loadDict(d1)
        # print 'a2 dict: ', a2.dumpDict()

        a2.dumpLuaTable('output.txt')

        a3.loadLuaTable('output.txt')
        d3 = a3.dumpDict()
        print 'Lua Table:  ', s
        print 'dict Table: ', d3
        print '\n'
