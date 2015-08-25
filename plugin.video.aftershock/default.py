import xbmc,xbmcgui, xbmcaddon, xbmcplugin
import urllib,re,string,os,time,threading
import urllib2
from resources.libs import settings
import base64, urlparse
import CommonFunctions as common
import commonsources
from operator import itemgetter
try:
    import json
except:
    import simplejson as json

action              = None
getSetting          = xbmcaddon.Addon().getSetting
language            = xbmcaddon.Addon().getLocalizedString
addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
addonDesc           = "Aftershock Addon"
dataPath            = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile")).decode("utf-8")
addonSettings       = os.path.join(dataPath,'settings.db')
addonSources        = os.path.join(dataPath,'sources.db')
addonCache          = os.path.join(dataPath,'cache.db')

class Main:
    def __init__(self):
        global action
        params = {}
        print sys.argv[0], sys.argv[1], sys.argv[2]
        splitparams = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')
        print 'splitparams %s' % splitparams
        for param in splitparams:
            print 'params %s length %s' % (param, len(param))
            if (len(param) > 0):
                splitparam = param.split('=')
                key = splitparam[0]
                try:    value = splitparam[1].encode("utf-8")
                except: value = splitparam[1]
                params[key] = value

        try:        action = urllib.unquote_plus(params["action"])
        except:     action = None
        try:        name = urllib.unquote_plus(params["name"])
        except:     name = None
        try:        title = urllib.unquote_plus(params["title"])
        except:     title = None
        try:        year = urllib.unquote_plus(params["year"])
        except:     year = None
        try:        imdb = urllib.unquote_plus(params["imdb"])
        except:     imdb = None
        try:        tvdb = urllib.unquote_plus(params["tvdb"])
        except:     tvdb = None
        try:        season = urllib.unquote_plus(params["season"])
        except:     season = None
        try:        episode = urllib.unquote_plus(params["episode"])
        except:     episode = None
        try:        show = urllib.unquote_plus(params["show"])
        except:     show = None
        try:        show_alt = urllib.unquote_plus(params["show_alt"])
        except:     show_alt = None
        try:        date = urllib.unquote_plus(params["date"])
        except:     date = None
        try:        genre = urllib.unquote_plus(params["genre"])
        except:     genre = None
        try:        url = urllib.unquote_plus(params["url"])
        except:     url = None
        try:        image = urllib.unquote_plus(params["image"])
        except:     image = None
        try:        meta = urllib.unquote_plus(params["meta"])
        except:     meta = None
        try:        query = urllib.unquote_plus(params["query"])
        except:     query = None
        try:        source = urllib.unquote_plus(params["source"])
        except:     source = None
        try:        provider = urllib.unquote_plus(params["provider"])
        except:     provider = None
        
        print "action [%s] name [%s] title [%s] year [%s] imdb [%s] tvdb [%s] season [%s] episode [%s] show [%s] show_alt [%s] date [%s] genre [%s] url [%s] image [%s] meta [%s] query [%s] source [%s] provider [%s]" % (action, name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url, image, meta, query, source, provider)
        
        if action == None: Menu().getHomeItems()
        elif action == 'home_az': Menu().getAtoZItems()
        elif action == 'home_genre': Menu().getHomeGenre() 
        elif action == 'home_year' : Menu().getHomeYear() 
        elif action == 'home_hindimovie' : Menu().getDesiHomeItems() 
        elif action == 'home_featured' : Movies().featured()
        elif action == 'home_hd' : Movies().HD()
        elif action == 'home_latest' : Movies().latestAdded()
        elif action == 'home_newreleases' : Movies().newReleases()
        elif action == 'home_mostviewed' : Movies().mostViewed()
        elif action == 'home_mostvoted' : Movies().mostVoted()
        elif action == 'home_settings' : settings.openSettings()
        elif action == 'movie_list' : Movies().moviesList(url)
        elif action == 'desi_home_newreleases' : Movies().desiNewReleases()
        elif action == 'desi_home_az' : Menu().getDesiAtoZItems()
        elif action == 'desi_home_latest' : Movies().desiLatestAdded()
        elif action == 'desi_home_hd' : Movies().desiHD()
        elif action == 'desi_home_genre' : Menu().getDesiGenre()
        elif action == 'desi_home_year' : Menu().getDesiYear()
        elif action == 'home_international' : Menu().getInternationalTV()
        elif action == 'desi_movie_list' : Movies().desi_movie_list(url)
        elif action == 'desi_tv_channel' : Shows().getShows(url, name, provider)
        elif action == 'episodes' : Shows().getEpisodes(url, show, provider)
        elif action == 'get_host' : resolver().get_host(name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url, meta)
        elif action == 'play_moviehost' : resolver().play_host('movie', name, imdb, tvdb, url, source, provider)
        elif action == 'play_tvhost' : resolver().play_host('tv', name, imdb, tvdb, url, source, provider)

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

class Menu:
    def __init__(self):
        print "Menu Initialized"
    def getHomeItems(self):
        d = settings.getHomeItems(getSetting)
        homeItems = []
        for index, value in sorted(enumerate(d), key=lambda x:x[1]):
            if value==None: continue
            if index==0:
                homeItems.append({'name':language(90100).encode("utf-8"), 'image': 'search.png', 'action': 'home_search'})
            elif index==2:
                homeItems.append({'name':language(90102).encode("utf-8"), 'image': 'az.png', 'action': 'home_az'})
            elif index==3:
                homeItems.append({'name':language(90103).encode("utf-8"), 'image': 'new.png', 'action': 'home_newreleases'})
            elif index==4:
                homeItems.append({'name':language(90104).encode("utf-8"), 'image': 'latest.png', 'action': 'home_latest'})
            elif index==5:
                homeItems.append({'name':language(90105).encode("utf-8"), 'image': 'feat.png', 'action': 'home_featured'})
            elif index==6:
                homeItems.append({'name':language(90106).encode("utf-8"), 'image': 'view.png', 'action': 'home_mostviewed'})
            elif index==7:
                homeItems.append({'name':language(90107).encode("utf-8"), 'image': 'vote.png', 'action': 'home_mostvoted'})
            elif index==8:
                homeItems.append({'name':language(90108).encode("utf-8"), 'image': 'dvd2hd.png', 'action': 'home_hd'})
            elif index==9:
                homeItems.append({'name':language(90109).encode("utf-8"), 'image': 'genre.png', 'action': 'home_genre'})
            elif index==10:
                homeItems.append({'name':language(90110).encode("utf-8"), 'image': 'year.png', 'action': 'home_year'})
            elif index==12:
                homeItems.append({'name':language(90112).encode("utf-8"), 'image': 'intl.png', 'action': 'home_international'})
            elif index==13:
                homeItems.append({'name':language(90113).encode("utf-8"), 'image': 'hindimovies.png', 'action': 'home_hindimovie'})
        homeItems.append({'name':language(90116).encode("utf-8"), 'image':'settings.png','action':'home_settings'})
        Index().homeList(homeItems)
    def getDesiHomeItems(self):
        d = settings.getHomeItems(getSetting)
        homeItems = []
        for index, value in sorted(enumerate(d), key=lambda x:x[1]):
            if value==None: continue
            if index==0:
                homeItems.append({'name':language(90100).encode("utf-8"), 'image': 'search.png', 'action': 'desi_home_search'})
            elif index==3:
                homeItems.append({'name':language(90103).encode("utf-8"), 'image': 'new.png', 'action': 'desi_home_newreleases'})
            elif index==4:
                homeItems.append({'name':language(90104).encode("utf-8"), 'image': 'latest.png', 'action': 'desi_home_latest'})
            elif index==8:
                homeItems.append({'name':language(90108).encode("utf-8"), 'image': 'dvd2hd.png', 'action': 'desi_home_hd'})
            elif index==9:
                homeItems.append({'name':language(90109).encode("utf-8"), 'image': 'genre.png', 'action': 'desi_home_genre'})
            elif index==10:
                homeItems.append({'name':language(90110).encode("utf-8"), 'image': 'year.png', 'action': 'desi_home_year'})
        Index().homeList(homeItems)
        
    def getAtoZItems(self) :
        listItems = []
        listItems.append({'name':'0-9', 'image':'09.png', 'action':'movie_list', 'url':'/0-9/'})
        for i in string.ascii_uppercase:
            listItems.append({'name':i, 'image':i.lower()+'.png', 'action':'movie_list', 'url':'/'+i.lower()+'/'})
        Index().homeList(listItems)  
        
    def getHomeGenre(self) :
        listItems = []
        genres = ['Action','Adventure','Animation','Biography','Comedy','Crime','Documentary','Drama','Family','Fantasy','History','Horror','Music','Musical','Mystery','Romance','Sci-Fi','Short','Sport','Thriller','War','Western']
        
        for i in genres:
            listItems.append({'name':i, 'image':i[:3].lower()+'.png', 'action':'movie_list', 'url':'/' + i.lower()+'/'})
        Index().homeList(listItems)    
        
    def getHomeYear(self) :
        listItems = []
        for i in reversed(range(2003, 2016)):
            listItems.append({'name':str(i), 'image':str(i)+'.png', 'action':'movie_list', 'url':Links().getUrl('search.php?year='+str(i))})
        listItems.append({'name':'Enter Year', 'image':'enteryear.png', 'action':'movie_enter_year'})    
        Index().homeList(listItems)    
        
    def getDesiGenre(self) :
        listItems = []
        genres = ['Action','Comedy','Crime','Drama','Horror','Romance','Thriller']
        
        for i in genres:
            listItems.append({'name':i, 'image':i[:3].lower()+'.png', 'action':'desi_movie_list', 'url':'/category/' + i.lower()+'/feed'})
        Index().homeList(listItems)    
        
    def getDesiYear(self) :
        listItems = []
        for i in reversed(range(2003, 2016)):
            listItems.append({'name':str(i), 'image':str(i)+'.png', 'action':'desi_movie_list', 'url':'/category/'+str(i)+'/feed'})
        listItems.append({'name':'Enter Year', 'image':'enteryear.png', 'action':'desi_enter_year'})    
        Index().homeList(listItems)    
    
    def getInternationalTV(self):
        listItems = []
        logoBaseURL='http://www.lyngsat-logo.com/logo/tv'
        listItems.append({'provider':'desirulez', 'name':language(90200).encode("utf-8"), 'image': logoBaseURL+'/ss/star_plus.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=42'})
        listItems.append({'provider':'desirulez', 'name':language(90201).encode("utf-8"), 'image': logoBaseURL+'/zz/zee_tv.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=73'})
        listItems.append({'provider':'desirulez', 'name':language(90202).encode("utf-8"), 'image': logoBaseURL+'/zz/zindagi_tv_pk.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=00'})
        listItems.append({'provider':'desirulez', 'name':language(90203).encode("utf-8"), 'image': logoBaseURL+'/ss/set_in.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=63'})
        listItems.append({'provider':'desirulez', 'name':language(90204).encode("utf-8"), 'image': logoBaseURL+'/ss/sony_pal_in.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=00'})
        listItems.append({'provider':'desirulez', 'name':language(90205).encode("utf-8"), 'image': logoBaseURL+'/ll/life_ok_in.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=1375'})
        listItems.append({'provider':'desirulez', 'name':language(90206).encode("utf-8"), 'image': logoBaseURL+'/ss/sahara_one.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=134'})
        listItems.append({'provider':'desirulez', 'name':language(90207).encode("utf-8"), 'image': logoBaseURL+'/ss/star_jalsha.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=667'})
        listItems.append({'provider':'desirulez', 'name':language(90208).encode("utf-8"), 'image': logoBaseURL+'/cc/colors_in.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=176'})
        listItems.append({'provider':'desirulez', 'name':language(90209).encode("utf-8"), 'image': logoBaseURL+'/ss/sony_sab_tv.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=254'})
        listItems.append({'provider':'desirulez', 'name':language(90210).encode("utf-8"), 'image': logoBaseURL+'/ss/star_pravah.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=1138'})
        listItems.append({'provider':'desirulez', 'name':language(90211).encode("utf-8"), 'image': logoBaseURL+'/zz/zee_zing_asia.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=00'})
        listItems.append({'provider':'desirulez', 'name':language(90212).encode("utf-8"), 'image': logoBaseURL+'/mm/mtv_india.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=339'})
        listItems.append({'provider':'desirulez', 'name':language(90213).encode("utf-8"), 'image': logoBaseURL+'/cc/channel_v_in.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=633'})
        listItems.append({'provider':'desirulez', 'name':language(90214).encode("utf-8"), 'image': logoBaseURL+'/uu/utv_bindass.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=504'})
        listItems.append({'provider':'desirulez', 'name':language(90215).encode("utf-8"), 'image': logoBaseURL+'/uu/utv_stars.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=1274'})
        listItems.append({'provider':'desirulez', 'name':language(90216).encode("utf-8"), 'image': logoBaseURL+'/pp/pogo.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=500'})
        listItems.append({'provider':'desirulez', 'name':language(90217).encode("utf-8"), 'image': logoBaseURL+'/dd/disney_channel_in.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=479'})
        listItems.append({'provider':'desirulez', 'name':language(90218).encode("utf-8"), 'image': logoBaseURL+'/hh/hungama.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=472'})
        listItems.append({'provider':'desirulez', 'name':language(90219).encode("utf-8"), 'image': logoBaseURL+'/cc/cartoon_network_in.png', 'action': 'desi_tv_channel', 'url':'forumdisplay.php?f=509'})
        Index().homeList(listItems)

class Index:
    def __init__(self):
        print "Initialized"
    def infoDialog(self, str, header=addonName, time=3000):
        try: xbmcgui.Dialog().notification(header, str, self.addonArt('icon.png'), time, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, %s, %s)" % (header, str, time, self.addonArt('icon.png')))

    def addonArt(self, image):
        if image.startswith('http'):
            return image
        art = os.path.join(addonPath, 'resources/art')
        image = os.path.join(art, image)
        return image
        
    def setContainerView(self, contentType, view=None):
        if contentType == 'HOME':
            view = 500
        elif contentType == 'MOVIES':
            view = 500
        elif contentType == 'TVSHOWS' :
            view = 502
        xbmc.executebuiltin('Container.SetViewMode(%s)' % view)
        
    def homeList(self, homeList):
        if homeList == None or len(homeList) == 0: return
        
        total = len(homeList)
        for i in homeList:
            try:
                try: name = language(i['name']).encode("utf-8")
                except: name = i['name']
                
                action = i['action']
                try: image = self.addonArt(i['image'])
                except: image = i['image']

                u = '%s?action=%s' % (sys.argv[0], action)
                try: u += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass
                
                try: u += '&provider=%s' % urllib.quote_plus(i['provider'])
                except: pass
                
                try: u += '&name=%s' % urllib.quote_plus(i['name'])
                except: pass
                
                cm = []
                replaceItems = False

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo(type="Video", infoLabels={"Label": name, "Title": name, "Plot": addonDesc})
                item.setProperty("Fanart_Image", image)
                
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
                
            except:
                pass
        self.setContainerView('HOME')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
    def movieList(self, movieList, nextAction=None):
        if movieList == None or len(movieList) == 0: return
        
        addonPoster = self.addonArt('movie_poster.png')
        addonFanart = self.addonArt('fanart.jpg')
        
        total = len(movieList)
        for i in movieList:
            try:
                name, title, year, imdb, genre, url, poster, fanart, studio, duration, rating, votes, mpaa, director, plot, plotoutline, tagline = i['name'], i['title'], i['year'], i['imdb'], i['genre'], i['url'], i['poster'], i['fanart'], i['studio'], i['duration'], i['rating'], i['votes'], i['mpaa'], i['director'], i['plot'], i['plotoutline'], i['tagline']

                if poster == '0': poster = addonPoster
                if fanart == '0': fanart = addonFanart
                if duration == '0': duration == '120'

                sysname, systitle, sysyear, sysimdb, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(url), urllib.quote_plus(poster)

                meta = {'title': title, 'year': year, 'imdb_id' : 'tt' + imdb, 'genre' : genre, 'poster' : poster, 'fanart' : fanart, 'studio' : studio, 'duration' : duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'plot': plot, 'plotoutline': plotoutline, 'tagline': tagline, 'trailer': '%s?action=trailer&name=%s' % (sys.argv[0], sysname)}
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')
                sysmeta = urllib.quote_plus(json.dumps(meta))

                u = '%s?action=get_host&name=%s&title=%s&year=%s&imdb=%s&url=%s&meta=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl, sysmeta)
                isFolder = True
                
                cm = []
                cm.append((language(30412).encode('utf-8'), 'Action(Info)'))
                item = xbmcgui.ListItem(label=name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                try: item.setArt({'poster': poster, 'banner': poster})
                except: pass
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                #item.setProperty("Video", "true")
                #item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=isFolder)
            except:
                import traceback
                traceback.print_exc()
                pass

        try:
            if nextAction == None: nextAction = 'movie_list'
            next = movieList[0]['next']
            if next == '': raise Exception()
            name, url, image = 'Next', next, self.addonArt('next.png')
            if getSetting("appearance") == '-': image = 'DefaultFolder.png'
            u = '%s?action=%s&url=%s' % (sys.argv[0], str(nextAction), urllib.quote_plus(url))
            item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
            item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
            item.setProperty("Fanart_Image", addonFanart)
            item.addContextMenuItems([], replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)
        except:
            import traceback
            traceback.print_exc()
            pass

        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        self.setContainerView('MOVIES')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
    def moviesourceList(self, sourceList, name, imdb, tvdb, meta):
        if sourceList == None or len(sourceList) == 0: return

        total = len(sourceList)
        for i in sourceList:
            try:
                url, source, provider, quality = i['url'], i['source'], i['provider'], i['quality']
                poster, fanart = meta['poster'], meta['fanart']
                
                if not type(url) is str :
                    url = ",".join(url)
                sysname, sysimdb, systvdb, sysurl, syssource, sysprovider = urllib.quote_plus(name), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(url), urllib.quote_plus(source), urllib.quote_plus(provider)

                u = '%s?action=play_moviehost&name=%s&imdb=%s&tvdb=%s&url=%s&source=%s&provider=%s' % (sys.argv[0], sysname, sysimdb, systvdb, sysurl, syssource, sysprovider)
                
                cm = []
                cm.append((language(30412).encode("utf-8"), 'Action(Info)'))
                
                if not quality or quality == '':
                    item = xbmcgui.ListItem(name + ' | ' + provider + ' | [COLOR blue]'+ source.upper() + '[/COLOR]' , iconImage="DefaultVideo.png", thumbnailImage=poster)
                else :
                    item = xbmcgui.ListItem(name + ' | ' + provider + ' | [COLOR red]' + quality.upper() + '[/COLOR] | [COLOR blue] '+ source.upper() + '[/COLOR]' , iconImage="DefaultVideo.png", thumbnailImage=poster)
                try: item.setArt({'poster': poster, 'banner': poster})
                except: pass
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                import traceback
                traceback.print_exc()    
                pass

        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
    def showList(self, showList) :
        if showList == None or len(showList) == 0: return
        total = len(showList)
        addonPoster = ''
        addonBanner = ''
        addonFanart = ''
        for i in showList:
            try:
                name, title, year, imdb, tvdb, genre, url, poster, banner, fanart, studio, premiered, duration, rating, mpaa, plot = i['title'],  i['title'], i['year'], i['imdb'], i['tvdb'], i['genre'], i['url'], i['poster'], i['banner'], i['fanart'], i['studio'], i['premiered'], i['duration'], i['rating'], i['mpaa'], i['plot']

                if poster == '0': poster = addonPoster
                if banner == '0': banner = addonBanner
                if fanart == '0' or not getSetting("fanart") == 'true': fanart = addonFanart
                if duration == '0': duration = '30'

                systitle, sysyear, sysimdb, systvdb, sysurl, sysimage = urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(url), urllib.quote_plus(poster)

                meta = {'title': title, 'tvshowtitle': title, 'year': year, 'imdb_id' : 'tt' + imdb, 'tvdb_id': tvdb, 'genre' : genre, 'studio': studio, 'premiered': premiered, 'duration' : duration, 'rating' : rating, 'mpaa' : mpaa, 'plot': plot, 'trailer': '%s?action=trailer&name=%s' % (sys.argv[0], systitle)}
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                u = '%s?action=episodes&show=%s&year=%s&imdb=%s&tvdb=%s&url=%s' % (sys.argv[0], systitle, sysyear, sysimdb, systvdb, sysurl)
                try: u += '&provider=%s' % urllib.quote_plus(i['provider'])
                except: pass
                
                try:
                    match = [i for i in indicators if str(i['show']['ids']['tvdb']) == tvdb][0]
                    num_1 = 0
                    for i in range(0, len(match['seasons'])): num_1 += len(match['seasons'][i]['episodes'])
                    num_2 = int(match['show']['aired_episodes'])
                    if num_1 >= num_2: meta.update({'playcount': 1, 'overlay': 7})
                except:
                    pass

                cm = []
                cm.append((language(30413).encode("utf-8"), 'Action(Info)'))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=unwatched_shows&name=%s&year=%s&imdb=%s&tvdb=%s)' % (sys.argv[0], systitle, sysyear, sysimdb, systvdb)))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=watched_shows&name=%s&year=%s&imdb=%s&tvdb=%s)' % (sys.argv[0], systitle, sysyear, sysimdb, systvdb)))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                except: pass
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(tvshows)'):
                return Index().setContainerView('TVSHOWS', {'skin.confluence' : 500})
            xbmc.sleep(100)
    def episodeList(self, episodeList) :
        if episodeList == None or len(episodeList) == 0: return
        total = len(episodeList)
        
        for i in episodeList:
            try:
                show, title, url= i['show'], i['title'], i['url']

                duration = '30'

                sysshow, systitle, sysurl = urllib.quote_plus(show), urllib.quote_plus(title), urllib.quote_plus(url)

                meta = {'title': title, 'tvshowtitle': show, 'duration' : duration}
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                u = '%s?action=get_host&show=%s&title=%s&url=%s' % (sys.argv[0], sysshow, systitle, sysurl)
                
                item = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png")
                item.setInfo(type="Video", infoLabels = meta)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                import traceback
                traceback.print_exc()  
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(tvshows)'):
                return Index().setContainerView('TVSHOWS', {'skin.confluence' : 500})
            xbmc.sleep(100)
    def tvsourceList(self, sourceList, name, imdb, tvdb, meta):
        if sourceList == None or len(sourceList) == 0: return

        total = len(sourceList)
        imdb, tvdb = '', ''
        for i in sourceList:
            try:
                url, source, provider = i['url'], i['source'], i['provider']
                if not type(url) is str :
                    url = ",".join(url)
                if meta :
                    poster, banner, thumb, fanart = meta['poster'], meta['banner'], meta['thumb'], meta['fanart']
                else :
                    poster, banner, thumb, fanart = 'DefaultVideo.png','DefaultVideo.png','DefaultVideo.png','DefaultVideo.png'
                sysname, sysimdb, systvdb, sysurl, syssource, sysprovider = urllib.quote_plus(name), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(url), urllib.quote_plus(source), urllib.quote_plus(provider)

                u = '%s?action=play_tvhost&name=%s&imdb=%s&tvdb=%s&url=%s&source=%s&provider=%s' % (sys.argv[0], sysname, sysimdb, systvdb, sysurl, syssource, sysprovider)

                item = xbmcgui.ListItem(source, iconImage="DefaultVideo.png", thumbnailImage=thumb)
                try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                except: 
                    import traceback
                    traceback.print_exc()  
                    pass
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                import traceback
                traceback.print_exc()  
                pass

        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

class Links:
    def __init__(self):
        self.imdb_title = 'http://www.imdb.com/title/tt%s/'
        self.imdb_search = 'http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q=%s'

        self.tmdb_base = 'http://api.themoviedb.org'
        self.tmdb_key = base64.urlsafe_b64decode('MTdmMjI3YmVjNTdkOTQ4OGJiYzgyNzYyZmMxNDQ0NmM=') ## using my key kodi-plugin-aftershock 17f227bec57d9488bbc82762fc14446c
        self.tmdb_info = 'http://api.themoviedb.org/3/movie/tt%s?language=en&api_key=%s'
        self.tmdb_info2 = 'http://api.themoviedb.org/3/movie/%s?language=en&api_key=%s'
        self.tmdb_image = 'http://image.tmdb.org/t/p/original'
        self.tmdb_image2 = 'http://image.tmdb.org/t/p/w500'

        self.tvdb_base = 'http://thetvdb.com'
        self.tvdb_key = base64.urlsafe_b64decode('OUZDQkM2MjlEQzgyRjA4Qw==') ## using my key kodi-plugin-aftershock	9FCBC629DC82F08C
        self.tvdb_search = 'http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=tt%s&language=en'
        self.tvdb_search2 = 'http://thetvdb.com/api/GetSeries.php?seriesname=%s&language=en'
        self.tvdb_info = 'http://thetvdb.com/api/%s/series/%s/all/en.zip'
        self.tvdb_info2 = 'http://thetvdb.com/api/%s/series/%s/en.xml'
        self.tvdb_image = 'http://thetvdb.com/banners/'
        self.tvdb_image2 = 'http://thetvdb.com/banners/_cache/'

        self.eng_base = 'http://www.movie25.ag'
        self.eng_link_1 = 'http://www.movie25.ag'
        self.eng_link_2 = 'http://translate.googleusercontent.com/translate_c?anno=2&hl=en&sl=mt&tl=en&u=http://www.movie25.ag'
        self.eng_link_3 = 'https://movie25.unblocked.pw'
        self.eng_new_releases = '/new-releases/'
        self.eng_latest_added = '/latest-added/'
        self.eng_featured = '/featured-movies/'
        self.eng_popular = '/most-viewed/'
        self.eng_most_voted = '/most-voted/'
        self.eng_hd = '/latest-hd-movies/'
        
        self.desi_base = 'http://www.playindiafilms.com'
        self.desi_link_1 = 'http://www.playindiafilms.com'
        self.desi_link_2 = ''
        self.desi_link_3 = ''
        self.desi_new_releases = '/category/2015/feed'
        self.desi_latest_added = '/category/hindi-movies/feed'
        self.desi_hd = '/category/hindi-blurays/feed'
        
    def getUrl(self, url):
        return self.eng_base + '/' + url

class Trailer:
    def __init__(self):
        print "Trailer Initialized"
    def dummy():
        print "hello"

class Movies:
    def __init__(self):
        self.list = []
        print "Movies Initialized"
    def featured(self):
        url = Links().eng_featured
        self.list = self.scn_list(url)
        Index().movieList(self.list)
    def HD(self):
        url = Links().eng_hd
        self.list = self.scn_list(url)
        Index().movieList(self.list)
    def latestAdded(self):
        url = Links().eng_latest_added
        self.list = self.scn_list(url)
        Index().movieList(self.list)
    def newReleases(self):
        url = Links().eng_new_releases
        self.list = self.scn_list(url)
        Index().movieList(self.list)
    def mostViewed(self):
        url = Links().eng_popular
        self.list = self.scn_list(url)
        Index().movieList(self.list)
    def mostVoted(self):
        url = Links().eng_most_voted
        self.list = self.scn_list(url)
        Index().movieList(self.list)
    def moviesList(self, url):
        self.list = self.scn_list(url)
        Index().movieList(self.list)
    def cleantitle_movie(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title    
    def desiNewReleases(self):
        url = Links().desi_new_releases
        self.list = self.desi_full_list(url)
        Index().movieList(self.list, 'desi_movie_list')
    def desiLatestAdded(self):
        url = Links().desi_latest_added
        self.list = self.desi_full_list(url)
        Index().movieList(self.list,'desi_movie_list')
    def desiHD(self):
        url = Links().desi_hd
        self.list = self.desi_full_list(url)
        Index().movieList(self.list,'desi_movie_list')

    def desi_movie_list(self, url):
        self.list = self.desi_full_list(url)
        Index().movieList(self.list,'desi_movie_list')
    def scn_list(self, url):
        try:
            result = ''
            try: url = re.compile('//.+?(/.+)').findall(url)[0]
            except: pass
            links = [Links().eng_link_1, Links().eng_link_2, Links().eng_link_3]
            for base_link in links:
                try: result = getUrl(base_link + url).result
                except: result = ''
                if 'movie_table' in result: break

            result = result.decode('iso-8859-1').encode('utf-8')
            movies = common.parseDOM(result, "div", attrs = { "class": "movie_table" })
        except:
            return
        
        try:
            next = common.parseDOM(result, "div", attrs = { "class": "count_text" })[0]
            next = re.compile('(<a.+?</a>)').findall(next)
            next = [i for i in next if '>Next<' in i][-1]
            next = re.compile('href=(.+?)>').findall(next)[-1]
            next = re.sub('\'|\"','', next)
            next = common.replaceHTMLCodes(next)
            try: next = urlparse.parse_qs(urlparse.urlparse(next).query)['u'][0]
            except: pass
            next = urlparse.urljoin(Links().eng_base, next)
            next = next.encode('utf-8')
        except:
            next = ''
            
        for movie in movies:
            
            try:
                title = common.parseDOM(movie, "a", ret="title")[0]
                title = re.compile('(.+?) [(]\d{4}[)]$').findall(title)[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                
                year = common.parseDOM(movie, "a", ret="title")[0]
                year = re.compile('.+? [(](\d{4})[)]$').findall(year)[0]
                year = year.encode('utf-8')

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = common.parseDOM(movie, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
                except: pass
                url = urlparse.urljoin(Links().eng_base, url)
                url = url.encode('utf-8')

                poster = '0'
                try: poster = common.parseDOM(movie, "img", ret="src")[0]
                except: pass
                poster = common.replaceHTMLCodes(poster)
                try: poster = urlparse.parse_qs(urlparse.urlparse(poster).query)['u'][0]
                except: pass
                poster = poster.encode('utf-8')

                genre = common.parseDOM(movie, "div", attrs = { "class": "movie_about_genre" })
                genre = common.parseDOM(genre, "a")
                genre = " / ".join(genre)
                if genre == '': genre = '0'
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': '0000000', 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'date': '0', 'genre': genre, 'url': '0', 'poster': poster, 'fanart': '0', 'studio': '0', 'duration': '0', 'rating': '0', 'votes': '0', 'mpaa': '0', 'director': '0', 'plot': '0', 'plotoutline': '0', 'tagline': '0', 'next': next})
            except:
                pass
        
        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.imdb_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]
        
        
        self.list = [i for i in self.list if not i['imdb'] == '0000000']

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.tmdb_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]
        
        return self.list
    def desi_full_list(self, url):
        tmpList = []
        turl = url 
        pagesScanned = 0
        while((len(tmpList) < 15) and (pagesScanned < 10)):
            tmpList = self.desi_list(turl)
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
        self.list = tmpList 
        return self.list
        
    def desi_list(self, url):
        try:
            result = ''
            try: url = re.compile('//.+?(/.+)').findall(url)[0]
            except: pass
            links = [Links().desi_link_1, Links().desi_link_2, Links().desi_link_3]
            for base_link in links:
                try: result = getUrl(base_link + url).result
                except: result = ''
                if 'item' in result: break

            result = result.decode('iso-8859-1').encode('utf-8')
            movies = common.parseDOM(result, "item")
        except:
            return
        
        next = ''
        for movie in movies:
            try:
                title = common.parseDOM(movie, "title")[0]
                title = re.compile('(.+?) [(]\d{4}[)]$').findall(title)[0]
                title = common.replaceHTMLCodes(title)
                try : title = title.encode('utf-8')
                except: pass

                year = common.parseDOM(movie, "title")[0]
                year = re.compile('.+? [(](\d{4})[)]$').findall(year)[0]
                year = year.encode('utf-8')

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = common.parseDOM(movie, "link")[0]
                url = common.replaceHTMLCodes(url)
                try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
                except: pass
                url = urlparse.urljoin(Links().eng_base, url)
                url = url.encode('utf-8')
                
                poster = '0'
                try: poster = common.parseDOM(movie, "img", ret="src")[0]
                except: pass
                poster = common.replaceHTMLCodes(poster)
                try: poster = urlparse.parse_qs(urlparse.urlparse(poster).query)['u'][0]
                except: pass
                poster = poster.encode('utf-8')

                genre = common.parseDOM(movie, "div", attrs = { "class": "movie_about_genre" })
                genre = common.parseDOM(genre, "a")
                genre = " / ".join(genre)
                if genre == '': genre = '0'
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')
                
                hindiMovie = False
                categories = []
                try: categories = common.parseDOM(movie, "category")
                except : 
                    hindiMovie = True
                    pass
                
                for category in categories:
                    if re.search('Hindi', category, flags= re.I):
                        hindiMovie = True
                if hindiMovie :
                    self.list.append({'name': name, 'title': title, 'year': year, 'imdb': '0000000', 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'date': '0', 'genre': genre, 'url': '0', 'poster': poster, 'fanart': '0', 'studio': '0', 'duration': '0', 'rating': '0', 'votes': '0', 'mpaa': '0', 'director': '0', 'plot': '0', 'plotoutline': '0', 'tagline': '0', 'next': next})
            except:
                import traceback
                traceback.print_exc()
                pass
        
        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.imdb_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]
        
        
        self.list = [i for i in self.list if not i['imdb'] == '0000000']

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.tmdb_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]
        return self.list
    def imdb_info(self, i):
        try:
            match = []
            title = self.list[i]['title']
            year = self.list[i]['year']
            url = Links().imdb_search % urllib.quote_plus(title)
            result = getUrl(url, timeout='30').result
            result = common.replaceHTMLCodes(result)
            result = json.loads(result)
            for x in result.keys(): match += result[x]

            title = self.cleantitle_movie(title)
            years = [str(year), str(int(year)+1), str(int(year)-1)]
            match = [x for x in match if title == self.cleantitle_movie(x['title'])]
            match = [x for x in match if any(x['title_description'].startswith(y) for y in years)][0]

            title = match['title']
            if title == '' or title == None: title = '0'
            title = common.replaceHTMLCodes(title)
            title = title.encode('utf-8')
            if not title == '0': self.list[i].update({'title': title})

            year = match['title_description']
            year = re.sub('[^0-9]', '', str(year))[:4]
            self.list[i].update({'year': year})

            name = '%s (%s)' % (self.list[i]['title'], self.list[i]['year'])
            try: name = name.encode('utf-8')
            except: pass
            self.list[i].update({'name': name})

            imdb = match['id']
            imdb = re.sub('[^0-9]', '', str(imdb))
            imdb = imdb.encode('utf-8')
            self.list[i].update({'imdb': imdb})

            url = Links().imdb_title % imdb
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            self.list[i].update({'url': url})
        except:
            pass
    def tmdb_info(self, i):
        try:
            url = Links().tmdb_info % (self.list[i]['imdb'], Links().tmdb_key)
            result = getUrl(url, timeout='10').result
            result = json.loads(result)

            title = result['title']
            if title == '' or title == None: title = '0'
            title = common.replaceHTMLCodes(title)
            title = title.encode('utf-8')
            if not title == '0': self.list[i].update({'title': title})

            try: year = str(result['release_date'])
            except: year = '0000'
            year = re.compile('(\d{4})').findall(year)[0]
            year = year.encode('utf-8')
            if not year == '0000': self.list[i].update({'year': year})

            poster = result['poster_path']
            if poster == '' or poster == None: poster = '0'
            if not poster == '0': poster = '%s%s' % (Links().tmdb_image2, poster)
            poster = common.replaceHTMLCodes(poster)
            poster = poster.encode('utf-8')
            if not poster == '0': self.list[i].update({'poster': poster})

            fanart = result['backdrop_path']
            if fanart == '' or fanart == None: fanart = '0'
            if not fanart == '0': fanart = '%s%s' % (Links().tmdb_image, fanart)
            fanart = common.replaceHTMLCodes(fanart)
            fanart = fanart.encode('utf-8')
            if not fanart == '0': self.list[i].update({'fanart': fanart})

            genre = result['genres']
            try: genre = [x['name'] for x in genre]
            except: genre = '0'
            if genre == '' or genre == None or genre == []: genre = '0'
            genre = " / ".join(genre)
            genre = common.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')
            if not genre == '0': self.list[i].update({'genre': genre})

            studio = result['production_companies']
            try: studio = [x['name'] for x in studio][0]
            except: studio = '0'
            if studio == '' or studio == None: studio = '0'
            studio = common.replaceHTMLCodes(studio)
            studio = studio.encode('utf-8')
            if not studio == '0': self.list[i].update({'studio': studio})

            try: duration = str(result['runtime'])
            except: duration = '0'
            if duration == '' or duration == None or not self.list[i]['duration'] == '0': duration = '0'
            duration = common.replaceHTMLCodes(duration)
            duration = duration.encode('utf-8')
            if not duration == '0': self.list[i].update({'duration': duration})

            rating = str(result['vote_average'])
            if rating == '' or rating == None or not self.list[i]['rating'] == '0': rating = '0'
            rating = common.replaceHTMLCodes(rating)
            rating = rating.encode('utf-8')
            if not rating == '0': self.list[i].update({'rating': rating})

            votes = str(result['vote_count'])
            try: votes = str(format(int(votes),',d'))
            except: pass
            if votes == '' or votes == None or not self.list[i]['votes'] == '0': votes = '0'
            votes = common.replaceHTMLCodes(votes)
            votes = votes.encode('utf-8')
            if not votes == '0': self.list[i].update({'votes': votes})

            plot = result['overview']
            if plot == '' or plot == None: plot = '0'
            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
            if not plot == '0': self.list[i].update({'plot': plot})

            tagline = result['tagline']
            if (tagline == '' or tagline == None) and not plot == '0': tagline = plot.split('.', 1)[0]
            elif tagline == '' or tagline == None: tagline = '0'
            tagline = common.replaceHTMLCodes(tagline)
            tagline = tagline.encode('utf-8')
            if not tagline == '0': self.list[i].update({'tagline': tagline})
        except:
            pass

class Shows:
    def __init__(self):
        self.list = []
        
    def cleantitle_tv(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU|\d{4})(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    
    def getShows(self, url, name, provider):
        try :
            commonsource = getattr(commonsources, provider)()
            self.list = commonsource.get_shows(name, url)
            
            threads = []
            for i in range(0, len(self.list)): threads.append(Thread(self.tvdb_info, i))
            
            [i.start() for i in threads]
            [i.join() for i in threads]

            Index().showList(self.list)
            return self.list
        except:
            import traceback
            traceback.print_exc()  
            return 
    
    def getEpisodes(self, url, show, provider):
        try :
            commonsource = getattr(commonsources, provider)()
            self.list = commonsource.get_episodes(show, url)
            Index().episodeList(self.list)
            return self.list
        except:
            import traceback
            traceback.print_exc()  
            return 
    def tvdb_info(self, i):

        try:
            try: sid = self.list[i]['tvdb']
            except: sid = '0'
            
            if sid == '0':
                url = Links().tvdb_search % self.list[i]['imdb']
                result = getUrl(url, timeout='10').result

                try: name = common.parseDOM(result, "SeriesName")[0]
                except: name = '0'
                dupe = re.compile('[***]Duplicate (\d*)[***]').findall(name)

                year = self.list[i]['year']
                years = [str(year), str(int(year)+1), str(int(year)-1)]

                if len(dupe) > 0:
                    sid = str(dupe[0])
                elif name == '0':
                    show = self.list[i]['title']
                    title = self.cleantitle_tv(show)
                    url = Links().tvdb_search2 % urllib.quote_plus(show)
                    result = getUrl(url, timeout='10').result
                    result = common.replaceHTMLCodes(result)
                    result = common.parseDOM(result, "Series")
                    if result :
                        result = [x for x in result if title == self.cleantitle_tv(common.parseDOM(x, "SeriesName")[0])]
                        result = [x for x in result if any(y in common.parseDOM(x, "FirstAired")[0] for y in years)][0]
                
                if result:
                    sid = common.parseDOM(result, "seriesid")[0]


            url = Links().tvdb_info2 % (Links().tvdb_key, sid)
            
            result = getUrl(url, timeout='10').result

            tvdb = common.parseDOM(result, "id")[0]
            if tvdb == '': tvdb = '0'
            tvdb = common.replaceHTMLCodes(tvdb)
            tvdb = tvdb.encode('utf-8')
            if not tvdb == '0': self.list[i].update({'tvdb': tvdb})

            try: poster = common.parseDOM(result, "poster")[0]
            except: poster = ''
            if not poster == '': poster = Links().tvdb_image + poster
            else: poster = '0'
            poster = common.replaceHTMLCodes(poster)
            poster = poster.encode('utf-8')

            try: banner = common.parseDOM(result, "banner")[0]
            except: banner = ''
            if not banner == '': banner = Links().tvdb_image + banner
            else: banner = '0'
            banner = common.replaceHTMLCodes(banner)
            banner = banner.encode('utf-8')

            try: fanart = common.parseDOM(result, "fanart")[0]
            except: fanart = ''
            if not fanart == '': fanart = Links().tvdb_image + fanart
            else: fanart = '0'
            fanart = common.replaceHTMLCodes(fanart)
            fanart = fanart.encode('utf-8')
            if not fanart == '0': self.list[i].update({'fanart': fanart})

            if not poster == '0': self.list[i].update({'poster': poster})
            elif not fanart == '0': self.list[i].update({'poster': fanart})
            elif not banner == '0': self.list[i].update({'poster': banner})

            if not banner == '0': self.list[i].update({'banner': banner})
            elif not fanart == '0': self.list[i].update({'banner': fanart})
            elif not poster == '0': self.list[i].update({'banner': poster})

            try: genre = common.parseDOM(result, "Genre")[0]
            except: genre = ''
            genre = [x for x in genre.split('|') if not x == '']
            genre = " / ".join(genre)
            if genre == '': genre = '0'
            genre = common.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')
            if not genre == '0': self.list[i].update({'genre': genre})

            try: studio = common.parseDOM(result, "Network")[0]
            except: studio = ''
            if studio == '': studio = '0'
            studio = common.replaceHTMLCodes(studio)
            studio = studio.encode('utf-8')
            if not studio == '0': self.list[i].update({'studio': studio})

            try: premiered = common.parseDOM(result, "FirstAired")[0]
            except: premiered = ''
            if premiered == '': premiered = '0'
            premiered = common.replaceHTMLCodes(premiered)
            premiered = premiered.encode('utf-8')
            if not premiered == '0': self.list[i].update({'premiered': premiered})

            try: duration = common.parseDOM(result, "Runtime")[0]
            except: duration = ''
            if duration == '': duration = '0'
            duration = common.replaceHTMLCodes(duration)
            duration = duration.encode('utf-8')
            if not duration == '0': self.list[i].update({'duration': duration})

            try: rating = common.parseDOM(result, "Rating")[0]
            except: rating = ''
            if rating == '' or not self.list[i]['rating'] == '0': rating = '0'
            rating = common.replaceHTMLCodes(rating)
            rating = rating.encode('utf-8')
            if not rating == '0': self.list[i].update({'rating': rating})

            try: mpaa = common.parseDOM(result, "ContentRating")[0]
            except: mpaa = ''
            if mpaa == '': mpaa = '0'
            mpaa = common.replaceHTMLCodes(mpaa)
            mpaa = mpaa.encode('utf-8')
            if not mpaa == '0': self.list[i].update({'mpaa': mpaa})

            try: plot = common.parseDOM(result, "Overview")[0]
            except: plot = ''
            if plot == '': plot = '0'
            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
            if not plot == '0': self.list[i].update({'plot': plot})
        except:
            pass


class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)

class resolver:
    def __init__(self):
        self.sources = []
        self.hosthdfullDict = []
        self.hostsdfullDict = []
        self.hostlocDict = []
        
    def get_host(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url, meta):
        try:
            if show == None: content = 'movie'
            else: content = 'episode'

            self.sources = self.sources_get(name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url)
            if self.sources == []: raise Exception()
            self.sources = self.sources_filter() #For only displaying supported sources
            if meta : meta = json.loads(meta)

            if content == 'movie': 
                Index().moviesourceList(self.sources, name, imdb, '0', meta)
            else:
                Index().tvsourceList(self.sources, title, imdb, tvdb, meta)
        except:
            import traceback
            traceback.print_exc()
            Index().infoDialog(language(30308).encode("utf-8"))
            return
    def sources_get(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url):
        try :
            import inspect
            sourceDict = inspect.getmembers(commonsources, inspect.isclass)
            sourceDict = [i for i in sourceDict if hasattr(i[1], 'get_sources')]
            if show == None: content = 'movie'
            else: content = 'episode'

            if content == 'movie':
                sourceDict = [str(i[0]) for i in sourceDict if hasattr(i[1], 'get_movie')]
                sourceDict = [(i, 'true') for i in sourceDict]
            else:
                sourceDict = [str(i[0]) for i in sourceDict if hasattr(i[1], 'get_show')]
                sourceDict = [(i, 'true') for i in sourceDict]
            
            global global_sources
            global_sources = []
            
            threads = []
            sourceDict = [i[0] for i in sourceDict if i[1] == 'true']
            
            if content == 'movie':
                title = self.normaltitle(title)
                for source in sourceDict: threads.append(Thread(self.sources_movie, name, title, year, imdb, source))
            else:
                for source in sourceDict: threads.append(Thread(self.sources_tv, name, title, url, source))


            timeout = 10
            
            [i.start() for i in threads]

            for i in range(0, timeout * 2):
                is_alive = [x.is_alive() for x in threads]
                if all(x == False for x in is_alive): break
                time.sleep(0.5)

            for i in range(0, 5 * 2):
                is_alive = len([i for i in threads if i.is_alive() == True])
                if is_alive < 10: break
                time.sleep(0.5)
            self.sources = global_sources
            return self.sources
        except:
            import traceback
            traceback.print_exc()
            Index().infoDialog(language(30308).encode("utf-8"))
            return
        
    
    def sources_movie(self, name, title, year, imdb, source):
        quality = ''
        try:
            commonsource = getattr(commonsources, source)()
            url = None
            if url == None: url = commonsource.get_movie(imdb, title, year)
            if url == None: raise Exception()
            if type(url) is dict:
                quality = url['quality']
                url = url['url']
        except:
            import traceback
            traceback.print_exc()
            pass
        
        try:
            sources = []
            
            sources = commonsource.get_sources(url, self.hosthdfullDict, self.hostsdfullDict, self.hostlocDict, quality=quality)
            if sources == None: sources = []
            global_sources.extend(sources)
        except:
            import traceback
            traceback.print_exc()    
            pass
    def sources_tv(self, name, title, url, source):
        quality = ''
        try:
            commonsource = getattr(commonsources, source)()
            if url == None: url = commonsource.get_show(imdb, title, year)
            if url == None: raise Exception()
            if type(url) is dict:
                quality = url['quality']
                url = url['url']
        except:
            import traceback
            traceback.print_exc()
            pass
        
        try:
            sources = []
            
            sources = commonsource.get_sources(url, self.hosthdfullDict, self.hostsdfullDict, self.hostlocDict, quality=quality)
            if sources == None: sources = []
            global_sources.extend(sources)
        except:
            import traceback
            traceback.print_exc()    
            pass
    
    def sources_filter(self):
        try :
            supportedDict = ['GVideo', 'VK', 'Videomega', 'Sweflix', 'Muchmovies', 'YIFY', 'Einthusan', 'Movreel', '180upload', 'Mightyupload', 'Clicknupload', 'Tusfiles', 'Grifthost', 'Openload', 'Uptobox', 'Primeshare', 'iShared', 'Vidplay', 'Xfileload', 'Mrfile', 'Ororo', 'Animeultima','Allmyvideos', 'VodLocker']
            excludeDict = ['embed upload', 'vidgg']
            for i in range(len(self.sources)): 
                if not self.sources[i]['provider'].lower() == 'DesiRulez'.lower():
                    self.sources[i]['source'] = self.sources[i]['source'].lower()
            self.sources = sorted(self.sources, key=itemgetter('source'))
            
            filter = []
            for host in supportedDict: 
                filter += [i for i in self.sources if i['source'] == host.lower()]
            filter += [i for i in self.sources if i['provider'].lower() == 'PlayIndiaFilms'.lower()]
            filter += [i for i in self.sources if i['provider'].lower() == 'DesiRulez'.lower()]
            
            for i in filter:
                for j in excludeDict:
                    if i['provider'].lower() == 'DesiRulez'.lower() and j in i['source'].lower() :
                        filter.pop(filter.index(i))
            self.sources = filter
            
        except:
            import traceback
            traceback.print_exc()    
            pass
        return self.sources

    def normaltitle(self, title):
        try:
            try: return title.decode('ascii').encode("utf-8")
            except: pass

            import unicodedata
            t = ''
            for i in title:
                c = unicodedata.normalize('NFKD',unicode(i,"ISO-8859-1"))
                c = c.encode("ascii","ignore").strip()
                if i == ' ': c = i
                t += c

            return t.encode("utf-8")
        except:
            return title
    def play_host(self, content, name, imdb, tvdb, url, source, provider):
        try:
            url = self.sources_resolve(url, provider)
            if url == None: raise Exception()

            if getSetting("playback_info") == 'true':
                Index().infoDialog(source, header=name)

            player().run(content, name, url, imdb, tvdb)
            return url
        except:
            Index().infoDialog(language(30308).encode("utf-8"))
            return
    def sources_resolve(self, url, provider):
        try:
            provider = provider.lower()
            commonsource = getattr(commonsources, provider)()
            url = commonsource.resolve(url)
            return url
        except:
            return
class player(xbmc.Player):
    def __init__ (self):
        self.folderPath = xbmc.getInfoLabel('Container.FolderPath')
        self.loadingStarting = time.time()
        xbmc.Player.__init__(self)
        
    def run(self, content, name, url, imdb, tvdb):
        try :
            print 'Content [%s] Name [%s] url [%s] imdb [%s] tvdb [%s]' % (content, name, url, imdb, tvdb)
            self.video_info(content, name, imdb, tvdb)
            self.resume_info()
            thumb = ''
            
            if self.folderPath.startswith(sys.argv[0]):
                if type(url) is str:
                    tUrl = url.split(',')
                    if len(tUrl) > 0:
                        url = tUrl
                    else:
                        url = [url]
                try :
                    if self.content == 'movie':
                            meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["title", "originaltitle", "year", "genre", "studio", "country", "runtime", "rating", "votes", "mpaa", "director", "writer", "plot", "plotoutline", "tagline", "thumbnail", "file"]}, "id": 1}' % (self.year, str(int(self.year)+1), str(int(self.year)-1)))
                            meta = unicode(meta, 'utf-8', errors='ignore')
                            meta = json.loads(meta)['result']['movies']
                            self.meta = [i for i in meta if i['file'].endswith(self.file)][0]

                            meta = {'title': self.meta['title'], 'originaltitle': self.meta['originaltitle'], 'year': self.meta['year'], 'genre': str(" / ".join(self.meta['genre'])), 'studio' : str(" / ".join(self.meta['studio'])), 'country' : str(" / ".join(self.meta['country'])), 'duration' : self.meta['runtime'], 'rating': self.meta['rating'], 'votes': self.meta['votes'], 'mpaa': self.meta['mpaa'], 'director': str(" / ".join(self.meta['director'])), 'writer': str(" / ".join(self.meta['writer'])), 'plot': self.meta['plot'], 'plotoutline': self.meta['plotoutline'], 'tagline': self.meta['tagline']}

                            thumb = self.meta['thumbnail']
                            poster = thumb
                except :
                    poster, thumb, meta = '', '', {'title': self.name}
                
                playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                playList.clear()
                
                i = 0
                for urlItem in url:
                    i = i+1
                    item = xbmcgui.ListItem(name + ' Part #' + str(i), path=urlItem,thumbnailImage=thumb)
                    try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster})
                    except: pass
                    try :
                        meta['title'] = item.getLabel()
                        item.setInfo(type="Video", infoLabels = meta)
                    except : 
                        pass
                    playList.add(urlItem, item)
                
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
                self.play(playList)   
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
            else:
                try:
                    if self.content == 'movie':
                        meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["title", "originaltitle", "year", "genre", "studio", "country", "runtime", "rating", "votes", "mpaa", "director", "writer", "plot", "plotoutline", "tagline", "thumbnail", "file"]}, "id": 1}' % (self.year, str(int(self.year)+1), str(int(self.year)-1)))
                        meta = unicode(meta, 'utf-8', errors='ignore')
                        meta = json.loads(meta)['result']['movies']
                        self.meta = [i for i in meta if i['file'].endswith(self.file)][0]

                        meta = {'title': self.meta['title'], 'originaltitle': self.meta['originaltitle'], 'year': self.meta['year'], 'genre': str(" / ".join(self.meta['genre'])), 'studio' : str(" / ".join(self.meta['studio'])), 'country' : str(" / ".join(self.meta['country'])), 'duration' : self.meta['runtime'], 'rating': self.meta['rating'], 'votes': self.meta['votes'], 'mpaa': self.meta['mpaa'], 'director': str(" / ".join(self.meta['director'])), 'writer': str(" / ".join(self.meta['writer'])), 'plot': self.meta['plot'], 'plotoutline': self.meta['plotoutline'], 'tagline': self.meta['tagline']}

                        thumb = self.meta['thumbnail']
                        poster = thumb

                    elif self.content == 'episode':
                        meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["title", "season", "episode", "showtitle", "firstaired", "runtime", "rating", "director", "writer", "plot", "thumbnail", "file"]}, "id": 1}' % (self.season, self.episode))
                        meta = unicode(meta, 'utf-8', errors='ignore')
                        meta = json.loads(meta)['result']['episodes']
                        self.meta = [i for i in meta if i['file'].endswith(self.file)][0]

                        meta = {'title': self.meta['title'], 'season' : self.meta['season'], 'episode': self.meta['episode'], 'tvshowtitle': self.meta['showtitle'], 'premiered' : self.meta['firstaired'], 'duration' : self.meta['runtime'], 'rating': self.meta['rating'], 'director': str(" / ".join(self.meta['director'])), 'writer': str(" / ".join(self.meta['writer'])), 'plot': self.meta['plot']}

                        thumb = self.meta['thumbnail']

                        poster = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter": {"field": "title", "operator": "is", "value": "%s"}, "properties": ["thumbnail"]}, "id": 1}' % self.meta['showtitle'])
                        poster = unicode(poster, 'utf-8', errors='ignore')
                        poster = json.loads(poster)['result']['tvshows'][0]['thumbnail']

                except:
                    poster, thumb, meta = '', '', {'title': self.name}

                tUrl = url.split(',')
                if len(tUrl) > 0:
                    url = tUrl
                else:
                    url = [url]
                
                playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                playList.clear()
                
                i = 0
                for urlItem in url:
                    i = i+1
                    item = xbmcgui.ListItem(path=urlItem, iconImage="DefaultVideo.png", thumbnailImage=thumb)
                    try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster})
                    except: pass
                    if len(url) > 1:
                        meta['title'] = meta['title'] + ' Part #' + str(i)
                    item.setInfo(type="Video", infoLabels = meta)
                    playList.add(urlItem, item)
                
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
                self.play(playList)   

            for i in range(0, 240):
                if self.isPlayingVideo(): break
                xbmc.sleep(1000)
            while self.isPlayingVideo():
                try: self.totalTime = self.getTotalTime()
                except: pass
                try: self.currentTime = self.getTime()
                except: pass
                xbmc.sleep(1000)
            time.sleep(5)
        except:
            import traceback
            traceback.print_exc()
            pass

        
    def video_info(self, content, name, imdb, tvdb):
        try:
            self.name = name
            self.content = content
            self.totalTime = 0
            self.currentTime = 0
            self.file = self.name + '.strm'
            self.file = self.file.translate(None, '\/:*?"<>|').strip('.')
            self.imdb = re.sub('[^0-9]', '', imdb)
            if tvdb == None: tvdb = '0'
            self.tvdb = tvdb

            if self.content == 'movie':
                self.title, self.year = re.compile('(.+?) [(](\d{4})[)]$').findall(self.name)[0]

            elif self.content == 'episode':
                self.show, self.season, self.episode = re.compile('(.+?) S(\d*)E(\d*)$').findall(self.name)[0]
                self.season, self.episode = '%01d' % int(self.season), '%01d' % int(self.episode)
        except:
            pass
    
    def resume_info(self):
        try:
            self.offset = '0'
            if not getSetting("resume_playback") == 'true': return

            import hashlib
            n = (hashlib.md5())
            n.update(str(self.name))
            n = str(n.hexdigest())
            i = 'tt' + self.imdb
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM points WHERE name = '%s' AND imdb_id = '%s'" % (n, i))
            match = dbcur.fetchone()
            self.offset = str(match[2])
            dbcon.commit()
        except:
            pass

        try:
            if self.offset == '0': return

            minutes, seconds = divmod(float(self.offset), 60)
            hours, minutes = divmod(minutes, 60)
            offset_time = '%02d:%02d:%02d' % (hours, minutes, seconds)

            yes = index().yesnoDialog('%s %s' % (language(30342).encode("utf-8"), offset_time), '', self.name, language(30343).encode("utf-8"), language(30344).encode("utf-8"))
            if not yes: self.offset = '0'
        except:
            pass

    def change_watched(self):
        if self.content == 'movie':
            try:
                if self.folderPath.startswith(sys.argv[0]): raise Exception()
                xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %s, "playcount" : 1 }, "id": 1 }' % str(self.meta['movieid']))
                index().container_refresh()
            except:
                pass

            try:
                if not self.folderPath.startswith(sys.argv[0]): raise Exception()
                from metahandler import metahandlers
                metaget = metahandlers.MetaData(preparezip=False)
                metaget.get_meta('movie', self.title ,year=self.year)
                metaget.change_watched(self.content, '', self.imdb, season='', episode='', year='', watched=7)
            except:
                pass

            
        elif self.content == 'episode':
            try:
                if self.folderPath.startswith(sys.argv[0]): raise Exception()
                xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %s, "playcount" : 1 }, "id": 1 }' % str(self.meta['episodeid']))
                index().container_refresh()
            except:
                pass

            try:
                if not self.folderPath.startswith(sys.argv[0]): raise Exception()
                from metahandler import metahandlers
                metaget = metahandlers.MetaData(preparezip=False)
                metaget.get_meta('tvshow', self.show, imdb_id=self.imdb)
                metaget.get_episode_meta(self.show, self.imdb, self.season, self.episode)
                metaget.change_watched(self.content, '', self.imdb, season=self.season, episode=self.episode, year='', watched=7)
            except:
                pass

            
    def onPlayBackStarted(self):
        try:
			if self.offset == '0': raise Exception()
			seekTime = float(self.offset)
			self.seekTime(seekTime)
        except:
			pass

        if getSetting("playback_info") == 'true':
            elapsedTime = '%s %s seconds' % (language(30309).encode("utf-8"), int((time.time() - self.loadingStarting)))     
            index().infoDialog(elapsedTime, header=self.name)

    def onPlayBackStopped(self):

        try:
            import hashlib
            n = (hashlib.md5())
            n.update(str(self.name))
            n = str(n.hexdigest())
            i = 'tt' + self.imdb
            r = str(self.currentTime)
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS points (""name TEXT, ""imdb_id TEXT, ""resume_point TEXT, ""UNIQUE(name, imdb_id)"");")
            dbcur.execute("DELETE FROM points WHERE name = '%s' AND imdb_id = '%s'" % (n, i))
            ok = int(self.currentTime) > 180 and (self.currentTime / self.totalTime) <= .92
            if ok: dbcur.execute("INSERT INTO points Values (?, ?, ?)", (n, i, r))
            dbcon.commit()
        except:
            pass

        try:
            ok = self.currentTime / self.totalTime >= .9
            if ok: self.change_watched()
        except:
            pass

    def onPlayBackEnded(self):

        try:
            import hashlib
            n = (hashlib.md5())
            n.update(str(self.name))
            n = str(n.hexdigest())
            i = 'tt' + self.imdb
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS points (""name TEXT, ""imdb_id TEXT, ""resume_point TEXT, ""UNIQUE(name, imdb_id)"");")
            dbcur.execute("DELETE FROM points WHERE name = '%s' AND imdb_id = '%s'" % (n, i))
            dbcon.commit()
        except:
            pass

        try:
            self.change_watched()
        except:
            pass
Main()
