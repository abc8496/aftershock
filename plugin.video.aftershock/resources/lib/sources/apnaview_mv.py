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


import re,urllib,urlparse,datetime, random

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib import resolvers
from resources.lib.libraries import metacache

class source:
    def __init__(self):
        self.base_link = 'http://www.apnaview.com'
        self.search_link = '/browse?q=%s'
        self.now = datetime.datetime.now()
        self.theaters_link = '/browse/%s?year=%s' % ('%s', self.now.year)
        self.added_link = '/browse/%s?'
        self.sort_link = '&order=desc&sort=date'
        self.langMap = {'hindi':'hi', 'tamil':'ta', 'telugu':'te','ml':'malayalam', 'kn':'kannada', 'bn':'bengali', 'mr':'marathi', 'pa':'punjabi'}

    def scn_full_list(self, url, lang=None, provider=None):
        tmpList = []
        self.list = []

        pagesScanned = 0
        try :
            url = getattr(self, url + '_link')
            url = url % lang
        except:pass

        links = [self.base_link, self.base_link, self.base_link]
        for base_link in links:
            try: result = client.source(base_link + url + self.sort_link)
            except:
                result = ''

            if 'row movie-list' in result: break

        result = result.decode('iso-8859-1').encode('utf-8')
        movies = client.parseDOM(result, "div", attrs={"class":"movie"})

        for movie in movies:
            try :
                title = client.parseDOM(movie, "span", attrs={"class":"title"})[0]
                title = client.replaceHTMLCodes(title)
                try : title = title.encode('utf-8')
                except: pass

                year = client.parseDOM(movie, "small")[0]
                year = re.compile('(.+?) watch online').findall(year)[0]
                year = year.encode('utf-8')

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = client.parseDOM(movie, "a", ret="href")[0]
                url = client.replaceHTMLCodes(url)
                try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
                except: pass

                poster = '0'
                try:
                    poster = client.parseDOM(movie, "img", ret="src")[0]
                    poster = '%s%s' % (self.base_link, poster)
                except: pass
                poster = client.replaceHTMLCodes(poster)
                try: poster = urlparse.parse_qs(urlparse.urlparse(poster).query)['u'][0]
                except: pass
                poster = poster.encode('utf-8')

                duration = '0'

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'duration': duration, 'name': name, 'poster': poster, 'banner': '0', 'fanart': '0', 'tvdb':'0'})
            except:
                pass
        try :
            next = client.parseDOM(result, "li", attrs={"class":"next page"})
            url = client.parseDOM(next, "a", ret="href")[0]
            url = re.compile('(.+?)&amp;page=(.+?)').findall(url)[0]
            self.list[0].update({'next':url[0]+'&page='+url[1]})
        except:
            pass

        return self.list

    def get_movie(self, imdb, title, year):
        try:
            self.base_link = self.base_link
            query = '%s' % (title)
            query = self.search_link % (urllib.quote_plus(query))
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)

            result = result.decode('iso-8859-1').encode('utf-8')
            result = client.parseDOM(result, "div", attrs={"class":"movie"})

            title = cleantitle.movie(title)
            for item in result:
                searchTitle = client.parseDOM(item, "span", attrs={"class":"title"})[0]
                searchTitle = cleantitle.movie(searchTitle)
                if title == searchTitle:
                    url = client.parseDOM(item, "a", ret="href")[0]
                    break
            if url == None or url == '':
                raise Exception()
            return url
        except:
            return


    def get_sources(self, url):
        try:
            quality = ''
            sources = []

            if url == None: return sources

            url = '%s%s' % (self.base_link, url)

            try: result = client.source(url)
            except: result = ''

            result = result.decode('iso-8859-1').encode('utf-8')

            result = client.parseDOM(result, "table", attrs={"class":"table table-bordered"})[0]
            result = client.parseDOM(result, "tbody")[0]
            result = client.parseDOM(result, "tr")

            for item in result:
                try :
                    urls = client.parseDOM(item, "td")[1]
                    urls = client.parseDOM(urls, "a", ret="href")
                    for i in range(0, len(urls)):
                        result = client.source(urls[i], mobile=False)
                        result = result.replace('\n','').replace('\t','')
                        if 'Could not connect to mysql! Please check your database' in result:
                            result = client.source(urls[i], mobile=True)
                        try :
                            item = client.parseDOM(result, "div", attrs={"class":"videoplayer"})[0]
                            item = re.compile('(SRC|src|data-config)=\"(.+?)\"').findall(item)[0][1]
                        except :
                            item = re.compile('(SRC|src|data-config)=\'(.+?)\'').findall(item)[0][1]
                            pass
                        urls[i] = item
                    host = client.host(urls[0])
                    if len(urls) > 1:
                        url = "##".join(urls)
                    else:
                        url = urls[0]
                    sources.append({'source': host, 'parts' : str(len(urls)), 'quality': quality, 'provider': 'ApnaView', 'url': url, 'direct':False})
                except :
                    pass
            return sources
        except:
            return sources


    def resolve(self, url, resolverList):
        try:
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
            return url
        except:
            return False