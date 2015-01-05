import urllib,re,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import BeautifulSoup
import simplejson as json

from resources.libs import main, settings , constants, jsonutil, fileutil
addon_id = settings.getAddOnID()

selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
baseUrl=settings.getSominalURL()
prettyName='Somminal'

def LISTMOVIES(murl,name, index, page=1):
    turl = murl
        
    totalMoviesToLoad = settings.getNoOfMoviesToLoad()
        
    dialogWait = xbmcgui.DialogProgress()
    
    ret = dialogWait.create('Please wait until [Movies] are cached.')
    loadedLinks = 0
    totalLinks = totalMoviesToLoad
    remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
    xbmc.executebuiltin("XBMC.Dialog.Close(busydialog,true)")
    
    quality = None
    hindiMovie = False
    year = None
    pagesScanned = 0
    while ((pagesScanned < 5) and (loadedLinks <= totalMoviesToLoad)):
        purl = turl
        if int(page) > 1:
            purl = turl + "?paged=" + str(page)
        link = main.OPENURL(purl)
        soup = BeautifulSoup.BeautifulSoup(link).findAll('item')
        for item in soup:
            quality = ''
            hindiMovie = False
            year = ''
            
            name=item.title.text
            url = item.comments.text.replace('#comments','')
            for category in item.findAll('category'):
                if category.text == 'Hindi Movies':
                    #print item
                    hindiMovie = True
                elif re.search('DVD',category.text, flags=re.I):
                    quality = ' [COLOR red][DVD][/COLOR] '
                elif re.search('/*BluRay/*',category.text, flags=re.I):
                    quality = ' [COLOR red][HD][/COLOR] '
                elif re.search('[1-2][0,9][0-9][0-9]',category.text,flags=re.I):
                    year = category.text
                if dialogWait.iscanceled(): return False   
            if dialogWait.iscanceled(): return False   
            if hindiMovie :
                pagesScanned = 0
                main.addDirX(name + quality, url,constants.SOMINAL_LOADVIDEOS,'',searchMeta=True,metaType='Movies', year=year)
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if loadedLinks >= totalLinks : 
                    print 'BREAKING'
                    break
                if dialogWait.iscanceled(): return False   
        if dialogWait.iscanceled(): return False   
        page = str(int(page) + 1)
        pagesScanned = pagesScanned + 1
    dialogWait.close()
    del dialogWait
    
    main.addDir('[COLOR blue]Next[/COLOR]',murl,constants.SOMINAL_LISTMOVIES,art+'/next.png',index=index,page=str(page))
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    main.setSeasonView()

def playNow(video_source, name):
    PlayNowPreferredOrder = ['mediaplaybox','desiflicks']
    
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

def LOADVIDEOS(url, name):
    
    link = main.OPENURL(url)
    
    soup = BeautifulSoup.BeautifulSoup(link)
    tags = soup.findAll('p')
    
    if len(tags) < 5:
        tags.extend(soup.findAll('span'))
    
    video_playlist_items = []
    video_source_id = 0
    video_source_name = None
    video_source = {}
    
    for tag in tags:
        if re.search('^(Source|ONLINE|Server)', tag.getText(), re.IGNORECASE):
            if len(video_playlist_items) > 0:
                main.addPlayList(video_source_name, url,constants.SOMINAL_PLAY, video_source_id, video_playlist_items, name, '')
                
                video_source[video_source_name] = video_playlist_items
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
        if len(video_source) == 0 :
            video_source_id = video_source_id + 1
        print 'HERE >>>>>>>> ' + str(video_source_id)
        main.addPlayList(video_source_name, url,constants.SOMINAL_PLAY, video_source_id, video_playlist_items, name, '')
        video_source[video_source_name] = video_playlist_items
        
    playNow(video_source, name)

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
        