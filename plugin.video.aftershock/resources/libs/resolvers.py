# -*- coding: cp1252 -*-
import urllib,urllib2,re,cookielib,string,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from t0mm0.common.net import Net as net
import urlresolver
import CommonFunctions as common
import traceback
import sys

from resources.libs import settings, main 
addon_id = settings.getAddOnID()
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
elogo = xbmc.translatePath('special://home/addons/'+addon_id+'/resources/art/bigx.png')

class ResolverError(Exception):
    def __init__(self, value, value2):
        value = value
        value2 = value2
    def __str__(self):
        return repr(value,value2)

def jsunpack(script):
    def __itoa(num, radix):
        result = ""
        while num > 0:
            result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
            num /= radix
        return result

    def __unpack(p, a, c, k, e, d):
        while (c > 1):
            c = c -1
            if (k[c]):
                p = re.sub('\\b' + str(__itoa(c, a)) +'\\b', k[c], p)
        return p

    aSplit = script.split(";',")
    p = str(aSplit[0])
    aSplit = aSplit[1].split(",")
    a = int(aSplit[0])
    c = int(aSplit[1])
    k = aSplit[2].split(".")[0].replace("'", '').split('|')
    e = ''
    d = ''
    sUnpacked = str(__unpack(p, a, c, k, e, d))
    return sUnpacked.replace('\\', '')

def resolve_url(url, filename = False):
    stream_url = False
    
    if(url):
        try:
            url = url.split('"')[0]
            match = re.search('xoxv(.+?)xoxe(.+?)xoxc',url)
            print "host "+url
            if(match):
                source = urlresolver.HostedMediaFile(host=match.group(1), media_id=match.group(2))
                if source:
                    stream_url = source.resolve()
            elif re.search('180upload',url,re.I): #fixed
                stream_url=resolve_180upload(url)
            elif re.search('hugefiles',url,re.I):
                stream_url=resolve_hugefiles(url)
            elif re.search('veehd',url,re.I):
                stream_url=resolve_veehd(url)
            elif re.search('epicshare',url,re.I):
                stream_url=resolve_epicshare(url)
            elif re.search('lemuploads',url,re.I):
                stream_url=resolve_lemupload(url)
            elif re.search('mightyupload',url,re.I):
                stream_url=resolve_mightyupload(url)               
            elif re.search('megarelease',url,re.I):
                stream_url=resolve_megarelease(url)
            elif re.search('movreel',url,re.I):
                stream_url=resolve_movreel(url)
            elif re.search('bayfiles',url,re.I):
                stream_url=resolve_bayfiles(url)
            elif re.search('nowvideo',url,re.I):
                stream_url=resolve_nowvideo(url)
            elif re.search('novamov',url,re.I):
                stream_url=resolve_novamov(url)
            elif re.search('vidspot',url,re.I):
                stream_url=resolve_vidspot(url)
            elif re.search('videomega',url,re.I):
                stream_url=resolve_videomega(url)
            elif re.search('youwatch',url,re.I):
                stream_url=resolve_youwatch(url)
            elif re.search('vk.com',url,re.I):
                stream_url=resolve_VK(url)
            elif re.search('(?i)(firedrive|putlocker)',url):
                stream_url=resolve_firedrive(url)               
            elif re.search('project-free-upload',url,re.I):
                stream_url=resolve_projectfreeupload(url)
            elif re.search('yify.tv',url,re.I):
                stream_url=resolve_yify(url)
            elif re.search('mail.ru',url,re.I):
                stream_url=resolve_mailru(url)
            elif re.search('g2g.fm',url,re.I):
                stream_url=resolve_g2g(url)
            elif re.search('docs.google',url,re.I):
                stream_url=resolve_googleDocs(url)
            elif re.search('mrfile',url,re.I):
                stream_url=resolve_mrfile(url)
            elif re.search('sockshare',url,re.I):
                stream_url=resolve_sockshare(url)
            elif re.search('picasaweb.google',url,re.I):
                stream_url=resolve_picasaWeb(url)
            elif re.search('youtube',url,re.I):
                try:url=url.split('watch?v=')[1]
                except:
                    try:url=url.split('com/v/')[1]
                    except:url=url.split('com/embed/')[1]
                stream_url='plugin://plugin.video.youtube/?action=play_video&videoid=' +url
            elif re.search('dailymotion', filename, flags=re.I):
                stream_url=resolve_dailymotion(url)
            elif re.search('letwatch', filename, flags=re.I):
                stream_url=resolve_letwatch(url)
            elif re.search('flash', filename, flags=re.I):
                stream_url=resolve_playwire(url)
            elif re.search('videohut',filename,flags=re.I):
                stream_url=resolve_videohut(url)
            elif re.search('vidto.php',url,flags=re.I):
                stream_url=resolve_vidtophp(url)
            elif re.search('tanker',filename,flags=re.I):
                stream_url=resolve_videotanker(url)
            elif re.search('cloud|cl.php',url,flags=re.I):
                stream_url=resolve_cloud(url)
            elif re.search('weed|vw.php',url,flags=re.I):
                stream_url=resolve_weed(url)
            elif re.search('mediaplaybox',url,flags=re.I):
                stream_url = resolve_mediaplaybox(url)
            elif re.search('desiflicks',url,flags=re.I):
                stream_url = resolve_desiflicks(url)
            else:
                print "host "+url
                source = urlresolver.HostedMediaFile(url)
                if source:
                    stream_url = source.resolve()
                    if isinstance(stream_url,urlresolver.UrlResolver.unresolvable):
                        showUrlResoverError(stream_url)
                        stream_url = False
                else:
                    stream_url=url
            try:
                stream_url=stream_url.split('referer')[0]
                stream_url=stream_url.replace('|','')
            except:
                pass
        except ResolverError as e:
            #logerror(str(e))
            #showpopup('[COLOR=FF67cc33]Aftershock URLresolver Error[/COLOR] ' + e.value2,'[B][COLOR red]'+e.value+'[/COLOR][/B]',5000, elogo)
            try:
                #import urlresolver
                source = urlresolver.HostedMediaFile(url)
                if source:
                    stream_url = source.resolve()
                    if isinstance(stream_url,urlresolver.UrlResolver.unresolvable):
                        showUrlResoverError(stream_url)
                        stream_url = False
            except Exception as e:
                logerror(str(e))
                showpopup('[COLOR=FF67cc33]Aftershock URLresolver Error[/COLOR]','[B][COLOR red]'+str(e)+'[/COLOR][/B]',5000, elogo)
        except Exception as e:
            logerror(str(e))
            showpopup('[COLOR=FF67cc33]Aftershock URLresolver Error[/COLOR]','[B][COLOR red]'+str(e)+'[/COLOR][/B]',5000, elogo)
    else:
        logerror("video url not valid")
        showpopup('[COLOR=FF67cc33]Aftershock URLresolver Error[/COLOR]','[B][COLOR red]video url not valid[/COLOR][/B]',5000, elogo)
    if stream_url and re.search('\.(zip|rar|7zip)$',stream_url,re.I):
        logerror("video url found is an archive")
        showpopup('[COLOR=FF67cc33]Aftershock URLresolver Error[/COLOR]','[B][COLOR red]video url found is an archive[/COLOR][/B]',5000, elogo)
        return False
    return stream_url

def showUrlResoverError(unresolvable):
    logerror(str(unresolvable.msg))
    showpopup('[B]UrlResolver Error[/B]','[COLOR red]'+str(unresolvable.msg)+'[/COLOR]',10000, elogo)
def logerror(log):
    xbmc.log(log, xbmc.LOGERROR)
def showpopup(title='', msg='', delay=5000, image=''):
    xbmc.executebuiltin('XBMC.Notification("%s","%s",%d,"%s")' % (title, msg, delay, image))
    
def grab_cloudflare(url):

    class NoRedirection(urllib2.HTTPErrorProcessor):
        # Stop Urllib2 from bypassing the 503 page.    
        def http_response(self, request, response):
            code, msg, hdrs = response.code, response.msg, response.info()

            return response
        https_response = http_response

    cj = cookielib.CookieJar()
    
    opener = urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')]
    response = opener.open(url).read()
        
    jschl=re.compile('name="jschl_vc" value="(.+?)"/>').findall(response)
    if jschl:
        import time
        jschl = jschl[0]    
    
        maths=re.compile('value = (.+?);').findall(response)[0].replace('(','').replace(')','')

        domain_url = re.compile('(https?://.+?/)').findall(url)[0]
        domain = re.compile('https?://(.+?)/').findall(domain_url)[0]
        
        time.sleep(5)
        
        normal = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        normal.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')]
        final= normal.open(domain_url+'cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s'%(jschl,eval(maths)+len(domain))).read()
        
        response = normal.open(url).read()

    return response

def millis():
      import time as time_
      return int(round(time_.time() * 1000))
    
def load_json(data):
      def to_utf8(dct):
            rdct = {}
            for k, v in dct.items() :
                  if isinstance(v, (str, unicode)) :
                        rdct[k] = v.encode('utf8', 'ignore')
                  else :
                        rdct[k] = v
            return rdct
      try :        
            from lib import simplejson
            json_data = simplejson.loads(data, object_hook=to_utf8)
            return json_data
      except:
            try:
                  import json
                  json_data = json.loads(data, object_hook=to_utf8)
                  return json_data
            except:
                  import sys
                  for line in sys.exc_info():
                        print "%s" % line
      return None
def getVideoID(url):
    return re.compile('(id|url|v|si|data-config)=(.+?)/').findall(url + '/')[0][1]
def resolve_desiflicks(url):
    from resources.universal import EnkDekoder
    import BeautifulSoup
    link = main.OPENURL(url)
    dek = EnkDekoder.dekode(link)
    
    if dek is not None:
        link = dek
    
    if re.search(';video_url',link):
        stream_url = re.findall(';video_url=(.+?)&amp',link)[0]
        stream_url = stream_url.replace('_ipod.mp4', '.flv')
    elif re.search('iframe src=', link):
        stream_url = re.findall('<iframe src="(.+?)"',link)[0]
        stream_url = stream_url.replace('preview','edit')
    print '>>>>> STREAM URL(desiflicks) >>>> ' + str(stream_url)
    return stream_url
    
def resolve_mediaplaybox(url):
    url = url + '#'
    video_id = re.compile('http://www.mediaplaybox.com/video/(.+?)#').findall(url)[0]
    
    url = 'http://www.mediaplaybox.com/mobile?vinf=' + str(video_id)
    link = main.OPENURL(url)
    video_file = re.compile('href="http://www.mediaplaybox.com.+?/media/files_flv/(.+?)"').findall(link)[0]
    stream_url = 'http://www.mediaplaybox.com/media/files_flv/' + video_file.replace('_ipod.mp4', '.flv')
    # TODO : Implement HD Resoolver
    #hd_video_link = 'http://www.mediaplaybox.com/media/files_flv/' + video_file.replace('_ipod.mp4', '_hd.mp4')
    #response = HttpUtils.HttpClient().getResponse(url=hd_video_link)
    #if response.status < 400:
    #    stream_url= hd_video_link
    
    print '>>>>> STREAM URL(mediaplaybox) >>>> ' + str(stream_url)
    return stream_url

def resolve_vidtophp(url):
    video_id = getVideoID(url)
    if not video_id :
        stream_url = resolve_vidto(url)
    else:
        stream_url = 'http://vidto.me/'+video_id+'.html'
        stream_url = urlresolver.resolve(stream_url)
    print '>>>>> STREAM URL(vidto) >>>> ' + str(stream_url)
    return stream_url
def resolve_weed(url):
    stream_url='http://www.videoweed.es/file/' + str(getVideoID(url))
    stream_url = urlresolver.resolve(stream_url)
    print '>>>>> STREAM URL(videoweed) >>>> ' + str(stream_url)
    return stream_url

def resolve_cloud(url):
    stream_url='http://www.cloudy.ec/embed.php?id=' + str(getVideoID(url))
    stream_url = urlresolver.resolve(stream_url)
    print '>>>>> STREAM URL(cloud_EC) >>>> ' + str(stream_url)
    return stream_url

def resolve_videotanker(url):
    stream_url='http://videotanker.co/player/embed_player.php?vid=' + str(getVideoID(url))
    stream_url = urlresolver.resolve(stream_url)
    print '>>>>> STREAM URL(videotanker) >>>> ' + str(stream_url)
    return stream_url

def resolve_videohut(url):
    stream_url='http://www.videohut.to/embed.php?id=' + str(getVideoID(url))
    stream_url = urlresolver.resolve(stream_url)
    print '>>>>> STREAM URL(videohut) >>>> ' + str(stream_url)
    return stream_url
    
def resolve_dailymotion(url):
    stream_url='http://www.dailymotion.com/embed/video/' + str(getVideoID(url))
    stream_url = urlresolver.resolve(stream_url)
    print '>>>>> STREAM URL(dailymotion) >>>> ' + str(stream_url)
    return stream_url

def resolve_letwatch(url):
    print '>>>>>> INSIDE LETWATCH'
    stream_url='http://letwatch.us/embed-'+str(getVideoID(url))+'-520x400.html'
    
    link = main.OPENURL(stream_url)
    result = common.parseDOM(link, "script", attrs= {"type":"text/javascript"})
    for item in result:
        match = re.findall('file:"(.+?)",label:',item)
        if match:
            stream_url = match[0]
            break 
    print '>>>>> STREAM URL(letwatch) >>>> ' + str(stream_url)
    return stream_url

    
def resolve_playwire(url):
    #NEED TO FIGURE OUT A WAY TO READ THIS FROM THE SIRE. RIGHT NOW THE URL IS HARDCODED
    #link = main.OPENURL(url)
    #match = re.findall('data-config="(.+?)"',link)
    #stream_url = ''
    #for dataconfig in match:
    #    print 'DATA CONFIG >>>>>>>> ' + dataconfig
    #    stream_url = dataconfig.replace('player.json','manifest.f4m')
    #    print 'MANIFEST URL >>>>>>>>>>>> ' + stream_url
    stream_url = 'http://config.playwire.com/12376/videos/v2/'+str(getVideoID(url))+'/manifest.f4m'
    #stream_url = 'http://config.playwire.com/18875/videos/v2/'+str(getVideoID(url))+'/manifest.f4m'
    link = main.OPENURL(stream_url)
    import xml.etree.ElementTree as ET
    #print link
    root = ET.fromstring(link)
    baseURL = root.find('{http://ns.adobe.com/f4m/1.0}baseURL').text
    mediaurl = root.find('{http://ns.adobe.com/f4m/1.0}media').attrib['url']
    #print baseURL
    #print mediaurl
    stream_url = baseURL+'/'+mediaurl
    print '>>>>> STREAM URL >>>> ' + stream_url
    return stream_url
    
def resolve_realdebrid(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock Real-Debrid Link...')       
        dialog.update(0)
        import main
        cookie_file = os.path.join(os.path.join(main.datapath,'Cookies'), 'realdebrid.cookies')
        cookieExpired = False
        if os.path.exists(cookie_file):
            try:
                cookie = open(cookie_file).read()
                expire = re.search('expires="(.*?)"',cookie, re.I)
                if expire:
                    expire = str(expire.group(1))
                    import time
                    if time.time() > time.mktime(time.strptime(expire, '%Y-%m-%d %H:%M:%SZ')):
                       cookieExpired = True
            except: cookieExpired = True 
        if not os.path.exists(cookie_file) or cookieExpired:
            import hashlib
            login_data = urllib.urlencode({'user' : xbmcaddon.Addon(id='script.module.urlresolver').getSetting('RealDebridResolver_username'),
                                            'pass' : hashlib.md5(xbmcaddon.Addon(id='script.module.urlresolver').getSetting('RealDebridResolver_password')).hexdigest()})
            surl = 'https://real-debrid.com/ajax/login.php?' + login_data
            source = main.OPENURL(surl,verbose=False,cookie='realdebrid',log=False)
            dialog.update(50)
            if re.search('OK', source): print "Real Debrid Login Successful"
            if dialog.iscanceled(): return None
        url = 'https://real-debrid.com/ajax/unrestrict.php?link=%s' % url
        source = main.OPENURL(url,cookie='realdebrid',verbose=False,log=False)
        if dialog.iscanceled(): return None
        dialog.update(100)
        dialog.close()
        del dialog
        import json
        jsonresult = json.loads(source)
        if 'generated_links' in jsonresult :
            generated_links = jsonresult['generated_links']
            if len(generated_links) == 1:
                return generated_links[0][2].encode('utf-8')
            line = []
            for link in generated_links :
                extension = link[0].split('.')[-1]
                line.append(extension.encode('utf-8'))
            result = dialog.select('Choose the link', line)
            if result != -1 :
                link = generated_links[result][2]
                return link.encode('utf-8')
            else :
                return False
        elif 'main_link' in jsonresult :
            return jsonresult['main_link'].encode('utf-8')
        else :
            if 'message' in jsonresult :
                logerror('**** Real Debrid Error occured: %s' % jsonresult['message'].encode('utf-8'))
                showpopup(title='[B][COLOR white]Aftershock REAL-DEBRID[/COLOR][/B]', msg='[COLOR red]%s[/COLOR]' % jsonresult['message'].encode('utf-8'), delay=5000, image=elogo)
                main.removeFile(cookie_file)
                return False
            else: return False
    except Exception, e:
        logerror('**** Real-Debrid Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]Real-Debrid[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)


def resolve_sockshare(url):
        try:
            html = net().http_GET(url).content
            dialog = xbmcgui.DialogProgress()
            dialog.create('Resolving', 'Resolving Aftershock Sockshare Link...')
            pattern = '<a href="(/.+?)" class="download_file_link" style="margin:0px 0px;">Download File</a>'
            link = re.search(pattern, html)
            if link:
                logerror('Direct link found: %s' % link.group(1))
                return 'http://www.sockshare.com%s' % link.group(1)

            r = re.search('value="([^"]+)" name="hash"', html)
            if r:
                session_hash = r.group(1)
            else:
                raise Exception ('Sockshare: session hash not found')

            html = net().http_POST(url, form_data={'hash': session_hash,'confirm': 'Continue as Free User'}).content
        
            r = re.search('\?stream=(.+?)\'', html)
            if r:
                playlist_code = r.group(1)
            else:
                r = re.search('key=(.+?)&',html)
                playlist_code = r.group(1)
            Avi = "http://sockshare.com/get_file.php?stream=%s&original=1"%playlist_code
            if Avi:
                html = net().http_GET(Avi).content
                final=re.compile('url="(.+?)"').findall(html)[0].replace('&amp;','&')
                return "%s?User-Agent=%s"%(final,'Mozilla%2F5.0%20(Windows%20NT%206.1%3B%20rv%3A11.0)%20Gecko%2F20100101%20Firefox%2F11.0')
            else:
                xml_url = re.sub('/(file|embed)/.+', '/get_file.php?stream=', url)
                xml_url += playlist_code
                html = net().http_GET(xml_url).content

                r = re.search('url="(.+?)"', html)
                if r:
                    flv_url = r.group(1)
                else:
                    raise Exception ('Sockshare: stream url not found')

                return "%s?User-Agent=%s"%(flv_url.replace('&amp;','&'),'Mozilla%2F5.0%20(Windows%20NT%206.1%3B%20rv%3A11.0)%20Gecko%2F20100101%20Firefox%2F11.0')
        
        except urllib2.URLError, e:
            logerror('Sockshare: got http error %d fetching %s' %
                                    (e.code, url))
            #return unresolvable(code=3, msg=e)
        except Exception, e:
            logerror('**** Sockshare Error occured: %s' % e)
            xbmc.executebuiltin('[B][COLOR white]Sockshare[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)
            return unresolvable(code=0, msg=e)
        
def resolve_mrfile(url):
    try:
        import jsunpack
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock MR.File Link...')       
        dialog.update(0)
        print 'Aftershock MR.File - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        embed=re.findall('<IFRAME SRC="(http://mrfile[^"]+)"',html)
        html = net().http_GET(embed[0]).content
        r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?)</script>',html,re.M|re.DOTALL)
        try:unpack=jsunpack.unpack(r[1])
        except:unpack=jsunpack.unpack(r[0])
        try:stream_url=re.findall('<param name="src"value="(.+?)"/>',unpack)[0]
        except:stream_url=re.findall("file: '([^']+)'",html)[0]
        return stream_url
        if dialog.iscanceled(): return None
    except Exception, e:
        logerror('**** MR.File Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]MR.File[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)

  

def resolve_g2g(url):
    html3 = net().http_GET(url).content 
    url2 = re.findall('(?sim)<iframe src="(http://g2g.fm/pasmov3p.php.+?)"', html3)[0]
    req = urllib2.Request(url2)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Referer', url)
    response = urllib2.urlopen(req)
    html=response.read()
    response.close()
    phpUrl = re.findall('(?sim)<iframe id="ggplayer" src="(.+?php)"', html)[0]
    req = urllib2.Request(phpUrl)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Referer', url)   
    response = urllib2.urlopen(req)
    html2=response.read()
    response.close()
    googleUrl = re.findall('(?sim)<iframe src="(.+?preview)"', html2)[0]
    return resolve_googleDocs(googleUrl)
     
def unescapes(text):
    if text:
        rep = {"\u003d":"=","\u0026":"&","u003d":"=","u0026":"&","%26":"&","&#38;":"&","&amp;":"&","&#044;": ",","&nbsp;": " ","\n": "","\t": "","\r": "","%5B": "[","%5D": "]",
               "%3a": ":","%3A":":","%2f":"/","%2F":"/","%3f":"?","%3F":"?","%3d":"=","%3D":"=","%2C":",","%2c":",","%3C":"<",
               "%20":" ","%22":'"',"%3D":"=","%3A":":","%2F":"/","%3E":">","%3B":",","%27":"'","%0D":"","%0A":"","%92":"'",
               "&lt;": "<","&gt;": ">","&quot": '"',"&rsquo;": "'","&acute;": "'"}
        for s, r in rep.items():
            text = text.replace(s, r) 
    #except TypeError: pass
    return text

def resolve_picasaWeb(url):
    run = net().http_GET(url)
    cjList=[]
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler())
    req = urllib2.Request(url)
    f = opener.open(req)
    html = f.read()
    for cookie in cj:
            cjList.append(str(cookie).replace('<Cookie ','').replace(' for picasaweb.google.com/>','').replace('for .google.com/>',''))
    Lid=re.search('https://picasaweb.google.com/(.+?)/.+?authkey=(.+?)#([^<]+)',url)
    url='https://picasaweb.google.com/data/entry/base/user/'+Lid.group(1)+'/photoid/'+Lid.group(3)+'?alt=rss&authkey='+Lid.group(2)
    namelist=[]
    urllist=[]
    dialog = xbmcgui.DialogProgress()
    dialog.create('Resolving', 'Resolving Aftershock Picassa Link...')       
    dialog.update(0)
    print 'Aftershock GoogleDoc - Requesting GET URL: %s' % url
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36')
    req.add_header('cookie', 'xnfo=1; PREF=ID=85556f1a24007f7a:U=dc2692c0a6061b26:FF=0:LD=en:TM=1373784453:LM=1389395973:GM=1:S=qR9eOdnLEbmW_TLb; HSID=A20CRcfWXDjH2t8pM; SSID=AT-HtXZJKl-_80o2K; APISID=Oxz2q50wC6cLlo6-/AGZzvI9THf_52xvSO; SAPISID=kF1H8rjAwWjKPFU6/AjxdPvG1MVo2oU8aT; lh=DQAAAM4AAACjRFpk1gWTm8hUwNXV8b4iTC6-IIL6RsAD8urndnSZYTYKgkuDD4aOktLrRQXWX4--37oGvyHC4c07ooRuZ0AxVdGINz5UCX5n4-63PwQDpKnqvJnFiv4SaS3UQlLrlXsoeSPDs2-bWOpBNn9b7BCfQr9XJXC5OJrpiDFlKOJ3XIjJ8Kh3M0Z2K84u2k3pb7l2ODvIFGjk38GLmn-gPSHENZEmCgV-KsqpgDTQ0EnPU-h03OHch9xEmof7HD4TzzV71YS5X9hNGbYzp3ux5asE;  '+cjList[1]+'; noRedirect=1; SID=DQAAAMwAAABwVBj_2BKoFX1DvzaYSC2Vd7ieIUcNRpOHAmwDkKE4KEmzBiIUPoGedSnY91jnlOUk7wysRSWIaT_NiI6SfpFHRS9FA59wG7XETqInr0vUA2si8J1IefoooMj6i3JBxdsc6wZ-XUYu57czbICcBshac3_al7xJLQJnGd1kz-2Zxn3IVi3c5sDL21pCc_1SegSDBFughkCAY7p7T8prVX6XLqf_JGv34RIx6pPYZ_emGzjEOVbbjswVvX-9uKLvARvYgsjXseS5k3_TMHNLYQWp; '+cjList[0])
    
    response = urllib2.urlopen(req)
    html=response.read()
    response.close()
    dialog.update(100)
    link2=unescapes(html)
    streams_map = str(link2)
    stream= re.compile("url='(http://redirector.googlevideo.com[^']+)' height='([^']+)'").findall(streams_map)
    for stream_url,stream_quality in reversed(stream):
        stream_url = unescapes(stream_url)
        urllist.append(stream_url)
        stream_qlty = stream_quality.upper()
        if (stream_qlty == '720'):
            stream_qlty = 'HD-720p'
        elif (stream_qlty == '480'):
            stream_qlty = 'SD-480p'
        elif (stream_qlty == '360'):
            stream_qlty = 'SD-360p'
        elif (stream_qlty == '240'):
            stream_qlty = 'SD-240p'
        namelist.append(stream_qlty)
    dialog = xbmcgui.Dialog()
    answer =dialog.select("Quality Select", namelist)
    if answer==-1:
        return
    else:
        return urllist[int(answer)]
    
def resolve_googleDocs(url):
    namelist=[]
    urllist=[]
    dialog = xbmcgui.DialogProgress()
    dialog.create('Resolving', 'Resolving Aftershock GoogleDoc Link...')       
    dialog.update(0)
    print 'Aftershock GoogleDoc - Requesting GET URL: %s' % url
    html = net().http_GET(url).content
    dialog.update(100)
    link2=unescapes(html)
    match= re.compile('url_encoded_fmt_stream_map":"(.+?),"').findall(link2)[0]
    if match:
        streams_map = str(match)
    else:
        streams_map = str(link2)
    stream= re.compile('url=(.+?)&type=.+?&quality=(.+?),').findall(streams_map)
    for stream_url,stream_quality in stream:
        stream_url = stream_url
        stream_url = unescapes(stream_url)
        urllist.append(stream_url)
        stream_qlty = stream_quality.upper()
        if (stream_qlty == 'hd1080'):
            stream_qlty = 'HD-1080p'
        elif (stream_qlty == 'hd720'):
            stream_qlty = 'HD-720p'
        elif (stream_qlty == 'latge'):
            stream_qlty = 'SD-480p'
        elif (stream_qlty == 'medium'):
            stream_qlty = 'SD-360p'
        namelist.append(stream_qlty)
    dialog = xbmcgui.Dialog()
    answer =dialog.select("Quality Select", namelist)
    if answer==-1:
        return
    else:
        return urllist[int(answer)]

def resolve_firedrive(url):
    try:
        url=url.replace('putlocker.com','firedrive.com').replace('putlocker.to','firedrive.com')
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock Firedrive Link...')       
        dialog.update(0)
        print 'Aftershock Firedrive - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        dialog.update(50)
        if dialog.iscanceled(): return None
        post_data = {}
        r = re.findall(r'(?i)<input type="hidden" name="(.+?)" value="(.+?)"', html)
        for name, value in r:
            post_data[name] = value
        post_data['referer'] = url
        html = net().http_POST(url, post_data).content
        embed=re.findall('(?sim)href="([^"]+?)">Download file</a>',html)
        if not embed:
            embed=re.findall("(?sim)'(http://dl.firedrive.com/[^']+?)'",html)
        if dialog.iscanceled(): return None
        if embed:
            dialog.update(100)
            return embed[0]
        else:
            logerror('Aftershock: Resolve Firedrive - File Not Found')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,Firedrive,2000)")
            return False
    except Exception, e:
        logerror('**** Firedrive Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]Firedrive[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)

def resolve_mightyupload(url):
    from resources.libs import jsunpack
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock MightyUpload Link...')       
        dialog.update(0)
        html = net().http_GET(url).content
        if dialog.iscanceled(): return False
        dialog.update(50)
        logerror('Aftershock: Resolve MightyUpload - Requesting GET URL: '+url)
        embed=re.findall('<IFRAME SRC="(http://www.mightyupload.com/embed[^"]+?)"',html)
        if embed:
            html2 = net().http_GET(embed[0]).content
            try:vid=re.findall("file: '([^']+?)',",html2)[0]
            except:
                r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?)</script>',html2,re.M|re.DOTALL)
                unpack=jsunpack.unpack(r[1])
                vid=re.findall('<param name="src"value="(.+?)"/>',unpack)[0]
            return vid
        r = re.findall(r'name="(.+?)" value="?(.+?)"', html, re.I|re.M)
        if r:
            puzzle_img = os.path.join(datapath, "mightyupload_puzzle.png")
            solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)
            if solvemedia:
                html = net().http_GET(solvemedia.group(1)).content
                hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
                open(puzzle_img, 'wb').write(net().http_GET("http://api.solvemedia.com%s" % re.search('img src="(.+?)"', html).group(1)).content)
                img = xbmcgui.ControlImage(450,15,400,130, puzzle_img)
                wdlg = xbmcgui.WindowDialog()
                wdlg.addControl(img)
                wdlg.show()
            
                xbmc.sleep(3000)
    
                kb = xbmc.Keyboard('', 'Type the letters in the image', False)
                kb.doModal()
                capcode = kb.getText()
       
                if (kb.isConfirmed()):
                    userInput = kb.getText()
                    if userInput != '':
                        solution = kb.getText()
                    elif userInput == '':
                        xbmc.executebuiltin("XBMC.Notification(No text entered, You must enter text in the image to access video,2000)")
                        return False
            post_data = {}
            for name, value in r:
                post_data[name] = value
            post_data['referer'] = url
            post_data['adcopy_response'] = solution
            post_data['adcopy_challenge'] = hugekey
            html = net().http_POST(url, post_data).content
            if dialog.iscanceled(): return False
            dialog.update(100)
            r = re.findall(r'<a href=\"(.+?)(?=\">Download the file</a>)', html)
            return r[0]
        else:
            logerror('***** MightyUpload - File not found')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,MightyUpload,2000,"+elogo+")")
            return False
    except Exception, e:
        logerror('Aftershock: Resolve MightyUpload Error - '+str(e))
        raise ResolverError(str(e),"MightyUpload")       
        
def resolve_bayfiles(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock Bayfiles Link...')       
        dialog.update(0)
        print 'Aftershock Bayfiles - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        try: vfid = re.compile('var vfid = ([^;]+);').findall(html)[0]
        except:pass
        try:urlpremium='http://'+ re.compile('<a class="highlighted-btn" href="http://(.+?)">Premium Download</a>').findall(html)[0]
        except:urlpremium=[]
        if urlpremium:
                return urlpremium
        else:
                try:
                    delay = re.compile('var delay = ([^;]+);').findall(html)[0]
                    delay = int(delay)
                except: delay = 300
                t = millis()
                html2 = net().http_GET("http://bayfiles.net/ajax_download?_=%s&action=startTimer&vfid=%s"%(t,vfid)).content
                datajson=load_json(html2)
                if datajson['set']==True:
                    token=datajson['token']
                    url_ajax = 'http://bayfiles.net/ajax_download'
                    post = "action=getLink&vfid=%s&token=%s" %(vfid,token)
                    finaldata=net().http_GET(url_ajax + '?' + post).content
                    patron = 'onclick="javascript:window.location.href = \'(.+?)\''
                    matches = re.compile(patron,re.DOTALL).findall(finaldata)
                    return matches[0] #final url mp4
    except:
        html = net().http_GET(url).content
        try:
                match2=re.compile('<div id="content-inner">\n\t\t\t\t<center><strong style="color:#B22B13;">Your IP (.+?) has recently downloaded a file. Upgrade to premium or wait (.+?) min.</strong>').findall(html)[0]
                raise ResolverError('You recently downloaded a file. Upgrade to premium or wait',"Bayfiles")
                return
        except:
                match3=re.compile('<div id="content-inner">\n\t\t\t\t<center><strong style="color:#B22B13;">Your IP (.+?) is already downloading. Upgrade to premium or wait.</strong>').findall(html)
                raise ResolverError('You are already downloading. Upgrade to premium or wait.',"Bayfiles")
                return

def resolve_mailru(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock MailRU Link...')       
        dialog.update(0)
        print 'Aftershock MailRU - Requesting GET URL: %s' % url
        link = net().http_GET(url).content
        match=re.compile('videoSrc = "(.+?)",',re.DOTALL).findall(link)
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler())
        req = urllib2.Request(url)
        f = opener.open(req)
        html = f.read()
        for cookie in cj:
            cookie=str(cookie)

        rcookie=cookie.replace('<Cookie ','').replace(' for .video.mail.ru/>','')

        vlink=match[0]+'&Cookie='+rcookie
        return vlink
    except Exception, e:
        logerror('**** MailRU Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]MailRU[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)


def resolve_yify(url):
    try:
        referer = url
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock Yify Link...')       
        dialog.update(0)
        print 'Aftershock Yify - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        url = re.compile('showPkPlayer[(]"(.+?)"[)]').findall(html)[0]
        key=url
        url = 'http://yify.tv/reproductor2/pk/pk/plugins/player_p2.php?url=' + url
        print url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36')
        req.add_header('Referer', referer)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        
        if 'captcha' in link:
            captcha=re.search('{"captcha":(.+?),"k":"([^"]+)"}',link)
            curl='http://www.google.com/recaptcha/api/challenge?k='+captcha.group(2)+'&ajax=1&cachestop=0.7698786298278719'
            html = net().http_GET(curl).content
            print html
            image_id=re.findall("challenge : '([^']+)'",html)
            img_id=image_id[0]
            image_url='http://www.google.com/recaptcha/api/image?c='+img_id
            img = xbmcgui.ControlImage(450,15,400,130, image_url)
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
        
            kb = xbmc.Keyboard('', 'Type the letters in the image', False)
            kb.doModal()
            capcode = kb.getText()
   
            if (kb.isConfirmed()):
                userInput = kb.getText()
                if userInput != '':
                    solution = kb.getText()
                elif userInput == '':
                    xbmc.executebuiltin('big', 'No text entered', 'You must enter text in the image to access video', '')
                    return False
            else:
                return False
               
            wdlg.close()
            url = 'http://yify.tv/reproductor2/pk/pk/plugins/player_p2.php'
            user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36'
            values = {'url' : key,'chall' : img_id,'type' :  captcha.group(1),'res':solution,'':'','':''}
            headers = { 'User-Agent' : user_agent,'Referer':'referer'}

            data = urllib.urlencode(values)
            req = urllib2.Request(url, data, headers)
            response = urllib2.urlopen(req)
            link = response.read()
        if '.pdf' in link:
            html = re.findall('{"url":"([^"]+.pdf)",',link)[0]
        else:
            html = re.compile('{"url":"([^"]+)"').findall(link)[1]
        stream_url = html
        return stream_url
    except Exception, e:
        logerror('**** Yify Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]Yify[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)


def resolve_VK(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock VK Link...')       
        dialog.update(0)
        print 'Aftershock VK - Requesting GET URL: %s' % url
        useragent='Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7'
        link2 = net(user_agent=useragent).http_GET(url).content
        if re.search('This video has been removed', link2, re.I):
            logerror('***** Aftershock VK - This video has been removed')
            xbmc.executebuiltin("XBMC.Notification(This video has been removed,VK,2000)")
            return Fals
        urllist=[]
        quaList=[]
        match=re.findall('(?sim)<source src="([^"]+)"',link2)
        for url in match:
            print url
            urllist.append(url)
            qua=re.findall('(?sim).(\d+).mp4',url)
            quaList.append(str(qua[0]))
        dialog2 = xbmcgui.Dialog()
        ret = dialog2.select('[COLOR=FF67cc33][B]Select Quality[/COLOR][/B]',quaList)
        if ret == -1:
            return False
        stream_url = urllist[ret]
        if match: 
            return stream_url.replace("\/",'/')
    except Exception, e:
        logerror('**** VK Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]VK[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)

def resolve_youwatch(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock Youwatch Link...')       
        dialog.update(0)
        print 'Aftershock Youwatch - Requesting GET URL: %s' % url
        if 'embed' not in url:
            mediaID = re.findall('http://youwatch.org/([^<]+)', url)[0]
            url='http://youwatch.org/embed-'+mediaID+'.html'
        else:url=url
        html = net().http_GET(url).content
        try:
                html=html.replace('|','/')
                stream=re.compile('/mp4/video/(.+?)/(.+?)/(.+?)/setup').findall(html)
                for id,socket,server in stream:
                    continue
        except:
                raise ResolverError('This file is not available on',"Youwatch")
        stream_url='http://'+server+'.youwatch.org:'+socket+'/'+id+'/video.mp4?start=0'
        return stream_url
    except Exception, e:
        logerror('**** Youwatch Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]Youwatch[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)


def resolve_projectfreeupload(url):
    try:
        import jsunpack
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock Project Free Link...')       
        dialog.update(0)
        print 'Aftershock Project Free - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        r = re.findall(r'\"hidden\"\sname=\"?(.+?)\"\svalue=\"?(.+?)\"\>', html, re.I)
        post_data = {}
        for name, value in r:
            post_data[name] = value
        post_data['referer'] = url
        post_data['method_premium']=''
        post_data['method_free']=''
        html = net().http_POST(url, post_data).content
        embed=re.findall('<IFRAME SRC="(.+?)"',html)
        html = net().http_GET(embed[0]).content
        r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?)</script>',html,re.M|re.DOTALL)
        try:unpack=jsunpack.unpack(r[1])
        except:unpack=jsunpack.unpack(r[0])
        stream_url=re.findall('<param name="src"value="(.+?)"/>',unpack)[0]
        return stream_url
        if dialog.iscanceled(): return None
    except Exception, e:
        logerror('**** Project Free Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]Project Free[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)

def resolve_videomega(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock Videomega Link...')       
        dialog.update(0)
        print 'Aftershock Videomega - Requesting GET URL: %s' % url
        try:
            mediaID = re.findall('http://videomega.tv/.?ref=([^<]+)', url)[0]
            url='http://videomega.tv/iframe.php?ref='+mediaID
        except:url=url
        html = net().http_GET(url).content
        try:
                encodedurl=re.compile('unescape.+?"(.+?)"').findall(html)
        except:
                raise ResolverError('This file is not available on',"VideoMega")
        url2=urllib.unquote(encodedurl[0])
        stream_url=re.compile('file: "(.+?)"').findall(url2)[0]
        return stream_url
    except Exception, e:
        logerror('**** Videomega Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]Videomega[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)
    
def resolve_vidspot(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock Vidspot Link...')       
        dialog.update(0)
        print 'Aftershock Vidspot - Requesting GET URL: %s' % url
        mediaID=re.findall('http://vidspot.net/([^<]+)',url)[0]
        url='http://vidspot.net/embed-'+mediaID+'.html'
        print url
        html = net().http_GET(url).content
        r = re.search('"file" : "(.+?)",', html)
        if r:
            stream_url = urllib.unquote(r.group(1))

        return stream_url

    except Exception, e:
        logerror('**** Vidspot Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]Vidspot[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)

    
def resolve_novamov(url):
        try:
            import unwise
            dialog = xbmcgui.DialogProgress()
            dialog.create('Resolving', 'Resolving Aftershock Novamov Link...')       
            dialog.update(0)
            print 'Aftershock Novamov - Requesting GET URL: %s' % url
            html = net().http_GET(url).content
            html = unwise.unwise_process(html)
            
            filekey = unwise.resolve_var(html, "flashvars.filekey")
            media_id=re.findall('.+?/video/([^<]+)',url)
            #get stream url from api
            api = 'http://www.novamov.com/api/player.api.php?key=%s&file=%s' % (filekey, media_id)
            html = net().http_GET(api).content
            r = re.search('url=(.+?)&title', html)
            if r:
                stream_url = urllib.unquote(r.group(1))
            else:
                r = re.search('file no longer exists',html)
                if r:
                    raise ResolverError('File Not Found or removed',"Novamov")
                raise ResolverError('Failed to parse url',"Novamov")
                
            return stream_url
        except urllib2.URLError, e:
            logerror('Novamov: got http error %d fetching %s' %
                                    (e.code, web_url))
            return unresolvable(code=3, msg=e)
        except Exception, e:
            logerror('**** Novamov Error occured: %s' % e)
            xbmc.executebuiltin('[B][COLOR white]Novamov[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)
            return unresolvable(code=0, msg=e)

def resolve_nowvideo(url):
        try:
            import unwise
            dialog = xbmcgui.DialogProgress()
            dialog.create('Resolving', 'Resolving Aftershock Nowvideo Link...')       
            dialog.update(0)
            print 'Aftershock Nowvideo - Requesting GET URL: %s' % url
            html = net().http_GET(url).content
            html = unwise.unwise_process(html)
            
            filekey = unwise.resolve_var(html, "flashvars.filekey")
            try:media_id=re.findall('.+?/video/([^<]+)',url)[0]
            except:media_id=re.findall('http://embed.nowvideo.+?/embed.php.?v=([^<]+)',url)[0]
            #get stream url from api
            api = 'http://www.nowvideo.sx/api/player.api.php?key=%s&file=%s' % (filekey, media_id)
            html = net().http_GET(api).content
            r = re.search('url=(.+?)&title', html)
            if r:
                stream_url = urllib.unquote(r.group(1))
            else:
                r = re.search('file no longer exists',html)
                if r:
                    raise ResolverError('File Not Found or removed',"Nowvideo")
                raise ResolverError('Failed to parse url',"Nowvideo")
                
            return stream_url
        except urllib2.URLError, e:
            logerror('Nowvideo: got http error %d fetching %s' %
                                    (e.code, web_url))
            return unresolvable(code=3, msg=e)
        except Exception, e:
            logerror('**** Nowvideo Error occured: %s' % e)
            xbmc.executebuiltin('[B][COLOR white]Nowvideo[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)
            return unresolvable(code=0, msg=e)

def resolve_movreel(url):

    try:
        print 'Aftershock Movreel - Requesting GET URL: %s' % url
        
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock Movreel Link...')
        dialog.update(0)

        
        user = ''
        password = ''
        login = 'http://movreel.com/login.html'
        post = {'op': 'login', 'login': user, 'password': password, 'redirect': url}
        result = main.OPENURL(url)
        result += main.OPENURL(login, data=post)
        dialog.update(33)

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "name": "F1" })[-1]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': '', 'method_premium': ''})
        post = urllib.urlencode(post)
        
        import time
        request = urllib2.Request(url, post)
        dialog.update(66)
        for i in range(0, 5):
            try:
                response = urllib2.urlopen(request, timeout=5)
                result = response.read()
                response.close()
                url = re.compile('(<a .+?</a>)').findall(result)
                url = [i for i in url if 'Download Link' in i][-1]
                url = common.parseDOM(url, "a", ret="href")[0]
                return url
            except:
                print traceback.format_exc()
                time.sleep(1)

    except Exception, e:
        logerror('**** Aftershock Movreel Error occured: %s' % e)
        raise ResolverError(str(e),"Movreel")
    finally:
        dialog.close()

def resolve_megarelease(url):
    try:
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock MegaRelease Link...')
        dialog.update(0)
        
        print 'MegaRelease Aftershock - Requesting GET URL: %s' % url
        html = net().http_GET(url).content

        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            logerror('***** MegaRelease - Site reported maintenance mode')
            xbmc.executebuiltin("XBMC.Notification(File is currently unavailable,MegaRelease in maintenance,2000)")                                
            return False
        if re.search('<b>File Not Found</b>', html):
            logerror('Aftershock: Resolve MegaRelease - File Not Found')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,MegaRelease,2000)")
            return False

        filename = re.search('You have requested <font color="red">(.+?)</font>', html).group(1)
        filename = filename.split('/')[-1]
        extension = re.search('(\.[^\.]*$)', filename).group(1)
        guid = re.search('http://megarelease.org/(.+)$', url).group(1)
        
        vid_embed_url = 'http://megarelease.org/vidembed-%s%s' % (guid, extension)
        UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
        ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        request = urllib2.Request(vid_embed_url)
        request.add_header('User-Agent', UserAgent)
        request.add_header('Accept', ACCEPT)
        request.add_header('Referer', url)
        response = urllib2.urlopen(request)
        redirect_url = re.search('(http://.+?)video', response.geturl()).group(1)
        download_link = redirect_url + filename
        
        dialog.update(100)

        return download_link
        
    except Exception, e:
        logerror('**** Aftershock MegaRelease Error occured: %s' % e)
        raise ResolverError(str(e),"MegaRelease")
    finally:
        dialog.close()
        
def setCookie(url):
    from random import choice
    cookieExpired = False
    name = "veeHD"
    userName = ['Aftershock12', 'Aftershock13', 'Aftershock14', 'Aftershock15', 'Aftershock16']
    ref = 'http://veehd.com'
    submit = 'Login'
    terms = 'on'
    remember_me = 'on'
    net().http_GET(url)
    net().http_POST('http://veehd.com/login',{'ref': ref, 'uname': choice(userName), 'pword': 'xbmcisk00l', 'submit': submit, 'terms': terms,'remember_me':remember_me})

        
def resolve_veehd(url):
    
    
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock VeeHD Link...')       
        dialog.update(0)
        if dialog.iscanceled(): return False
        dialog.update(33)
        headers = {}
        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7','Referer':url}
        print 'Aftershock VeeHD - Requesting GET URL: %s' % url
        setCookie('http://veehd.com')
        html = net().http_GET(url, headers).content
        if dialog.iscanceled(): return False
        dialog.update(66)
        fragment = re.findall('playeriframe".+?attr.+?src : "(.+?)"', html)
        for frags in fragment:
            pass
        frag = 'http://%s%s'%('veehd.com',frags)
        setCookie('http://veehd.com')
        html = net().http_GET(frag, headers).content
        va=re.search('iframe" src="([^"]+?)"',html)
        if va:
            poop='http://veehd.com'+va.group(1)
            headers = {'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7','Referer':frag,'Cache-Control':'max-age=0'}
            setCookie(poop)
            html = net().http_GET(frag, headers).content
        r = re.search('"video/divx" src="(.+?)"', html)
        if r:
            stream_url = r.group(1)
        if not r:
            a = re.search('"url":"(.+?)"', html)
            if a:
                r=urllib.unquote(a.group(1))
                if r:
                    stream_url = r
                else:
                    logerror('***** VeeHD - File Not Found')
                    xbmc.executebuiltin("XBMC.Notification(File Not Found,VeeHD,2000)")
                    return False
            if not a:
                a = re.findall('href="(.+?)">', html)
                stream_url = a[1]
        if dialog.iscanceled(): return False
        dialog.update(100)
        return stream_url
    except Exception, e:
        logerror('**** Aftershock VeeHD Error occured: %s' % e)
        raise ResolverError(str(e),"VeeHD")

def resolve_180upload(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock 180Upload Link...')
        dialog.update(0)
        
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://180upload.com/embed-%s.html' % url
        result = main.OPENURL(url)
        
        post = {}
        f = common.parseDOM(result, "form", attrs = { "id": "captchaForm" })[0]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        
        result = main.OPENURL(url, data=post)
        
        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
        result = jsunpack(result)

        url = re.compile("'file' *, *'(.+?)'").findall(result)
        url += re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(result)
        url += common.parseDOM(result, "embed", ret="src")
        url = 'http://' + url[-1].split('://', 1)[-1]
        
        return url
    except Exception, e:
        logerror('**** Aftershock 180Upload Error occured: %s' % e)
        raise ResolverError(str(e),"180Upload") 
    finally:
        dialog.close()

                
def resolve_vidto(url):
    user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    from resources.libs import jsunpack
    import time
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock Vidto Link...')
        dialog.update(0)
        html = net(user_agent).http_GET(url).content
        if dialog.iscanceled(): return False
        dialog.update(11)
        logerror('Aftershock: Resolve Vidto - Requesting GET URL: '+url)
        r = re.findall(r'<font class="err">File was removed</font>',html,re.I)
        if r:
            logerror('Aftershock: Resolve Vidto - File Was Removed')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,Vidto,2000)")
            return False
        if not r:
            r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?flvplayer.+?)</script>'
                           ,html,re.M|re.DOTALL)
            if r:
                unpacked = jsunpack.unpack(r[0])#this is where it will error, not sure if resources,libs added to os path
                try:
                    r = re.findall(r'label:"360p",file:"(.+?)"}',unpacked)[0]
                except:
                    r = re.findall(r'label:"240p",file:"(.+?)"}',unpacked)[0]
            if not r:
                r = re.findall('type="hidden" name="(.+?)" value="(.+?)">',html)
                post_data = {}
                for name, value in r:
                    post_data[name] = value.encode('utf-8')
                post_data['usr_login'] = ''
                post_data['referer'] = url
                for i in range(7):
                    time.sleep(1)
                    if dialog.iscanceled(): return False
                    dialog.update(22+i*11.3)
                html = net(user_agent).http_POST(url,post_data).content
                r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?flvplayer.+?)</script>'
                               ,html,re.M|re.DOTALL)
                if r:
                    unpacked = jsunpack.unpack(r[0])
                    try:
                        r = re.findall(r'label:"360p",file:"(.+?)"}',unpacked)[0]
                    except:
                        r = re.findall(r'label:"240p",file:"(.+?)"}',unpacked)[0]
                if not r:
                    r = re.findall(r"var file_link = '(.+?)';",html)[0]
        if dialog.iscanceled(): return False
        dialog.update(100)
        return r
    except Exception, e:
        logerror('Aftershock: Resolve Vidto Error - '+str(e))
        raise ResolverError(str(e),"Vidto") 
    finally:
        dialog.close()

def resolve_epicshare(url):
    try:
        puzzle_img = os.path.join(datapath, "epicshare_puzzle.png")
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock EpicShare Link...')
        dialog.update(0)
        
        print 'EpicShare - Aftershock Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        if dialog.iscanceled(): return False
        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            logerror('***** EpicShare - Site reported maintenance mode')
            xbmc.executebuiltin("XBMC.Notification(File is currently unavailable,EpicShare in maintenance,2000)")  
            return False
        if re.search('<b>File Not Found</b>', html):
            logerror('***** EpicShare - File not found')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,EpicShare,2000)")
            return False

        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)

        if r:
            for name, value in r:
                data[name] = value
        else:
            logerror('***** EpicShare - Cannot find data values')
            raise Exception('Unable to resolve EpicShare Link')
        
        #Check for SolveMedia Captcha image
        solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)

        if solvemedia:
           dialog.close()
           html = net().http_GET(solvemedia.group(1)).content
           hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
           open(puzzle_img, 'wb').write(net().http_GET("http://api.solvemedia.com%s" % re.search('<img src="(.+?)"', html).group(1)).content)
           img = xbmcgui.ControlImage(450,15,400,130, puzzle_img)
           wdlg = xbmcgui.WindowDialog()
           wdlg.addControl(img)
           wdlg.show()
        
           kb = xbmc.Keyboard('', 'Type the letters in the image', False)
           kb.doModal()
           capcode = kb.getText()
   
           if (kb.isConfirmed()):
               userInput = kb.getText()
               if userInput != '':
                   solution = kb.getText()
               elif userInput == '':
                   Notify('big', 'No text entered', 'You must enter text in the image to access video', '')
                   return False
           else:
               return False
               
           wdlg.close()
           dialog.create('Resolving', 'Resolving Aftershock EpicShare Link...') 
           dialog.update(50)
           if solution:
               data.update({'adcopy_challenge': hugekey,'adcopy_response': solution})

        print 'EpicShare - Aftershock Requesting POST URL: %s' % url
        html = net().http_POST(url, data).content
        if dialog.iscanceled(): return False
        dialog.update(100)
        
        link = re.search('<a id="lnk_download"  href=".+?product_download_url=(.+?)">', html)
        if link:
            print 'Aftershock EpicShare Link Found: %s' % link.group(1)
            return link.group(1)
        else:
            logerror('***** EpicShare - Cannot find final link')
            raise Exception('Unable to resolve EpicShare Link')
        
    except Exception, e:
        logerror('**** EpicShare Aftershock Error occured: %s' % e)
        raise ResolverError(str(e),"EpicShare") 
    finally:
        dialog.close()

def resolve_lemupload(url):
    try:
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Aftershock LemUpload Link...')       
        dialog.update(0)
#         
        print 'LemUpload - Aftershock Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        if dialog.iscanceled(): return False
        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('<b>File Not Found</b>', html):
            print '***** LemUpload - File Not Found'
            xbmc.executebuiltin("XBMC.Notification(File Not Found,LemUpload,2000)")
            return False
        
        if re.search('This server is in maintenance mode', html):
            print '***** LemUpload - Server is in maintenance mode'
            xbmc.executebuiltin("XBMC.Notification(Site In Maintenance,LemUpload,2000)")
            return False

        filename = re.search('<h2>(.+?)</h2>', html).group(1)
        extension = re.search('(\.[^\.]*$)', filename).group(1)
        guid = re.search('http://lemuploads.com/(.+)$', url).group(1)
        vid_embed_url = 'http://lemuploads.com/vidembed-%s%s' % (guid, extension)
        request = urllib2.Request(vid_embed_url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36')
        request.add_header('Referer', url)
        response = urllib2.urlopen(request)
        if dialog.iscanceled(): return False
        dialog.update(100)
        link = response.geturl()
        if link:
            redirect_url = re.search('(http://.+?)video', link)
            if redirect_url:
                link = redirect_url.group(1) + filename
            print 'Aftershock LemUpload Link Found: %s' % link
            return  link
        else:
            logerror('***** LemUpload - Cannot find final link')
            raise Exception('Unable to resolve LemUpload Link')

    except Exception, e:
        logerror('**** LemUpload Error occured: %s' % e)
        raise ResolverError(str(e),"LemUpload") 
    finally:
        dialog.close()
def captcha(data):
    try:
        captcha = {}

        def get_response(response):
            try:
                dataPath = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile"))
                i = os.path.join(dataPath.decode("utf-8"),'img')
                f = xbmcvfs.File(i, 'w')
                f.write(getUrl(response).result)
                f.close()
                f = xbmcgui.ControlImage(450,5,375,115, i)
                d = xbmcgui.WindowDialog()
                d.addControl(f)
                xbmcvfs.delete(i)
                d.show()
                xbmc.sleep(3000)
                t = 'Type the letters in the image'
                c = common.getUserInput(t, '')
                d.close()
                return c
            except:
                return

        solvemedia = common.parseDOM(data, "iframe", ret="src")
        solvemedia = [i for i in solvemedia if 'api.solvemedia.com' in i]

        if len(solvemedia) > 0:
            url = solvemedia[0]
            result = getUrl(url).result
            challenge = common.parseDOM(result, "input", ret="value", attrs = { "id": "adcopy_challenge" })[0]
            response = common.parseDOM(result, "iframe", ret="src")
            response += common.parseDOM(result, "img", ret="src")
            response = [i for i in response if '/papi/media' in i][0]
            response = 'http://api.solvemedia.com' + response
            response = get_response(response)
            captcha.update({'adcopy_challenge': challenge, 'adcopy_response': response})
            return captcha

        recaptcha = []
        if data.startswith('http://www.google.com'): recaptcha += [data]
        recaptcha += common.parseDOM(data, "script", ret="src", attrs = { "type": "text/javascript" })
        recaptcha = [i for i in recaptcha if 'http://www.google.com' in i]

        if len(recaptcha) > 0:
            url = recaptcha[0]
            result = getUrl(url).result
            challenge = re.compile("challenge\s+:\s+'(.+?)'").findall(result)[0]
            response = 'http://www.google.com/recaptcha/api/image?c=' + challenge
            response = get_response(response)
            captcha.update({'recaptcha_challenge_field': challenge, 'recaptcha_challenge': challenge, 'recaptcha_response_field': response, 'recaptcha_response': response})
            return captcha

        numeric = re.compile("left:(\d+)px;padding-top:\d+px;'>&#(.+?);<").findall(data)

        if len(numeric) > 0:
            result = sorted(numeric, key=lambda ltr: int(ltr[0]))
            response = ''.join(str(int(num[1])-48) for num in result)
            captcha.update({'code': response})
            return captcha

    except:
        return captcha

def resolve_hugefiles(url):
    print ">>>>>>>>> INSIDE HUGEFILES"
    try:
        result = main.OPENURL(url)
        post = {}
        f = common.parseDOM(result, "Form", attrs = { "action": "" })
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': 'Free Download'})
        post.update(captcha(result))
        
        #post = urllib.urlencode(post)

        result = main.OPENURL(url, data=post)

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "action": "" })
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': 'Free Download'})
        
        print post
        #post = urllib.urlencode(post)

        u = main.OPENURL(url, output='geturl', data=post)
        print ">>>>>>>>>>>>>> U " + str(u)
        if not url == u: return u
    except:
        return