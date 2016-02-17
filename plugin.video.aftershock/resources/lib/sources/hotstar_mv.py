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


import re,urllib,urlparse,random, datetime, json

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib import resolvers


class source:
    def __init__(self):
        self.base_link_1 = 'http://%s.hotstar.com'
        self.base_link_2 = self.base_link_1
        self.search_link = '/AVS/besc?action=GetSuggestionsStar&query=%s&type=vod'
        self.info_link = ''
        self.now = datetime.datetime.now()
        self.theaters_link = '/category/%s/feed' % (self.now.year)
        self.added_link = '/category/hindi-movies/feed'
        self.HD_link = '/category/hindi-blurays/feed'
        self.list = []

    def get_movie(self, imdb, title, year):
        try:
            self.base_link = random.choice([self.base_link_1, self.base_link_2])

            query = '%s %s' % (title, year)
            query = self.search_link % (urllib.quote_plus(query))
            query = urlparse.urljoin(self.base_link % 'search', query)

            result = client.source(query)

            result = result.decode('iso-8859-1').encode('utf-8')
            result = json.loads(result)

            result = result['resultObj']['suggestion']

            title = cleantitle.movie(title)
            for item in result:
                searchTitle = cleantitle.movie(item['title'])
                if title == searchTitle:
                    url = item['contentId']
                    break
            if url == None or url == '':
                raise Exception()
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            quality = ''
            sources = []

            if url == None: return sources

            try: result = client.source(url)
            except: result = ''

            result = result.decode('iso-8859-1').encode('utf-8')

            result = result.replace('\n','')

            try :
                quality = client.parseDOM(result, name="title")[0]
                quality = quality.upper()
            except:
                quality = 'CAM'

            if "BLURAY" in quality:
                quality = "HD"
            elif "DVD" in quality:
                quality = "DVD"
            else:
                quality = "SD"

            result = client.parseDOM(result, "p", attrs= {"style":"text-align: center;"})

            try :
                host = ''
                urls = []
                for tag in result:
                    if len(client.parseDOM(tag, "span", attrs= {"class":"btn btn-custom btn-custom-large btn-black "})) > 0:
                        link = client.parseDOM(tag, "strong")
                        if len(urls) > 0 :
                            url = "##".join(urls)
                            sources.append({'source': host, 'parts' : str(len(urls)), 'quality': quality, 'provider': 'PlayIndiaFilms', 'url': url})
                            urls = []
                    else :
                        link = client.parseDOM(tag, "a", attrs= {"class":"btn btn-custom btn-medium btn-red btn-red "}, ret="href")
                        if len(link) > 0 :
                            host = re.compile('\.(.+?)\.').findall(link[0])[0]
                            urls.append(link[0])
                if len(urls) > 0:
                    url = "##".join(urls)
                    sources.append({'source': host, 'parts': str(len(urls)), 'quality': quality, 'provider': 'PlayIndiaFilms', 'url': url})
            except:
                pass
            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            tUrl = url.split('##')
            if len(tUrl) > 0:
                url = tUrl
            else :
                url = urlparse.urlparse(url).path

            links = []
            for item in url:
                links.append(resolvers.request(item))
            url = links
            return url
        except:
            return



