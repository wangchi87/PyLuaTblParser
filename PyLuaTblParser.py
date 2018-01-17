class PyLuaTblParser:
    '''
    This is a lua table parser
    note that
    1. the 'dict like data' from lua table is stored in dictData and accessible by dumpDict() function
    2. the 'list like data' from lua table is stored in listData and accessible by dumpList() function
    '''

    # string to be parsed
    luaString = ''
    result = []
    # the dict data from Lua table
    dictData = {}
    # the dict data from Lua table
    listData = []

    def __init__(self):
        self.result = []
        self.luaString = ''
        self.dictData = {}
        self.listData = []

    def load(self, myStr):
        if len(myStr) == 0:
            raise Exception('Empty input Lua Table string')
        self.luaString = myStr
        self.parseLuaTbl()

    def dump(self):
        return self.luaString

    def loadLuaTable(self, filePath):
        try:
            luaFile = open(filePath)
        except IOError as e:
            print 'file reading error:', e.strerror, e.errno

        luaStr = luaFile.read()
        # this is left to be extended if needed
        escapeStrings = ['\n', '\t']
        # delete all the possible escape strings
        for escStr in escapeStrings:
            luaStr = luaStr.replace(escStr, '')
        self.luaString = luaStr
        self.parseLuaTbl()

        # load an external dict, and store in class

    def loadDict(self, dict):
        self.dictData = dict

    # export dict data
    def dumpDict(self):
        return self.dictData

    # export dict data
    def dumpList(self):
        return self.listData

    # the following three functions export python data in Lua table form
    def dumpLuaTable(self, filePath):

        try:
            outputFile = open(filePath, 'w')
            outputFile.write('{')

            # write list data
            for x in self.listData:
                outputFile.write(str(x))
                outputFile.write(',')

            self.writeDictData(self.dictData, outputFile)
            outputFile.write('}')
            outputFile.close()
        except:
            raise Exception('errors in exporting data')

    def parseLuaTbl(self):
        self.result = self.processString(self.luaString)
        self.seperateDictAndListData()

    # write dict data recursively
    def writeDictData(self, dictData, outputFileHandle):
        # write dict data
        for k, v in dictData.items():
            outputFileHandle.write(str(k) + '=')
            self.writeDictKeyData(v, outputFileHandle)
            outputFileHandle.write(',')

    # write the key element in dict data
    def writeDictKeyData(self, dictKeyData, outputFileHandle):

        if type(dictKeyData) == type([]):
            outputFileHandle.write('{')
            for y in dictKeyData:
                if type(y) == type({}):
                    self.writeDictData(y, outputFileHandle)
                else:
                    if y != None:
                        outputFileHandle.write(str(y))
                    else:
                        outputFileHandle.write('nil')
                    outputFileHandle.write(',')
            outputFileHandle.write('}')
        else:
            if dictKeyData != None:
                outputFileHandle.write(str(dictKeyData))
            else:
                outputFileHandle.write('nil')

    # as we store the resulting list data and dict data in 'result' list
    # we have to seperate these two type of data into individual structure
    def seperateDictAndListData(self):
        self.listData = [x for x in self.result if type(x) != type({})]

        for x in self.result:
            if type(x) == type({}):
                for k, v in x.items():
                    self.dictData[k] = v

    # find the indexs of all the charLetter in myStr
    def rtnCharLoc(self, myStr, charLetter):
        locations = []
        index = myStr.find(charLetter)
        while index > -1:
            locations.append(index)
            index = myStr.find(charLetter, index + 1)
        return locations

    # find corresponding bracelet pairs in given string
    # e.g. input : {1,2,{3,4}}
    #      output: [(0,10),(5,9)]
    def braceletDict(self, myStr):

        lList = self.rtnCharLoc(myStr, '{')
        rList = self.rtnCharLoc(myStr, '}')

        if len(lList) != len(rList):
            raise Exception('Incorrect input Lua Table')

        # we use a stack to find corresponding bracelet
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

    # judge whether the index is inside of the range of index of each bracelet or not
    # e.g. if index is 2, the braceletPair is (3,4) (5,10) then the index is not inside(return False)
    def isIndexInBracelet(self, index, braceletPair):
        for i in range(0, len(braceletPair)):
            if index in range(braceletPair[i][0], braceletPair[i][1]):
                return True
        return False

    # test if a string represent a float number
    def isFloat(self, myStr):
        try:
            float(myStr)
            return True
        except:
            return False

    # tell whether the string is a number(float or int?) or a Boolean value, or a string
    # return their corresponding types
    def rtnCorrectType(self, myStr):
        stripedStr = myStr.strip().lower()

        # is Boolean type ?
        if stripedStr == 'false':
            return False
        if stripedStr == 'true':
            return True

        if stripedStr == 'nil':
            return None

        # is a int number ?
        if stripedStr.isdigit():
            return int(stripedStr)
        if self.isFloat(stripedStr):
            return float(stripedStr)

        return stripedStr

    # split given string with comma at top level
    # e.g. input : '1,2,{3,4}'
    #      output: {'1','2','{3,4}'}
    def strPartition(self, myStr, braceletPair):

        commaStart = 0
        strStart = 0
        partition = []
        end = myStr.find(',', commaStart)

        while end != -1:
            if not self.isIndexInBracelet(end, braceletPair):
                partition.append(myStr[strStart:end])
                strStart = end + 1

            commaStart = end + 1
            end = myStr.find(',', commaStart)

        if strStart != end:
            partition.append(myStr[strStart:])
        return partition

    # when the given string has '=' symbol, turn it into python dict type
    # e.g. input : 'a={1,2}'
    #      output: {'a' : {1,2}}
    def processDictStr(self, myStr, symbolPos):

        leftPartStr = myStr[:symbolPos].strip()
        rightPartStr = myStr[symbolPos + 1:].strip()
        myDict = {}
        value = self.processString(rightPartStr)
        if value != None:
            myDict[leftPartStr] = value
        return myDict

    # core function of string processing
    def processString(self, myStr):

        res = []
        hasBracelet = (myStr.find('{') != -1)

        if hasBracelet:
            # if string starts with '{' and ends with '}'
            if (myStr.find('{') == 0) and (myStr.rfind('}') == len(myStr) - 1):
                newStr = myStr[1:len(myStr) - 1]
                pairsTuple = self.braceletDict(newStr)
                partition = self.strPartition(newStr, pairsTuple)
                for s in partition:
                    temp = self.processString(s)
                    if temp != '' and temp != {}:
                        res.append(temp)
                return res
            else:
                # if string does not start with '{' and end with '}'
                # in this case, we will probably deal with a dict element

                symbolPos = myStr.find('=')
                # if we find a '=', it means we are dealing with a dict element
                if symbolPos != -1:
                    return self.processDictStr(myStr, symbolPos)
                else:
                    raise Exception('Incorrect input Lua Table')
        else:
            # return the strings which fall into here
            # there are only two types of strings which might end up here
            # 1. single strings, like 'abcdefg', or '123'
            # 2. dict type strings without '{}', like 'abc={123}'

            symbolPos = myStr.find('=')
            # if we find a '=', it means we are dealing with a dict element
            if symbolPos != -1:
                return self.processDictStr(myStr, symbolPos)
            else:
                return self.rtnCorrectType(myStr)