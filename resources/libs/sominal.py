import urllib,re,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main
import BeautifulSoup
import simplejson as json

from resources.libs import settings 
addon_id = settings.getAddOnID()

selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
baseUrl=settings.getSominalURL()
prettyName='Somminal'

def LISTMOVIES(murl,name, index, categoryURL,page):
    turl = baseUrl + 'category/'+ categoryURL + '/feed'
    
    totalMoviesToLoad = 25
        
    dialogWait = xbmcgui.DialogProgress()
    
    ret = dialogWait.create('Please wait until [Movies] are cached.')
    loadedLinks = 0
    totalLinks = totalMoviesToLoad
    remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
    xbmc.executebuiltin("XBMC.Dialog.Close(busydialog,true)")
    
    while (loadedLinks <= totalMoviesToLoad):
        purl = turl
        if int(page) > 1:
            purl = turl + "?paged=" + str(page)
        link = main.OPENURL(purl)
        soup = BeautifulSoup.BeautifulSoup(link).findAll('item')
        for item in soup:
            name=item.title.text
            url = item.comments.text.replace('#comments','')
            
            for category in item.findAll('category'):
                if category.text == 'Hindi Movies':
                    main.addDirX(name, url,52,'',searchMeta=True,metaType='Movies',categoryURL=categoryURL)
                    loadedLinks = loadedLinks + 1
                    percent = (loadedLinks * 100)/totalLinks
                    remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                    dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                    if dialogWait.iscanceled(): return False   
                if dialogWait.iscanceled(): return False   
            if dialogWait.iscanceled(): return False   
        if dialogWait.iscanceled(): return False   
        page = str(int(page) + 1)
    dialogWait.close()
    del dialogWait
    
    main.addDir('[COLOR blue]Page '+ str(page) +'[/COLOR]',murl,51,art+'/next.png',index=index, categoryURL=categoryURL,page=str(page))
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    main.VIEWS()
def LOADVIDEOS(url, name):
    
    link = main.OPENURL(url)
    
    soup = BeautifulSoup.BeautifulSoup(link)
    tags = soup.findAll('p')
    
    if len(tags) < 5:
        tags.extend(soup.findAll('span'))
    
    video_playlist_items = []
    video_source_id = 0
    video_source_name = None
    
    for tag in tags:
        if re.search('^(Source|ONLINE|Server)', tag.getText(), re.IGNORECASE):
            if len(video_playlist_items) > 0:
                main.addPlayList(video_source_name, url,53, video_source_id, video_playlist_items, name, '')
            video_playlist_items = []
            video_source_id = video_source_id + 1
            video_source_name = tag.getText()
        else:
            aTags = tag.findAll('a', attrs={'target':re.compile('_blank'),'href':re.compile('(mediaplaybox.com|desiflicks.com|desionlinetheater.com|wp.me|cine.sominaltvfilms.com|media.thesominaltv.com)')}, recursive=True)
            if aTags is None or len(aTags) != 1:
                continue
            aTag = aTags[0]
            if aTag is not None:
                video_playlist_items.append(str(aTag['href']))
                video_source_name = re.findall('/.(.+?)/.',str(aTag['href']))[0]
    if len(video_playlist_items) > 0 :
        main.addPlayList(video_source_name, url,53, video_source_id, video_playlist_items, name, '')

def preparevideolink(video_url, video_source):
    return main.resolve_url(video_url, video_source)
    
def PLAY(name, items, movieName, video_source):
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
        playbackengine.PlayAllInPL(movieName, video_stream_links, img='')
        