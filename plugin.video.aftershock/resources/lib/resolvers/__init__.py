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


import urlparse, urllib
from resources.lib.resolvers import realdebrid
from resources.lib.resolvers import premiumize
from resources.lib.libraries import client

def request(url, resolverList):

    try :
        u = client.host(url)

        r = [i['class'] for i in info() if u in i['host']][0]
        r = __import__(r, globals(), locals(), [], -1)
        r = r.resolve(url)
        if not r:
            raise Exception()
        h = dict('')
        h['User-Agent'] = client.agent()
        h['Referer'] = url
        r = '%s|%s' % (r.split('|')[0], urllib.urlencode(h))

        return r
    except :
        pass

    u = url
    try:
        url = [(i, i.get_host_and_id(u)) for i in resolverList]
        print '%s %s' % ('1', url)
        url = [i for i in url if not i[1] == False]
        print '%s %s' % ('2', url)
        url = [(i[0], i[0].valid_url(u, i[1][0]), i[1][0], i[1][1]) for i in url]
        print '%s %s' % ('3', url)
        url = [i for i in url if not i[1] == False][0]
        print '%s %s' % ('4', url)
        url = url[0].get_media_url(url[2], url[3])
        print '%s %s' % ('5', url)
        return url
    except:
        return False

def info():
    return [
          {'class':'desiflicks','host':'desiflicks'}
        , {'class':'playwire','host': ['playwire']}
        , {'class': 'vidshare', 'host': ['vidshare','idowatch','watchvideo2', 'tvlogy']}
        , {'class': 'xpressvids', 'host': ['xpressvids']}
        , {'class': 'playu', 'host': ['playu']}
        , {'class': 'apnasave', 'host': 'apnasave' }
    ]