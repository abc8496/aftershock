import urllib,re,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main

import CommonFunctions as common

from resources.libs import settings, constants, jsonutil, fileutil
addon_id = settings.getAddOnID()

selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
MainUrl='http://www.movie25.cm/'
prettyName='Movie25'

def LISTMOVIES(murl,index=False):
    link = main.OPENURL(murl)
    result = common.parseDOM(link, "div", attrs = { "class" : "movie_table" })
    result = common.parseDOM(result, "div", attrs = {"class": "movie_pic"})
    
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until Movie list is cached.')
    
    totalLinks = len(result)
    loadedLinks = 0
    remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
    xbmc.executebuiltin("XBMC.Dialog.Close(busydialog,true)")
    
    for item in result:
        title = common.parseDOM(item, "a", ret="title")[0]
        url = common.parseDOM(item, "a", ret="href")[0]
        thumb = common.parseDOM(item, "img" , ret="src")[0]
        
        title = title.replace('-','').replace('&','').replace('acute;','').strip()
        title = title.encode('utf-8')
        
        if index == 'True':
            main.addInfo(title,MainUrl+url,21,thumb,'','')
        else:
            main.addInfo(title,MainUrl+url,constants.MOVIE25_VIDEOLINKS,thumb,'','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if dialogWait.iscanceled(): return False   
    dialogWait.close()
    del dialogWait
    
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    
    paginate = common.parseDOM(link, "div", attrs = { "class" : "count_text" })[0]
    href = common.parseDOM(paginate, "a", ret="href")
    content = common.parseDOM(paginate, "a")
    indx = 0
    pageNo = 0
    lastPg = 0
    pageIndx = 0
    for i in content:
        if i == "Next":
            pageNo = re.findall('/.+?/(\d+)',href[indx])
            if len(pageNo) == 0:
                pageNo = re.findall("search.php.?page=([^<]+)&year=.+?", href[indx])
                href[indx] = "/" + href[indx]
            pageNo=int(pageNo[0])
            pageIndx = indx
        if i == "Last":
            lastPg = re.findall('/.+?/(\d+)',href[indx])
            if len(lastPg) == 0:
                lastPg = re.findall("search.php.?page=([^<]+)&year=.+?", href[indx])
                href[indx] = "/" + href[indx]
            if len(lastPg) > 0 :
                lastPg = int(lastPg[0])
            else :
                lastPg = 0
        indx=indx+1
    
    searchPage = re.findall("search.php.?page=([^<]+)&year=.+?", href[pageIndx])
    if not len(searchPage) > 0 and lastPg > 0 :
        main.addDir('[COLOR red]Enter Page #[/COLOR]',murl,constants.MOVIE25_GOTOPAGE,art+'/gotopage.png',index=index)
    if lastPg > 0 :
        main.addDir('[COLOR blue]Page '+ str(pageNo) + ' of ' + str(lastPg) +'[/COLOR]',MainUrl+href[pageIndx],constants.MOVIE25_LISTMOVIES,art+'/next.png',index=index)
    elif pageNo <> lastPg :
        main.addDir('[COLOR blue]Page '+ str(pageNo)+'[/COLOR]',MainUrl+href[pageIndx],constants.MOVIE25_LISTMOVIES,art+'/next.png',index=index)
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    main.VIEWS()

def Searchhistory(index=False):
    seapath=os.path.join(main.datapath,'Search')
    SeaFile=os.path.join(seapath,'SearchHistory25')
    if not os.path.exists(SeaFile):
        SEARCH(index=index)
    else:
        main.addDir('Search','###',constants.MOVIE25_SEARCH,art+'/search.png',index=index)
        main.addDir('Clear History',SeaFile,constants.MAIN_CLEAR_HISTORY,art+'/cleahis.png')
        thumb=art+'/link.png'
        searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
        for seahis in reversed(searchis):
            url=seahis
            seahis=seahis.replace('%20',' ')
            main.addDir(seahis,url,constants.MOVIE25_SEARCH,thumb,index=index)
            
def SEARCH(murl = '',index=False):
    encode = main.updateSearchFile(murl,'Movies')
    if not encode: return False   
    surl=MainUrl+'/search.php?key='+encode+'&submit='
    LISTMOVIES(surl, index)

def ENTYEAR(index=False):
    dialog = xbmcgui.Dialog()
    d = dialog.numeric(0, 'Enter Year')
    if d:
        encode=urllib.quote(d)
        if encode < '2015' and encode > '1900':
            surl=MainUrl + '/search.php?year='+encode+'/'
            LISTMOVIES(surl,index=index)
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.ok('Wrong Entry', 'Must enter year in four digit format like 1999','Entry must be between 1900 and 2014')
        
def GotoPage(url,index=False):
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    r = re.findall('>Next</a><a href=\'/.+?/(\d+)\'>Last</a>',link)
    x = re.findall('>Next</a><a href=\'([^<]+)/.+?\'>Last</a>',link)
    dialog = xbmcgui.Dialog()
    d = dialog.numeric(0, 'Section Last Page = '+r[0])
    if d:
        pagelimit=int(r[0])
        if int(d) <= pagelimit:
            encode=urllib.quote(d)
            surl=MainUrl+x[0]+'/'+encode
            LISTMOVIES(surl,index=index)
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.ok('Wrong Entry', 'The page number you entered does not exist.',' This sections page limit is '+str(pagelimit) )
    else:
        xbmcplugin.endOfDirectory(int(sys.argv[1]), False, False)
        return False

def YEARB(murl,index=False):
    LISTMOVIES(murl, index)
        
def VIDEOLINKS(name,url):
    link=main.OPENURL(url)
    #link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    print link
    qual = re.compile('<h1 >Links - Quality\s*?([^\s]+?)\s*?</h1>').findall(link)
    print qual
    quality = str(qual)
    quality = quality.replace("'","")
    name  = name.split('[COLOR blue]')[0]
    
    links = common.parseDOM(link, "div", attrs = { "class" : "links"})
    if len(links) > 0:
        links = links[0]
    else :
        links = common.parseDOM(link, "div", attrs = { "id" : "links"})[0]
    
    tmplinks = common.parseDOM(links, "ul")
    tmplinks += common.parseDOM(links, "ul", attrs = {"class": "hidden"})
    links = tmplinks
    import collections
    all_coll = collections.defaultdict(list)
    
    for item in links:
        host = common.parseDOM(item, "li", attrs = { "class": "link_name" })
        
        if len(host) > 0:
            host = host[0]
        else :
            host = common.parseDOM(item, "li", attrs = { "id": "link_name" })[0]
        url = common.parseDOM(item, "a", ret="href")
        if len(url) > 0: 
            url = url[0]
        else :
            #url = re.findall(',\'(.+?)\'.;',item)[0] # Gets the direct URL
            url = common.parseDOM(item,"li", attrs = {"id" : "download"}, ret="onclick")[0]
            url = re.findall('open\(\'(.+?)\'\)', url)[0]
        all_coll[host].append(url)

    all_coll = all_coll.items()
    sortorder = "vk, gvideo, muchmovies, sweflix, yify, enithusan, movreel, 180upload, vidplay, uptobox, mrfile, mightyupload, hugefiles, filecloud, uploadrocket, kingfiles, ororo, putlocker,sockshare,lemuploads,megarelease,filenuke,flashx,veehd,vidto,allmyvideos,dailymotion,movshare,nosvideo,novamov,nowvideo,played,playwire,sharerepo,sharesix,streamcloud,thefile,vidbull,videotanker,videoweed,vidxden,xvidstage,youtube,youwatch,vodlocker, streamin, letwatch,uploaddc, vidbux, grifthost, putstream, bestreams, oboom, tusfiles, realvid, noslocker, vid, plocker, video, netu, vshare, rocvideo, cloudyvideos, filehoot, exashare, shared, divxpress, vidlockers, goodvideohost, junkyvideo, cloudtime, yourvideohost, thevideo, vidspot, zettahost, videomega"
    sortorder = ','.join((sortorder.split(',')[::-1]))
    all_coll = sorted(all_coll, key=lambda word: sortorder.find(word[0].lower())*-1)
    for host,urls in all_coll:
        if host.lower() in sortorder:
            host = host.strip()
            main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+" [COLOR blue]"+host.upper()+"[/COLOR]",str(urls),constants.MOVIE25_GROUPED_HOSTS,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')

def GroupedHosts(name,url,thumb):
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    urls = eval(url)
    for url in urls:
        main.addDown2(name,MainUrl+url,constants.MOVIE25_PLAY,thumb,thumb)
        
def resolveM25URL(url):
    html=main.OPENURL(url)
    url = common.parseDOM(html, "iframe", ret="src")
    url += common.parseDOM(html, "IFRAME", ret="SRC")
    if len(url) == 0 :
        url = common.parseDOM(html, "div", attrs = {"class":"left_body"})[0]
        url = common.parseDOM(url, "input", ret="onclick")[0]
    elif len(url) == 1:
        url = url[0]
    url = re.compile('(http.+)').findall(url)[0]
    url = url.replace("'","")
    return url
    
def PLAY(name,murl):
    ok=True
    hname=name
    name  = name.split('[COLOR blue]')[0]
    name  = name.split('[COLOR red]')[0]
    infoLabels = main.GETMETAT(name,'','','')
    murl = resolveM25URL(murl)
    if not murl: return False
    video_type='movie'
    season=''
    episode=''
    img=infoLabels['cover_url']
    fanart =infoLabels['backdrop_url']
    imdb_id=infoLabels['imdb_id']
    infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }

    try:
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
        stream_url = main.resolve_url(murl)
        
        infoL={'Title': infoLabels['metaName'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
        # play with bookmark
        from resources.universal import playbackengine
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            from resources.universal import watchhistory
            wh = watchhistory.WatchHistory(addon_id)
            wh.add_item(hname+' '+'[COLOR green]Movie25[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
        player.KeepAlive()
        return ok
    except Exception, e:
        if stream_url != False:
                main.ErrorReport(e)
        return ok

def PLAYB(name,murl):
    ok=True
    hname=name
    name  = name.split('[COLOR blue]')[0]
    name  = name.split('[COLOR red]')[0]
    infoLabels = main.GETMETAT(name,'','','')
    video_type='movie'
    season=''
    episode=''
    img=infoLabels['cover_url']
    fanart =infoLabels['backdrop_url']
    imdb_id=infoLabels['imdb_id']
    infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }

    try:
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
        stream_url = main.resolve_url(murl)

        infoL={'Title': infoLabels['metaName'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
        # play with bookmark
        from resources.universal import playbackengine
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            from resources.universal import watchhistory
            wh = watchhistory.WatchHistory(addon_id)
            wh.add_item(hname+' '+'[COLOR green]Movie25[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
        player.KeepAlive()
        return ok
    except Exception, e:
        if stream_url != False:
                main.ErrorReport(e)
        return ok
