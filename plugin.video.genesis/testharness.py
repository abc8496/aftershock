#!/usr/bin/python

import sys, traceback

import xbmcaddon, xbmc

def usage() :
    print 'Usage : python testharness.py <FunctionName> <Source>'
    print '\t Where'
    print '\t  FunctionName = ALL, TV, MOVIES'
    print '\t  Source = ALL, SOURCENAME'

params = {}
functionName = None
sourceName = None

if len(sys.argv) != 3 :
    usage()
else : 
    params = sys.argv
    functionName = params[1]
    sourceName = params[2]
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List: FunctionName (%s) SourceName (%s)' % (functionName, sourceName)
    sys.argv[1] = 10
    #try :
    #    from resources.lib.indexers import movies
    #    from resources.lib.sources import sources
    #except:
    #    traceback.print_exc()
    #    pass

    name = 'Minions'
    title = 'Minions'
    year = '2015'
    imdb = None
    tmdb = None
    tvdb = None
    tvrage = None
    season = None
    episode = None
    tvshowtitle = None
    alter = None
    date = None
    meta = None
    url = None
    #action [play] name [Game of Thrones S04E09] title [The Watchers on the Wall] year [2011] imdb [0944947] tvdb [121361] tvrage [0] season [4] episode [9] tvshowtitle [Game of Thrones] alter [Adventure / Drama / Fantasy] date [2014-06-08] url [http://www.imdb.com/title/tt0944947/] image [None] meta [None] query [None] source [None] content [None] provider [None]
    #print movies.movies().get('featured')
    #print sources().addItem(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta)
    #print sources().play(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta, url)

    name = 'Heroes Reborn S01E12'
    title = 'Company Woman'
    year = '2015'
    imdb = 'tt3556944'
    tmdb = None
    tvdb = '279201'
    tvrage = '41064'
    season = '1'
    episode = '12'
    tvshowtitle = 'Heroes Reborn'
    alter = '0'
    date = '2016-01-14'
    meta = None
    url = 'plugin://plugin.video.genesis/?action=play&name=Heroes+Reborn+S01E12&title=Company+Woman&year=2015&imdb=tt3556944&tmdb=60858&tvdb=279201&tvrage=41064&season=1&episode=12&tvshowtitle=Heroes+Reborn&alter=0&date=2016-01-14'


    #from resources.lib.resolvers import urlresolver
    #print urlresolver.resolve('http://clicknupload.me/typkfk6034rb')

    #from resources.lib import resolvers

    #print resolvers.request('http://clicknupload.me/typkfk6034rb')
    #from resources.lib.sources import icefilms_mv_tv
    #CLICKNUPLOAD
    #icefilms_mv_tv.source().resolve('/membersonly/components/com_iceplayer/video.phpAjaxResp.php?id=1260904&s=10744&iqs=&url=&m=10390&cap= &sec=37fn8Oklq&t=226629&image=')

    #TUSFILES
    #icefilms_mv_tv.source().resolve('/membersonly/components/com_iceplayer/video.phpAjaxResp.php?id=1260903&s=10241&iqs=&url=&m=10363&cap= &sec=37fn8Oklq&t=226629&image=')

    #TVRELEASE UPTOBOX
    #from resources.lib.sources import tvrelease_tv
    #tvrelease_tv.source().resolve('http://uptobox.com/u55uff2fsozg')

    #DIZIBOX VKPASS
    #from resources.lib.sources import dizibox_tv
    #dizibox_tv.source().resolve('http://vkpass.com/token/MjA1SjTVJVPQ/vkphash/QCtQw58YHalirHpOkTwl0bCxp0lJpQErpC5AJ4p7mImFMX4djMGfrOqdLvPVpEB0mWW8q7RWQgtc10UpSiiyMdoVn8LqXA17lx2hmsIZXnLXUNpxk25zY86zehRwFOUzNp7OGctWlybKxKj2UjZJvf1YGgntupVmYb6aVZpMWmBK8ajaq96SoMDkHjkth2ZBbzWPWTaCHrqKyN.JbLw8YdkXfu.d87ZO9hFEi8w7HJEOFiSNAZmOUs5EhpAvRaiG|YydxBp3ytjf5zezcB83O1IfmNQHHrgu+.Ycb+v0NsHk=')

    import urllib
    from resources.lib.libraries import client

    keyBing = 'btcCcvQ4Sfo9P2Q7u62eOREA1NfLEQPezqCNb+2LVhY'        # get Bing key from: https://datamarket.azure.com/account/keys
    credentialBing = 'Basic ' + (':%s' % keyBing).encode('base64')[:-1] # the "-1" is to remove the trailing "\n" which encode adds

    headers = {}
    headers['Authorization'] = credentialBing

    baseURL = 'https://api.datamarket.azure.com/Bing/Search/v1/Image?Query=%27{query}%27&$format=json'
    channelName = 'Colors tv'
    showName = 'Bigg Boss season 9'
    query = channelName.lower() + ' ' + showName.lower() + ' poster'
    url = baseURL.format(query=urllib.quote_plus(query))
    result = client.request(url, headers=headers)
    print result
    import json
    results = json.loads(result)['d']['results']

    for image_info in results:
        print image_info
        iconImage = image_info['MediaUrl']