## @package xbmcaddon
#  A class to access addon properties.
#
"""
A class to access addon properties
"""

__author__ = 'Team Kodi <http://kodi.tv>'
__credits__ = 'Team Kodi'
__date__ = 'Fri May 01 16:22:07 BST 2015'
__platform__ = 'ALL'
__version__ = '2.20.0'


class Addon(object):
    setting = None
    addonInfo = None
    def __init__(self, id=None):
        """Creates a new Addon class.

        id: string - id of the addon (autodetected in XBMC Eden)

        Example:
            self.Addon = xbmcaddon.Addon(id='script.recentlyadded')
        """
        self.addonInfo = {'profile':'data/plugin.video.genesis/',
                          'path':'data/plugin.video.genesis',
                          'name':'plugin.video.genesis',
                          'icon':'icon',
                          'id' : 'plugin.video.geneis'}

        self.setting = {'appearance':'',
                        'icon':''}
        from xml.dom import minidom
        xmldoc = minidom.parse('../plugin.video.genesis/resources/settings.xml')
        settingList = xmldoc.getElementsByTagName('setting')
        for s in settingList:
            try :
                self.setting[s.attributes['id'].value] = s.attributes['id'].value
            except :
                pass
        #    self.setSetting(s.attributes['id'], s.attributes['id'].value)

        print self.setting
        #    print(s.attributes['id'].value)
        #import xml.etree.ElementTree
        #e = xml.etree.ElementTree.parse('../plugin.video.genesis/resources/settings.xml').getroot()

        pass

    def getLocalizedString(self, id):
        """Returns an addon's localized 'unicode string'.

        id: integer - id# for string you want to localize.

        Example:
            locstr = self.Addon.getLocalizedString(id=6)
        """
        return unicode

    def getSetting(self, id):
        """Returns the value of a setting as a unicode string.

        id: string - id of the setting that the module needs to access.

        Example:
        apikey = self.Addon.getSetting('apikey')
        """
        return unicode(self.setting[id])

    def setSetting(self, id, value):
        """Sets a script setting.

        id: string - id of the setting that the module needs to access.
        value: string or unicode - value of the setting.

        Example:
            self.Settings.setSetting(id='username', value='teamxbmc')
        """
        pass

    def openSettings(self):
        """Opens this scripts settings dialog."""
        pass


    def getAddonInfo(self, id=None):
        """Returns the value of an addon property as a string.

        id: string - id of the property that the module needs to access.

        Note:
            Choices are (author, changelog, description, disclaimer, fanart, icon, id, name, path
            profile, stars, summary, type, version)

        Example:
            version = self.Addon.getAddonInfo('version')
        """
        return self.addonInfo[id]
