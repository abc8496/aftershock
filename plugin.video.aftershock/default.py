import xbmc,xbmcgui, xbmcaddon, xbmcplugin
import urllib,re,string,os,time,threading
import urllib2

import pickle

try:
    from resources.libs import main,settings, constants, fileutil
except Exception, e:
    elogo = xbmc.translatePath('special://home/addons/plugin.video.aftershock/resources/art/bigx.png')
    dialog = xbmcgui.Dialog()
    ok=dialog.ok('[B][COLOR=FF67cc33]Aftershock Import Error[/COLOR][/B]','Failed To Import Needed Modules',str(e),'Report missing Module at [COLOR=FF67cc33]https://code.google.com/p/innovate-dev/issues/list[/COLOR] to Fix')
    xbmc.log('Aftershock ERROR - Importing Modules: '+str(e), xbmc.LOGERROR)

addon_id = settings.getAddOnID()
selfAddon = xbmcaddon.Addon(id=addon_id)

art = main.art
################################################################################ Directories ##########################################################################################################
fileutil.createDefaultDataDir(main.datapath)

mainurl = settings.getMovie25URL()
sominalurl = settings.getSominalURL()
desirulezurl = settings.getDesiRulezURL()



################################# START NEW IMPL ################################################################
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
        splitparams = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')
        for param in splitparams:
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
        elif action == 'movie_list' : Movies().moviesList(url)
        elif action == 'desi_home_newreleases' : Movies().desiNewReleases()
        elif action == 'desi_home_az' : Menu().getDesiAtoZItems()
        elif action == 'desi_home_latest' : Movies().desiLatestAdded()
        elif action == 'desi_home_hd' : Movies().desiHD()
        elif action == 'desi_home_genre' : Menu().getDesiGenre()
        elif action == 'desi_home_year' : Menu().getDesiYear()
        elif action == 'desi_movie_list' : Movies().desi_movie_list(url)
        elif action == 'get_host' : resolver().get_host(name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url, meta)
        elif action == 'play_moviehost' : resolver().play_host('movie', name, imdb, tvdb, url, source, provider)

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
            elif index==1:
                homeItems.append({'name':language(90101).encode("utf-8"), 'image': 'favsu.png', 'action': 'home_fav'})
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
            elif index==11:
                homeItems.append({'name':language(90111).encode("utf-8"), 'image': 'whistory.png', 'action': 'home_history'})
            elif index==12:
                homeItems.append({'name':language(90112).encode("utf-8"), 'image': 'intl.png', 'action': 'home_international'})
            elif index==13:
                homeItems.append({'name':language(90113).encode("utf-8"), 'image': 'hindimovies.png', 'action': 'home_hindimovie'})
            elif index==14:
                homeItems.append({'name':language(90114).encode("utf-8"), 'image': 'live.png', 'action': 'home_livetv'})
            elif index==22:
                homeItems.append({'name':language(90115).encode("utf-8"), 'image': 'kidzone.png', 'action': 'home_kids'})
        homeItems.append({'name':language(90116).encode("utf-8"), 'image':'settings.png','action':'settings_home'})
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

class Index:
    def __init__(self):
        print "Initialized"
    def infoDialog(self, str, header=addonName, time=3000):
        try: xbmcgui.Dialog().notification(header, str, self.addonArt('icon.png'), time, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, %s, %s)" % (header, str, time, self.addonArt('icon.png')))

    def addonArt(self, image):
        art = os.path.join(addonPath, 'resources/art')
        image = os.path.join(art, image)
        return image
        
    def setContainerView(self, contentType, view=None):
        if contentType == 'HOME':
            view = 500
        elif contentType == 'MOVIES':
            view = 500
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
                cm.append(('Movie Information', 'Action(Info)'))
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
                    item = xbmcgui.ListItem(name + ' [COLOR blue]'+ source.upper() + '[/COLOR]' , iconImage="DefaultVideo.png", thumbnailImage=poster)
                else :
                    item = xbmcgui.ListItem(name + ' [COLOR red] [' + quality.upper() + '] [/COLOR][COLOR blue]'+ source.upper() + '[/COLOR]' , iconImage="DefaultVideo.png", thumbnailImage=poster)
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
class Links:
    def __init__(self):
        #self.imdb_base = 'http://www.imdb.com'
        #self.imdb_mobile = 'http://m.imdb.com'
        #self.imdb_genre = 'http://www.imdb.com/genre/'
        #self.imdb_language = 'http://www.imdb.com/language/'
        self.imdb_title = 'http://www.imdb.com/title/tt%s/'
        #self.imdb_info = 'http://www.imdbapi.com/?t=%s&y=%s'
        #self.imdb_media = 'http://ia.media-imdb.com'
        #self.imdb_seasons = 'http://www.imdb.com/title/tt%s/episodes'
        #self.imdb_episodes = 'http://www.imdb.com/title/tt%s/episodes?season=%s'
        #self.imdb_genres = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&sort=boxoffice_gross_us&count=25&start=1&genres=%s'
        #self.imdb_certificates = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&sort=boxoffice_gross_us&count=25&start=1&certificates=us:%s'
        #self.imdb_languages = 'http://www.imdb.com/search/title?languages=%s|1&title_type=feature,tv_movie&sort=moviemeter,asc&count=25&start=1'
        #self.imdb_years = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&sort=boxoffice_gross_us&count=25&start=1&year=%s,%s'
        #self.imdb_popular = 'http://www.imdb.com/search/title?groups=top_1000&sort=moviemeter,asc&count=25&start=1'
        #self.imdb_boxoffice = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&sort=boxoffice_gross_us,desc&count=25&start=1'
        #self.imdb_views = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&sort=num_votes,desc&count=25&start=1'
        #self.imdb_oscars = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&groups=oscar_best_picture_winners&sort=year,desc&count=25&start=1'
        #self.imdb_tv_genres = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&sort=moviemeter,asc&count=25&start=1&genres=%s'
        #self.imdb_tv_certificates = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&sort=moviemeter,asc&count=25&start=1&certificates=us:%s'
        #self.imdb_tv_popular = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&sort=moviemeter,asc&count=25&start=1'
        #self.imdb_tv_rating = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=5000,&sort=user_rating,desc&count=25&start=1'
        #self.imdb_tv_views = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&sort=num_votes,desc&count=25&start=1'
        #self.imdb_tv_active = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&production_status=active&sort=moviemeter,asc&count=25&start=1'
        self.imdb_search = 'http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q=%s'
        #self.imdb_people_search = 'http://www.imdb.com/search/name?count=100&name=%s'
        #self.imdb_people = 'http://www.imdb.com/search/title?count=25&sort=year,desc&title_type=feature,tv_movie&start=1&role=nm%s'
        #self.imdb_tv_people = 'http://www.imdb.com/search/title?count=25&sort=year,desc&title_type=tv_series,mini_series&start=1&role=nm%s'
        #self.imdb_userlists = 'http://www.imdb.com/user/ur%s/lists?tab=all&sort=modified:desc&filter=titles'
        #self.imdb_watchlist ='http://www.imdb.com/user/ur%s/watchlist'
        #self.imdb_list = 'http://www.imdb.com/list/%s/?view=detail&sort=title:asc&title_type=feature,short,tv_movie,tv_special,video,documentary,game&start=1'
        #self.imdb_tv_list = 'http://www.imdb.com/list/%s/?view=detail&sort=title:asc&title_type=tv_series,mini_series&start=1'
        #self.imdb_user = getSetting("imdb_user").replace('ur', '')

        self.tmdb_base = 'http://api.themoviedb.org'
        self.tmdb_key = base64.urlsafe_b64decode('MTdmMjI3YmVjNTdkOTQ4OGJiYzgyNzYyZmMxNDQ0NmM=') ## using my key kodi-plugin-aftershock 17f227bec57d9488bbc82762fc14446c
        self.tmdb_info = 'http://api.themoviedb.org/3/movie/tt%s?language=en&api_key=%s'
        self.tmdb_info2 = 'http://api.themoviedb.org/3/movie/%s?language=en&api_key=%s'
        #self.tmdb_theaters = 'http://api.themoviedb.org/3/movie/now_playing?api_key=%s&page=1'
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

            self.sources = self.sources_get(name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre)
            if self.sources == []: raise Exception()
            self.sources = self.sources_filter() #For only displaying supported sources

            meta = json.loads(meta)

            if content == 'movie': 
                Index().moviesourceList(self.sources, name, imdb, '0', meta)
            else:
                Index().tvsourceList(self.sources, name, imdb, tvdb, meta)
        except:
            import traceback
            traceback.print_exc()
            Index().infoDialog(language(30308).encode("utf-8"))
            return
    def sources_get(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre):
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
            try: sourceDict = [(i, getSetting(i + '_tv')) for i in sourceDict]
            except: sourceDict = [(i, 'true') for i in sourceDict]

        global global_sources
        global_sources = []
        
        threads = []
        sourceDict = [i[0] for i in sourceDict if i[1] == 'true']
        
        if content == 'movie':
            title = self.normaltitle(title)
            for source in sourceDict: threads.append(Thread(self.sources_movie, name, title, year, imdb, source))
        else:
            show, show_alt = self.normaltitle(show), self.normaltitle(show_alt)
            season, episode = episodes().tvrage_redirect(title, year, imdb, tvdb, season, episode, show, date, genre)
            for source in sourceDict: threads.append(Thread(self.sources_tv, name, title, year, imdb, tvdb, date, season, episode, show, show_alt, source))


        #timeout = int(getSetting("sources_timeout_beta"))
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
    
    def sources_filter(self):
        try :
            supportedDict = ['GVideo', 'VK', 'Videomega', 'Sweflix', 'Muchmovies', 'YIFY', 'Einthusan', 'Movreel', '180upload', 'Mightyupload', 'Clicknupload', 'Tusfiles', 'Grifthost', 'Openload', 'Uptobox', 'Primeshare', 'iShared', 'Vidplay', 'Xfileload', 'Mrfile', 'Ororo', 'Animeultima','Allmyvideos']

            for i in range(len(self.sources)): self.sources[i]['source'] = self.sources[i]['source'].lower()
            self.sources = sorted(self.sources, key=itemgetter('source'))
            
            filter = []
            for host in supportedDict: 
                filter += [i for i in self.sources if i['source'] == host.lower()]
            filter += [i for i in self.sources if i['provider'].lower() == 'PlayIndiaFilms'.lower()]
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
                    meta['title'] = item.getLabel()
                    item.setInfo(type="Video", infoLabels = meta)
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
#Menu()
#Trailer()
#International()
#HindiMovies()
#FileUtils()

################################# END NEW IMPL ################################################################
        
def INT(url):
    logoBaseURL='http://www.lyngsat-logo.com/logo/tv'
    main.addDir('Hindi Movies',url+'forums/20-Latest-Exclusive-Movie-HQ',constants.DESIRULEZ_LISTSHOWS,art+'/hindimovies.png')
    main.addDir('Star Plus',url+'forumdisplay.php?f=42',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/ss/star_plus.jpg')
    main.addDir('Zee TV',url+'forumdisplay.php?f=73',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/zz/zee_tv.jpg')
    main.addDir('Zindagi TV',url+'forumdisplay.php?f=00',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/zz/zindagi_tv_pk.png')
    main.addDir('Sony TV',url+'forumdisplay.php?f=63',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/ss/set_in.jpg')
    main.addDir('Sony Pal',url+'forumdisplay.php?f=00',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/ss/sony_pal_in.png')
    main.addDir('Life OK',url+'forumdisplay.php?f=1375',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/ll/life_ok_in.jpg')
    main.addDir('Sahara One',url+'forumdisplay.php?f=134',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/ss/sahara_one.jpg')
    main.addDir('Star Jalsha',url+'forumdisplay.php?f=667',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/ss/star_jalsha.jpg')
    main.addDir('Colors TV',url+'forumdisplay.php?f=176',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/cc/colors_in.jpg')
    main.addDir('Sab TV',url+'forumdisplay.php?f=254',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/ss/sony_sab_tv.jpg')
    main.addDir('Star Pravah',url+'forumdisplay.php?f=1138',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/ss/star_pravah.png')
    main.addDir('Zing TV',url+'forumdisplay.php?f=00',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/zz/zee_zing_asia.png')
    main.addDir('MTV',url+'forumdisplay.php?f=339',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/mm/mtv_india.jpg')
    main.addDir('Channel [V]',url+'forumdisplay.php?f=633',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/cc/channel_v_in.jpg')
    main.addDir('Bindass TV',url+'forumdisplay.php?f=504',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/uu/utv_bindass.jpg')
    main.addDir('UTV Stars',url+'forumdisplay.php?f=1274',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/uu/utv_stars.jpg')
    main.addDir('POGO',url+'forumdisplay.php?f=500',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/pp/pogo.jpg')
    main.addDir('Disney',url+'forumdisplay.php?f=479',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/dd/disney_channel_in.jpg')
    main.addDir('Hungama TV',url+'forumdisplay.php?f=472',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/hh/hungama.jpg')
    main.addDir('Cartoon Network',url+'/orumdisplay.php?f=509',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/cc/cartoon_network_in.jpg')
    main.VIEWSB()

def getFavorites(section_title = None):
    from resources.universal import favorites
    fav = favorites.Favorites(addon_id, sys.argv)
    
    if(section_title):
        fav_items = fav.get_my_favorites(section_title=section_title, item_mode='addon')
    else:
        fav_items = fav.get_my_favorites(item_mode='addon')
    
    if len(fav_items) > 0:
    
        for fav_item in fav_items:
            if (fav_item['isfolder'] == 'false'):
                if (fav_item['section_addon_title'] == "iWatchOnline Fav's" or 
                    fav_item['section_addon_title'] == "Movie Fav's"):
                    main.addPlayM(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "TV Show Fav's"):
                    main.addPlayT(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "TV Episode Fav's"):
                    main.addPlayTE(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "Misc. Fav's"):
                    main.addPlayMs(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "Live Fav's"):
                    main.addPlayL(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "Movie25 Fav's"):
                    main.addInfo(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('genre',''), fav_item['infolabels'].get('year',''))
            else:
                if (fav_item['section_addon_title'] == "iWatchOnline Fav's" or 
                    fav_item['section_addon_title'] == "Movie Fav's"):
                    main.addDirM(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "TV Show Fav's"):
                    main.addDirT(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "TV Episode Fav's"):
                    main.addDirTE(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "Misc. Fav's"):
                    main.addDirMs(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "Live Fav's"):
                    main.addDirL(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "Movie25 Fav's"):
                    main.addInfo(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('genre',''), fav_item['infolabels'].get('year',''))
    else:
            xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]Aftershock Up[/COLOR][/B],[B]You Have No Saved Favourites[/B],5000,"")")
    return

def ListglobalFavALL():
    getFavorites()
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

def GlobalFav():
    if selfAddon.getSetting("groupfavs") == "true":
        ListglobalFavALL()
    else:
        main.addLink("[COLOR red]Aftershock Fav's can also be favorited under XBMC favorites[/COLOR]",'','')
        #main.addDir("Downloaded Content",'Aftershock',241,art+'/downloadlog.png')
        main.addDir("Movie Fav's",'http://www.movie25.so/',641,art+'/fav.png')
        main.addDir("TV Show Fav's",'http://www.movie25.so/',640,art+'/fav.png')
        #main.addDir("TV Episode Fav's",'http://www.movie25.so/',651,art+'/fav.png')
        #main.addDir("Live Fav's",'http://www.movie25.so/',648,art+'/fav.png')
        #main.addDir("Misc. Fav's",'http://www.movie25.so/',650,art+'/fav.png')
def History():
    whprofile = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
    whdb=os.path.join(whprofile,'Universal','watch_history.db')
    if  os.path.exists(whdb):
        main.addPlayc('Clear Watch History',whdb,constants.MAIN_CLEAR_HISTORY,art+'/cleahis.png','','','','','')
    from resources.universal import watchhistory
    wh = watchhistory.WatchHistory(addon_id)
    if selfAddon.getSetting("whistory") == "true":
        history_items = wh.get_my_watch_history()
        for item in history_items:
            item_title = item['title']
            item_url = item['url']
            item_image = item['image_url']
            item_fanart = item['fanart_url']
            item_infolabels = item['infolabels']
            item_isfolder = item['isfolder']
            if item_image =='':
                item_image= art+'/noimage.png'
            item_title=item_title.replace('[COLOR green]','[COLOR=FF67cc33]')
            main.addLink(item_title,item_url,item_image)
    else:
        dialog = xbmcgui.Dialog()
        ok=dialog.ok('[B]Aftershock History[/B]', 'Watch history is disabled' ,'To enable go to addon settings','and enable Watch History')
        history_items = wh.get_my_watch_history()
        for item in history_items:
            item_title = item['title']
            item_url = item['url']
            item_image = item['image_url']
            item_fanart = item['fanart_url']
            item_infolabels = item['infolabels']
            item_isfolder = item['isfolder']
            item_title=item_title.replace('[COLOR green]','[COLOR=FF67cc33]')
            main.addLink(item_title,item_url,item_image)
################################################################################ Modes ##########################################################################################################


params=None

url=None
name=None
mode=None
iconimage=None
fanart=None
plot=None
genre=None
title=None
season=None
episode=None
location=None
path=None
index=None
#categoryURL=None
page=None


try: name=urllib.unquote_plus(params["name"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: mode=int(params["mode"])
except: pass
try:
    iconimage=urllib.unquote_plus(params["iconimage"])
    iconimage = iconimage.replace(' ','%20')
except: pass
try: plot=urllib.unquote_plus(params["plot"])
except: pass
try:
    fanart=urllib.unquote_plus(params["fanart"])
    fanart = fanart.replace(' ','%20')
except: pass
try: genre=urllib.unquote_plus(params["genre"])
except: pass
try: title=urllib.unquote_plus(params["title"])
except: pass
try: episode=int(params["episode"])
except: pass
try: season=int(params["season"])
except: pass
try: location=urllib.unquote_plus(params["location"])
except: pass
try: path=urllib.unquote_plus(params["path"])
except: pass
try: index=urllib.unquote_plus(params["index"])
except: pass
try: page=urllib.unquote_plus(params["page"])
except: pass

if mode==None or url==None or len(url)<1:
    print "Hello Nothing Here"
    #MAIN()
    #main.VIEWSB()        
   
elif mode==constants.MOVIE25_LISTMOVIES:
    from resources.libs import movie25
    movie25.LISTMOVIES(url,index=index)
    
elif mode==constants.MOVIE_GENRE:
    print ""+url
    GENRE(url,index=index)

elif mode==constants.MOVIE25_VIDEOLINKS:
    from resources.libs import movie25
    print ""+url
    movie25.VIDEOLINKS(name,url)

elif mode==constants.MOVIE25_SEARCH:
    from resources.libs import movie25
    print ""+url
    movie25.SEARCH(url,index=index)
elif mode==constants.MOVIE25_PLAY:
    from resources.libs import movie25
    print ""+url
    movie25.PLAY(name,url)

elif mode==constants.MOVIE_ATOZ:
    AtoZ(index=index)

elif mode==constants.MOVIE_YEAR:
    YEAR(index=index)

elif mode==constants.LIST_GLOBAL_FAV:
    from resources.libs import movie25
    ListglobalFavM25()

elif mode==constants.MOVIE25_GROUPED_HOSTS:
    from resources.libs import movie25
    print ""+url
    movie25.GroupedHosts(name,url,iconimage)

elif mode==constants.MOVIE25_ENTERYEAR:
    from resources.libs import movie25
    movie25.ENTYEAR(index=index)
elif mode==constants.DESIRULEZ_CHANNELS:
    print ""+url
    INT(url)
elif mode==constants.DESIRULEZ_LISTSHOWS:
    from resources.libs import desitv
    print ""+url
    desitv.LISTSHOWS(url, name, fileutil.getPath(main.datapath, constants.CACHE_FILENAME))
elif mode==constants.DESIRULEZ_LISTEPISODES: # International LIST EPISODES
    from resources.libs import desitv
    print ""+url
    desitv.LISTEPISODES(genre,url)
elif mode==constants.DESIRULEZ_VIDEOLINKS: # International - MOVIE LINKS
    from resources.libs import desitv
    print ""+url
    desitv.VIDEOLINKS(name,url)
elif mode==constants.DESIRULEZ_PLAY: # Play all videos in the list
    from resources.libs import desitv
    items = xbmc.getInfoLabel('ListItem.Property("videosList")')
    video_source = xbmc.getInfoLabel('ListItem.Label')
    if items :
        desitv.PLAY(name, pickle.loads(items), xbmc.getInfoLabel('ListItem.Property("episodeName")'), video_source)
elif mode==constants.HINDI_MOVIES_MENU:
    HINDI_MOVIE_MENU(url, index)
elif mode==constants.SOMINAL_LISTMOVIES:
    from resources.libs import sominal
    sominal.LISTMOVIES(url, name, index, page=page)
elif mode==constants.SOMINAL_LOADVIDEOS:
    from resources.libs import sominal
    sominal.LOADVIDEOS(url, name)
elif mode==constants.SOMINAL_PLAY:
    from resources.libs import sominal
    items = xbmc.getInfoLabel('ListItem.Property("videosList")')
    video_source = xbmc.getInfoLabel('ListItem.Label')
    if items :
        sominal.PLAY(name, pickle.loads(items), xbmc.getInfoLabel('ListItem.Property("episodeName")'), video_source)
elif mode==constants.SOMINAL_GENRE:
    print ""+url
    SOMINAL_GENRE(url, index)
elif mode==constants.SOMINAL_YEAR:
    print ""+url
    SOMINAL_YEAR(index)
elif mode==constants.LIVETV_MENU:
    print ""+url
    from resources.libs import livetv
    livetv.LIVETV_MENU(url, name, index)
elif mode==constants.LIVETV_PLAY:
    from resources.libs import livetv
    livetv.PLAY(url, name, index)
    
elif mode==constants.NATGEO_NGDIR:
    from resources.libs.adventure import nationalgeo
    print ""+url
    nationalgeo.NGDir(url)
elif mode==constants.NATGEO_LISTNG:
    from resources.libs.adventure import nationalgeo
    print ""+url
    nationalgeo.LISTNG(url)

elif mode==constants.NATGEO_LISTNG2:
    from resources.libs.adventure import nationalgeo
    print ""+url
    nationalgeo.LISTNG2(url)

elif mode==constants.NATGEO_LINKNG:
    from resources.libs.adventure import nationalgeo
    print ""+url
    nationalgeo.LINKNG(name,url)

elif mode==constants.NATGEO_LINKNG2:
    from resources.libs.adventure import nationalgeo
    print ""+url
    nationalgeo.LINKNG2(name,url)

elif mode==constants.KIDZONE_MENU:
    print ""+url
    KIDZone(url)
elif mode==constants.DISNEYJR:
    from resources.libs.kids import disneyjr
    disneyjr.DISJR()
        
elif mode==constants.DISNEYJR_LIST:
    from resources.libs.kids import disneyjr
    disneyjr.DISJRList(url)

elif mode==constants.DISNEYJR_LIST2:
    from resources.libs.kids import disneyjr
    disneyjr.DISJRList2(url)
        
elif mode==constants.DISNEYJR_LINK:
    from resources.libs.kids import disneyjr
    disneyjr.DISJRLink(name,url,iconimage)       
elif mode==constants.MAIN_CLEAR_HISTORY:
    main.Clearhistory(url)
elif mode==constants.MAIN_HISTORY:
    print ""+url
    History()

elif mode==constants.MOVIE25_SEARCH_HISTORY:
    from resources.libs import movie25
    print ""+url
    movie25.Searchhistory(index=index)
elif mode==constants.MOVIE25_GOTOPAGE:
    from resources.libs import movie25
    print ""+url
    movie25.GotoPage(url,index=index)

elif mode==constants.MOVIE25_GOTOPAGEB:
    from resources.libs import movie25
    print ""+url
    movie25.GotoPageB(url,index=index)

elif mode==constants.MAIN_GLOBALFAV:
    print ""+url
    GlobalFav()
elif mode == constants.TOGGLE_WATCHED: #TOGGLE WATCHED
    main.ChangeWatched(iconimage, url, name, '', '')
elif mode == constants.REFRESH_METADATA: #REFRESH METADATA
    main.refresh_movie(name,iconimage)
elif mode == constants.MAIN_SETTINGS:
    settings.openSettings()

#xbmcplugin.endOfDirectory(int(sys.argv[1]))
