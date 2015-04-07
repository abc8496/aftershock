import simplejson as json
import fileutil

def createBlankChannelCache(jsonFilePath):
    dummyObj = {'channels':{}}
    writeJson(dummyObj, jsonFilePath)
    
def writeJson(jsonObj, jsonFilePath):
    jsonFile = fileutil.openFile(jsonFilePath, 'w')
    json.dump(jsonObj, jsonFile, encoding='utf-8')
    jsonFile.close()
    
def readJson(jsonFilePath):
    jsonFile = fileutil.openFile(jsonFilePath, 'r')
    jsonObj = json.load(jsonFile, encoding='utf-8')
    jsonFile.close()
    return jsonObj
