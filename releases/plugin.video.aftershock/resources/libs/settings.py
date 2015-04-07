import xbmc,xbmcaddon,os
addon_id = 'plugin.video.aftershock'
selfAddon = xbmcaddon.Addon(id=addon_id)
# Examples:
#Commands.append(('Add-on settings','XBMC.RunScript('+xbmc.translatePath('special://home/addons/' + addon_id + '/resources/libs/settings.py')+')'))
# or
#Commands.append(('Add-on settings','XBMC.RunScript('+xbmc.translatePath(afterpath + '/resources/libs/settings.py')+')'))
# or
#Commands.append(('[B][COLOR lime]Aftershock[/COLOR] Settings[/B]','XBMC.RunScript('+xbmc.translatePath(afterpath + '/resources/libs/settings.py')+')'))

def getAddOnID():
    d=addon_id
    return d
    
def getHomeItems():
    d=[]
    for x in range(40): 
        d.append(None);
        itemid = str(x + 1)
        if selfAddon.getSetting("homeitems_" +itemid+ "_enabled")== "true":
            d[x]=int(selfAddon.getSetting("homeitems_" + itemid))
    return d
def getMovie25URL():
    return selfAddon.getSetting("movie25-url")
    
def getSominalURL():
    return selfAddon.getSetting("sominal-url")
def getDesiRulezURL():
    return selfAddon.getSetting("desirulez-url")
def getNoOfMoviesToLoad():
    return int(selfAddon.getSetting("sominal-moviesPerPage"))
    
def getRefreshRequiredSettings():
    s=[]
    s.append(selfAddon.getSetting("meta-view"))
    s.append(selfAddon.getSetting("meta-view-tv"))
    s.append(selfAddon.getSetting("groupfavs"))
    s.append(selfAddon.getSetting("con-view"))
    s.append(selfAddon.getSetting("xpr-view"))
    return s

def openSettings():
    d = getHomeItems()
    s = getRefreshRequiredSettings()
    selfAddon.openSettings()
    dnew = getHomeItems()
    snew = getRefreshRequiredSettings()
    if d != dnew or s != snew:
        ClearDir(os.path.join(xbmc.translatePath(selfAddon.getAddonInfo('profile')),'Temp'))
        xbmc.executebuiltin("XBMC.Container.Refresh")  

def ClearDir(dir):
    if os.path.exists(dir):
        if os.path.isfile(dir): os.remove(dir)
        else:
            for the_file in os.listdir(dir):
                file_path = os.path.join(dir, the_file)
                try:os.unlink(file_path)
                except Exception, e: print str(e)

if  __name__ == "__main__": openSettings()
