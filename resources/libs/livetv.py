import urllib,re,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import BeautifulSoup
import simplejson as json

from resources.libs import main, settings , constants
addon_id = settings.getAddOnID()

selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
prettyName='LiveTV'

def LIVETV_MENU(murl, name, index):
    logoBaseURL='http://www.lyngsat-logo.com/logo/tv'
    main.addDir('Willow Cricket','rtmp://80.82.78.15:443/liverepeater playpath=38 live=1 pageUrl=http://popeoftheplayers.pw/Vd?u#bt!25 timeout=15 token=#atd%#$ZH timeout=15',constants.LIVETV_PLAY,logoBaseURL+'/ww/willow_us.png')
    #main.addDir('9X Tashan','http://yamgo.com/#9x-tashan',constants.LIVETV_PLAY,logoBaseURL+'/num/9x_tashan.png')
    #main.addDir('Aaj Tak','http://aajtak.intoday.in/livetv.html',constants.LIVETV_PLAY, logoBaseURL+'/aa/aaj_tak.png')
    main.addDir('ABP News','http://hindiabp-lh.akamaihd.net/z/hindiabp1new_1@192103/manifest.f4m', constants.LIVETV_PLAY, logoBaseURL + '/aa/abp_news_in.png')
    main.VIEWSB()
    #http://www.desifree.tv/geonews/
    #9X Tashan -> http://yamgo.com/#9x-tashan
    #Aaj Tak -> http://aajtak.intoday.in/livetv.html
    #ABP News -> http://www.abplive.in/livetv/#.VJJEFCvF9Qc
    #DD News -> http://webcast.gov.in/live/
    #India TV -> http://www.indiatvnews.com/livetv/
    #NDTV India -> http://khabar.ndtv.com/videos/live/channel/ndtvindia/
    #NDTV 24X7 -> http://www.ndtv.com/video/live/channel/ndtv24x7
    #NDTV Prime -> http://prime.ndtv.com/
    
    #POGO TV -> http://www.zengatv.com/live/Pogo.html
    #SAB TV -> http://yamgo.com/#sony-sab-tv

    #Sahara One -> http://www.zengatv.com/live/SaharaOne.html -> NOT AVAILABLE
    #Times Now -> http://live.indiatimes.com/default.cms?timesnow=1
    #Zee News -> http://zeenews.india.com/live-tv
    #Zing -> http://yamgo.com/#zing
    #Zoom TV -> http://zoomtv.indiatimes.com/livetv.cms
    #Bollywood Action -> http://yamgo.com/#bollywood-action
    #Sahara Filmy -> http://www.zengatv.com/live/SaharaFilmy.html
    
    #http://yamgo.com/
    #9X E -> http://yamgo.com/9xe
    #V Hunt Bollywood -> http://yamgo.com/#v-hunt-bollywood
    #Bollywood Movies -> http://yamgo.com/#bollywood-movies
    #Bollywood Cinema 1 -> http://yamgo.com/#bollywood-cinema
    #Bollywood Cinema 2 -> http://yamgo.com/#bollywood-cinema-2
    #Bollywood Action 2 -> http://yamgo.com/#bollywood-action-2
    #Films Of India -> http://yamgo.com/#films-of-india
    #9X M -> http://yamgo.com/#9xm
    #9X Jalwa -> http://yamgo.com/#9x-jalwa
    
def PLAY(murl, name, index):
    print '>>>>>>>> INSIDE PLAY'
    ok=True
    hname=name
    # WORKING
    #murl = 'rtmp://live.server4sale.com/live/PTVnews swfUrl=http://live.server4sale.com:81/swfs/videoPlayer.swf live=true pageUrl=news.ptv.com.pk/livestreaming.asp'
    # END WORKING
    #murl = 'http://bglive-a.bitgravity.com/ndtv/247hi/live/native'
    murl = 'rtsp://46.249.213.87/broadcast/bollywoodaction2-tablet.3gp'
    murl = 'rtsp://46.249.213.87/broadcast/bollywoodhungama-tablet.3gp'
    murl = 'http://bglive-a.bitgravity.com/ndtv/247hi/live/native'
    if not murl: return False
    video_type='movie'
    season=''
    episode=''
    #img=infoLabels['cover_url']
    #fanart =infoLabels['backdrop_url']
    #imdb_id=infoLabels['imdb_id']
    #infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }

    try:
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
        stream_url = murl
        import urlresolver
        print 'INDIDE PLAY >>>>>>>>>>>>>>>>>>>>>: ' + stream_url
        stream_url = prepareVideoLink(stream_url)
        print 'INDIDE PLAY >>>>>>>>>>>>>>>>>>>>>: ' + stream_url

        #infoL={'Title': infoLabels['metaName'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
        # play with bookmark
        from resources.universal import playbackengine
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type='live', title=name, season=season, episode=episode, year='')
        #WatchHistory
        #if selfAddon.getSetting("whistory") == "true":
        #    from resources.universal import watchhistory
        #    wh = watchhistory.WatchHistory(addon_id)
        #    wh.add_item(hname+' '+'[COLOR green]Movie25[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
        #player.KeepAlive()
        return ok
    except Exception, e:
        if stream_url != False:
                main.ErrorReport(e)
        return ok

    #main.resolve_url(murl)
    
def prepareVideoLink(stream_url):
    #if re.search('rtmp://', stream_url, flags=re.I):
    #    return stream_url
    #stream_url = main.resolve_url(stream_url)
    return stream_url