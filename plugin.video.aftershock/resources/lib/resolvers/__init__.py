# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2015 Innovate

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


import re,urllib,urlparse

from resources.lib.libraries import client
from resources.lib.resolvers import realdebrid
from resources.lib.resolvers import premiumize


def request(url):
    try:
        if '</regex>' in url:
            import regex ; url = regex.resolve(url)

        rd = realdebrid.resolve(url)
        if not rd == None: return rd
        pz = premiumize.resolve(url)
        if not pz == None: return pz

        if url.startswith('rtmp'):
            if len(re.compile('\s*timeout=(\d*)').findall(url)) == 0: url += ' timeout=10'
            return url

        # Uncomment after testing
        #import urlresolver
        #r = urlresolver.resolve(url)

        r = False
        if r == False:
            u = urlparse.urlparse(url).netloc
            u = u.replace('www.', '').replace('embed.', '').replace('config.','')
            u = u.lower()

            r = [i['class'] for i in info() if u in i['netloc']][0]
            r = __import__(r, globals(), locals(), [], -1)
            r = r.resolve(url)

        if r == None: return r
        elif type(r) == list: return r
        elif not r.startswith('http'): return r

        try: h = dict(urlparse.parse_qsl(r.rsplit('|', 1)[1]))
        except: h = dict('')

        if not 'User-Agent' in h: h['User-Agent'] = client.agent()
        if not 'Referer' in h: h['Referer'] = url

        r = '%s|%s' % (r.split('|')[0], urllib.urlencode(h))
        return r
    except:
        import traceback
        traceback.print_exc()
        return url


def info():
    return [
    { 'class': 'playindiafilms',
        'netloc': ['mediaplaybox', 'desiflicks'],
        'host': ['mediaplaybox', 'desiflicks'],
        'quality': 'High',
        'captcha': False,
        'a/c': False
    },{ 'class': 'mediaplaybox',
        'netloc': ['mediaplaybox.com'],
        'host': ['mediaplaybox'],
        'quality': 'High',
        'captcha': False,
        'a/c': False
    },{ 'class': 'desiflicks',
        'netloc': ['desiflicks.com', 'media.desiflicks.com'],
        'host': ['desiflicks'],
        'quality': 'High',
        'captcha': False,
        'a/c': False
    },{ 'class': 'tellycolors',
        'netloc': ['tellycolors.me', 'bestarticles.me', 'desimania.net'],
        'host': ['tellycolors.me','bestarticles.me'],
        'quality': 'High',
        'captcha': False,
        'a/c': False
    },{ 'class': 'playwire',
        'netloc': ['playwire.com'],
        'host': ['playwire'],
        'quality': 'High',
        'captcha': False,
        'a/c': False
    }, { 'class': 'vidshare',
         'netloc': ['vidshare.us', 'idowatch.net', 'watchvideo2.us'],
         'host': ['vidshare.us'],
         'quality': 'High',
         'captcha': False,
         'a/c': False
    }, { 'class': 'dailymotion',
         'netloc': ['dailymotion.com'],
         'host': ['dailymotion.com'],
         'quality': 'High',
         'captcha': False,
         'a/c': False
    }, { 'class': 'playu',
         'netloc': ['xpressvids.info'],
         'host': ['xpressvids.info'],
         'quality': 'High',
         'captcha': False,
         'a/c': False
    }]


