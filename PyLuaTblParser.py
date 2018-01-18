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

    def removeEscapeStr(self):
        # this is left to be extended if needed
        escapeStrings = ['\n', '\t', ' ']
        # delete all the possible escape strings
        for escStr in escapeStrings:
            self.luaString = self.luaString.replace(escStr, '')

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
                outputFileHandle.write(str(k) + '=')
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

        leftPartStr = myStr[:symbolPos]
        rightPartStr = myStr[symbolPos + 1:]
        leftPartStr = leftPartStr.strip('[')
        leftPartStr = leftPartStr.strip(']')
        key = self.processString(leftPartStr)
        value = self.processString(rightPartStr)
        return (key, value)

    def processString(self, myStr):

        hasBracelet = (myStr.find('{') != -1)

        if hasBracelet:

            if (myStr.find('{') == 0) and (myStr.rfind('}') == len(myStr) - 1):
                # if string starts with '{' and ends with '}'
                newStr = myStr[1:len(myStr) - 1]

                pairsTuple = self.braceletDict(newStr)
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

                        if symbolPos == -1 :
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
                            if value != None and ( key not in keyList):
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
                # deal with the string like a = {1,2,3}, return a dict data
                pass
        else:
            # deal with single value data, like '1' or 'abc'
            return self.rtnCorrectType(myStr)

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

        return myStr.strip('"')

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