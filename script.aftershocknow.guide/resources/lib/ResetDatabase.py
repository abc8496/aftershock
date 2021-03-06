# -*- coding: utf-8 -*-
# USTVnow Guide
# Developed by mhancoc7
# Forked from FTV Guide:
#
# Copyright (C) 2014 Sean Poyser and Richard Dean (write2dixie@gmail.com)
#
#      Modified for FTV Guide (09/2014 onwards)
#      by Thomas Geppert [bluezed] - bluezed.apps@gmail.com
#
# This Program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This Program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with XBMC; see the file COPYING. If not, write to
# the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# http://www.gnu.org/copyleft/gpl.html
#

import os
import xbmc
import xbmcgui
import xbmcaddon

def deleteDB():
    try:
        xbmc.log("[script.aftershocknow.guide] Deleting database...", xbmc.LOGDEBUG)
        basePath = xbmc.translatePath(xbmcaddon.Addon(id = 'script.aftershocknow.guide').getAddonInfo('profile'))

        for db in ['source.db','cache.db','user.db']:
            dbPath = os.path.join(basePath, db)
            delete_file(dbPath)

        passed = not os.path.exists(os.path.join(basePath, 'source.db'))

        if passed:
            xbmc.log("[script.aftershocknow.guide] Deleting database...PASSED", xbmc.LOGDEBUG)
        else:
            xbmc.log("[script.aftershocknow.guide] Deleting database...FAILED", xbmc.LOGDEBUG)

        return passed

    except Exception, e:
        xbmc.log('[script.aftershocknow.guide] Deleting database...EXCEPTION', xbmc.LOGDEBUG)
        return False

def delete_file(filename):
    tries = 10
    while os.path.exists(filename) and tries > 0:
        try:
            os.remove(filename)
            break
        except:
            tries -= 1

if __name__ == '__main__':
    if deleteDB():
        d = xbmcgui.Dialog()
        d.ok('AftershockNow Guide', 'The database has been successfully deleted.', 'It will be re-created next time you start the guide.')
    else:
        d = xbmcgui.Dialog()
        d.ok('AftershockNow Guide', 'Failed to delete database.', 'Database may be locked,', 'please restart Kodi and try again')

