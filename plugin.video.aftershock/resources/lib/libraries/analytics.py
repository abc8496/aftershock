# -*- coding: utf-8 -*-

'''
    Copyright (C) 2015 IDev

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import xbmc, uuid, base64, json

from resources.lib.libraries import control
from resources.lib.libraries import client

def sendAnalytics(screenName):
    try :
        if not (control.setting('analytics.enabled') == 'true' or 'Installed' in screenName):
            raise Exception()
        try:
            guid = control.setting("guid")
            if guid == None or guid == '':
                raise Exception()
        except:
            guid = uuid.uuid4()
            control.setSetting(id="guid", value="%s" % guid)
        url = base64.urlsafe_b64decode("aHR0cDovL3d3dy5nb29nbGUtYW5hbHl0aWNzLmNvbS9jb2xsZWN0")
        version = control.addonInfo('version')
        post = base64.urlsafe_b64decode("eyJ2IjoiMSIsInQiOiJzY3JlZW52aWV3IiwidGlkIjoiVUEtNzQ2Mzg0NjQtMSIsImFuIjoiQWZ0ZXJzaG9jay1Lb2RpIiwiYXYiOiIlcyIsImNpZCI6IiVzIiwiY2QiOiIlcyJ9") % (version, guid, screenName)
        post = json.loads(post)
        client.request(url, post=post)
        return '1'
    except:
        return '1'
        pass