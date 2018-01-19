# -*- coding: utf-8 -*-

class InvalidLuaTableError(Exception):
    pass

class PyLuaTblParser:
    '''
    This is a lua table parser
    '''

    # string to be parsed
    luaString = ''
    result = None

    def __init__(self):
        self.result = None
        self.luaString = ''

    def load(self, myStr):
        if len(myStr) == 0:
            raise Exception('Empty input Lua Table string')
        self.luaString = myStr
        self.removeEscapeStr()
        self.checkLuaTbl()

    def dump(self):
        return self.luaString

    def loadLuaTable(self, filePath):
        try:
            luaFile = open(filePath)
        except IOError as e:
            print 'file reading error:', e.strerror, e.errno
            raise Exception('file reading error')
        self.luaString = luaFile.read()
        self.removeEscapeStr()
        self.checkLuaTbl()

    def checkLuaTbl(self):
        # make sure lua table starts and ends with { }
        if (self.luaString.find('{') != 0) or (self.luaString.rfind('}') != len(self.luaString) - 1):
            raise InvalidLuaTableError('Incorrect input Lua Table: table string does not start and end with { and }.')

        # checck if bracket number matches
        lList = self.rtnCharLoc(self.luaString, '{')
        rList = self.rtnCharLoc(self.luaString, '}')

        if len(lList) != len(rList):
            raise InvalidLuaTableError('Incorrect input Lua Table: bracket number does not match')

    def removeEscapeStr(self):
        pass
        # this is left to be extended if needed
        #escapeStrings = ['\n', '\t', '\r', '\v', '\f', '\'', '\a', '\b']
        # delete all the possible escape strings
        #for escStr in escapeStrings:
            #self.luaString = self.luaString.replace(escStr, '')

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
            self.result = self.processString(self.luaString)
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

    # when the given string has '=' symbol, turn it into python dict type
    # note leftPartStr is the key of the returned key
    def processDictStr(self, myStr, symbolPos):

        leftPartStr = myStr[:symbolPos].strip()
        rightPartStr = myStr[symbolPos + 1:].strip()
        leftPartStr = leftPartStr.strip('[')
        leftPartStr = leftPartStr.strip(']')
        key = self.rtnCorrectType(leftPartStr)
        value = self.processString(rightPartStr)
        return (key, value)

    # core function of lua table string parser
    # add a lable of the string here!!!
    def processString(self, myStr):

        hasBracket = (myStr.find('{') != -1)

        if hasBracket:

            if (myStr.find('{') == 0) and (myStr.rfind('}') == len(myStr) - 1):
                # if string starts with '{' and ends with '}'
                newStr = myStr[1:len(myStr) - 1]

                pairsTuple = self.bracketDict(newStr)
                partition = self.strPartition(newStr, pairsTuple)

                if newStr.find('=') != -1:
                    # deal with the string like {1,{1,2,3},a=1}
                    # return a dict type
                    tempDict = {}

                    # turn every one into dict element
                    index = 1
                    # record the all the keys
                    keyList = []
                    for tmp in partition:
                        symbolPos = tmp.find('=')

                        if symbolPos == -1:
                            if len(tmp) != 0 and tmp.strip().lower() != 'nil':
                                # if this tmp is not a dict element
                                # tmp might be like 1 or {1,2,3}
                                tmp = self.processString(tmp)
                                tempDict[index] = tmp
                                keyList.append(index)
                                index += 1
                        else:
                            # tmp is a dict element
                            key, value = self.processDictStr(tmp, symbolPos)
                            if value != None and (key not in keyList):
                                # make sure the key is not used
                                # in case the key is used, discard this pair
                                tempDict[key] = value
                    return tempDict

                else:
                    # deal with a list case, like {1, 2, 3}, return a list type data []
                    tempList = []
                    for s in partition:
                        temp = self.processString(s)
                        if temp != '' and temp != {}:
                            tempList.append(temp)
                    return tempList

            else:
                # deal with the string like a{1,2,3}, return a dict data
                return self.rtnCorrectType(myStr)
        else:
            # deal with single value data, like '1' or 'abc'
            return self.rtnCorrectType(myStr)

    def rtnCharLoc(self, myStr, charLetter):
        '''
        return the indices of all the charLetter in myStr
        e.g. input : {1,2,{3,4}}, and charLetter is '}'
              output: [9,10]
        :param    myStr:      input string
        :param    charLetter: char letter to fined
        :return:  the indices of all the charLetter in myStr
        '''
        locations = []
        index = myStr.find(charLetter)
        while index > -1:
            locations.append(index)
            index = myStr.find(charLetter, index + 1)
        return locations


    def bracketDict(self, myStr):
        '''
        find corresponding bracket pairs in given string
        e.g.    input : '{1,2,{3,4}}'
                output: [(0,10),(5,9)]
        :param myStr:   input string
        :return:        corresponding bracket pairs in given string
        '''
        try:
            lList = self.rtnCharLoc(myStr, '{')
            rList = self.rtnCharLoc(myStr, '}')

            # if len(lList) != len(rList):
            #    raise Exception('Incorrect input Lua Table')

            # we use a stack to find corresponding bracket
            stack = []
            ref = {}
            popIndex = 0

            while len(stack) > 0 or len(lList) > 0:
                if len(lList) > 0:
                    if lList[popIndex] < rList[popIndex]:
                        stack.append(lList.pop(popIndex))
                    else:
                        lpos = stack.pop(len(stack) - 1)
                        rpos = rList.pop(popIndex)
                        ref[lpos] = rpos
                else:
                    lpos = stack.pop(len(stack) - 1)
                    rpos = rList.pop(popIndex)
                    ref[lpos] = rpos

            return [(k, ref[k]) for k in sorted(ref.keys())]
        except:
            raise Exception("invalid bracket pair in string")

    # judge whether the index is inside of the range of index of each bracket or not
    # e.g. if index is 2, the bracketPair is (3,4) (5,10) then the index is not inside(return False)
    def isIndexInBracket(self, index, bracketPair):
        for i in range(0, len(bracketPair)):
            if index in range(bracketPair[i][0], bracketPair[i][1]):
                return True
        return False

    def isFloat(self, myStr):
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
        if myStr.lower() == 'false':
            return False
        if myStr.lower() == 'true':
            return True

        if myStr == 'nil':
            return None

        # is a int number ?
        if myStr.isdigit():
            return int(myStr)
        if self.isFloat(myStr):
            return float(myStr)

        value = myStr

        # process escape string
        value = value.replace('abc', 'cba')

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

        return value.strip().strip('"')

    # split given string with comma at top level
    # e.g. input : '1,2,{3,4}'
    #      output: {'1','2','{3,4}'}
    def strPartition(self, myStr, bracketPair):

        commaStart = 0
        strStart = 0
        partition = []
        end = self.findLuaTblSep(myStr, commaStart)

        while end != -1:
            if not self.isIndexInBracket(end, bracketPair):
                partition.append(myStr[strStart:end])
                strStart = end + 1

            commaStart = end + 1
            end = self.findLuaTblSep(myStr, commaStart)

        if strStart != end:
            partition.append(myStr[strStart:])
        return partition


    # find separation index of given string with first ',' or ';'
    def findLuaTblSep(self, myStr, index):
        end1 = myStr.find(',', index)
        end2 = myStr.find(';', index)
        if end2 == -1 or end2 > end1:
            return end1
        else:
            return end2

    def strPreProcessing(self, myStr = 'ds\\ta=ssd da= {dsadwa}'):
        '''
        1. 删除注释
            '--{}'，以及'-- \n'类型
        2. 删除多余的转义字符
            多余：'\n "dsad\\t " \t\n ', 在 " " 之外字符
            这里不处理""内部的转义字符
        3. 判断字符是否代表一个dict数据，并返回划分位置
        :param mystr:
        :return:
        '''
        pass

        myStr = self.removeComment(myStr)
        myStr = self.removeExtraEscapeString(myStr)



        return myStr

    def removeComment(self, myStr='abc--{bhgy--ijk}1234--nbkyg8t87tgh\nxyz'):

        # find the first comment symbol
        commentSymbol = ['--', '- -']
        posList = []
        for sym in commentSymbol:
            posList.append(myStr.find(sym))
        posList = [ x for x in sorted(posList) if x >= 0]

        commentStart = -1
        if len(posList) > 0:
            commentStart = posList[0]

        # comment processing
        if commentStart != -1:
            bracketPair = self.bracketDict(myStr)
            if len(bracketPair) > 0 :
                leftBracket = bracketPair[0][0]
                rightBracket = bracketPair[0][1]
                if rightBracket > leftBracket:
                    # 用 {} 标识注释的位置
                    myStr = myStr[0:commentStart] + myStr[rightBracket+1:]
            else:
                # 否则用 \n 标识注释的结束位置
                endPos = myStr.find('\n', commentStart + 1)
                myStr = myStr[0:commentStart] + myStr[endPos+1:]

            myStr = self.removeComment(myStr)
        return myStr

    def removeExtraEscapeString(self, myStr = ' \n\t"r\\t     \\n" '):

        # 检查myStr中是否包含 " " 子串
        # 子串中的空格不可去除
        start = myStr.find('"')
        end = myStr.find('"', start+1)

        if start == -1 and end == -1:
            return myStr.strip()
        else:
            escapeStrings = ['\n', '\t', ' ']
            newStr = ''
            for s in range(0, len(myStr)):
                if s in range(start, end+1):
                    newStr = newStr + myStr[s]
                else:
                    if myStr[s] not in escapeStrings:
                        # " " 外的非转义字符怎么办？
                        pass

            return newStr

    def isDictStr(self, myStr='*Sdsa=132easd={231rfs3=P{}}'):
        pass