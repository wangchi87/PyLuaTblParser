

from PyLuaTblParser import *


if __name__ == '__main__':
    path = r'LuaTable1.txt'
    test_str0 = '{1,4,dsa,abc=1,false,true}'
    test_str1 = '{array = {65;23,5,a={1,3;4,b=23}};bb = {65,23,5,}}'
    test_str2 = '{array = {65,23;5,},dict = {mixed = {43;54.33,false,9,string = "VALue",};array = {3,6;4,},string = "value",},}'
    test_str3 = '{dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
    test_str4 = '{  sd,r\\t     \\n, {12, false; nil}, a = false; [1] = 123}'
    test_str5 = '{ a=2, a{sda}; sd,\t     \n \rroot = sadd, s=true}'
    test_str6 = '{dict = {mixed = {43,54.33,false,nil,string = nil,};array = {3,6,4,},string = "value",}}'
    test_str7 = '{ "x";[4] = "y"; x = 1;"sd", [30] = 23; 45 }'

    test_str8 = '''{
root = {
	"Test Pattern String",
	-- {"object with 1 member" = {"array with 1 element",},},
	{["object with 1 member"] = {"array with 1 element",},},
	{},
	[99] = -42,
	[98] = {{}},
	[97] = {{},{}},
	[96] = {{}, 1, 2, nil},
	[95] = {1, 2, {["1"] = 1}},
	[94] = { {["1"]=1, ["2"]=2}, {1, ["2"]=2}, ["3"] = 3 },
	true,
	false,
	nil,
	{
		["integer"]= 1234567890,
		real=-9876.543210,
		e= 0.123456789e-12,
		E= 1.234567890E+34,
		zero = 0,
		one = 1,
		space = " ",
		quote = "\"",
		backslash = "\\",
		controls = "\b\f\n\r\t",
		slash = "/ & \\",
		alpha= "abcdefghijklmnopqrstuvwyz",
		ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWYZ",
		digit = "0123456789",
		special = "`1~!@#$%^&*()_+-={':[,]}|;.</>?",
		hex = "0x01230x45670x89AB0xCDEF0xabcd0xef4A",
		["true"] = true,
		["false"] = false,
		["nil"] = nil,
		array = {nil, nil,},
		object = {  },
		address = "50 St. James Street",
		url = "http://www.JSON.org/",
		comment = "// /* <!-- --",
		["# -- --> */"] = " ",
		[" s p a c e d " ] = {1,2 , 3

			,

			4 , 5        ,          6           ,7        },
		--[[[][][]  Test multi-line comments
			compact = {1,2,3,4,5,6,7},
	- -[luatext = "{\"object with 1 member\" = {\"array with 1 element\"}}",
		quotes = "&#34; (0x0022) %22 0x22 034 &#x22;",
		["\\\"\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?"]
		= "A key can be any string"]]
	--         ]]
		compact = {1,2,3,4,5,6,7},
		luatext = "{\"object with 1 member\" = {\"array with 1 element\"}}",
		quotes = "&#34; (0x0022) %22 0x22 034 &#x22;",
		["\\\"\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?"]
		= "A key can be any string"
	},
	0.5 ,31415926535897932384626433832795028841971693993751058209749445923.
	,
	3.1415926535897932384626433832795028841971693993751058209749445923
	,

	1066


	,"rosebud"

}}
'''
    test_str9 = '{root = {"Test Pattern String",123}}'

    test_str = [test_str0, test_str1, test_str2, test_str3, test_str4, test_str5, test_str6]

    test_str = ['{ "r\\t     \\n", \"a={12, false; nil}\" }']
    # #['{["\\\"\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:',./<>?"] = 1}']


'''
    for s in test_str:
        a1 = PyLuaTblParser()
        a2 = PyLuaTblParser()
        a3 = PyLuaTblParser()

        a1.load(s)

        d1 = a1.dumpDict()
        print 'Lua Table:\t', s
        print 'a1 dict:  \t', a1.dumpDict()

        a2.loadDict(d1)
        print 'a2 dict:  \t', a2.dumpDict()

        a2.dumpLuaTable('output.txt')

        a3.loadLuaTable('output.txt')
        d3 = a3.dumpDict()

        print 'a3 dict: \t', d3
        print '\n'
'''

test = 'sad--[luatext = "{\"object with 1 {{{&&%^%%%@%%@#}}member\" = {\"array with 1 element\"}}1234--sda\nxyz'
b = PyLuaTblParser()
#print b.removeComment(test)

t2 = '''			4 , 5        ,          6           ,7        },
		--[[[][][]  Test multi-line comments
			compact = {1,2,3,4,5,6,7},
	- -[luatext = "{\"object with 1 member\" = {\"array with 1 element\"}}",
		quotes = "&#34; (0x0022) %22 0x22 034 &#x22;",
		["\\\"\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?"]
		= "A key can be any string"]]
	--         ]]
		compact = {1,2,3,4,5,6,7213414},
		luatext = "{\"object with 1 member\" = {\"array with 1 element\"}}",
		quotes = "&#34; (0x0022) %22 0x22 034 &#x22;",
		["\\\"\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?"]
		= "A key can be any string"'''

commentTest = '''abc--[[[][][]  Test multi-line comments
			compact = {1,2,3,4,5,6,7},
	- -[luatext = "{\"object with 1 member\" = {\"array with 1 element\"}}",
		quotes = "&#34; (0x0022) %22 0x22 034 &#x22;",
		["\\\"\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:',./<>?"]
		= "A key can be any string"]]
	--         ]]def'''
print b.removeComment(commentTest)

#print b.removeExtraEscapeString(''' \n\t["\\\"\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:',./<>?"] ''')

#print b.removeExtraEscapeString(' \n\t243rfdsf   ')