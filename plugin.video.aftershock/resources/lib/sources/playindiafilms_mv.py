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


import re,urllib,urlparse,random, datetime

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import metacache
from resources.lib import resolvers

class source:
    def __init__(self):
        self.base_link_1 = 'http://www.playindiafilms.com'
        self.base_link_2 = self.base_link_1
        self.search_link = '/feed/?s=%s&submit=Search'
        self.info_link = ''
        self.now = datetime.datetime.now()
        self.theaters_link = '/category/%s/feed' % (self.now.year)
        self.added_link = '/category/hindi-movies/feed'
        self.HD_link = '/category/hindi-blurays/feed'
        self.list = []

    def scn_full_list(self, url):
        tmpList = []
        self.list = []

        pagesScanned = 0
        try : url = getattr(self, url + '_link')
        except:pass

        turl = url

        while((len(self.list) < 15) and (pagesScanned < 10)):
            self.scn_list(turl)
            try : url =  re.compile('(.+)\?paged=.+').findall(turl)[0]
            except :
                pass
            try: pageNo =  re.compile('paged=(.+)').findall(turl)[0]
            except:
                pageNo = 1
                pass
            pageNo = int(pageNo) + 1
            turl = url + '?paged=' + str(pageNo)
            pagesScanned = pagesScanned + 1
        self.list[0].update({'next':url + '?paged='+str(pageNo)})
        self.list = metacache.fetchImdb(self.list)
        return self.list

    def scn_list(self, url):
        try :
            links = [self.base_link_1, self.base_link_1, self.base_link_1]
            for base_link in links:
                try: result = client.source(base_link + url)
                except:
                    result = ''

                if 'item' in result: break

            if result == '' :
                return result

            result = result.decode('iso-8859-1').encode('utf-8')
            movies = client.parseDOM(result, "item")
            for movie in movies:
                try:
                    title = client.parseDOM(movie, "title")[0]
                    title = re.compile('(.+?) [(]\d{4}[)]$').findall(title)[0]
                    title = client.replaceHTMLCodes(title)
                    try : title = title.encode('utf-8')
                    except: pass

                    year = client.parseDOM(movie, "title")[0]
                    year = re.compile('.+? [(](\d{4})[)]$').findall(year)[0]
                    year = year.encode('utf-8')

                    name = '%s (%s)' % (title, year)
                    try: name = name.encode('utf-8')
                    except: pass

                    url = client.parseDOM(movie, "link")[0]
                    url = client.replaceHTMLCodes(url)
                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
                    except: pass

                    poster = '0'
                    try: poster = client.parseDOM(movie, "img", ret="src")[0]
                    except: pass
                    poster = client.replaceHTMLCodes(poster)
                    try: poster = urlparse.parse_qs(urlparse.urlparse(poster).query)['u'][0]
                    except: pass
                    poster = poster.encode('utf-8')

                    genre = client.parseDOM(movie, "div", attrs = { "class": "movie_about_genre" })
                    genre = client.parseDOM(genre, "a")
                    genre = " / ".join(genre)
                    if genre == '': genre = '0'
                    genre = client.replaceHTMLCodes(genre)
                    genre = genre.encode('utf-8')

                    hindiMovie = False
                    categories = []
                    try: categories = client.parseDOM(movie, "category")
                    except :
                        hindiMovie = True
                        pass

                    for category in categories:
                        if re.search('Hindi', category, flags= re.I):
                            hindiMovie = True
                    duration = 0 ; rating = 0; votes = 0; director = ''; cast = '' ; plot = ''; tagline = ''; mpaa = ''; next = ''; tvdb = '0'


                    if hindiMovie :
                        self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': '0', 'studio': '0', 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': '0', 'cast': cast, 'plot': plot, 'tagline': tagline, 'name': name, 'tvdb': tvdb, 'tvrage': '0', 'poster': poster, 'banner': '0', 'fanart': '0', 'lang':'en','next': next})

                except:
                    pass

            return self.list

        except:
            pass
        return

    def get_movie(self, imdb, title, year):
        try:
            self.base_link = random.choice([self.base_link_1, self.base_link_2])

            query = '%s %s' % (title, year)
            query = self.search_link % (urllib.quote_plus(query))
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)

            result = result.decode('iso-8859-1').encode('utf-8')
            result = client.parseDOM(result, "item")

            title = cleantitle.movie(title)
            for item in result:
                searchTitle = client.parseDOM(item, "title")[0]
                searchTitle = cleantitle.movie(searchTitle)
                if title == searchTitle:
                    url = client.parseDOM(item, "link")[0]
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
                quality = "CAM"

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



