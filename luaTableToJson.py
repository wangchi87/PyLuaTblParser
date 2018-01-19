# -*- coding: utf-8 -*-
import json
import types

def space_str(layer):
	lua_str = ""
	for i in range(0,layer):
		lua_str += '\t'
	return lua_str

def dic_to_lua_str(data,layer=0):

	d_type = type(data)
	if  d_type is types.StringTypes or d_type is str or d_type is types.UnicodeType:
		return "'" + data + "'"
	elif d_type is types.BooleanType:
		if data:
			return 'true'
		else:
			return 'false'
	elif d_type is types.IntType or d_type is types.LongType or d_type is types.FloatType:
		return str(data)
	elif d_type is types.ListType:
		lua_str = "{\n"
		lua_str += space_str(layer+1)
		for i in range(0,len(data)):
			lua_str += dic_to_lua_str(data[i],layer+1)
			if i < len(data)-1:
				lua_str += ','
		lua_str += '\n'
		lua_str += space_str(layer)
		lua_str +=  '}'
		return lua_str
	elif d_type is types.DictType:
		lua_str = ''
		lua_str += "\n"
		lua_str += space_str(layer)
		lua_str += "{\n"
		data_len = len(data)
		data_count = 0
		for k,v in data.items():
			data_count += 1
			lua_str += space_str(layer+1)
			if type(k) is types.IntType:
				lua_str += '[' + str(k) + ']'
			else:
				lua_str += k
			lua_str += ' = '
			try:
				lua_str += dic_to_lua_str(v,layer +1)
				if data_count < data_len:
					lua_str += ',\n'

			except Exception, e:
				print 'error in ',k,v
				raise
		lua_str += '\n'
		lua_str += space_str(layer)
		lua_str += '}'
		return lua_str
	else:
		print d_type , 'is error'
		return None



json_dic = '{"age": 22, "__module__": "Person", "__class__": "Person", "name": "Peter","作者":"liangneo","说明":"转载请保留原文地址:","blog":"http://blog.csdn.net/liangneo/"}'
print(dic_to_lua_str(json.loads(json_dic)))

json_dic = '''	
{
	"maxStep":20,
	"goals":
	[
		{
			"type":"piece",
			"id":1,
			"num":20
		},
		{
			"type":"piece",
			"id":2,
			"num":5
		},
		{
			"type":"monster",
			"num":5
		}

	],
	"atk":[1,22,33,44],
	"ai":
	{
		"level1":
		{
			"attack_round":[44,47,55]
		},
		"level2":
		{
			"def":
			{
				"normal":[1,2,3,4],
				"wounded":[10,12,23,25]
			}
		}
	}
}
'''
print(dic_to_lua_str(json.loads(json_dic)))