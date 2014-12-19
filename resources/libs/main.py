import urllib,re,string,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import time,threading

import pickle

from resources.libs import settings, constants
addon_id = settings.getAddOnID()
selfAddon = xbmcaddon.Addon(id=addon_id)
afterpath = selfAddon.getAddonInfo('path')

grab = None
fav = False
hostlist = None

Dir = xbmc.translatePath(os.path.join('special://home/addons/'+addon_id, ''))
datapath = xbmc.translatePath(selfAddon.getAddonInfo('profile'))

################################################################################ Common Calls ##########################################################################################################
art = Dir+'/resources/art/'
fanartimage=Dir+'fanart2.jpg'
elogo = art+'/bigx.png'
slogo = art+'/smallicon.png'

def removeColoredText(text):
    return re.sub('\[COLOR.*?\[/COLOR\]','',text,re.I|re.DOTALL).strip()


################################################################################ Types of Directories ##########################################################################################################

def addDirX(name,url,mode,iconimage,plot='',fanart='',dur=0,genre='',year='',imdb='',tmdb='',isFolder=True,searchMeta=False,addToFavs=True,
            id=None,fav_t='',fav_addon_t='',fav_sub_t='',metaType='Movies',menuItemPos=None,menuItems=None,down=False,replaceItems=True,index=False,page=1):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)+"&index="+str(index)+"&page="+str(page)
    if searchMeta:
        if metaType == 'TV':
            infoLabels = GETMETAEpiT(name,iconimage,plot)
        else:
            infoLabels = GETMETAT(name,genre,fanart,iconimage,plot,imdb,tmdb)
        iconimage = infoLabels['cover_url']
        if iconimage.startswith('w342') or iconimage.startswith('w92') or iconimage.startswith('w500') or iconimage.startswith('original') or iconimage.startswith('w154') or iconimage.startswith('w185'):
            iconimage = 'http://image.tmdb.org/t/p/' + iconimage
        fanart = infoLabels['backdrop_url']
        if fanart.startswith('original') or fanart.startswith('w1280') or fanart.startswith('w780') or fanart.startswith('w300'):
            fanart = 'http://image.tmdb.org/t/p/' + fanart
        plot = infoLabels['plot']
    if not fanart: fanart=fanartimage
    if not iconimage: iconimage=art+'/vidicon.png'
    if not plot: plot='Sorry description not available'
    plot=plot.replace(",",'.')
    Commands = []
    if selfAddon.getSetting("ctx_fav") != "false" and addToFavs: 
        fav = getFav()
        fname = name.replace(",",'')
        if isFolder:
            Commands.append(("[B][COLOR blue]Add[/COLOR][/B] to My Fav's",fav.add_directory(fname, u, section_title=fav_t, section_addon_title=fav_addon_t+" Fav's", sub_section_title=fav_sub_t, img=iconimage, fanart=fanart, infolabels={'item_mode':mode, 'item_url':url, 'plot':plot,'duration':dur,'genre':genre,'year':year})))
        else:
            Commands.append(("[B][COLOR blue]Add[/COLOR][/B] to My Fav's",fav.add_video_item(fname, u, section_title=fav_t, section_addon_title=fav_addon_t+" Fav's", sub_section_title=fav_sub_t, img=iconimage, fanart=fanart, infolabels={'item_mode':mode, 'item_url':url, 'plot':plot,'duration':dur,'genre':genre,'year':year})))
        Commands.append(("[B][COLOR red]Remove[/COLOR][/B] from My Fav's",fav.delete_item(fname, section_title=fav_t, section_addon_title=fav_addon_t+" Fav's", sub_section_title=fav_sub_t)))
    
    if searchMeta:
        if metaType == 'TV' and selfAddon.getSetting("meta-view-tv") == "true":
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            cname = infoLabels['title']
            cname = cname.decode('ascii', 'ignore')
            cname = urllib.quote_plus(cname)
            sea = infoLabels['season']
            epi = infoLabels['episode']
            imdb_id = infoLabels['imdb_id']
            if imdb_id != '':
                if infoLabels['overlay'] == 6: watched_mark = 'Mark as Watched'
                else: watched_mark = 'Mark as Unwatched'
                Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=779&name=%s&url=%s&iconimage=%s&season=%s&episode=%s)' % (sys.argv[0], cname, 'episode', imdb_id,sea,epi)))
            Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=780&name=%s&url=%s&iconimage=%s&season=%s&episode=%s)' % (sys.argv[0], cname, 'episode',imdb_id,sea,epi)))
        elif metaType == 'Movies' and selfAddon.getSetting("meta-view") == "true":
            xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
            if id != None: xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PLAYLIST_ORDER )
            else: xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_TITLE )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )
            cname=urllib.quote_plus(infoLabels['metaName'])
            imdb_id = infoLabels['imdb_id']
            if infoLabels['overlay'] == 6: watched_mark = 'Mark as Watched'
            else: watched_mark = 'Mark as Unwatched'
            Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=777&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, 'movie',imdb_id)))
            Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=778&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, 'movie',imdb_id)))
    else:
        infoLabels={ "Title": name, "Plot": plot, "Duration": dur, "Year": year ,"Genre": genre,"OriginalTitle" : removeColoredText(name) }
    if id != None: infoLabels["count"] = id
    Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
    
    if menuItemPos != None:
        for mi in reversed(menuItems):
            Commands.insert(menuItemPos,mi)
    
    liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
    liz.addContextMenuItems( Commands, replaceItems=False)
    if searchMeta:
        liz.setInfo( type="Video", infoLabels=infoLabels )
    liz.setProperty('fanart_image', fanart)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)

def addLink(name,url,iconimage):
    liz=xbmcgui.ListItem(name, iconImage=art+'/link.png', thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('fanart_image', fanartimage)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    
def addPlayList(name, url, mode, video_source_id, items, episodeName, iconImage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&index="+str(video_source_id)
    liz=xbmcgui.ListItem(label='[B]' + name + '[/B]' + ' | ' + 'Source #' + str(video_source_id) + ' | ' + 'Parts = ' + str(len(items)) , iconImage=iconImage, thumbnailImage=iconImage)
    liz.setProperty('videosList', pickle.dumps(items))
    liz.setProperty('episodeName',episodeName)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=True)

def addPlayc(name,url,mode,iconimage,plot,fanart,dur,genre,year):
    return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,isFolder=0,addToFavs=0)
def addPlayMs(name,url,mode,iconimage,plot,fanart,dur,genre,year):
    return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,isFolder=0,fav_t='Misc.',fav_addon_t='Misc.')

def addDirb(name,url,mode,iconimage,fanart):
    return addDirX(name,url,mode,iconimage,'',fanart,addToFavs=0)
    
def addDir(name,url,mode,iconimage,plot='',fanart='',index=False,page=1):
    return addDirX(name,url,mode,iconimage,plot,fanart,addToFavs=0,replaceItems=False,index=index,page=page)

def addDirHome(name,url,mode,iconimage,index=False):
    return addDirX(name,url,mode,iconimage,addToFavs=0,index=index)
def addDown2(name,url,mode,iconimage,fanart):
    return addDirX(name,url,mode,iconimage,'',fanart,isFolder=0,addToFavs=0,id=id,down=1)

def addInfo(name,url,mode,iconimage,genre,year):
    mi = []
    return addDirX(name,url,mode,iconimage,'','','',genre,year,searchMeta=1,fav_t='Movies',fav_addon_t='Movie',menuItemPos=0,menuItems=mi)
def addTVInfo(name,url,mode,iconimage,genre,year):
    mi = []
    return addDirX(name,url,mode,iconimage,'','','',genre,year,searchMeta=0,fav_t='TV',fav_addon_t='TV',menuItemPos=0,menuItems=mi,metaType='TV')

def formatCast(cast):
    roles = "\n\n"
    for role in cast:
        roles =  roles + "[COLOR blue]" + role[0] + "[/COLOR] as " + role[1] + " | "
    return roles

def getFav():
    global fav
    if not fav:
        from resources.universal import favorites
        fav = favorites.Favorites(addon_id, sys.argv)
    return fav
def VIEWS():
    if selfAddon.getSetting("auto-view") == "true":
        if selfAddon.getSetting("choose-skin") == "true":
            if selfAddon.getSetting("con-view") == "0":
                    xbmc.executebuiltin("Container.SetViewMode(50)")
            elif selfAddon.getSetting("con-view") == "1":
                    xbmc.executebuiltin("Container.SetViewMode(51)")
            elif selfAddon.getSetting("con-view") == "2":
                    xbmc.executebuiltin("Container.SetViewMode(500)")
            elif selfAddon.getSetting("con-view") == "3":
                    xbmc.executebuiltin("Container.SetViewMode(501)")
            elif selfAddon.getSetting("con-view") == "4":
                    xbmc.executebuiltin("Container.SetViewMode(508)")
            elif selfAddon.getSetting("con-view") == "5":
                    xbmc.executebuiltin("Container.SetViewMode(504)")
            elif selfAddon.getSetting("con-view") == "6":
                    xbmc.executebuiltin("Container.SetViewMode(503)")
            elif selfAddon.getSetting("con-view") == "7":
                    xbmc.executebuiltin("Container.SetViewMode(515)")
            return
        elif selfAddon.getSetting("choose-skin") == "false":
            if selfAddon.getSetting("xpr-view") == "0":
                    xbmc.executebuiltin("Container.SetViewMode(50)")
            elif selfAddon.getSetting("xpr-view") == "1":
                    xbmc.executebuiltin("Container.SetViewMode(52)")
            elif selfAddon.getSetting("xpr-view") == "2":
                    xbmc.executebuiltin("Container.SetViewMode(501)")
            elif selfAddon.getSetting("xpr-view") == "3":
                    xbmc.executebuiltin("Container.SetViewMode(55)")
            elif selfAddon.getSetting("xpr-view") == "4":
                    xbmc.executebuiltin("Container.SetViewMode(54)")
            elif selfAddon.getSetting("xpr-view") == "5":
                    xbmc.executebuiltin("Container.SetViewMode(60)")
            elif selfAddon.getSetting("xpr-view") == "6":
                    xbmc.executebuiltin("Container.SetViewMode(53)")
            return
    else:
        return
    
def VIEWSB():
    if selfAddon.getSetting("auto-view") == "true":
        if selfAddon.getSetting("home-view") == "0":
                xbmc.executebuiltin("Container.SetViewMode(50)")
        elif selfAddon.getSetting("home-view") == "1":
                xbmc.executebuiltin("Container.SetViewMode(500)")
        return

def OPENURL(url, mobile = False, q = False, verbose = True, timeout = 10, cookie = None, data = None, cookiejar = False, log = True, headers = [], type = '',ua = False):
    import urllib2 
    UserAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    if ua: UserAgent = ua
    try:
        if log:
            print "MU-Openurl = " + url
        if cookie and not cookiejar:
            import cookielib
            cookie_file = os.path.join(os.path.join(datapath,'Cookies'), cookie+'.cookies')
            cj = cookielib.LWPCookieJar()
            if os.path.exists(cookie_file):
                try: cj.load(cookie_file,True)
                except: cj.save(cookie_file,True)
            else: cj.save(cookie_file,True)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        elif cookiejar:
            import cookielib
            cj = cookielib.LWPCookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        else:
            opener = urllib2.build_opener()
        if mobile:
            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')]
        else:
            opener.addheaders = [('User-Agent', UserAgent)]
        for header in headers:
            opener.addheaders.append(header)
        if data:
            if type == 'json': 
                import json
                data = json.dumps(data)
                opener.addheaders.append(('Content-Type', 'application/json'))
            else: data = urllib.urlencode(data)
            response = opener.open(url, data, timeout)
        else:
            response = opener.open(url, timeout=timeout)
        if cookie and not cookiejar:
            cj.save(cookie_file,True)
        link=response.read()
        response.close()
        opener.close()
        link=link.replace('&#39;',"'").replace('&quot;','"').replace('&amp;',"&").replace("&#39;","'").replace('&lt;i&gt;','').replace("#8211;","-").replace('&lt;/i&gt;','').replace("&#8217;","'").replace('&amp;quot;','"').replace('&#215;','x').replace('&#038;','&').replace('&#8216;','').replace('&#8211;','').replace('&#8220;','').replace('&#8221;','').replace('&#8212;','')
        link=link.replace('%3A',':').replace('%2F','/')
        if q: q.put(link)
        return link
    except Exception as e:
        if verbose:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Source Website is Down,3000,"+elogo+")")
        xbmc.log('***********Website Error: '+str(e)+'**************', xbmc.LOGERROR)
        import traceback
        traceback.print_exc()
        link ='website down'
        if q: q.put(link)
        return link

################################################################################ TV Shows Metahandler ##########################################################################################################

def GETMETAEpiT(mname,thumb,desc):
        originalName=mname
        mname = removeColoredText(mname)
        if selfAddon.getSetting("meta-view-tv") == "true":
                setGrab()
                mname = mname.replace('New Episode','').replace('Main Event','').replace('New Episodes','')
                mname = mname.strip()
                r = re.findall('(.+?)\ss(\d+)e(\d+)\s',mname + " ",re.I)
                if not r: r = re.findall('(.+?)\sseason\s(\d+)\sepisode\s(\d+)\s',mname + " ",re.I)
                if not r: r = re.findall('(.+?)\s(\d+)x(\d+)\s',mname + " ",re.I)
                if r:
                    for name,sea,epi in r:
                        year=''
                        name=name.replace(' US','').replace(' (US)','').replace(' (us)','').replace(' (uk Series)','').replace(' (UK)','').replace(' UK',' (UK)').replace(' AU','').replace(' AND',' &').replace(' And',' &').replace(' and',' &').replace(' 2013','').replace(' 2011','').replace(' 2012','').replace(' 2010','')
                        if re.findall('twisted',name,re.I):
                            year='2013'
                        if re.findall('the newsroom',name,re.I):
                            year='2012'
                        metaq = grab.get_meta('tvshow',name,None,None,year)
                        imdb=metaq['imdb_id']
                        tit=metaq['title']
                        year=metaq['year']
                        epiname=''
                else:       
                    metaq=''
                    name=mname
                    epiname=''
                    sea=0
                    epi=0
                    imdb=''
                    tit=''
                    year=''
                meta = grab.get_episode_meta(str(name),imdb, int(sea), int(epi))
                print "Episode Mode: Name %s Season %s - Episode %s"%(str(name),str(sea),str(epi))
                infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'premiered':meta['premiered'],
                      'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'overlay':meta['overlay'],'episode': meta['episode'],
                              'season': meta['season'],'backdrop_url': meta['backdrop_url']}

                if infoLabels['cover_url']=='':
                        if metaq!='':
                            thumb=metaq['cover_url']
                            infoLabels['cover_url']=thumb
                           
                if infoLabels['backdrop_url']=='':
                        fan=fanartimage
                        infoLabels['backdrop_url']=fan
                if infoLabels['cover_url']=='':
                    if thumb=='':
                        thumb=art+'/vidicon.png'
                        infoLabels['cover_url']=thumb
                    else:
                        infoLabels['cover_url']=thumb
                infoLabels['imdb_id']=imdb
                if meta['overlay'] == 7:
                   infoLabels['playcount'] = 1
                else:
                   infoLabels['playcount'] = 0
                
                infoLabels['showtitle']=tit
                infoLabels['year']=year
                infoLabels['metaName']=infoLabels['title']
                infoLabels['title']=originalName
                   
        else:
                fan=fanartimage
                infoLabels = {'title': originalName,'metaName': mname,'cover_url': thumb,'backdrop_url': fan,'season': '','episode': '','year': '','plot': desc,'genre': '','imdb_id': ''}       
        
        return infoLabels

def GETMETAT(mname,genre,fan,thumb,plot='',imdb='',tmdb=''):
    originalName=mname
    if selfAddon.getSetting("meta-view") == "true":
        setGrab()
        mname = re.sub(r'\[COLOR red\]\(?(\d{4})\)?\[/COLOR\]',r'\1',mname)
        mname = removeColoredText(mname)
        mname = mname.replace(' EXTENDED and UNRATED','').replace('Webrip','').replace('MaxPowers','').replace('720p','').replace('1080p','').replace('TS','').replace('HD','').replace('R6','').replace('H.M.','').replace('HackerMil','').replace('(','').replace(')','').replace('[','').replace(']','')
        mname = mname.replace(' Extended Cut','').replace('Awards Screener','')
        mname = re.sub('Cam(?![A-Za-z])','',mname)
        mname = re.sub('(?i)3-?d h-?sbs','',mname)
        mname = mname.strip()
        if re.findall('\s\d{4}',mname):
            r = re.split('\s\d{4}',mname,re.DOTALL)
            name = r[0]
            year = re.findall('\s(\d{4})\s',mname + " ")
            if year: year = year[0]
            else: year=''
        else:
            name=mname
            year=''
        name = name.decode("ascii", "ignore")
        meta = grab.get_meta('movie',name,imdb,tmdb,year)# first is Type/movie or tvshow, name of show,tvdb id,imdb id,string of year,unwatched = 6/watched  = 7
        if not meta['year']:
            name  = re.sub(':.*','',name)
            meta = grab.get_meta('movie',name,imdb,tmdb,year)
        print "Movie mode: %s"%name
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
          'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],'overlay':meta['overlay'],
          'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year'],
          'imdb_id' : meta['imdb_id']}
        if infoLabels['genre']=='':
            infoLabels['genre']=genre
        if infoLabels['cover_url']=='':
            infoLabels['cover_url']=thumb
        if infoLabels['backdrop_url']=='':
            if fan=='': fan=fanartimage
            else: fan=fan
            infoLabels['backdrop_url']=fan
        if meta['overlay'] == 7: infoLabels['playcount'] = 1
        else: infoLabels['playcount'] = 0
        if infoLabels['cover_url']=='':
            thumb=art+'/vidicon.png'
            infoLabels['cover_url']=thumb
        #if int(year+'0'):
        #    infoLabels['year']=year 
        infoLabels['metaName']=infoLabels['title']
        infoLabels['title']=originalName
        if infoLabels['plot']=='': infoLabels['plot']=plot
        else: infoLabels['plot'] = infoLabels['plot'] + formatCast(infoLabels['cast'])
    else:
        if thumb=='': thumb=art+'/vidicon.png'
        if fan=='': fan=fanartimage
        else: fan=fan
        infoLabels = {'title': mname,'metaName': mname,'cover_url': thumb,'backdrop_url': fan,'season': '','episode': '','year': '','plot': '','genre': genre,'imdb_id': '','tmdb_id':''}
    return infoLabels

def setGrab():
    global grab
    if grab is None:
        from metahandler import metahandlers
        grab = metahandlers.MetaData()

def resolve_url(url,filename = False):
    import resolvers
    return resolvers.resolve_url(url,filename)

def ErrorReport(e):
    elogo = xbmc.translatePath('special://home/addons/'+addon_id+'/resources/art/bigx.png')
    xbmc.executebuiltin("XBMC.Notification([COLOR=FF67cc33]Aftershock Error[/COLOR],"+str(e)+",10000,"+elogo+")")
    xbmc.log('***********Aftershock Error: '+str(e)+'**************', xbmc.LOGERROR)

############################################################################### Playback resume/ mark as watched #################################################################################

def WatchedCallback():
        xbmc.log('%s: %s' % (selfAddon.addon.getAddonInfo('name'), 'Video completely watched.'), xbmc.LOGNOTICE)
        videotype='movies'
        setGrab()
        grab.change_watched(videotype, name, iconimage, season='', episode='', year='', watched=7)
        xbmc.executebuiltin("XBMC.Container.Refresh")

def WatchedCallbackwithParams(video_type, title, imdb_id, season, episode, year):
    print "worked"
    setGrab()
    grab.change_watched(video_type, title, imdb_id, season=season, episode=episode, year=year, watched=7)
    xbmc.executebuiltin("XBMC.Container.Refresh")

def ChangeWatched(imdb_id, videoType, name, season, episode, year='', watched='', refresh=False):
        setGrab()
        grab.change_watched(videoType, name, imdb_id, season=season, episode=episode, year=year, watched=watched)
        xbmc.executebuiltin("XBMC.Container.Refresh")

def refresh_movie(vidtitle,imdb, year=''):

    #global metaget
    #if not metaget:
    #    metaget=metahandlers.MetaData()
    vidtitle = vidtitle.decode("ascii", "ignore")
    if re.search("^\d+", vidtitle):
        m = re.search('^(\d+)(.*)', vidtitle)
        vidtitle = m.group(1) + m.group(2) 
    else: vidtitle = re.sub("\d+", "", vidtitle)
    vidtitle=vidtitle.replace('  ','')
    setGrab()
    search_meta = grab.search_movies(vidtitle)
    
    if search_meta:
        movie_list = []
        for movie in search_meta:
            movie_list.append(movie['title'] + ' (' + str(movie['year']) + ')')
        dialog = xbmcgui.Dialog()
        index = dialog.select('Choose', movie_list)
        
        if index > -1:
            new_imdb_id = search_meta[index]['imdb_id']
            new_tmdb_id = search_meta[index]['tmdb_id']
            year=search_meta[index]['year']

            meta=grab.update_meta('movie', vidtitle, imdb, '',new_imdb_id,new_tmdb_id,year)
            


            xbmc.executebuiltin("Container.Refresh")
    else:
        xbmcgui.Dialog().ok('Refresh Results','No matches found')

def updateSearchFile(searchQuery,searchType,defaultValue = '###',searchMsg = ''):
    addToSearchHistory = True
    searchpath=os.path.join(datapath,'Search')
    searchHistoryFile = "SearchHistory25"
    if not searchMsg: searchMsg = 'Search For Movies' 
    SearchFile=os.path.join(searchpath,searchHistoryFile)
    searchQuery=urllib.unquote(searchQuery)
    if not searchQuery or searchQuery == defaultValue:
        searchQuery = ''
        try: os.makedirs(searchpath)
        except: pass
        keyb = xbmc.Keyboard('', searchMsg )
        keyb.doModal()
        if (keyb.isConfirmed()):
            searchQuery = keyb.getText()
        else:
            xbmcplugin.endOfDirectory(int(sys.argv[1]),False,False)
            return False
    else:
        addToSearchHistory = False
    searchQuery=urllib.quote(searchQuery)
    if os.path.exists(SearchFile):
        searchitems=re.compile('search="([^"]+?)",').findall(open(SearchFile,'r').read())
        if searchitems.count(searchQuery) > 0: addToSearchHistory = True
    if addToSearchHistory:
        if not os.path.exists(SearchFile) and searchQuery != '':
            open(SearchFile,'w').write('search="%s",'%searchQuery)
        elif searchQuery != '':
            open(SearchFile,'a').write('search="%s",'%searchQuery)
        else: return False
        searchitems=re.compile('search="([^"]+?)",').findall(open(SearchFile,'r').read())
        rewriteSearchFile = False
        if searchitems.count(searchQuery) > 1:
            searchitems.remove(searchQuery)
            rewriteSearchFile = True
        if len(searchitems)>=10:
            searchitems.remove(searchitems[0])
            rewriteSearchFile = True
        if rewriteSearchFile:   
            os.remove(SearchFile)
            for searchitem in searchitems:
                try: open(SearchFile,'a').write('search="%s",'%searchitem)
                except: pass
    return searchQuery
def Clearhistory(path):
    if os.path.exists(path):
        os.remove(path)
def removeNonASCII(text):
    return re.sub(r'[^\x00-\x7F]','-', text)
    
