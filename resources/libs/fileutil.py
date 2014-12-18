import re,os, time

def lastModifiedTime(filePath):
    return os.path.getmtime(filePath)
    
def openFile(filePath, mode):
    if mode == 'r':
        if not os.path.exists(filePath):
            raise Exception("File Doesn't Exist")
        return open(filePath, mode)
    else :
        return open(filePath, mode)

def makeDir(dataPath, dirName):
    dirPath = os.path.join(dataPath, dirName)
    try : os.makedirs(dirPath)
    except : pass
    
def getPath(dataPath,dirName):
    return os.path.join(dataPath, dirName)
    
def createDefaultDataDir(dataPath):
    makeDir(dataPath,'Cache')
    makeDir(dataPath, 'Cookies')
    makeDir(dataPath, 'Temp')