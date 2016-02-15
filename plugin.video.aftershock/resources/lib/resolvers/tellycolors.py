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

import re
from resources.lib.libraries import client
from resources.lib import resolvers

def resolve(url):
    try:
        rUrl = None
        result = client.source(url)
        try :
            item = client.parseDOM(result, name="div", attrs={"style":"float:right;margin-bottom:10px"})[0]
            rUrl = re.compile('(SRC|src|data-config)=\"(.+?)\"').findall(item)[0][1]
        except:
            pass

        try :
            videoId = re.compile('(id)=(.+?)/').findall(url + '/')[0][1]
            if 'idowatch' in url :
                rUrl = 'http://idowatch.net/embed-%s-520x400.html' % (videoId)
            elif 'watchvideo' in url:
                rUrl = 'http://watchvideo2.us/embed-%s-520x400.html' % (videoId)
        except: pass

        return resolvers.request(rUrl)
    except:
        client.printException('tellycolors.resolve(url=%s)' % url)
        return