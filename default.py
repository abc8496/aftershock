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

def MAIN():
    xbmcgui.Window(10000).clearProperty('AFTERSHOCK_SSR_TYPE')
    d = settings.getHomeItems()
    for index, value in sorted(enumerate(d), key=lambda x:x[1]):
        if value==None: continue
        if index==0:
            main.addDirHome('Search',mainurl,constants.MOVIE25_SEARCH_HISTORY,art+'/search.png')
        elif index==1:
            main.addDirHome("All Fav's",mainurl,constants.MAIN_GLOBALFAV,art+'/favsu.png')
        elif index==2:
            main.addDirHome('A-Z',mainurl,constants.MOVIE_ATOZ,art+'/az.png')
        elif index==3:
            main.addDirHome('New Releases',mainurl + 'new-releases/',constants.MOVIE25_LISTMOVIES,art+'/new.png')
        elif index==4:
            main.addDirHome('Latest Added',mainurl + 'latest-added/',constants.MOVIE25_LISTMOVIES,art+'/latest.png')
        elif index==5:
            main.addDirHome('Featured Movies',mainurl + 'featured-movies/',constants.MOVIE25_LISTMOVIES,art+'/feat.png')
        elif index==6:
            main.addDirHome('Most Viewed',mainurl + 'most-viewed/',constants.MOVIE25_LISTMOVIES,art+'/view.png')
        elif index==7:
            main.addDirHome('Most Voted',mainurl + 'most-voted/',constants.MOVIE25_LISTMOVIES,art+'/vote.png')
        elif index==8:
            main.addDirHome('HD Releases',mainurl + 'latest-hd-movies/',constants.MOVIE25_LISTMOVIES,art+'/dvd2hd.png')
        elif index==9:
            main.addDirHome('Genre',mainurl,constants.MOVIE_GENRE,art+'/genre.png')
        elif index==10:
            main.addDirHome('By Year',mainurl,constants.MOVIE_YEAR,art+'/year.png')
        elif index==11:
            main.addDirHome('Watch History','history',constants.MAIN_HISTORY,art+'/whistory.png')
        elif index==12:
            main.addDirHome('International',desirulezurl,constants.DESIRULEZ_CHANNELS,art+'/intl.png')
        elif index==13:
            main.addDirHome('Hindi Movies',sominalurl,constants.HINDI_MOVIES_MENU,art+'/hindimovies.png')
        elif index==14:
            main.addDirHome('Live TV',mainurl,constants.LIVETV_MENU,art+'/live.png')
        elif index==22:
            main.addDirHome('Kids Zone',mainurl,constants.KIDZONE_MENU,art+'/kidzone.png')
    main.addPlayc('Aftershock Settings',mainurl,constants.MAIN_SETTINGS,art+'/MashSettings.png','','','','','')

def AtoZ(index):
    main.addDir('0-9',mainurl + '0-9/',constants.MOVIE25_LISTMOVIES,art+'/09.png')
    for i in string.ascii_uppercase:
            main.addDir(i,mainurl+i.lower()+'/',constants.MOVIE25_LISTMOVIES,art+'/'+i.lower()+'.png')

def HINDI_MOVIE_MENU(url, index=False):
    xbmcgui.Window(10000).clearProperty('AFTERSHOCK_SSR_TYPE')
    d = settings.getHomeItems()
    for index, value in sorted(enumerate(d), key=lambda x:x[1]):
        if value==None: continue
        if index==2:
            pass
            #main.addDirHome('A-Z',sominalurl,constants.MOVIE_ATOZ,art+'/az.png')
        elif index==3:
            main.addDirHome('New Releases',sominalurl + 'category/2014/feed',constants.SOMINAL_LISTMOVIES,art+'/new.png')
        elif index==4:
            main.addDirHome('Latest Added',sominalurl + 'category/hindi-movies/feed',constants.SOMINAL_LISTMOVIES,art+'/latest.png')
        elif index==5:
            pass
            #main.addDirHome('Featured Movies',sominalurl + 'category/featured_movies/',constants.MOVIE25_LISTMOVIES,art+'/feat.png')
        elif index==8:
            main.addDirHome('HD Releases',sominalurl + 'category/hindi-blurays/feed',constants.SOMINAL_LISTMOVIES,art+'/dvd2hd.png')
        elif index==9:
            main.addDirHome('Genre',sominalurl,constants.SOMINAL_GENRE,art+'/genre.png')
        elif index==10:
            main.addDirHome('By Year',sominalurl,constants.SOMINAL_YEAR,art+'/year.png')
    main.VIEWSB()

    ##main.addDir('New Releases',sominalurl,constants.SOMINAL_LISTMOVIES,art+'/new.png',categoryURL='2014',page=1)
    ##main.addDir('Latest Added',sominalurl,constants.SOMINAL_LISTMOVIES,art+'/latest.png',categoryURL='hindi-movies',page=1)
    ##main.addDir('HD Releases',sominalurl,constants.SOMINAL_LISTMOVIES,art+'/dvd2hd.png',categoryURL='hindi-blurays',page=1)
    #main.addDir('Genre',mainurl,51,art+'/genre.png')
    #main.addDir('By Year',mainurl,51,art+'/year.png')
    
def GENRE(url,index=False):
    main.addDir('Action',mainurl + 'action/',constants.MOVIE25_LISTMOVIES,art+'/act.png',index=index)
    main.addDir('Adventure',mainurl + 'adventure/',constants.MOVIE25_LISTMOVIES,art+'/adv.png',index=index)
    main.addDir('Animation',mainurl + 'animation/',constants.MOVIE25_LISTMOVIES,art+'/ani.png',index=index)
    main.addDir('Biography',mainurl + 'biography/',constants.MOVIE25_LISTMOVIES,art+'/bio.png',index=index)
    main.addDir('Comedy',mainurl + 'comedy/',constants.MOVIE25_LISTMOVIES,art+'/com.png',index=index)
    main.addDir('Crime',mainurl + 'crime/',constants.MOVIE25_LISTMOVIES,art+'/cri.png',index=index)
    main.addDir('Documentary',mainurl + 'documentary/',constants.MOVIE25_LISTMOVIES,art+'/doc.png',index=index)
    main.addDir('Drama',mainurl + 'drama/',constants.MOVIE25_LISTMOVIES,art+'/dra.png',index=index)
    main.addDir('Family',mainurl + 'family/',constants.MOVIE25_LISTMOVIES,art+'/fam.png',index=index)
    main.addDir('Fantasy',mainurl + 'fantasy/',constants.MOVIE25_LISTMOVIES,art+'/fant.png',index=index)
    main.addDir('History',mainurl + 'history/',constants.MOVIE25_LISTMOVIES,art+'/history.png',index=index)
    main.addDir('Horror',mainurl + 'horror/',constants.MOVIE25_LISTMOVIES,art+'/hor.png',index=index)
    main.addDir('Music',mainurl + 'music/',constants.MOVIE25_LISTMOVIES,art+'/mus.png',index=index)
    main.addDir('Musical',mainurl + 'musical/',constants.MOVIE25_LISTMOVIES,art+'/mucl.png',index=index)
    main.addDir('Mystery',mainurl + 'mystery/',constants.MOVIE25_LISTMOVIES,art+'/mys.png',index=index)
    main.addDir('Romance',mainurl + 'romance/',constants.MOVIE25_LISTMOVIES,art+'/rom.png',index=index)
    main.addDir('Sci-Fi',mainurl + 'sci-fi/',constants.MOVIE25_LISTMOVIES,art+'/sci.png',index=index)
    main.addDir('Short',mainurl + 'short/',constants.MOVIE25_LISTMOVIES,art+'/sho.png',index=index)
    main.addDir('Sport',mainurl + 'sport/',constants.MOVIE25_LISTMOVIES,art+'/spo.png',index=index)
    main.addDir('Thriller',mainurl + 'thriller/',constants.MOVIE25_LISTMOVIES,art+'/thr.png',index=index)
    main.addDir('War',mainurl + 'war/',constants.MOVIE25_LISTMOVIES,art+'/war.png',index=index)
    main.addDir('Western',mainurl + 'western/',constants.MOVIE25_LISTMOVIES,art+'/west.png',index=index)
    main.VIEWSB()
    
def SOMINAL_GENRE(url,index=False):
    main.addDir('Action',sominalurl + 'category/action/feed',constants.SOMINAL_LISTMOVIES,art+'/act.png',index=index)
    main.addDir('Comedy',sominalurl + 'category/comedy/feed',constants.SOMINAL_LISTMOVIES,art+'/com.png',index=index)
    main.addDir('Crime',sominalurl + 'category/crime/feed',constants.SOMINAL_LISTMOVIES,art+'/cri.png',index=index)
    main.addDir('Drama',sominalurl + 'category/drama/feed',constants.SOMINAL_LISTMOVIES,art+'/dra.png',index=index)
    main.addDir('Horror',sominalurl + 'category/horror/feed',constants.SOMINAL_LISTMOVIES,art+'/hor.png',index=index)
    main.addDir('Romance',sominalurl + 'category/romance/feed',constants.SOMINAL_LISTMOVIES,art+'/rom.png',index=index)
    main.addDir('Social',sominalurl + 'category/social/feed',constants.SOMINAL_LISTMOVIES,art+'/soc.png',index=index)
    main.addDir('Thriller',sominalurl + 'category/thriller/feed',constants.SOMINAL_LISTMOVIES,art+'/thr.png',index=index)
    main.VIEWSB()

        
def YEAR(index=False):
    for x in reversed(range(2003, 2016)):
        main.addDir(str(x),'http://www.movie25.so/search.php?year='+str(x)+'/',constants.MOVIE_YEARB,art+'/'+str(x)+'.png',index=index)
    main.addDir('Enter Year','http://www.movie25.com',constants.MOVIE25_ENTERYEAR,art+'/enteryear.png',index=index)
    main.VIEWSB()
    
def SOMINAL_YEAR(index=False):
    for x in reversed(range(2003, 2016)):
        main.addDir(str(x),sominalurl + 'category/'+str(x)+'/feed',constants.SOMINAL_LISTMOVIES,art+'/'+str(x)+'.png',index=index)
    #main.addDir('Enter Year','http://www.movie25.com',constants.MOVIE25_ENTERYEAR,art+'/enteryear.png',index=index)
    main.VIEWSB()

def INT(url):
    logoBaseURL='http://www.lyngsat-logo.com/logo/tv'
    main.addDir('Hindi Movies',url+'/forums/20-Latest-Exclusive-Movie-HQ',constants.DESIRULEZ_LISTSHOWS,art+'/hindimovies.png')
    main.addDir('Star Plus',url+'/forumdisplay.php?f=42',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/ss/star_plus.jpg')
    main.addDir('Zee TV',url+'/forumdisplay.php?f=73',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/zz/zee_tv.jpg')
    main.addDir('Zindagi TV',url+'/forumdisplay.php?f=00',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/zz/zindagi_tv_pk.png')
    main.addDir('Sony TV',url+'/forumdisplay.php?f=63',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/ss/set_in.jpg')
    main.addDir('Sony Pal',url+'/forumdisplay.php?f=00',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/ss/sony_pal_in.png')
    main.addDir('Life OK',url+'/forumdisplay.php?f=1375',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/ll/life_ok_in.jpg')
    main.addDir('Sahara One',url+'/forumdisplay.php?f=134',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/ss/sahara_one.jpg')
    main.addDir('Star Jalsha',url+'/forumdisplay.php?f=667',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/ss/star_jalsha.jpg')
    main.addDir('Colors TV',url+'/forumdisplay.php?f=176',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/cc/colors_in.jpg')
    main.addDir('Sab TV',url+'/forumdisplay.php?f=254',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/ss/sony_sab_tv.jpg')
    main.addDir('Star Pravah',url+'/forumdisplay.php?f=1138',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/ss/star_pravah.png')
    main.addDir('Zing TV',url+'/forumdisplay.php?f=00',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/zz/zee_zing_asia.png')
    main.addDir('MTV',url+'/forumdisplay.php?f=339',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/mm/mtv_india.jpg')
    main.addDir('Channel [V]',url+'/forumdisplay.php?f=633',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/cc/channel_v_in.jpg')
    main.addDir('Bindass TV',url+'/forumdisplay.php?f=504',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/uu/utv_bindass.jpg')
    main.addDir('UTV Stars',url+'/forumdisplay.php?f=1274',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/uu/utv_stars.jpg')
    main.addDir('POGO',url+'/forumdisplay.php?f=500',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/pp/pogo.jpg')
    main.addDir('Disney',url+'/forumdisplay.php?f=479',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/dd/disney_channel_in.jpg')
    main.addDir('Hungama TV',url+'/forumdisplay.php?f=472',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/hh/hungama.jpg')
    main.addDir('Cartoon Network',url+'/forumdisplay.php?f=509',constants.DESIRULEZ_LISTSHOWS,logoBaseURL+'/cc/cartoon_network_in.jpg')
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

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Thumb: "+str(iconimage)

if mode==None or url==None or len(url)<1:
    MAIN()
    main.VIEWSB()        
   
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

elif mode==constants.MOVIE_YEARB:
    from resources.libs import movie25
    print ""+url
    movie25.YEARB(url,index=index)

elif mode==constants.MOVIE25_NEXTPAGE:
    from resources.libs import movie25
    print ""+url
    movie25.NEXTPAGE(url,index=index)
    
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

xbmcplugin.endOfDirectory(int(sys.argv[1]))
