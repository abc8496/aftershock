# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2017 Aftershockpy

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

import datetime
import re
import urllib
import urlparse

import BeautifulSoup

from resources.lib import resolvers
from ashock.modules import client
from ashock.modules import logger


class source:
    def __init__(self):
        self.base_link_1 = 'http://www.desiplex.me'
        self.base_link_2 = 'http://www.desiplex.net'
        self.base_link_3 = 'http://www.desiplex.net'

        self.search_link = '/feed/?s=%s&submit=Search'
        self.info_link = '%s/watch/?id=%s'
        self.now = datetime.datetime.now()

        self.srcs = []

    def tvshow(self, tvshowurl, imdb, tvdb, tvshowtitle, year):
        if tvshowurl:
            return tvshowtitle

    def episode(self, url, ep_url, imdb, tvdb, title, date, season, episode):
        if imdb == 'Naamkarann':
            imdb = 'Naamkaran'
        query = '%s %s' % (imdb, title)
        query = self.search_link % (urllib.quote_plus(query))
        ep_url = query
        if ep_url :
            return ep_url

    def sources(self, url):
        try:
            logger.debug('SOURCES URL %s' % url, __name__)
            quality = ''
            srcs = []

            result = ''

            links = [self.base_link_1, self.base_link_2, self.base_link_3]
            for base_link in links:
                try:
                    result = client.request(base_link + '/' + url)
                except: result = ''
                if 'item' in result: break

            result = result.decode('iso-8859-1').encode('utf-8')

            result = result.replace('\n','').replace('\t','')

            items = client.parseDOM(result, 'content:encoded')[0]

            items = re.compile('class=\"single-heading\">(.+?)<span').findall(items)

            for i in range(0, len(items)):
                try :
                    if '720p' in items[i]:
                        quality = 'HD'
                    else:
                        quality = 'SD'

                    urls = client.parseDOM(items[i], "a", ret="href")
                    for j in range(0,len(urls)):
                        videoID = getVideoID(urls[j])
                        result = client.request(urls[j])
                        item = BeautifulSoup.BeautifulSoup(result, parseOnlyThese=BeautifulSoup.SoupStrainer("iframe"))
                        if len(item) == 0:
                            item = re.compile('data-config="(.+?)"').findall(result)[0]
                            item = [{"src":item}]
                        for links in item:
                            rUrl = links["src"]
                            if rUrl.startswith('//'):
                                rUrl='http:%s'%rUrl
                            urls[j] = rUrl
                            host = client.host(urls[0])
                    url = "##".join(urls)
                    srcs.append({'source':host, 'parts': str(len(urls)), 'quality':quality,'provider':'DesiPlex','url':url, 'direct':False})
                    urls = []
                except:
                    pass
            logger.debug('SOURCES [%s]' % srcs, __name__)
            return srcs
        except:
            return srcs

    def resolve(self, url, resolverList):
        try:
            logger.debug('ORIGINAL URL [%s]' % url, __name__)
            tUrl = url.split('##')
            if len(tUrl) > 0:
                url = tUrl
            else :
                url = urlparse.urlparse(url).path

            links = []
            for item in url:
                r = resolvers.request(item, resolverList)
                if not r :
                    raise Exception()
                links.append(r)
                url = links
            logger.debug('RESOLVED URL [%s]' % url, __name__)
            return url
        except:
            return False

def getVideoID(url):
    try :
        return re.compile('(id|url|v|si|sim|data-config)=(.+?)/').findall(url + '/')[0][1]
    except:
        return