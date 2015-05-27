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

            url = url.encode('utf-8')
            return url
        except:
            import traceback
            traceback.print_exc()    
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict):
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
            links = common.parseDOM(links, "ul")

            for i in links:
                try:
                    host = common.parseDOM(i, "li", attrs = { "id": "link_name" })[-1]
                    try: host = common.parseDOM(host, "span", attrs = { "class": "google-src-text" })[0]
                    except: pass
                    host = host.strip().lower()
                    #if not host in hostDict: raise Exception() ## UNCOMMENT TO ENABLE SUPPORTED HOSTS ONLY
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
            url = commonresolvers.get(url).result
            return url
        except:
            return
