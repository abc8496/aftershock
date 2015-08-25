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
    
def getHomeItems(getSetting):
    d=[]
    for x in range(40): 
        d.append(None);
        itemid = str(x + 1)
        if getSetting("homeitems_" +itemid+ "_enabled")== "true":
            d[x]=int(getSetting("homeitems_" + itemid))
    return d
def openSettings():
    xbmc.executebuiltin('Addon.OpenSettings(%s)' % addon_id)

if  __name__ == "__main__": openSettings()
