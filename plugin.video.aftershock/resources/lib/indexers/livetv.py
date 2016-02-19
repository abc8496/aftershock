# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
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


import sys,json,urllib, base64

from resources.lib.libraries import control
from resources.lib.libraries import client
from resources.lib.libraries import views



class channels:
    def __init__(self):
        self.list = []

        self.live_link = base64.b64decode('aHR0cDovL29mZnNob3JlZ2l0LmNvbS92aW5lZWd1L2FmdGVyc2hvY2stcmVwby9saXZlc3RyZWFtcy5qc29u')


    def get(self):
        try :
            result = client.request(self.live_link)
            channels = json.loads(result)

            channelNames = channels.keys()
            channelNames.sort()

            for channel in channelNames:
                channelObj = channels[channel]
                self.list.append({'name':channel, 'poster':channelObj['iconimage'],'url':channelObj['channelUrl']})

            self.channelDirectory(self.list)
            return self.list
        except :
            client.printException('livetv.get()')
            pass

    def channelDirectory(self, items):
        if items == None or len(items) == 0: return

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart = control.addonFanart()
        sysaddon = sys.argv[0]


        for i in items:
            try:
                label = "%s" % (i['name'])
                sysname = urllib.quote_plus(i['name'])

                poster, banner = i['poster'], i['poster']
                if poster == '0': poster = addonPoster
                if banner == '0' and poster == '0': banner = addonBanner
                elif banner == '0': banner = poster

                url = i['url']

                item = control.item(label=label, iconImage=poster, thumbnailImage=poster)

                try: item.setArt({'poster': poster, 'banner': banner})
                except: pass

                if not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.setProperty('Video', 'true')
                item.addContextMenuItems([], replaceItems=True)
                control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
            except:
                pass

        control.content(int(sys.argv[1]), 'video')
        control.directory(int(sys.argv[1]), cacheToDisc=False)
        views.setView('movies', {'skin.confluence': 500})



