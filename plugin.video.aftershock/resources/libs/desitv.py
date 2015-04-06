import urllib,re,sys,os, time
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import BeautifulSoup
import simplejson as json
import CommonFunctions as common
from resources.libs import main, settings, constants, jsonutil, fileutil

addon_id = settings.getAddOnID()

selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
MainUrl='http://www.desirulez.net/'
prettyName='DesiRulez'
cacheFileName = 'DesiRulez.json'

def getShowImage(channelName, showName, retry):
    if retry == 0:
        return ''
    baseURL = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q={query}'
    query = channelName.lower() + ' ' + showName.lower() + ' poster'
    url = baseURL.format(query=urllib.quote_plus(query))
    try:
        link = main.OPENURL(url)
        results = json.loads(link)['responseData']['results']
        for image_info in results:
            iconImage = image_info['unescapedUrl']
            break
        if iconImage is not None:
            return iconImage
        else:
            return ''
    except Exception, e:
        xbmc.log('Aftershock ERROR - Importing Show Image: '+str(e), xbmc.LOGERROR)
        return getShowImage(channelName, showName, retry-1)
    return ''

def checkCache(murl, channel, cacheFilePath):
    refreshCache = True
    
    if not os.path.exists(cacheFilePath):
        jsonutil.createBlankChannelCache(cacheFilePath)
    else:
        lastModifiedTime = fileutil.lastModifiedTime(cacheFilePath)
        diffTime = long((time.time() - lastModifiedTime)/3600)
        if diffTime < 720:
            try :
                jsonChannelData = jsonutil.readJson(cacheFilePath)
                if jsonChannelData['channels'][channel]:
                    if re.search('past',murl,re.I):
                        if jsonChannelData['channels'][channel]['pastTVShows']:
                            refreshCache = False
                    elif jsonChannelData['channels'][channel]['currentTVShows']:
                        refreshCache = False
            except Exception, e:
                refreshCache = True
    print '>>>>>>>>>> RESRESH CACHE : ' + str(refreshCache)
    
    return refreshCache

def buildCache(murl, channel, cacheFilePath, index):
    channels = {}
    channelDict = {}
    channelData = {}
    tvShows = []
    tvShow = {}
    pastTVShowURL = ''
    link=main.OPENURL(murl)
    link = link.decode('iso-8859-1').encode('utf-8')
    result = common.parseDOM(link, "h2", attrs = {"class" : "forumtitle"})
    label='TV Shows'
    if len(result) <= 0:
        label = 'Movies'
        result = common.parseDOM(link, "h3", attrs = {"class":"threadtitle"})

    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until ' + label + ' Show list is cached.')
    totalLinks = len(result)
    loadedLinks = 0
    remaining_display = label + ' loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
    xbmc.executebuiltin("XBMC.Dialog.Close(busydialog,true)")
    
    for item in result:
        name = common.parseDOM(item, "a", attrs = {"class":"title threadtitle_unread"})
        
        if not name:
            name = common.parseDOM(item, "a", attrs = {"class":"title"})
            if name:
                name = name[0]
            else :
                name = common.parseDOM(item, "a")
                if len(name) > 1 :
                    name = name[1]
                else :
                    name = name[0]
        elif len(name) > 1 :
            name = name[1]
        else :
            name = name[0]
        
        url = common.parseDOM(item, "a", attrs = {"class":"title threadtitle_unread"}, ret="href")
        url = common.parseDOM(item, "a", ret="href")
        
        if not url:
            url = common.parseDOM(item, "a", attrs = {"class":"title"}, ret="href")
            if url :
                url = url[0]
        elif len(url) > 1 :
            url = url[1]
        else :
            url = url[0]
        
        if "color" in name:
            name=name.replace('<b><font color=red>','[COLOR red]').replace('</font></b>','[/COLOR]')
            name=name.replace('<b><font color="red">','[COLOR red]').replace('</font></b>','[/COLOR]')
            pastTVShowURL = MainUrl + url
        elif label == 'Movies':
            name = name.replace('Watch Online / Download','')
            main.addDirX(name, MainUrl+url,constants.DESIRULEZ_VIDEOLINKS,'',searchMeta=True, metaType='Movies')
        else:
            tvShow['url'] = MainUrl + url
            tvShow['iconimage'] = getShowImage(channel, name, 2)
            tvShow['name'] = name
            tvShows.append(tvShow)
            tvShow = {}
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = label + ' loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if dialogWait.iscanceled(): return False   
    dialogWait.close()
    del dialogWait
    
    # Writing data to JSON File
    jsonChannelData = jsonutil.readJson(cacheFilePath)
    channels = jsonChannelData['channels']
    try :
        channelData = channels[channel]
    except Exception, e:
        print 'exception'
    if re.search('past', murl, re.I):
        channelData['pastTVShows']=tvShows
    else :
        channelData['currentTVShows']=tvShows
        channelData['currentTVShowURL'] = murl
        channelData['pastTVShowURL'] = pastTVShowURL
    channels[channel] = channelData
    jsonutil.writeJson(jsonChannelData, cacheFilePath)
   
def loadFromCache(murl, channel, cacheFilePath):
    channels = jsonutil.readJson(cacheFilePath)['channels']
    channelData = channels[channel]
    tvShows = channelData['currentTVShows']
    for tvShow in tvShows:
        main.addTVInfo(tvShow['name'],tvShow['url'],constants.DESIRULEZ_LISTEPISODES,tvShow['iconimage'],tvShow['name'],'')
    if not re.search('past',murl,re.I):
        main.addTVInfo('[COLOR red]' + channel + ' Past Shows[/COLOR]',channelData['pastTVShowURL'],constants.DESIRULEZ_LISTSHOWS,'','Past Shows','')

def LISTSHOWS(murl,channel, CachePath, index=False):
    cacheFilePath = os.path.join(CachePath, cacheFileName)
    channel = channel.replace('[COLOR red]','').replace(' Past Shows[/COLOR]','')
    label = 'TV Show'
    if re.search('movie',murl,re.I):
        label = 'Movies'
    if checkCache(murl, channel, cacheFilePath) :
        buildCache(murl, channel, cacheFilePath, index)
        loadFromCache(murl, channel, cacheFilePath)
    else:
        loadFromCache(murl, channel, cacheFilePath)
    xbmcplugin.setContent(int(sys.argv[1]), label)
    if label == 'Movies' :
        main.setSeasonView()
    else: 
        main.VIEWS()

def LISTEPISODES(tvshowname,url):
    link=main.OPENURL(url)
    link=link.decode('iso-8859-1').encode('utf-8')
    result = common.parseDOM(link, "h3", attrs = {"class":"title threadtitle_unread"})
    result += common.parseDOM(link, "h3", attrs = {"class":"threadtitle"})
    
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until ['+tvshowname+'] Episodes are cached.')
    totalLinks = len(result)
    loadedLinks = 0
    remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
    xbmc.executebuiltin("XBMC.Dialog.Close(busydialog,true)")
    
    for item in result:
        name = common.parseDOM(item, "a", attrs = {"class":"title"})
        name += common.parseDOM(item, "a", attrs = {"class":"title threadtitle_unread"})
        if name:
            name = name[0]
        url = common.parseDOM(item, "a", ret="href")
        if url: 
            url = url[0]
    
        if "Online" not in name: continue
        name=name.replace(tvshowname,'').replace('Watch Online','').replace('Video','')
        name=main.removeNonASCII(name)
        main.addTVInfo(name,MainUrl+url,constants.DESIRULEZ_VIDEOLINKS,'',tvshowname,'') 
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if dialogWait.iscanceled(): return False   
    result = common.parseDOM(link, "div", attrs = {"class":"threadpagenav"})
    if result:
        result = result[0]
    result = common.parseDOM(result, "span")
    for item in result:
        name = common.parseDOM(item, "a")
        if name :
            name = name[0]
        url = common.parseDOM(item, "a", ret="href")
        if url:
            url = url[0]
        if not re.search('javascript',url,re.I):
            main.addTVInfo('-> Page ' + str(name),MainUrl+url,constants.DESIRULEZ_LISTEPISODES,'',tvshowname,'')
    dialogWait.close()
    del dialogWait
    xbmcplugin.setContent(int(sys.argv[1]), 'TV Shows')
    main.setEpisodeView()

def getVideoSourceIcon(source_name):
    img_url=None
    if re.search('dailymotion',source_name,flags=re.I):
        img_url = 'http://fontslogo.com/wp-content/uploads/2013/02/Dailymotion-LOGO.jpg'
    elif re.search('flash',source_name,flags=re.I):
        img_url = 'http://www.playwire.com/images/logo.png'
    elif re.search('cloud',source_name,flags=re.I):
        img_url = 'http://www.cloudy.ec/img/logo.png'
    elif re.search('videohut',source_name,flags=re.I):
        img_url = 'http://thumbs.videohut.to//logo/5.jpg'
    elif re.search('vidto',source_name,flags=re.I):
        img_url = 'http://static.vidto.me/static/images/header-logo.png'
    elif re.search('video tanker',source_name,flags=re.I):
        img_url = 'http://videotanker.co/styles/cbv2new/images/dot.gif'
    elif re.search('videoweed',source_name,flags=re.I):
        img_url = 'http://www.videoweed.es/images/logo.png'
    return img_url
    
def PLAY(name, items, episodeName, video_source):
    video_stream_links = []
    dialog = xbmcgui.DialogProgress()
    dialog.create('Resolving', 'Resolving Aftershock '+video_source+' Link...')       
    dialog.update(0)
    index = 0
    
    for item in items:
        video_stream_links.append(preparevideolink(item, name))
        dialog.update((100/len(items))*index)
        index = index+1
        if dialog.iscanceled(): return None
    if dialog.iscanceled(): return None
    dialog.update(100)
    dialog.close()
    del dialog
    
    from resources.universal import playbackengine
    if len(video_stream_links) > 0:
        playbackengine.PlayAllInPL(episodeName, video_stream_links, img=getVideoSourceIcon(video_source))

def playNow(video_source, name):
    PlayNowPreferredOrder = ['Flash Player [COLOR red][HD][/COLOR]','Flash Player [COLOR blue][DVD][/COLOR]','Flash Player','dailymotion','PlayCineFlix', 'Letwatch']
    
    preferredFound = False
    prefKey = ''
    for source_name in PlayNowPreferredOrder:
        for key in video_source.keys():
            if re.search(source_name, key, flags=re.I):
                preferredFound = True
                prefKey = key
        if preferredFound :
            break
    
    PLAY(prefKey, video_source[prefKey],name, prefKey)

def VIDEOLINKS(name, url):
    supportedHosts = ['flash player', 'dailymotion','letwatch','video tanker','video hut','cloudy','video weed']
    allHosts = ['flash player', 'dailymotion','letwatch','videotanker','videohut','vshare','cloudy','nowvideo','videoweed','movshare','novamov','single']
    video_source_id = 1
    video_source_name = None
    video_playlist_items = []
    
    video_source = {}
    
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    soup = BeautifulSoup.BeautifulSoup(link).findAll('blockquote', {'class':re.compile(r'\bpostcontent\b')})[0]
    
    for e in soup.findAll('br'):
        e.extract()
    if soup.has_key('div'):
        soup = soup.findChild('div', recursive=False)
    
    print soup
    for child in soup.findChildren():
        if (child.getText() == '') or ((child.name == 'font' or child.name == 'a') and re.search('DesiRulez', str(child.getText()),re.IGNORECASE)):
            continue
        elif (child.name == 'font') and re.search('Links|Online',str(child.getText()),re.IGNORECASE):
            if len(video_playlist_items) > 0:
                tmp_video_source = video_source_name.lower()
                indx = tmp_video_source.find('[')
                if indx > 0 :
                    tmp_video_source = tmp_video_source[:indx-1]
                if tmp_video_source in supportedHosts:
                    main.addPlayList(video_source_name, url,constants.DESIRULEZ_PLAY, video_source_id, video_playlist_items, name, getVideoSourceIcon(video_source_name))
                video_source_id = video_source_id + 1
                video_source[video_source_name] = video_playlist_items
                video_playlist_items = []
            video_source_name = child.getText()
            video_source_name = video_source_name.replace('Online','').replace('Links','').replace('Quality','').replace('Watch','').replace('-','').replace('Download','').replace('  ','').replace('720p HD','[COLOR red][HD][/COLOR]').replace('DVD','[COLOR blue][DVD][/COLOR]').strip()
            print video_source_name
        elif (child.name =='a') and not child.getText() == 'registration':
            video_playlist_items.append(str(child['href']))
    playNow(video_source, name)
    
def preparevideolink(video_url, video_source):
    stream_url = main.resolve_url(video_url, video_source)
    return stream_url
