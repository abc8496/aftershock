import sys

sys.argv = ['plugin.video.aftershock', '1']
try :
    from resources.lib.sources import playindiafilms_mv

    # MediaPlayBox URL
    url = "http://www.mediaplaybox.com/video/Bajrangi_Bhaijaan_Eng_Sub_Part_1##http://www.mediaplaybox.com/video/Bajrangi_Bhaijaan_Eng_Sub_Part_2##http://www.mediaplaybox.com/video/Bajrangi_Bhaijaan_Eng_Sub_Part_3##http://www.mediaplaybox.com/video/Bajrangi_Bhaijaan_Eng_Sub_Part_4##http://www.mediaplaybox.com/video/Bajrangi_Bhaijaan_Eng_Sub_Part_5##http://www.mediaplaybox.com/video/Bajrangi_Bhaijaan_Eng_Sub_Part_6"

    # desiflicks URL

    url = "http://www.desiflicks.com/video/bajrangi-bhaijaan-2015-english-subtitles-hindi-movie-part-1/##http://www.desiflicks.com/video/bajrangi-bhaijaan-2015-english-subtitles-hindi-movie-part-2/"

    # desiflicks URL2

    url = "http://media.desiflicks.com/4939##http://media.desiflicks.com/4940##http://media.desiflicks.com/4941##http://media.desiflicks.com/4942##http://media.desiflicks.com/4943##http://media.desiflicks.com/4944"
    #print playindiafilms_mv.source().resolve(url)

    #from resources.lib.indexers import tvshows

    #url = 'forumdisplay.php?f=176'
    #channel = 'Colors'
    #provider = 'desirulez_tv'
    #tvshows.tvshows().get(url, channel=channel, provider=provider)

    #params for getepisodes
    #params = {'tmdb': '39083', 'tvdb': '273190', 'tvshowtitle': 'Sasural Simar Ka', 'year': '0', 'url': 'forums/2498-Sasural-Simar-Ka?s=485267fe875e5e71d08730ed0ad7f24f', 'imdb': 'tt1934806', 'provider': 'desirulez_tv', 'action': 'episodes', 'tvrage': '0'}


    # params for getsources
    params =  {'tmdb': '0', 'episode': '0', 'name': '5th February 2016', 'title': '5th February 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Sasural Simar Ka', 'year': '0', 'date': '0', 'meta': '{"tvshowurl": "forums/2498-Sasural-Simar-Ka?s=bbbd558b7a817327c6c5cac90a92e545", "title": "5th February 2016", "url": "threads/850585-Sasural-Simar-Ka-5th-February-2016-Watch-Online?s=bbbd558b7a817327c6c5cac90a92e545", "tvshowtitle": "Sasural Simar Ka", "next": "forums/2498-Sasural-Simar-Ka/page2?s=bbbd558b7a817327c6c5cac90a92e545", "provider": "desirulez_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Sasural+Simar+Ka", "name": "5th February 2016"}', 'imdb': '0', 'provider': 'desirulez_tv', 'action': 'sources', 'tvrage': '0', 'alter': '0'}
    params = {'name': 'Airlift (2016)', 'tvdb': '0', 'content': 'movie', 'source': '[{"url": "http://www.awesomevids.pw/video/105169##http://www.awesomevids.pw/video/105170##http://www.awesomevids.pw/video/105171", "label": "06 | [B]APNAVIEW[/B] | LETWATCH | [I]CAM [/I] [3]", "source": "letwatch", "parts": "3", "provider": "ApnaView", "quality": "CAM"}]', 'imdb': 'tt4387040', 'year': '2016', 'action': 'playItem'}
    params = {'name': 'Airlift (2016)', 'tvdb': '0', 'content': 'movie', 'source': '[{"url": "http://www.awesomevids.pw/video/105159##http://www.awesomevids.pw/video/105160##http://www.awesomevids.pw/video/105161", "label": "04 | [B]APNAVIEW[/B] | PLAYWIRE | [I]CAM [/I] [3]", "source": "playwire", "parts": "3", "provider": "ApnaView", "quality": "CAM"}]', 'imdb': 'tt4387040', 'year': '2016', 'action': 'playItem'}
    params = {'name': 'Airlift (2016)', 'tvdb': '0', 'content': 'movie', 'source': '[{"url": "http://www.awesomevids.pw/video/105169##http://www.awesomevids.pw/video/105170##http://www.awesomevids.pw/video/105171", "label": "06 | [B]APNAVIEW[/B] | LETWATCH | [I]CAM [/I] [3]", "source": "letwatch", "parts": "3", "provider": "ApnaView", "quality": "CAM"}]', 'imdb': 'tt4387040', 'year': '2016', 'action': 'playItem'}
    params = {'tmdb': '348892', 'name': 'Bajrangi Bhaijaan (2015)', 'title': 'Bajrangi Bhaijaan', 'meta': '{"rating": "7.9", "code": "tt3863552", "tmdb": "348892", "imdb": "tt3863552", "year": "2015", "duration": "9540", "plot": "A young mute girl from Pakistan loses herself in India with no way to head back. A devoted man with a magnanimous spirit undertakes the task to get her back to her motherland and unite her with her family.", "votes": "80", "title": "Bajrangi Bhaijaan", "fanart": "http://image.tmdb.org/t/p/original/gT3xgPyb7yoaVJoeiCefxe0TtTD.jpg", "tagline": "A young mute girl from Pakistan loses herself in India with no way to head back", "writer": "K. V. Vijayendra Prasad", "next": "/category/hindi-blurays/feed?paged=4", "poster": "http://image.tmdb.org/t/p/w500/71dIayQVmWw2QEs4AJFpqdv2n0S.jpg", "director": "Kabir Khan", "studio": "Kabir Khan Films", "genre": "Drama / Action / Comedy / Romance", "metacache": false, "lang": "en", "name": "Bajrangi Bhaijaan (2015)", "premiered": "2015-07-17", "originaltitle": "Bajrangi Bhaijaan", "cast": [["Salman Khan", "Pawan Kumar Chaturvedi / Bajrangi"], ["Kareena Kapoor", "Rasika"], ["Harshaali Malthotra", "Munni / Shahida"], ["Nawazuddin Siddiqui", "Chand Nawab (Pakistani Reporter)"], ["Rajesh Sharma", "Senior Pakistani Police Officer"], ["Sharat Saxena", "Dayanand, Rasika\'s Father"], ["Om Puri", "Molana"], ["Meher Vij", "Shahida\'s mother"]], "mpaa": "UA", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Bajrangi+Bhaijaan+%282015%29"}', 'imdb': 'tt3863552', 'year': '2015', 'action': 'sources'}
    params = {'tmdb': '0', 'episode': '0', 'name': '12th February 2016', 'title': '12th February 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Saubhaghyalakshmi', 'year': '0', 'date': '0', 'meta': '{"tvshowurl": "forums/3830-Saubhaghyalakshmi?s=3a76fabc38cf22276befc1ed452f24fa", "title": "12th February 2016", "url": "threads/854548-Saubhaghyalakshmi-12th-February-2016-Watch-Online?s=3a76fabc38cf22276befc1ed452f24fa", "tvshowtitle": "Saubhaghyalakshmi", "next": "forums/3830-Saubhaghyalakshmi/page2?s=3a76fabc38cf22276befc1ed452f24fa", "provider": "desirulez_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Saubhaghyalakshmi", "name": "12th February 2016"}', 'imdb': '0', 'provider': 'desirulez_tv', 'action': 'sources', 'tvrage': '0', 'alter': '0'}
    params = {'action': 'movies', 'url': 'added', 'provider': 'apnaview_mv'}
    params = {'action': 'movies', 'url': '/browse/hindi?order=desc&sort=date&page=2', 'provider': 'apnaview_mv'}

    #params = {'name': '13th February 2016', 'tvdb': '0', 'content': 'episode', 'source': '[{"url": "http://www.tellycolors.me/shashtri-sisters/?si=4593378##http://www.tellycolors.me/shashtri-sisters/?si=4593382", "label": "01 | [B]DESIRULEZ[/B] | FLASH PLAYER | [B][I]HD [/I][/B] [2]", "source": "flash player", "parts": "2", "provider": "DesiRulez", "quality": "HD"}]', 'meta': '{"tvshowurl": "forums/3520-Ishq-Ka-Rang-Safed?s=03cbe759a7ebd67edb9897a970f02f97", "title": "13th February 2016", "url": "threads/855607-Ishq-Ka-Rang-Safed-13th-February-2016-Watch-Online?s=03cbe759a7ebd67edb9897a970f02f97", "tvshowtitle": "Ishq Ka Rang Safed", "next": "forums/3520-Ishq-Ka-Rang-Safed/page2?s=03cbe759a7ebd67edb9897a970f02f97", "provider": "desirulez_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Ishq+Ka+Rang+Safed", "name": "13th February 2016"}', 'imdb': 'tt0000000', 'year': '0', 'action': 'playItem'}
    params = {'name': '12th February 2016', 'tvdb': '0', 'content': 'episode', 'source': '[{"url": "http://bestarticles.me/yeh-rishta-kya-kehlata-hai/?si=kHMUn3GMpg9mmafqMNd##http://bestarticles.me/yeh-rishta-kya-kehlata-hai/?si=k7yzAb5NYhp5KifqMNm", "label": "02 | [B]DESIRULEZ[/B] | DAILYMOTION | [B][I]HD [/I][/B] [2]", "source": "dailymotion", "parts": "2", "provider": "DesiRulez", "quality": "HD"}]', 'imdb': 'tt0000000', 'year': '0', 'action': 'playItem'}
    params = {'name': '12th February 2016', 'tvdb': '0', 'content': 'episode', 'source': '[{"url": "http://www.tellysony.com/sony-tv/?si=n7zkup140hu0##http://www.tellysony.com/sony-tv/?si=rkr9w38ionmj", "label": "03 | [B]DESIRULEZ[/B] | LETWATCH | [B][I]HD [/I][/B] [2]", "source": "letwatch", "parts": "2", "provider": "DesiRulez", "quality": "HD"}]', 'imdb': 'tt0000000', 'year': '0', 'action': 'playItem'}
    #params = {'name': '12th February 2016', 'tvdb': '0', 'content': 'episode', 'source': '[{"url": "http://bestarticles.me/yeh-rishta-kya-kehlata-hai/?si=4590144##http://bestarticles.me/yeh-rishta-kya-kehlata-hai/?si=4590143", "label": "01 | [B]DESIRULEZ[/B] | FLASH PLAYER | [B][I]HD [/I][/B] [2]", "source": "flash player", "parts": "2", "provider": "DesiRulez", "quality": "HD"}]', 'meta': '{"tvshowurl": "forums/3699-Yeh-Rishta-Kya-Kehlata-Hai?s=03cbe759a7ebd67edb9897a970f02f97", "title": "12th February 2016", "url": "threads/854208-Yeh-Rishta-Kya-Kehlata-Hai-12th-February-2016-Watch-Online?s=03cbe759a7ebd67edb9897a970f02f97", "tvshowtitle": "Yeh Rishta Kya Kehlata Hai", "provider": "desirulez_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Yeh+Rishta+Kya+Kehlata+Hai", "name": "12th February 2016"}', 'imdb': 'tt0000000', 'year': '0', 'action': 'playItem'}
    params = {'name': '12th February 2016', 'tvdb': '0', 'content': 'episode', 'source': '[{"url": "http://hd-rulez.info/idowatch.php?id=r7vaeza4ktu9##http://hd-rulez.info/idowatch.php?id=r8x8qjhjeszj", "label": "04 | [B]DESIRULEZ[/B] | IDOWATCH | [B][I]HD [/I][/B] [2]", "source": "idowatch", "parts": "2", "provider": "DesiRulez", "quality": "HD"}]', 'imdb': 'tt0000000', 'year': '0', 'action': 'playItem'}
    params = {'name': '12th February 2016', 'tvdb': '0', 'content': 'episode', 'source': '[{"url": "http://xpressvids.info/playu.php?id=ck5o03zprixc##http://xpressvids.info/playu.php?id=h0s7l5mg2q3o", "label": "05 | [B]DESIRULEZ[/B] | PLAYU | [B][I]HD [/I][/B] [2]", "source": "playu", "parts": "2", "provider": "DesiRulez", "quality": "HD"}]', 'imdb': 'tt0000000', 'year': '0', 'action': 'playItem'}

    params = {'name': 'Fitoor (2016)', 'tvdb': '0', 'content': 'movie', 'source': '[{"url": "http://www.awesomevids.pw/video/105749##http://www.awesomevids.pw/video/105750##http://www.awesomevids.pw/video/105751", "label": "08 | [B]APNAVIEW[/B] | PLAYWIRE | [I]CAM [/I] [3]", "source": "playwire", "parts": "3", "provider": "ApnaView", "quality": "CAM"}]', 'imdb': 'tt4399594', 'year': '2016', 'action': 'playItem'}
    #params = {'name': 'Fitoor (2016)', 'tvdb': '0', 'content': 'movie', 'source': '[{"url": "http://www.awesomevids.pw/video/105779##http://www.awesomevids.pw/video/105780##http://www.awesomevids.pw/video/105781", "label": "01 | [B]APNAVIEW[/B] | APNASAVE | [I]CAM [/I] [3]", "source": "apnasave", "parts": "3", "provider": "ApnaView", "quality": "CAM"}]', 'meta': '{"rating": "10.0", "code": "tt4399594", "tmdb": "376047", "imdb": "tt4399594", "year": "2016", "duration": "0", "plot": "Follows a young Kashmiri boy Noor, his muse Firdaus and a mercurial Begum.", "votes": "1", "title": "Fitoor", "tagline": "Follows a young Kashmiri boy Noor, his muse Firdaus and a mercurial Begum.", "next": "/browse/hindi?order=desc&sort=date&page=2", "poster": "http://image.tmdb.org/t/p/w500/wkF0R7sAMIGAk2SnIr2JpErJdTd.jpg", "director": "Abhishek Kapoor", "studio": "UTV Motion Pictures", "genre": "Romance / Drama", "metacache": true, "lang": "en", "name": "Fitoor (2016)", "premiered": "2016-02-12", "originaltitle": "Fitoor", "cast": [["Katrina Kaif", "Firdous"], ["Aditya Roy Kapoor", "Noor"]], "mpaa": "", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Fitoor+%282016%29"}', 'imdb': 'tt4399594', 'year': '2016', 'action': 'playItem'}



    try:
        action = params['action']
    except:
        action = None
    try:
        name = params['name']
    except:
        name = None
    try:
        title = params['title']
    except:
        title = None
    try:
        year = params['year']
    except:
        year = None
    try:
        imdb = params['imdb']
    except:
        imdb = '0'
    try:
        tmdb = params['tmdb']
    except:
        tmdb = '0'
    try:
        tvdb = params['tvdb']
    except:
        tvdb = '0'
    try:
        tvrage = params['tvrage']
    except:
        tvrage = '0'
    try:
        season = params['season']
    except:
        season = None
    try:
        episode = params['episode']
    except:
        episode = None
    try:
        tvshowtitle = params['tvshowtitle']
    except:
        tvshowtitle = None
    try:
        tvshowtitle = params['show']
    except:
        pass
    try:
        alter = params['alter']
    except:
        alter = '0'
    try:
        alter = params['genre']
    except:
        pass
    try:
        date = params['date']
    except:
        date = None
    try:
        url = params['url']
    except:
        url = None
    try:
        image = params['image']
    except:
        image = None
    try:
        meta = params['meta']
    except:
        meta = None
    try:
        query = params['query']
    except:
        query = None
    try:
        source = params['source']
    except:
        source = None
    try:
        content = params['content']
    except:
        content = None
    try:
        provider = params['provider']
    except:
        provider = None

    #title = 'Ghayal Once Again'
    #year = '2016'
    #imdb = 'tt00000000'

    #from resources.lib.sources import apnaview_mv

    #url = apnaview_mv.source().get_movie(imdb,title, year)
    #print 'Movie URL = %s' % url
    #print apnaview_mv.source().get_sources(url, [], [], [])

    #from resources.lib.sources import apnaview_mv
    #url = '/hindi-movies/watch/35416/Airlift-2016'
    #apnaview_mv.source().get_sources(url, [], [], [])

    from resources.lib.indexers import movies

    movies.movies().get(url, provider=provider)
    from resources.lib.sources import sources
    # from resources.lib.indexers import episodes
    #
    # #episodes.episodes().get(tvshowtitle, year, imdb, tmdb, tvdb, tvrage, season, episode, provider=provider, url=url)
    sources().playItem(content, name, year, imdb, tvdb, source)
    #sources().addItem(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta)
    #from resources.lib import resolvers
    #print resolvers.supportedHosts()

    #
    # #from resources.lib.sources import desirulez_tv
    # #title = 'Sasural Simar Ka'
    # #url = 'forums/2498-Sasural-Simar-Ka?s=485267fe875e5e71d08730ed0ad7f24f'
    # #url = 'forums/2498-Sasural-Simar-Ka/page2?s=b1b769323933aeeff5c937efd024008a'
    # #desirulez_tv.source().get_episodes(title, url)
    #
    # # test search sources
    # from resources.lib.sources import sources
    # sources().addItem(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta)
    #
    # from resources.lib.resolvers import tellycolors
    # # Playwire
    # url = 'http://www.tellycolors.me/balika-vadhu/?si=4576302'
    #
    # # vidhsare url
    # url = 'http://www.tellycolors.me/colors/?si=v8m8ab3g72bs'
    # url = 'http://vidshare.us/embed-v8m8ab3g72bs-595x430.html'
    # # DAILYMOTION
    # url = 'http://www.tellycolors.me/balika-vadhu/?si=k1xvL0nEgZZNg9flv6Z'
    # #IDOWATCH
    # url = 'http://bestarticles.me/colors/?si=970446x6ywj7'
    #
    # #playu
    # url = 'http://xpressvids.info/playu.php?id=bkp9bewk35ex'
    #
    # # video
    # url = 'http://desimania.net/colors/?si=39wbg65nqzxz'
    #
    # # letwatch
    # url = 'http://www.tellycolors.me/colors/?si=iyrasrqwffrt'
    #
    # # video
    # url = 'http://desimania.net/colors/?si=kwgnbk2k2qoq'
    # from resources.lib import resolvers
    # #resolvers.request(url)
except:
    from resources.lib.libraries import client
    client.printException('aftershock-testharness')