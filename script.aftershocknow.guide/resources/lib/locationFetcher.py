# -*- coding: utf-8 -*-
#
# This Program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import os, json
import logger
from fileFetcher import *

class LocationFetcher(object):

    aftershock_type = xbmcaddon.Addon('plugin.video.aftershock')
    basePath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.aftershocknow.guide'))

    def __init__(self, userEmail, addon):
        self.userEmail = userEmail
        self.addon = addon

    def fetchLocation(self):
        guidePath = False
        users = 'users.json'
        #fetcher = FileFetcher(users, self.addon)
        #retVal = fetcher.fetchFile(remoteUpdate=True)
        usersPath = os.path.join(self.basePath, users)

        try :
            logger.log(usersPath, __name__, level=xbmc.LOGNOTICE)
            filename = open(usersPath)
            result = filename.read()
            filename.close()
            users = json.loads(result)
            logger.log(users, __name__, level=xbmc.LOGNOTICE)
            valid = users[self.userEmail]
            guidePath = 'https://raw.githubusercontent.com/aftershockpy/aftershock-repo/master/releases/script.aftershocknow.guide/guides/'
        except:
            import traceback
            traceback.print_exc()
            guidePath = False
        return guidePath
