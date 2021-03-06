# -*- coding: utf-8 -*-

class InvalidLuaTableError(Exception):
    pass

class PyLuaTblParser:
    '''
    This is a lua table parser
    Chi Wang
    '''

    # string to be parsed
    luaString = ''
    result = None

    otherCharacterSet="~!@#$%^&*()+-={':[,]}|;.</>?"

    def __init__(self):
        self.result = None
        self.luaString = ''

    def load(self, myStr):
        if len(myStr) == 0:
            raise Exception('Empty input Lua Table string')
        self.luaString = self.__removeComment(myStr).strip()
        self.__checkLuaTbl()
        self.result = self.__processString(self.luaString)

    def dump(self):
        return self.luaString

    def loadLuaTable(self, filePath):
        try:
            luaFile = open(filePath)
        except IOError as e:
            print 'file reading error:', e.strerror, e.errno
            raise Exception('file reading error')
        fileStr = luaFile.read()
        self.luaString = self.__removeComment(fileStr).strip()
        self.__checkLuaTbl()
        self.result = self.__processString(self.luaString)

    def __checkLuaTbl(self):
        # make sure lua table starts and ends with { }
        if (self.luaString.find('{') != 0) or (self.luaString.rfind('}') != len(self.luaString) - 1):
            raise InvalidLuaTableError('Incorrect input Lua Table: table string does not start and end with { and }.')


    # load an external dict, and store in class
    def loadDict(self, dict):
        if type(dict) == type({}):
            newDict = {}
            typeSet = [type(2), type(2.3), type('a')]
            for k, v in dict.items():
                if type(k) in typeSet:
                    newDict[k] = self.loadDictValue(v)
            self.result = newDict
        else:
            raise Exception('input parameter is not a dict type data')

    def loadDictValue(self, dictValue):
        if type(dictValue) == type({}):
            newDict = {}
            typeSet = [type(2), type(2.3), type('a')]
            for k, v in dictValue.items():
                if type(k) in typeSet:
                    newDict[k] = self.loadDictValue(v)
            return newDict
        else:
            return dictValue

    # export dict data
    def dumpDict(self):
        if self.result == None and self.luaString != '':
            self.result = self.__processString(self.luaString)
        return self.result

    # the following three functions export python data in Lua table form
    def dumpLuaTable(self, filePath):
        try:
            outputFile = open(filePath, 'w')
            outputFile.write('{')

            if type(self.result) == type([]):
                for s in self.result:
                    self.writeSingleListData(s, outputFile)
                    outputFile.write(',')
            if type(self.result) == type({}):
                self.writeDictData(self.result, outputFile)

            outputFile.write('}')
            outputFile.close()
        except IOError as e:
            print e.errno, e.strerror
            raise Exception('errors in exporting data')


    # write dict data recursively
    def writeDictData(self, dictData, outputFileHandle):
        # write dict data
        for k, v in dictData.items():
            if type(k) == type(''):
                outputFileHandle.write('"'+str(k) + '"=')
            if type(k) == type(1):
                outputFileHandle.write('['+str(k) + ']=')
            self.writeDictKeyData(v, outputFileHandle)
            outputFileHandle.write(',')

    # write the key element in dict data
    def writeDictKeyData(self, dictKeyData, outputFileHandle):
        if type(dictKeyData) == type({}):
            # if dictKeyData is still a dict
            outputFileHandle.write('{')
            self.writeDictData(dictKeyData, outputFileHandle)
            outputFileHandle.write('}')
            return
        if type(dictKeyData) == type([]):
            # if dictKeyData is a list
            outputFileHandle.write('{')
            for y in dictKeyData:
                if type(y) == type({}):
                    self.writeDictData(y, outputFileHandle)
                else:
                    self.writeSingleListData(y, outputFileHandle)
                    outputFileHandle.write(',')
            outputFileHandle.write('}')
        else:
            # if dictKeyData is a single value
            self.writeSingleListData(dictKeyData, outputFileHandle)

    # write list data, we need to take care of None, False, and True etc.
    def writeSingleListData(self, singleValue, outputFileHandle):
        if singleValue != None:
            if str(singleValue) == 'False' or str(singleValue) == 'True':
                outputFileHandle.write(str(singleValue).lower())
            else:
                if type(singleValue) == type(''):
                    outputFileHandle.write('"' + str(singleValue) + '"')
                if type(singleValue) == type(1) or type(singleValue) == type(1.1):
                    outputFileHandle.write(str(singleValue))
        else:
            outputFileHandle.write('nil')

    def __parseKey(self, keyStr):
        keyStr = keyStr.strip()
        keyStr = keyStr.strip('[')
        keyStr = keyStr.strip(']')
        key = self.rtnCorrectType(keyStr)

        return key

    def __parseValue(self, valueStr):
        valueStr = valueStr.strip()
        value = self.__processString(valueStr)
        return value

    # core function of lua table string parser
    # add a lable of the string here!!!
    def __processString(self, myStr):

        myStr = myStr.strip()

        hasBracket = (myStr.find('{') == 0 and myStr.rfind('}') == len(myStr) - 1)

        if hasBracket:

            # if string starts with '{' and ends with '}'
            newStr = myStr[1:len(myStr) - 1].strip()

            # fix {}, {}, {} bugs
            allBracket = newStr.split(',')
            areAllBracket = True
            bracketList = []
            for s in allBracket:
                if s.strip() == '{}':
                    bracketList.append([])
                else:
                    areAllBracket = False
                    break
            if areAllBracket:
                return bracketList

            if (newStr.find('{') == 0 and newStr.rfind('}') == len(newStr) - 1):
                tmp = []
                tmp.append(self.__processString(newStr))
                return tmp

            # 按照逗号或分号，将字符串划分成若干子串
            partition = self.__stringPartition(newStr)

            dictStrList = []
            hasDictInTable = False
            for s in partition:
                dictStr = self.__parseDictStr(s)
                dictStrList.append(dictStr)
                if type(dictStr) != str:
                    hasDictInTable = True

            if hasDictInTable:
                # deal with the string like {1,{1,2,3},a=1}
                # return a dict type
                tempDict = {}

                # turn every one into dict element
                index = 1
                # record the all the keys
                keyList = []

                for tmp in dictStrList:

                    if type(tmp) == str:
                        if len(tmp) != 0 and tmp.strip().lower() != 'nil':
                            # if this tmp is not a dict element
                            # tmp might be like 1 or {1,2,3}
                            tmp = self.__processString(tmp)
                            tempDict[index] = tmp
                            keyList.append(index)
                            index += 1
                    else:
                        key = self.__parseKey(tmp[0])
                        value = self.__parseValue(tmp[1])

                        if value != None and (key not in keyList):
                            # make sure the key is not used
                            # in case the key is used, discard this pair
                            tempDict[key] = value
                return tempDict

            else:
                # deal with a list case, like {1, 2, 3}, return a list type data []
                tempList = []
                for s in partition:
                    temp = self.__processString(s)
                    if temp != '' and temp != {}:
                        tempList.append(temp)
                return tempList

        else:
            # deal with single value data, like '1' or 'abc'
            return self.rtnCorrectType(myStr)

    def __isNumber(self, myStr):
        return self.__isFloat(myStr.strip()) or myStr.strip().isdigit()

    def __isFloat(self, myStr):
        ''' test if a string represent a float number '''
        try:
            float(myStr)
            return True
        except:
            return False

    # tell whether the string is a number(float or int?) or a Boolean value, or a string
    # return their corresponding types
    def rtnCorrectType(self, myStr):
        '''
        tell whether the string is a number(float or int?) or a Boolean value, or a string
        return the value of their corresponding types
        '''

        # is Boolean type ?
        if myStr.strip().lower() == 'false':
            return False
        if myStr.strip().lower() == 'true':
            return True

        if myStr.strip() == 'nil':
            return None

        # is a int number ?
        if myStr.strip().isdigit():
            return int(myStr.strip())
        if self.__isFloat(myStr.strip()):
            return float(myStr.strip())

        value = myStr.strip()

        # remove quote
        if self.__isAStrWithQuote(value):
            value = value[1:len(value)-1]

        # process escape string

        value = value.replace('\\"', '\"')
        value = value.replace("\\'", '\'')
        value = value.replace('\\a', '\a')
        value = value.replace('\\b', '\b')
        value = value.replace('\\x08', '\b')
        value = value.replace('\\x0c', '\f')
        value = value.replace('\\n', '\n')
        value = value.replace('\\r', '\r')
        value = value.replace('\\t', '\t')
        value = value.replace('\\f', '\f')
        value = value.replace('\\\\', '\\')
        value = value.replace('\\/', '/')
        value = value.replace('\\v', '\v')

        return value

    # split given string with comma at top level
    # e.g. input : {'1','2','{3,4}'}
    #      output: '1,2,{3,4}'R
    def __stringPartition(self, myStr):
        partition = []

        seperatorList = [',', ';']

        strBeginPos = 0
        seperatorPos = 0

        index = 0
        length = len(myStr)

        inQuote = False
        bracketLayer = 0

        while index < length:
            if myStr[index] == '"' and inQuote == False:
                inQuote = True
                index += 1
                continue
            if myStr[index] == '"' and inQuote == True:
                inQuote = False
                index += 1
                continue
            if myStr[index] == '\\':
                # 进入转义字符状态
                index += 2
                continue
            if inQuote == False and myStr[index] == '{':
                bracketLayer += 1
                index += 1
                continue
            if inQuote == False and myStr[index] == '}':
                bracketLayer -= 1
                index += 1
                continue
            if inQuote == True and (myStr[index] == '{' or myStr[index] == '}'):
                index += 1
                continue

            if myStr[index] in seperatorList and bracketLayer == 0 and inQuote == False:
                # find a partition
                partition.append(myStr[strBeginPos: index])
                index += 1
                strBeginPos = index
                continue
            index = index + 1

        if strBeginPos!= length :
            partition.append(myStr[strBeginPos:])

        return partition

    # find separation index of given string with first ',' or ';'
    def findLuaTblSep(self, myStr, index):
        sep = [',',';']
        pos = []
        for s in sep:
            pos.append(myStr.find(s,index))
        pos = [x for x in sorted(pos) if x > -1]
        if len(pos) == 0:
            return -1
        else:
            return pos[0]

    def __removeComment(self, myStr):

        uncommentedStr = myStr
        inQuote = False

        index = 0
        length = len(myStr)

        while index < length:
            if myStr[index] == '"' and inQuote == False:
                inQuote = True
                index += 1
                continue
            if myStr[index] == '"' and inQuote == True:
                inQuote = False
                index += 1
                continue
            if myStr[index] == '\\':
                # 转义字符，直接忽略其后面一个字符
                index += 2
                continue
            if myStr[index: index + 2] == '--':
                if inQuote == False:
                    uncommentedStr = self.__processComment(uncommentedStr, index)
                    break
                else:
                    index += 2
                    continue
            index += 1
        if uncommentedStr!=myStr:
            return self.__removeComment(uncommentedStr)
        else:
            return myStr

    def __processComment(self, myStr, commentStart):
        if self.__isMultiLineComment(myStr, commentStart):
            endPos = self.__locateMultiLineComment(myStr, commentStart)
        else:
            # 否则用 \n 标识注释的结束位置
            # 跳过字符中的 \\n

            jumpPos = myStr.find('\\n', commentStart + 1)
            endPos = myStr.find('\n', commentStart + 1)

            while endPos == jumpPos + 1:
                jumpPos = myStr.find('\\n', jumpPos + 1)
                endPos = myStr.find('\n', endPos + 1)

        myStr = myStr[0:commentStart] + myStr[endPos + 1:]
        return myStr

    def __isMultiLineComment(self,myStr, commentStart):
        ''' 是否有多行注释'''
        newStr = myStr[commentStart+2:].strip()

        if newStr.find('[[') == 0:
            return True
        return False

    def __locateMultiLineComment(self,myStr, commentStart):
        ''' 定位多行注释的结束位置'''

        # myStr might be '--   [[ dsa221rfcsdsadd[[]]   -- ]]abcd'
        end = -1
        if myStr.find('[[') != -1:
            end = myStr.find(']]')
            while end !=-1:
                tmp = myStr[:end].strip()
                if tmp.rfind('--') == len(tmp) - 2 :
                    break
                else:
                    end = myStr.find(']]', end + 1)
            if end == -1:
                raise Exception('invalide lua multi line comment')

        return end+2
        pass

    def __isAStrWithBracket(self, myStr):
        myStr = myStr.strip()
        return (myStr.find('{') == 0 and myStr.rfind('}') == len(myStr) - 1)


    def __parseDictStr(self, inputStr='*Sdsa={13}2easd={231rfs3=P{}}'):
        '''
        test if a given string represents a dict data
        correct lua dict form:
        ["x"] = 1, [1] = "x" , x = 1, x = {...}
        incorrect form:
        [ x ] = 1, [1] = x, "xyz" = 1

        ( 'x' is not valid here, because we are already inside of a string)

        如果遇到[],则[]内的字符串可以出现任意字符，包括 =，
        如果左侧字符不存在[],则第一个=就是划分的位置， 但是在=右侧出现"" 或者 {} 之前，再次出现=
        那么此字符串为invalid expression， 比如 xyz=x=1

        返回值，如果不是dict，返回 inputStr
        否则，返回 [key,value]，其中 key value 为一个字典的划分
        '''

        stripedStr = inputStr.strip()

        if self.__isAStrWithQuote(stripedStr) or self.__isAStrWithBracket(stripedStr) or len(stripedStr) == 0 :
            # 如果输入代表一个字符串， 例如"xyz=123"，则一定不是dict型数据
            return inputStr

        if stripedStr.find('=') == -1:
            return inputStr
        else:
            # might be a dict expression

            if stripedStr[0] == '[':
                # 如果字符串存在[]
                # 找到对应 ] 的位置, 其后的第一个 = 为划分位置
                leftBracket = inputStr.find('[')
                # 从左侧找到[ 之后的第一个"
                leftQuote = inputStr.find('"', leftBracket)

                if leftQuote != -1:
                    if self.__isBlankInTwoIndex(inputStr, leftBracket, leftQuote):
                        # ["abc"] = 1 case
                        # " ] = 组合 确定了一个字典的划分

                        rightQuote = inputStr.find('"', leftQuote + 1)
                        rightBracket = inputStr.find(']', rightQuote + 1)
                        equalPos = inputStr.find('=',rightBracket + 1)

                        while (rightQuote < rightBracket < equalPos and self.__isBlankInTwoIndex(inputStr,rightQuote,rightBracket) and self.__isBlankInTwoIndex(inputStr,rightBracket,equalPos)) == False:
                            rightQuote = inputStr.find('"', rightQuote + 1)
                            rightBracket = inputStr.find(']', rightQuote + 1)
                            equalPos = inputStr.find('=', rightBracket + 1)

                            if rightQuote == -1 or rightBracket == -1 or equalPos == -1:
                                raise InvalidLuaTableError('invalide lua table express, [ "abx" d] or [" ads case: non-closed bracket for a key string')
                    else:
                        #[1] = "x" case
                        rightBracket = inputStr.find(']', leftBracket)
                        tmp = inputStr[leftBracket+1: rightBracket].strip()
                        if self.__isNumber(tmp) == False:
                            # 处理 不带引号的key 不为数字的异常
                            #print inputStr
                            raise InvalidLuaTableError('invalide lua table express, [x]=1 case: unquoted string as key in bracket')
                else:
                    # [1] = 2 case
                    rightBracket = inputStr.find(']', leftBracket)
                    tmp = inputStr[leftBracket+1: rightBracket].strip()
                    if tmp.isdigit() == False:
                        #print inputStr
                        raise InvalidLuaTableError('invalide lua table express, [x]=1 case: unquoted string as key in bracket')

                pos = inputStr.find('=', rightBracket)

                if self.__isBlankInTwoIndex(inputStr, rightBracket, pos) == False:
                    # 处理 ["x"] abc = 1 的异常
                    raise InvalidLuaTableError(
                        'invalide lua table express, [x] abc = 1 case: extra string between ] and = ')

            else:
                # 如果 myStr不以[开头，则第一个=号，应该就是划分的位置
                pos = inputStr.find('=')
                # 在此种情况下，key的格式有特殊的要求：
                # n ame = 1, 4name = 1 , nam#e = 1 均为错
                key = inputStr[:pos].strip()

                if key.find(' ') != -1:
                    #print inputStr, key
                    raise InvalidLuaTableError('found blank inside of a key string')

                if key[0].isdigit():
                    #print inputStr, key
                    raise InvalidLuaTableError('found digit at the beginning of a key string')

                for s in self.otherCharacterSet:
                    if key.find(s) != -1:
                        #print inputStr, key
                        raise InvalidLuaTableError('found other character in a key string')

            # 测试字符串的有效性：不存在多个等号
            # 尝试寻找第二个等号
            pos2 = inputStr.find('=', pos + 1)
            if pos2 != -1:
                # 找到 第二个等号 后面的 第一个 " 或者 {
                firstQuoteAfterEqual = inputStr.find('"', pos + 1)
                firstBracketAfterEqual = inputStr.find('{', pos + 1)

                firstSeperator = -1
                if self.__isBlankInTwoIndex(inputStr, pos, firstQuoteAfterEqual):
                    firstSeperator = firstQuoteAfterEqual

                if self.__isBlankInTwoIndex(inputStr, pos, firstBracketAfterEqual):
                    firstSeperator = firstBracketAfterEqual

                if firstSeperator == -1:
                    raise InvalidLuaTableError('invalide lua table express, x==1 case: found two = in string')

                # 如果等号在"或者{ 之前，则为错误的输入格式
                if pos2 < firstSeperator:
                    # 如果第二个等号的位置，在左括弧的后面，则返回第一个等号的位置
                    # 作为划分的位置
                    raise InvalidLuaTableError('invalide lua table express, x == "123" or x == {123} case: found two = in string')

        key = inputStr[:pos]
        value = inputStr[pos+1:]
        return [key, value]

    def __isAStrWithQuote(self,myStr):
        # 判断输入字符串是否被" " 包围，如果是，则认为myStr代表一个字符串
        if len(myStr) > 1 and myStr[0] == '"' and myStr[len(myStr) - 1] == '"':
            return True
        else:
            return False

    def __isBlankInTwoIndex(self, myStr, start, end):
        # 测试字符串 start 和 end 之间是否只有空格
        tmp = myStr[start+1:end].strip()
        if tmp == '':
            return True
        else:
            return False