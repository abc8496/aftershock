import xbmc,xbmcgui, xbmcaddon, xbmcplugin
import urllib,re,string,os,time,threading
import urllib2

import pickle

try:
    from resources.libs import main,settings    
except Exception, e:
    elogo = xbmc.translatePath('special://home/addons/plugin.video.aftershock/resources/art/bigx.png')
    dialog = xbmcgui.Dialog()
    ok=dialog.ok('[B][COLOR=FF67cc33]Aftershock Import Error[/COLOR][/B]','Failed To Import Needed Modules',str(e),'Report missing Module at [COLOR=FF67cc33]https://code.google.com/p/innovate-dev/issues/list[/COLOR] to Fix')
    xbmc.log('Aftershock ERROR - Importing Modules: '+str(e), xbmc.LOGERROR)

addon_id = settings.getAddOnID()
selfAddon = xbmcaddon.Addon(id=addon_id)

art = main.art
################################################################################ Directories ##########################################################################################################
CachePath=os.path.join(main.datapath,'Cache')
try: os.makedirs(CachePath)
except: pass
CookiesPath=os.path.join(main.datapath,'Cookies')
try: os.makedirs(CookiesPath)
except: pass
TempPath=os.path.join(main.datapath,'Temp')
try: os.makedirs(TempPath)
except: pass

mainurl = settings.getMovie25URL()
sominalurl = settings.getSominalURL()
desirulezurl = settings.getDesiRulezURL()

def AtoZ(index):
    main.addDir('0-9',mainurl + '0-9/',1,art+'/09.png')
    for i in string.ascii_uppercase:
            main.addDir(i,mainurl+i.lower()+'/',1,art+'/'+i.lower()+'.png')

def MAIN():
    xbmcgui.Window(10000).clearProperty('AFTERSHOCK_SSR_TYPE')
    d = settings.getHomeItems()
    for index, value in sorted(enumerate(d), key=lambda x:x[1]):
        if value==None: continue
        if index==0:
            main.addDirHome('Search',mainurl,420,art+'/search.png')
        elif index==1:
            main.addDirHome("All Fav's",mainurl,639,art+'/favsu.png')
        elif index==2:
            main.addDirHome('A-Z',mainurl,6,art+'/az2.png')
        elif index==3:
            main.addDirHome('New Releases',mainurl + 'new-releases/',1,art+'/new.png')
        elif index==4:
            main.addDirHome('Latest Added',mainurl + 'latest-added/',1,art+'/latest.png')
        elif index==5:
            main.addDirHome('Featured Movies',mainurl + 'featured-movies/',1,art+'/feat.png')
        elif index==6:
            main.addDirHome('Most Viewed',mainurl + 'most-viewed/',1,art+'/view.png')
        elif index==7:
            main.addDirHome('Most Voted',mainurl + 'most-voted/',1,art+'/vote.png')
        elif index==8:
            main.addDirHome('HD Releases',mainurl + 'latest-hd-movies/',1,art+'/dvd2hd.png')
        elif index==9:
            main.addDirHome('Genre',mainurl,2,art+'/genre.png')
        elif index==10:
            main.addDirHome('By Year',mainurl,7,art+'/year.png')
        elif index==11:
            main.addDirHome('Watch History','history',222,art+'/whistory.png')
        elif index==12:
            main.addDirHome('International',desirulezurl,36,art+'/intl.png')
        elif index==13:
            main.addDirHome('Hindi Movies',sominalurl,50,art+'/intl.png')
        elif index==22:
            main.addDirHome('Kids Zone',mainurl,76,art+'/kidzone.png')
    main.addPlayc('Aftershock Settings',mainurl,1999,art+'/MashSettings.png','','','','','')

def MOVIES(url, index=False):
    main.addDir('New Releases',sominalurl,51,art+'/new.png',categoryURL='2014',page=1)
    main.addDir('Latest Added',sominalurl,51,art+'/latest.png',categoryURL='hindi-movies',page=1)
    main.addDir('HD Releases',sominalurl,51,art+'/dvd2hd.png',categoryURL='hindi-blurays',page=1)
    #main.addDir('Genre',mainurl,51,art+'/genre.png')
    #main.addDir('By Year',mainurl,51,art+'/year.png')
    
def GENRE(url,index=False):
    main.addDir('Action',mainurl + 'action/',1,art+'/act.png',index=index)
    main.addDir('Adventure',mainurl + 'adventure/',1,art+'/adv.png',index=index)
    main.addDir('Animation',mainurl + 'animation/',1,art+'/ani.png',index=index)
    main.addDir('Biography',mainurl + 'biography/',1,art+'/bio.png',index=index)
    main.addDir('Comedy',mainurl + 'comedy/',1,art+'/com.png',index=index)
    main.addDir('Crime',mainurl + 'crime/',1,art+'/cri.png',index=index)
    main.addDir('Documentary',mainurl + 'documentary/',1,art+'/doc.png',index=index)
    main.addDir('Drama',mainurl + 'drama/',1,art+'/dra.png',index=index)
    main.addDir('Family',mainurl + 'family/',1,art+'/fam.png',index=index)
    main.addDir('Fantasy',mainurl + 'fantasy/',1,art+'/fant.png',index=index)
    main.addDir('History',mainurl + 'history/',1,art+'/history.png',index=index)
    main.addDir('Horror',mainurl + 'horror/',1,art+'/hor.png',index=index)
    main.addDir('Music',mainurl + 'music/',1,art+'/mus.png',index=index)
    main.addDir('Musical',mainurl + 'musical/',1,art+'/mucl.png',index=index)
    main.addDir('Mystery',mainurl + 'mystery/',1,art+'/mys.png',index=index)
    main.addDir('Romance',mainurl + 'romance/',1,art+'/rom.png',index=index)
    main.addDir('Sci-Fi',mainurl + 'sci-fi/',1,art+'/sci.png',index=index)
    main.addDir('Short',mainurl + 'short/',1,art+'/sho.png',index=index)
    main.addDir('Sport',mainurl + 'sport/',1,art+'/spo.png',index=index)
    main.addDir('Thriller',mainurl + 'thriller/',1,art+'/thr.png',index=index)
    main.addDir('War',mainurl + 'war/',1,art+'/war.png',index=index)
    main.addDir('Western',mainurl + 'western/',1,art+'/west.png',index=index)
    main.VIEWSB()
        
def YEAR(index=False):
    main.addDir('2014','http://www.movie25.so/search.php?year=2014/',8,art+'/2014.png',index=index)
    main.addDir('2013','http://www.movie25.so/search.php?year=2013/',8,art+'/2013.png',index=index)
    main.addDir('2012','http://www.movie25.so/search.php?year=2012/',8,art+'/2012.png',index=index)
    main.addDir('2011','http://www.movie25.so/search.php?year=2011/',8,art+'/2011.png',index=index)
    main.addDir('2010','http://www.movie25.so/search.php?year=2010/',8,art+'/2010.png',index=index)
    main.addDir('2009','http://www.movie25.so/search.php?year=2009/',8,art+'/2009.png',index=index)
    main.addDir('2008','http://www.movie25.so/search.php?year=2008/',8,art+'/2008.png',index=index)
    main.addDir('2007','http://www.movie25.so/search.php?year=2007/',8,art+'/2007.png',index=index)
    main.addDir('2006','http://www.movie25.so/search.php?year=2006/',8,art+'/2006.png',index=index)
    main.addDir('2005','http://www.movie25.so/search.php?year=2005/',8,art+'/2005.png',index=index)
    main.addDir('2004','http://www.movie25.so/search.php?year=2004/',8,art+'/2004.png',index=index)
    main.addDir('2003','http://www.movie25.so/search.php?year=2003/',8,art+'/2003.png',index=index)
    main.addDir('Enter Year','http://www.movie25.com',23,art+'/enteryear.png',index=index)
    main.VIEWSB()
def INT(url):
    logoBaseURL='http://www.lyngsat-logo.com/logo/tv'
    main.addDir('Hindi Movies',url+'/forums/20-Latest-Exclusive-Movie-HQ',37,art+'/Movies.jpeg')
    main.addDir('Star Plus',url+'/forumdisplay.php?f=42',37,logoBaseURL+'/ss/star_plus.jpg')
    main.addDir('Zee TV',url+'/forumdisplay.php?f=73',37,logoBaseURL+'/zz/zee_tv.jpg')
    main.addDir('Zindagi TV',url+'/forumdisplay.php?f=00',37,logoBaseURL+'/zz/zindagi_tv_pk.png')
    main.addDir('Sony TV',url+'/forumdisplay.php?f=63',37,logoBaseURL+'/ss/set_in.jpg')
    main.addDir('Sony Pal',url+'/forumdisplay.php?f=00',37,logoBaseURL+'/ss/sony_pal_in.png')
    main.addDir('Life OK',url+'/forumdisplay.php?f=1375',37,logoBaseURL+'/ll/life_ok_in.jpg')
    main.addDir('Sahara One',url+'/forumdisplay.php?f=134',37,logoBaseURL+'/ss/sahara_one.jpg')
    main.addDir('Star Jalsha',url+'/forumdisplay.php?f=667',37,logoBaseURL+'/ss/star_jalsha.jpg')
    main.addDir('Colors TV',url+'/forumdisplay.php?f=176',37,logoBaseURL+'/cc/colors_in.jpg')
    main.addDir('Sab TV',url+'/forumdisplay.php?f=254',37,logoBaseURL+'/ss/sony_sab_tv.jpg')
    main.addDir('Star Pravah',url+'/forumdisplay.php?f=1138',37,logoBaseURL+'/ss/star_pravah.png')
    main.addDir('Zing TV',url+'/forumdisplay.php?f=00',37,logoBaseURL+'/zz/zee_zing_asia.png')
    main.addDir('MTV',url+'/forumdisplay.php?f=339',37,logoBaseURL+'/mm/mtv_india.jpg')
    main.addDir('Channel [V]',url+'/forumdisplay.php?f=633',37,logoBaseURL+'/cc/channel_v_in.jpg')
    main.addDir('Bindass TV',url+'/forumdisplay.php?f=504',37,logoBaseURL+'/uu/utv_bindass.jpg')
    main.addDir('UTV Stars',url+'/forumdisplay.php?f=1274',37,logoBaseURL+'/uu/utv_stars.jpg')
    main.addDir('POGO',url+'/forumdisplay.php?f=500',37,logoBaseURL+'/pp/pogo.jpg')
    main.addDir('Disney',url+'/forumdisplay.php?f=479',37,logoBaseURL+'/dd/disney_channel_in.jpg')
    main.addDir('Hungama TV',url+'/forumdisplay.php?f=472',37,logoBaseURL+'/hh/hungama.jpg')
    main.addDir('Cartoon Network',url+'/forumdisplay.php?f=509',37,logoBaseURL+'/cc/cartoon_network_in.jpg')
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
        main.addDir("Downloaded Content",'Aftershock',241,art+'/downloadlog.png')
        main.addDir("Movie Fav's",'http://www.movie25.so/',641,art+'/fav.png')
        main.addDir("TV Show Fav's",'http://www.movie25.so/',640,art+'/fav.png')
        main.addDir("TV Episode Fav's",'http://www.movie25.so/',651,art+'/fav.png')
        main.addDir("Live Fav's",'http://www.movie25.so/',648,art+'/fav.png')
        main.addDir("Misc. Fav's",'http://www.movie25.so/',650,art+'/fav.png')
def History():
    whprofile = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
    whdb=os.path.join(whprofile,'Universal','watch_history.db')
    if  os.path.exists(whdb):
        main.addPlayc('Clear Watch History',whdb,414,art+'/cleahis.png','','','','','')
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
def KIDZone(murl):
    main.addDir('Disney Jr.','djk',107,art+'/disjr.png')
    #main.addDir('National Geographic Kids','ngk',71,art+'/ngk.png')
    #main.addDir('WB Kids','wbk',77,art+'/wb.png')
    #main.addDir('Youtube Kids','wbk',84,art+'/youkids.png')
    #main.addDir('Staael1982 Animated Movies','https://github.com/Coolstreams/bobbyelvis/raw/master/kids%20%26%20animation.xml',236,art+'/kidzone2.png')
            
    main.VIEWSB()
    
################################################################################ Modes ##########################################################################################################


def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param
              
params=get_params()

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
categoryURL=None
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
try: categoryURL=urllib.unquote_plus(params["categoryURL"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Thumb: "+str(iconimage)

if mode==None or url==None or len(url)<1:
    MAIN()
    main.VIEWSB()        
   
elif mode==1:
    from resources.libs import movie25
    movie25.LISTMOVIES(url,index=index)
    
elif mode==2:
    print ""+url
    GENRE(url,index=index)

elif mode==3:
    from resources.libs import movie25
    print ""+url
    movie25.VIDEOLINKS(name,url)

elif mode==4:
    from resources.libs import movie25
    print ""+url
    movie25.SEARCH(url,index=index)
elif mode==5:
    from resources.libs import movie25
    print ""+url
    movie25.PLAY(name,url)

elif mode==6:
    AtoZ(index=index)

elif mode==7:
    YEAR(index=index)

elif mode==8:
    from resources.libs import movie25
    print ""+url
    movie25.YEARB(url,index=index)

elif mode==9:
    from resources.libs import movie25
    print ""+url
    movie25.NEXTPAGE(url,index=index)
    
elif mode==10:
    from resources.libs import movie25
    ListglobalFavM25()

elif mode==11:
    from resources.libs import movie25
    print ""+url
    movie25.GroupedHosts(name,url,iconimage)

elif mode==23:
    from resources.libs import movie25
    movie25.ENTYEAR(index=index)
elif mode==36:
    print ""+url
    INT(url)
elif mode==37:
    from resources.libs import desitv
    print ""+url
    desitv.LISTSHOWS(url, name)
elif mode==38: # International LIST EPISODES
    from resources.libs import desitv
    print ""+url
    desitv.LISTEPISODES(name,url)
elif mode==39: # International LIST EPISODES
    from resources.libs import desitv
    print ""+url
    desitv.VIDEOLINKS(name,url)
elif mode==40: # Play all videos in the list
    from resources.libs import desitv
    items = xbmc.getInfoLabel('ListItem.Property("videosList")')
    video_source = xbmc.getInfoLabel('ListItem.Label')
    if items :
        desitv.PLAY(name, pickle.loads(items), xbmc.getInfoLabel('ListItem.Property("episodeName")'), video_source)
elif mode==50:
    MOVIES(url, index)
elif mode==51:
    from resources.libs import sominal
    sominal.LISTMOVIES(url, name, index, categoryURL=categoryURL, page=page)
elif mode==52:
    from resources.libs import sominal
    sominal.LOADVIDEOS(url, name)
elif mode==53:
    from resources.libs import sominal
    items = xbmc.getInfoLabel('ListItem.Property("videosList")')
    video_source = xbmc.getInfoLabel('ListItem.Label')
    if items :
        sominal.PLAY(name, pickle.loads(items), xbmc.getInfoLabel('ListItem.Property("episodeName")'), video_source)
elif mode==71:
    from resources.libs.adventure import nationalgeo
    print ""+url
    nationalgeo.NGDir(url)
elif mode==72:
    from resources.libs.adventure import nationalgeo
    print ""+url
    nationalgeo.LISTNG(url)

elif mode==73:
    from resources.libs.adventure import nationalgeo
    print ""+url
    nationalgeo.LISTNG2(url)

elif mode==74:
    from resources.libs.adventure import nationalgeo
    print ""+url
    nationalgeo.LINKNG(name,url)

elif mode==75:
    from resources.libs.adventure import nationalgeo
    print ""+url
    nationalgeo.LINKNG2(name,url)

elif mode==76:
    print ""+url
    KIDZone(url)
elif mode==107:
    from resources.libs.kids import disneyjr
    disneyjr.DISJR()
        
elif mode==108:
    from resources.libs.kids import disneyjr
    disneyjr.DISJRList(url)

elif mode==109:
    from resources.libs.kids import disneyjr
    disneyjr.DISJRList2(url)
        
elif mode==110:
    from resources.libs.kids import disneyjr
    disneyjr.DISJRLink(name,url,iconimage)       
elif mode==128:
    main.Clearhistory(url)
elif mode==222:
    print ""+url
    History()

elif mode==420:
    from resources.libs import movie25
    print ""+url
    movie25.Searchhistory(index=index)
elif mode==639:
    print ""+url
    GlobalFav()
elif mode == 778: #REFRESH METADATA
    main.refresh_movie(name,iconimage)
elif mode == 1999:
    settings.openSettings()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
