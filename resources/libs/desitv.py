import urllib,re,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main
import BeautifulSoup
import simplejson as json

from resources.libs import settings 
addon_id = settings.getAddOnID()

selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
MainUrl='http://www.desirulez.net/'
prettyName='DesiRulez'
def getShowImage(channelName, showName):
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
        xbmc.log('Movie25-Mod ERROR - Importing Modules: '+str(e), xbmc.LOGERROR)
        return getShowImage(channelName, showName)
    return ''
    
def LISTSHOWS(murl,channel,index=False):
    link=main.OPENURL(murl)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match = re.findall('<div class="titleline"><h2 class="forumtitle"><a href="(.+?)">(.+?)</a></h2></div>',link)
    label='TV Shows'
    if not len(match) > 0:
        match = re.findall('<h3 class="threadtitle">.+?<a class=".+?" href="(.+?)" id=".+?">(.+?)</a></h3>', link)
        label = 'Movies'
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until ' + label + ' Show list is cached.')
    totalLinks = len(match)
    loadedLinks = 0
    remaining_display = label + ' loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
    xbmc.executebuiltin("XBMC.Dialog.Close(busydialog,true)")
    for url,name in match:
        if "color" in name:
            name=name.replace('<b><font color=red>','[COLOR red]').replace('</font></b>','[/COLOR]')
            name=name.replace('<b><font color="red">','[COLOR red]').replace('</font></b>','[/COLOR]')
        if label == 'Movies':
            main.addDirX(name, MainUrl+url,39,'',searchMeta=True, metaType='Movies')
        else:
            main.addTVInfo(name,MainUrl+url,38,getShowImage(channel,name),'','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = label + ' loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if dialogWait.iscanceled(): return False   
    dialogWait.close()
    del dialogWait
    xbmcplugin.setContent(int(sys.argv[1]), label)
    main.VIEWS()

def LISTEPISODES(tvshowname,url):
    link=main.OPENURL(url)
    print tvshowname
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match = re.findall('<a class=".+?" href="(.+?)" id=".+?">(.+?)</a>',link)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until ['+tvshowname+'] Episodes are cached.')
    totalLinks = len(match)
    loadedLinks = 0
    remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
    xbmc.executebuiltin("XBMC.Dialog.Close(busydialog,true)")
    for url,name in match:
        if "Online" not in name: continue
        name=name.replace(tvshowname,'').replace('Watch Online','')
        name=main.removeNonASCII(name)
        main.addTVInfo(name,MainUrl+url,39,'','','') 
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if dialogWait.iscanceled(): return False   
    match=re.findall('<div id="above_threadlist" class="above_threadlist">(.+?)</div>',link)
    for string in match:
        match1=re.findall('<a href="(.+?)" title="(.+?)">[0-9]+</a>', string)
        for url, page in match1:
            main.addTVInfo(page,MainUrl+url,38,'','','')
    dialogWait.close()
    del dialogWait
    xbmcplugin.setContent(int(sys.argv[1]), 'TV Shows')
    main.VIEWS()

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
    print 'NAME : ' + name
    print items
    print 'EPISODE NAME : ' + episodeName
    print 'VIDEO SOURCE : ' + video_source
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
    PlayNowPreferredOrder = ['Flash Player 720','Flash Player DVD','Flash Player','dailymotion','PlayCineFlix']
    print '**********************************'
    #print video_source
    
    preferredFound = False
    prefKey = ''
    for source_name in PlayNowPreferredOrder:
        for key in video_source.keys():
            if re.search(source_name, key, flags=re.I):
                preferredFound = True
                prefKey = key
                print video_source[prefKey]
        if preferredFound :
            break
    
    PLAY(prefKey, video_source[prefKey],name, prefKey)

def VIDEOLINKS(name, url):
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
    
    for child in soup.findChildren():
        if (child.name == 'font') and re.search('Links|Online',str(child.getText()),re.IGNORECASE):
                if len(video_playlist_items) > 0:
                    main.addPlayList(video_source_name, url,40, video_source_id, video_playlist_items, name, getVideoSourceIcon(video_source_name))
                    
                    video_source_id = video_source_id + 1
                    video_source[video_source_name] = video_playlist_items
                    video_playlist_items = []
                video_source_name = child.getText()
                video_source_name = video_source_name.replace('Online','').replace('Links','').replace('Quality','').replace('Watch','').replace('-','').replace('  ','')
        elif (child.name =='a') and not child.getText() == 'registration' :
            video_playlist_items.append(str(child['href']))
    playNow(video_source, name)
    
def preparevideolink(video_url, video_source):
    return main.resolve_url(video_url, video_source)
