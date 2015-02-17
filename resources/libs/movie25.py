import urllib,re,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main

import CommonFunctions as common

from resources.libs import settings, constants, jsonutil, fileutil
addon_id = settings.getAddOnID()

selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
MainUrl='http://www.movie25.cm'
prettyName='Movie25'

def LISTMOVIES(murl,index=False):
    link = main.OPENURL(murl)
    result = common.parseDOM(link, "div", attrs = { "class" : "movie_table" })[0]
    result = common.parseDOM(result, "li")
    
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
    for i in content:
        if i == "Next":
            pageNo = re.findall('/.+?/(\d+)',href[indx])
            pageNo=int(pageNo[0])
            main.addDir('[COLOR blue]Page '+ str(pageNo)+'[/COLOR]',MainUrl+href[indx],constants.MOVIE25_LISTMOVIES,art+'/next.png',index=index)
        indx=indx+1
    
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
            
def superSearch(encode,type):
    try:
        returnList=[]
        surl=MainUrl+'/search.php?key='+encode+'&submit='
        link=main.OPENURL(surl,verbose=False)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class="movie_pic"><a href="([^"]+?)"[^>]+?>\s*?<img src="([^"]+?)"[^>]+?>.+?<a href[^>]+?>([^<]+?)</a></h1><div class=".+?">().*?Views: <span>(.+?)</span>.+?id=RateCount_.+?>(.+?)</span>.*?<li class="current-rating" style="width:(\d+?)px').findall(link)
        for url,thumb,name,genre,views,votes,rating in match:
            url= MainUrl+url
            name=name.replace('  ','')
            returnList.append((name,prettyName,url,thumb,3,True))
        return returnList
    except: return []

def SEARCH(murl = '',index=False):
    encode = main.updateSearchFile(murl,'Movies')
    if not encode: return False   
    surl=MainUrl+'/search.php?key='+encode+'&submit='
    link=main.OPENURL(surl)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match=re.compile('<div class="movie_pic"><a href="([^"]+?)"[^>]+?>\s*?<img src="([^"]+?)"[^>]+?>.+?<a href[^>]+?>([^<]+?)</a></h1><div class=".+?">().*?Views: <span>(.+?)</span>.+?id=RateCount_.+?>(.+?)</span>.*?<li class="current-rating" style="width:(\d+?)px').findall(link)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until Movie list is cached.')
    totalLinks = len(match)
    loadedLinks = 0
    remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
    xbmc.executebuiltin("XBMC.Dialog.Close(busydialog,true)")
    for url,thumb,name,genre,views,votes,rating in match:
        name=name.replace('-','').replace('&','').replace('acute;','')
        furl= MainUrl+url
        if index == 'True':
            main.addInfo(name+'[COLOR blue] Views: '+views+'[/COLOR] [COLOR red]Votes: '+votes+'[/COLOR] [COLOR green]Rating: '+rating+'/100[/COLOR]',furl,21,thumb,genre,'')
        else:
            main.addInfo(name+'[COLOR blue] Views: '+views+'[/COLOR] [COLOR red]Votes: '+votes+'[/COLOR] [COLOR green]Rating: '+rating+'/100[/COLOR]',furl,constants.MOVIE25_VIDEOLINKS,thumb,genre,'')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if dialogWait.iscanceled(): return False 
    dialogWait.close()
    del dialogWait
    exist = re.findall("<a href='search.php.?page=.+?'>Next</a>",link)
    if exist:
        r = re.findall(""">Next</a><a href='search.php.?page=([^<]+)&key=.+?'>Last</a>""",link)
        if r:
            main.addDir('[COLOR blue]Page 1 of '+r[0]+'[/COLOR]','http://www.movie25.so/search.php?page=2&key='+encode,constants.MOVIE25_NEXTPAGE,art+'/next.png',index=index)
        else:
            main.addDir('[COLOR blue]Page 1[/COLOR]','http://www.movie25.so/search.php?page=2&key='+encode,constants.MOVIE25_NEXTPAGE,art+'/next.png',index=index)
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')



def ENTYEAR(index=False):
    dialog = xbmcgui.Dialog()
    d = dialog.numeric(0, 'Enter Year')
    if d:
        encode=urllib.quote(d)
        if encode < '2015' and encode > '1900':
            surl='http://www.movie25.so/search.php?year='+encode+'/'
            YEARB(surl,index=index)
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.ok('Wrong Entry', 'Must enter year in four digit format like 1999','Enrty must be between 1900 and 2014')
        
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

def GotoPageB(url,index=False):
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    r = re.findall('>Next</a><a href=\'search.php.?page=(.+?)&year=.+?\'>Last</a>',link)
    dialog = xbmcgui.Dialog()
    d = dialog.numeric(0, 'Section Last Page = '+r[0])
    if d:
        pagelimit=int(r[0])
        if int(d) <= pagelimit:
            encode=urllib.quote(d)
            year  = url.split('year=')
            url  = url.split('year=')
            url  = url[0].split('page=')
            surl=url[0]+'page='+encode+'&year='+year[1]
            NEXTPAGE(surl,index=index)
        else:
            dialog = xbmcgui.Dialog()
            ret = dialog.ok('Wrong Entry', 'The page number you entered does not exist.',' This sections page limit is '+str(pagelimit) )
    else:
        xbmcplugin.endOfDirectory(int(sys.argv[1]), False, False)
        return False

def YEARB(murl,index=False):
    link=main.OPENURL(murl)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match=re.compile('<div class="movie_pic"><a href="(.+?)" target=".+?">    <img src="(.+?)" width=".+?" height=".+?" />.+?<a href=".+?" target=".+?">(.+?)</a></h1><div class=".+?">Genre:  <a href=".+?" target=\'.+?\'>(.+?)</a>.+?Release:.+?<br/>Views: <span>(.+?)</span>.+?id=RateCount_.+?>(.+?)</span> votes.*?<li class="current-rating" style="width:(\d+?)px').findall(link)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until Movie list is cached.')
    totalLinks = len(match)
    loadedLinks = 0
    remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
    for url,thumb,name,genre,views,votes,rating in match:
        name=name.replace('-','').replace('&','').replace('acute;','')
        furl= 'http://movie25.com/'+url
        if index == 'True':
            main.addInfo(name+'[COLOR blue] Views: '+views+'[/COLOR] [COLOR red]Votes: '+votes+'[/COLOR] [COLOR green]Rating: '+rating+'/100[/COLOR]',furl,21,thumb,genre,'')
        else:
            main.addInfo(name+'[COLOR blue] Views: '+views+'[/COLOR] [COLOR red]Votes: '+votes+'[/COLOR] [COLOR green]Rating: '+rating+'/100[/COLOR]',furl,constants.MOVIE25_VIDEOLINKS,thumb,genre,'')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if dialogWait.iscanceled(): return False 
    dialogWait.close()
    del dialogWait
    ye = murl[38:45]
    r = re.findall("Next</a><a href='search.php.?page=([^<]+)&year=.+?'>Last</a>",link)
    if r:
        main.addDir('[COLOR red]Enter Page #[/COLOR]',murl,constants.MOVIE25_GOTOPAGEB,art+'/gotopage.png',index=index)
        main.addDir('[COLOR blue]Page 1 of '+r[0]+'[/COLOR]','http://www.movie25.so/search.php?page=2&year='+str(ye),constants.MOVIE25_NEXTPAGE,art+'/next.png',index=index)    
    else:
        main.addDir('[COLOR blue]Page 1[/COLOR]','http://www.movie25.so/search.php?page=2&year='+str(ye),constants.MOVIE25_NEXTPAGE,art+'/next.png',index=index)
    
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    main.VIEWS()
        
def NEXTPAGE(murl,index=False):
    link=main.OPENURL(murl)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match=re.compile('<div class="movie_pic"><a href="(.+?)" target=".+?">    <img src="(.+?)" width=".+?" height=".+?" />.+?<a href=".+?" target=".+?">(.+?)</a></h1><div class=".+?">Genre:  <a href=".+?" target=\'.+?\'>(.+?)</a>.+?Release:.+?<br/>Views: <span>(.+?)</span>.+?id=RateCount_.+?>(.+?)</span> votes.*?<li class="current-rating" style="width:(\d+?)px').findall(link)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until Movie list is cached.')
    totalLinks = len(match)
    loadedLinks = 0
    remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
    for url,thumb,name,genre,views,votes,rating in match:
        name=name.replace('-','').replace('&','').replace('acute;','')
        furl= MainUrl+url
        if index == 'True':
            main.addInfo(name+'[COLOR blue] Views: '+views+'[/COLOR] [COLOR red]Votes: '+votes+'[/COLOR] [COLOR green]Rating: '+rating+'/100[/COLOR]',furl,21,thumb,genre,'')
        else:
            main.addInfo(name+'[COLOR blue] Views: '+views+'[/COLOR] [COLOR red]Votes: '+votes+'[/COLOR] [COLOR green]Rating: '+rating+'/100[/COLOR]',furl,constants.MOVIE25_VIDEOLINKS,thumb,genre,'')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if dialogWait.iscanceled(): return False
    dialogWait.close()
    del dialogWait
    
    matchx=re.compile('http://www.movie25.so/search.php.+?page=(.+?)&year=(.+?)').findall(murl)
    if len(matchx)>0:
        durl = murl + '/'
        paginate=re.compile('http://www.movie25.so/search.php.+?page=(.+?)&year=(.+?)/').findall(durl)
        for page, yearb in paginate:
            pgs = int(page)+1
            jurl='http://www.movie25.so/search.php?page='+str(pgs)+'&year='+str(yearb)
#                 main.addDir('[COLOR red]Home[/COLOR]','',0,art+'/home.png')
        r = re.findall("Next</a><a href='search.php.?page=([^<]+)&year=.+?'>Last</a>",link)
        if r:
            main.addDir('[COLOR red]Enter Page #[/COLOR]',murl,constants.MOVIE25_GOTOPAGEB,art+'/gotopage.png',index=index)
            main.addDir('[COLOR blue]Page '+str(page)+' of '+r[0]+'[/COLOR]',jurl,constants.MOVIE25_NEXTPAGE,art+'/next.png',index=index)
        else:
            main.addDir('[COLOR blue]Page '+str(page)+'[/COLOR]',jurl,constants.MOVIE25_NEXTPAGE,art+'/next.png',index=index)
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        main.VIEWS()                
    else:
        durl = murl + '/'
        paginate=re.compile('http://www.movie25.so/search.php.+?page=(.+?)&key=(.+?)/').findall(durl)
        for page, search in paginate:
            pgs = int(page)+1
            jurl='http://www.movie25.so/search.php?page='+str(pgs)+'&key='+str(search)
#                 main.addDir('[COLOR red]Home[/COLOR]','',0,art+'/home.png')
        r = re.findall(""">Next</a><a href='search.php.?page=([^<]+)&key=.+?'>Last</a>""",link)
        if r:
            main.addDir('[COLOR blue]Page '+str(page)+' of '+r[0]+'[/COLOR]',jurl,constants.MOVIE25_NEXTPAGE,art+'/next.png',index=index)
        else:
            main.addDir('[COLOR blue]Page '+str(page)+'[/COLOR]',jurl,constants.MOVIE25_NEXTPAGE,art+'/next.png',index=index)

def VIDEOLINKS(name,url):
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    qual = re.compile('<h1 >Links - Quality\s*?([^\s]+?)\s*?</h1>').findall(link)
    quality = str(qual)
    quality = quality.replace("'","")
    name  = name.split('[COLOR blue]')[0]
    
    links = common.parseDOM(link, "div", attrs = { "class" : "links"})[0]
    links = common.parseDOM(links, "ul")
    import collections
    all_coll = collections.defaultdict(list)
    
    for item in links:
        host = common.parseDOM(item, "li", attrs = { "class": "link_name" })[0]
        url = common.parseDOM(item, "a", ret="href")[0]
        all_coll[host].append(url)

    all_coll = all_coll.items()
    sortorder = "putlocker,sockshare,billionuploads,hugefiles,mightyupload,movreel,lemuploads,180upload,megarelease,filenuke,flashx,gorillavid,bayfiles,veehd,vidto,epicshare,2gbhosting,alldebrid,allmyvideos,castamp,cheesestream,clicktoview,crunchyroll,cyberlocker,daclips,dailymotion,divxstage,donevideo,ecostream,entroupload,facebook,filebox,hostingbulk,hostingcup,jumbofiles,limevideo,movdivx,movpod,movshare,movzap,muchshare,nolimitvideo,nosvideo,novamov,nowvideo,ovfile,play44_net,played,playwire,premiumize_me,primeshare,promptfile,purevid,rapidvideo,realdebrid,rpnet,seeon,sharefiles,sharerepo,sharesix,skyload,stagevu,stream2k,streamcloud,thefile,tubeplus,tunepk,ufliq,upbulk,uploadc,uploadcrazynet,veoh,vidbull,vidcrazynet,video44,videobb,videofun,videotanker,videoweed,videozed,videozer,vidhog,vidpe,vidplay,vidstream,vidup_org,vidx,vidxden,vidzur,vimeo,vureel,watchfreeinhd,xvidstage,yourupload,youtube,youwatch,zalaa,zooupload,zshare,"
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
        print url
        main.addDown2(name,MainUrl+url,constants.MOVIE25_PLAY,thumb,thumb)
        
def resolveM25URL(url):
    html=main.OPENURL(url)
    url = common.parseDOM(html, "iframe", ret="src")
    url += common.parseDOM(html, "IFRAME", ret="SRC")
    if len(url) == 0 :
        url = common.parseDOM(html, "div", attrs = {"class":"left_body"})[0]
        url = common.parseDOM(url, "input", ret="onclick")[0]
    print url
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
    print murl
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
        
        print 'INDIDE PLAY : ' + stream_url

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
