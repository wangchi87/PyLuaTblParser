from PyLuaTblParser import *

lua_table_str = '{array = {65,23,5,},["dict"] = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,};string = "value",},}'

Parser1 = PyLuaTblParser()
Parser1.load(lua_table_str)
parsed_lua_table1 = Parser1.dumpDict()
print parsed_lua_table1


Parser2 = PyLuaTblParser()
Parser2.loadDict(parsed_lua_table1)
parsed_lua_table2 = Parser2.dumpDict()

print parsed_lua_table2


Parser1.dumpLuaTable("lua_table.lua")
Parser2.dumpLuaTable("lua_table.lua")

Parser1.loadLuaTable("lua_table.lua")
parsed_lua_table3 = Parser1.dumpDict()
print parsed_lua_table3


Parser3 = PyLuaTblParser()
Parser3.loadLuaTable("rawluatable.lua")
Parser3.dumpLuaTable('testcase.lua')

Parser3.loadLuaTable('testcase.lua')
Parser3.dumpLuaTable('testcase.lua')
Parser3.loadLuaTable('testcase.lua')
Parser3.dumpLuaTable('testcase.lua')
Parser3.loadLuaTable('testcase.lua')

parsed_lua_table3 = Parser3.dumpDict()
print parsed_lua_table3
print parsed_lua_table3['root'][7]['\\"\x08\x0c\n\r\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?']
