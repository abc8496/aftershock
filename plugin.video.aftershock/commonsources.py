import urllib,urllib2,urlparse,re,os,sys,datetime,base64,xbmcaddon

try:
    import CommonFunctions as common
except:
    import commonfunctionsdummy as common
try:
    import json
except:
    import simplejson as json


class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, headers=None, mobile=False, referer=None, cookie=None, output='', timeout='10'):
        handlers = []
        if not proxy == None:
            handlers += [urllib2.ProxyHandler({'http':'%s' % (proxy)}), urllib2.HTTPHandler]
            opener = urllib2.build_opener(*handlers)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookies = cookielib.LWPCookieJar()
            handlers += [urllib2.HTTPHandler(), urllib2.HTTPSHandler(), urllib2.HTTPCookieProcessor(cookies)]
            opener = urllib2.build_opener(*handlers)
            opener = urllib2.install_opener(opener)
        try:
            if sys.version_info < (2, 7, 9): raise Exception()
            import ssl; ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            handlers += [urllib2.HTTPSHandler(context=ssl_context)]
            opener = urllib2.build_opener(*handlers)
            opener = urllib2.install_opener(opener)
        except:
            pass
        try: headers.update(headers)
        except: headers = {}
        if 'User-Agent' in headers:
            pass
        elif not mobile == True:
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0'
        else:
            headers['User-Agent'] = 'Apple-iPhone/701.341'
        if 'referer' in headers:
            pass
        elif referer == None:
            headers['referer'] = url
        else:
            headers['referer'] = referer
        if not 'Accept-Language' in headers:
            headers['Accept-Language'] = 'en-US'
        if 'cookie' in headers:
            pass
        elif not cookie == None:
            headers['cookie'] = cookie
        request = urllib2.Request(url, data=post, headers=headers)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = []
            for c in cookies: result.append('%s=%s' % (c.name, c.value))
            result = "; ".join(result)
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result

class uniqueList(object):
    def __init__(self, list):
        uniqueSet = set()
        uniqueList = []
        for n in list:
            if n not in uniqueSet:
                uniqueSet.add(n)
                uniqueList.append(n)
        self.list = uniqueList

class cleantitle:
    def movie(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
        return title

    def tv(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU|\d{4})(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
        return title

class wso:
    def __init__(self):
        self.base_link = 'http://watchmovies-online.ch'
        self.tvbase_link = 'http://watchseries-online.ch'
        self.search_link = '/?s=%s'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "class": "Post-body" })

            title = cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href"), common.parseDOM(i, "a")) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i for i in result if title == cleantitle().movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict, quality=None):
        try:
            sources = []

            content = re.compile('/\d{4}/\d{2}/').findall(url)
            if len(content) > 0: url = self.tvbase_link + url 
            else: url = self.base_link + url

            result = getUrl(url).result
            links = common.parseDOM(result, "td", attrs = { "class": "even tdhost" })
            links += common.parseDOM(result, "td", attrs = { "class": "odd tdhost" })

            q = re.compile('<label>Quality</label>(.+?)<').findall(result)
            if len(q) > 0: q = q[0]
            else: q = ''

            if q.endswith(('CAM', 'TS')): quality = 'CAM'
            else: quality = 'SD'

            for i in links:
                try:
                    host = common.parseDOM(i, "a")[0]
                    host = host.split('<', 1)[0]
                    host = host.rsplit('.', 1)[0].split('.', 1)[-1]
                    host = host.strip().lower()
                    #if not host in hostDict: raise Exception()
                    host = common.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'provider': 'WSO', 'url': url})
                except:
                    import traceback
                    traceback.print_exc()
                    pass
            return sources
        except:
            import traceback
            traceback.print_exc()
            return sources

    def resolve(self, url):
        try:
            result = getUrl(url).result

            try: url = common.parseDOM(result, "a", ret="href", attrs = { "class": "wsoButton" })[0]
            except: pass

            import commonresolvers
            url = commonresolvers.get(url).result
            return url
        except:
            return
            
class yify:
    def __init__(self):
        self.base_link = 'http://yify.tv'
        self.search_link = '/wp-admin/admin-ajax.php'
        self.pk_link = '/player/pk/pk/plugins/player_p2.php'

    def get_movie(self, imdb, title, year):
        try:
            query = self.base_link + self.search_link
            post = urllib.urlencode({'action': 'ajaxy_sf', 'sf_value': title})

            result = getUrl(query, post=post).result
            result = result.replace('&#8211;','-').replace('&#8217;','\'')
            result = json.loads(result)
            result = result['post']['all']

            title = cleantitle().movie(title)
            result = [i['post_link'] for i in result if title == cleantitle().movie(i['post_title'])][0]

            check = getUrl(result).result
            if not str('tt' + imdb) in check: raise Exception()

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict, quality=None):
        try:
            sources = []

            base = self.base_link + url
            result = getUrl(base).result
            result = common.parseDOM(result, "script", attrs = { "type": "text/javascript" })
            result = ''.join(result)

            links = re.compile('pic=([^&]+)').findall(result)
            links = uniqueList(links).list

            import commonresolvers

            for i in links:
                try:
                    url = self.base_link + self.pk_link
                    post = urllib.urlencode({'url': i, 'fv': '16'})
                    result = getUrl(url, post=post).result
                    result = json.loads(result)

                    try: sources.append({'source': 'GVideo', 'quality': '1080p', 'provider': 'YIFY', 'url': [i['url'] for i in result if i['width'] == 1920 and 'google' in i['url']][0]})
                    except: pass
                    try: sources.append({'source': 'GVideo', 'quality': 'HD', 'provider': 'YIFY', 'url': [i['url'] for i in result if i['width'] == 1280 and 'google' in i['url']][0]})
                    except: pass

                    try: sources.append({'source': 'YIFY', 'quality': '1080p', 'provider': 'YIFY', 'url': [i['url'] for i in result if i['width'] == 1920 and not 'google' in i['url']][0]})
                    except: pass
                    try: sources.append({'source': 'YIFY', 'quality': 'HD', 'provider': 'YIFY', 'url': [i['url'] for i in result if i['width'] == 1280 and not 'google' in i['url']][0]})
                    except: pass
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            if url.startswith('stack://'): return url

            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return
            
class vkbox:
    def __init__(self):
        self.base_link = 'http://mobapps.cc'
        self.data_link = '/data/data_en.zip'
        self.moviedata_link = 'movies_lite.json'
        self.tvdata_link = 'tv_lite.json'
        self.movie_link = '/api/serials/get_movie_data/?id=%s'
        self.show_link = '/api/serials/es?id=%s'
        self.episode_link = '/api/serials/e/?h=%s&u=%01d&y=%01d'
        self.vk_link = 'http://vk.com/video_ext.php?oid=%s&id=%s&hash=%s'

    def get_movie(self, imdb, title, year):
        try:
            import zipfile, StringIO
            query = self.base_link + self.data_link
            data = urllib2.urlopen(query, timeout=5).read()
            zip = zipfile.ZipFile(StringIO.StringIO(data))
            result = zip.read(self.moviedata_link)
            zip.close()

            imdb = 'tt' + imdb
            result = json.loads(result)
            result = [i['id'] for i in result if imdb == i['imdb_id']][0]

            url = self.movie_link % result
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict, quality=None):
        try:
            sources = []

            url = self.base_link + url
            headers = {'User-Agent': 'android-async-http/1.4.1 (http://loopj.com/android-async-http)'}

            par = urlparse.parse_qs(urlparse.urlparse(url).query)
            try: num = int(par['h'][0]) + int(par['u'][0]) + int(par['y'][0])
            except: num = int(par['id'][0]) + 537

            result = getUrl(url, headers=headers).result
            result = json.loads(result)
            try: result = result['langs']
            except: pass
            i = [i for i in result if i['lang'] == 'en'][0]

            url = (str(int(i['apple']) + num), str(int(i['google']) + num), i['microsoft'])
            url = self.vk_link % url

            from commonresolvers import vk
            url = vk().resolve(url)

            for i in url: sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'VKBox', 'url': i['url']})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

class movie25:
    def __init__(self):
        self.base_link = 'http://www.movie25.ag'
        self.link_1 = 'http://www.movie25.ag'
        self.link_2 = 'http://translate.googleusercontent.com/translate_c?anno=2&hl=en&sl=mt&tl=en&u=http://www.movie25.ag'
        self.link_3 = 'https://movie25.unblocked.pw'
        self.search_link = '/search.php?key=%s'

    def get_movie(self, imdb, title, year):
        try:
            
            query = self.search_link % urllib.quote_plus(title)

            result = ''
            url = ''
            links = [self.link_1, self.link_2, self.link_3]
            for base_link in links:
                try: result = getUrl(base_link + query).result
                except: result = ''
                if 'movie_table' in result: break

            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "movie_table" })

            title = cleantitle().movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(common.parseDOM(i, "a", ret="href")[0], common.parseDOM(i, "a", ret="title")[1]) for i in result]
            result = [i for i in result if any(x in i[1] for x in years)]

            result = [(common.replaceHTMLCodes(i[0]), i[1]) for i in result]
            try: result = [(urlparse.parse_qs(urlparse.urlparse(i[0]).query)['u'][0], i[1]) for i in result]
            except: pass
            result = [(urlparse.urlparse(i[0]).path, i[1]) for i in result]

            match = [i[0] for i in result if title == cleantitle().movie(i[1])]

            match2 = [i[0] for i in result]
            match2 = uniqueList(match2).list
            if match2 == []: return

            for i in match2[:10]:
                try:
                    if len(match) > 0:
                        url = match[0]
                        break
                    result = getUrl(base_link + i).result
                    if str('tt' + imdb) in result:
                        url = i
                        break
                except:
                    pass
            if not url == '':
                url = url.encode('utf-8')
            return url
        except:
            #import traceback
            #traceback.print_exc()    
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict, quality=None):
        try:
            sources = []

            result = ''
            links = [self.link_1, self.link_2, self.link_3]
            for base_link in links:
                try: result = getUrl(base_link + url).result
                except: result = ''
                if 'link_name' in result: break

            result = result.decode('iso-8859-1').encode('utf-8')
            result = result.replace('\n','')

            quality = re.compile('>Links - Quality(.+?)<').findall(result)[0]
            quality = quality.strip()
            
            links = common.parseDOM(result, "div", attrs = { "id": "links" })[0]
            tLinks = common.parseDOM(links, "ul")
            tLinks = common.parseDOM(links, "ul", attrs = {"class": "hidden"})
            
            links = tLinks
            
            for i in links:
                try:
                    host = common.parseDOM(i, "li", attrs = { "id": "link_name" })[-1]
                    try: host = common.parseDOM(host, "span", attrs = { "class": "google-src-text" })[0]
                    except: pass
                    host = host.strip().lower()
                    host = common.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = common.replaceHTMLCodes(url)
                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
                    except: pass
                    if not url.startswith('http'): url = urlparse.urljoin(self.base_link, url)
                    url = url.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'provider': 'Movie25', 'url': url})
                except:
                    pass
            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            url = urlparse.urlparse(url).path

            result = ''
            links = [self.link_1, self.link_2, self.link_3]
            for base_link in links:
                try: result = getUrl(base_link + url).result
                except: result = ''
                if 'showvideo' in result: break

            result = result.decode('iso-8859-1').encode('utf-8')

            url = common.parseDOM(result, "div", attrs = { "id": "showvideo" })[0]
            url = url.replace('<IFRAME', '<iframe').replace(' SRC=', ' src=')
            url = common.parseDOM(url, "iframe", ret="src")[0]
            url = common.replaceHTMLCodes(url)
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
            except: pass
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['url'][0]
            except: pass

            import commonresolvers
            if url.startswith('external.php'):
                url = url.replace('external.php?url=','')
                url = base64.b64decode(url)
            url = commonresolvers.get(url).result
            return url
        except:
            import traceback
            traceback.print_exc()    
            return

class playindiafilms:
    def __init__(self):
        self.base_link = 'http://www.playindiafilms.com'
        self.link_1 = 'http://www.playindiafilms.com'
        self.link_2 = 'http://www.playindiafilms.com'
        self.link_3 = 'http://www.playindiafilms.com'
        self.search_link = '/feed/?s=%s&submit=Search'

    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % urllib.quote_plus(title)

            result = ''
            url = ''
            quality = 'CAM'
            links = [self.link_1, self.link_2, self.link_3]
            for base_link in links:
                try: result = getUrl(base_link + query).result
                except: result = ''
                if 'item' in result: break

            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "item")
            
            title = cleantitle().movie(title)
            for item in result:
                searchTitle = common.parseDOM(item, "title")[0]
                searchTitle = cleantitle().movie(searchTitle)
                if title == searchTitle:
                    url = common.parseDOM(item, "link")[0]
                    categories = common.parseDOM(item, "category")
                    for category in categories :
                        if 'dvd' in category.lower():
                            quality = 'DVD'
                            break
                        elif 'bluray' in category.lower():
                            quality = 'HD'
                            break
                        else :
                            quality = 'CAM'
                    break
            
            url = {'url' : url, 'quality' : quality}
            return url
        except:
            import traceback
            traceback.print_exc()    
            return
            
    def get_sources(self, url, hosthdDict, hostDict, locDict, quality=None):
        try:
            if quality is None:
                quality = ''
            sources = []

            result = ''
            try: result = getUrl(url).result
            except: result = ''
            
            result = result.decode('iso-8859-1').encode('utf-8')
            
            result = result.replace('\n','')
            
            result = common.parseDOM(result, "p", attrs= {"style":"text-align: center;"})
            
            try :
                host = ''
                urls = []
                for tag in result:
                    if len(common.parseDOM(tag, "span", attrs= {"class":"btn btn-custom btn-custom-large btn-black "})) > 0:
                        link = common.parseDOM(tag, "strong")
                        if len(urls) > 0 :
                            sources.append({'source': host + ' | Parts [' + str(len(urls)) + ']', 'quality': quality, 'provider': 'PlayIndiaFilms', 'url': urls})
                            urls = []
                    else :
                        link = common.parseDOM(tag, "a", attrs= {"class":"btn btn-custom btn-medium btn-red btn-red "}, ret="href")
                        if len(link) > 0 :
                            host = re.compile('\.(.+?)\.').findall(link[0])[0]
                            urls.append(link[0])
                if len(urls) > 0:
                    sources.append({'source': host + ' | Parts [' + str(len(urls)) + ']', 'quality': quality, 'provider': 'PlayIndiaFilms', 'url': urls})
            except:
                import traceback
                traceback.print_exc()    
                pass
            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            tUrl = url.split(',')
            if len(tUrl) > 0:
                url = tUrl
            else :
                url = urlparse.urlparse(url).path
            
            import commonresolvers
            links = []
            for item in url:
                vidLink = commonresolvers.get(item).result
                links.append(vidLink)
            url = links
            return url
        except:
            import traceback
            traceback.print_exc()    
            return
            
class desirulez:
    def __init__(self):
        self.base_link = 'http://www.desirulez.net'
        self.link_1 = 'http://www.desirulez.me'
        self.link_2 = 'http://www.desirulez.net'
        self.link_3 = 'http://www.desirulez.net'
        self.search_link = '/feed/?s=%s&submit=Search'

    def get_shows(self, name, url):
        try:
            result = ''
            shows = []
            links = [self.link_1, self.link_2, self.link_3]
            for base_link in links:
                try: result = getUrl(base_link + '/' + url).result
                except: result = ''
                if 'forumtitle' in result: break
            
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "h2", attrs = {"class" : "forumtitle"})
            
            for item in result:
                title = ''
                url = ''
                title = common.parseDOM(item, "a", attrs = {"class":"title threadtitle_unread"})
                
                if not title:
                    title = common.parseDOM(item, "a", attrs = {"class":"title"})
                    if title:
                        title = title[0]
                    else :
                        title = common.parseDOM(item, "a")
                
                if type(title) is list and len(title) > 0:
                    title = str(title[0])
                url = common.parseDOM(item, "a", ret="href")
                
                if not url:
                    url = common.parseDOM(item, "a", attrs = {"class":"title"}, ret="href")
                    
                if type(url) is list and len(url) > 0:
                    url = str(url[0])
                
                shows.append({'channel':name, 'title':title, 'url':url, 'year': '0', 'imdb': '0', 'tvdb': '0', 'genre': '0', 'poster': '0', 'banner': '0', 'fanart': '0', 'studio': '0', 'premiered': '0', 'duration': '0', 'rating': '0', 'mpaa': '0', 'plot': '0', 'next': '0', 'provider':'desirulez'})
        
            return shows
        except:
            import traceback
            traceback.print_exc()    
            return
    def get_show(self, name, url):
        return 
    def get_episodes(self, show, url):
        try :
            episodes = []
            links = [self.link_1, self.link_2, self.link_3]
            for base_link in links:
                try:
                    result = getUrl(base_link + '/' + url).result
                except: result = ''
                if 'threadtitle' in result: break
            
            
            rawResult = result.decode('iso-8859-1').encode('utf-8')
            
            result = common.parseDOM(rawResult, "h3", attrs = {"class" : "title threadtitle_unread"})
            result += common.parseDOM(rawResult, "h3", attrs = {"class" : "threadtitle"})
            
            for item in result:
                name = common.parseDOM(item, "a", attrs = {"class":"title"})
                name += common.parseDOM(item, "a", attrs = {"class":"title threadtitle_unread"})
                if type(name) is list:
                    name = name[0]
                url = common.parseDOM(item, "a", ret="href")
                if type(url) is list: 
                    url = url[0]
                if "Online" not in name: continue    
                name = name.replace(show, '').replace('Online','').replace('Watch','').replace('Video','')
                name = name.strip()
                episodes.append({'show':show, 'title':name, 'url' : url, 'provider':'desirulez'})
            return episodes
        except:
            import traceback
            traceback.print_exc()    
            return    
    def get_sources(self, url, hosthdDict, hostDict, locDict, quality=None):
        try:
            if quality is None:
                quality = ''
            sources = []

            result = ''
            links = [self.link_1, self.link_2, self.link_3]
            for base_link in links:
                try: result = getUrl(base_link + '/' + url).result
                except: result = ''
                if 'blockquote' in result: break
            
            result = result.decode('iso-8859-1').encode('utf-8')
            result = result.replace('\n','')
            
            ### DIRTY Implementation
            import BeautifulSoup
            soup = BeautifulSoup.BeautifulSoup(result).findAll('blockquote', {'class':re.compile(r'\bpostcontent\b')})[0]
            
            
            for e in soup.findAll('br'):
                e.extract()
            if soup.has_key('div'):
                soup = soup.findChild('div', recursive=False)
            urls = []
            for child in soup.findChildren():
                if (child.getText() == '') or ((child.name == 'font' or child.name == 'a') and re.search('DesiRulez', str(child.getText()),re.IGNORECASE)):
                    continue
                elif (child.name == 'font') and re.search('Links|Online',str(child.getText()),re.IGNORECASE):
                    if len(urls) > 0:
                        tmpHost = host.lower()
                        indx = host.find('[')
                        if indx > 0 :
                            tmpHost = tmpHost[:indx-1]
                        sources.append({'source':host+ ' | Parts [' + str(len(urls)) + ']', 'quality':quality,'provider':'DesiRulez','url':urls})
                        urls = []
                    host = child.getText()
                    host = host.replace('Online','').replace('Links','').replace('Quality','').replace('Watch','').replace('-','').replace('Download','').replace('  ','').replace('720p HD',' [COLOR red][HD][/COLOR]').replace('DVD',' [COLOR blue][DVD][/COLOR]').strip()
                elif (child.name =='a') and not child.getText() == 'registration':
                    urls.append(str(child['href']) + '###' + host)
            return sources
        except:
            import traceback
            traceback.print_exc()    
            return

    def resolve(self, url):
        try:
            tUrl = url.split(',')
            if len(tUrl) > 0:
                url = tUrl
            else :
                url = urlparse.urlparse(url).path
            
            import commonresolvers
            links = []
            for item in url:
                vidLink = commonresolvers.get(item).result
                links.append(vidLink)
            url = links
            return url
        except:
            import traceback
            traceback.print_exc()    
            return
            
class einthusan:
    def __init__(self):
        self.base_link = 'http://www.einthusan.com'
        self.search_link = '/search/?search_query=%s&lang=%s'


    def get_movie(self, imdb, title, year):
        try:
            search = 'http://www.omdbapi.com/?i=tt%s' % imdb
            search = client.source(search)
            search = json.loads(search)
            country = [i.strip() for i in search['Country'].split(',')]
            if not 'India' in country: return

            languages = ['hindi']
            language = [i.strip().lower() for i in search['Language'].split(',')]
            language = [i for i in language if any(x == i for x in languages)][0]

            query = self.search_link % (urllib.quote_plus(title), language)
            query = urlparse.urljoin(self.base_link, query)

            result = client.source(query)
            result = client.parseDOM(result, "div", attrs = { "class": "search-category" })
            result = [i for i in result if 'Movies' in client.parseDOM(i, "p")[0]][0]
            result = client.parseDOM(result, "li")

            title = cleantitle.movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(client.parseDOM(i, "a", ret="href")[0], client.parseDOM(i, "a")[0]) for i in result]
            r = [i for i in result if any(x in i[1] for x in years)]
            if not len(r) == 0: result = r
            result = [i[0] for i in result if title == cleantitle.movie(i[1])][0]

            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = url.replace('../', '/')
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict, quality=None):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)
            sources.append({'source': 'Einthusan', 'quality': 'HD', 'provider': 'Einthusan', 'url': url})
            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            result = client.request(url)
            url = re.compile("'file': '(.+?)'").findall(result)[0]
            return url
        except:
            return