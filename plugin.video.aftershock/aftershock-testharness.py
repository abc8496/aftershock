import sys, re

sys.argv = ['plugin.video.aftershock', '1']


try :
    # playItem
    #params = {'name': 'Piku (2015)', 'tvdb': '0', 'content': 'movie', 'source': '[{"url": "http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_1##http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_2##http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_3##http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_4", "label": "02 | [B]PLAYINDIAFILMS[/B] | MEDIAPLAYBOX | [B][I]HD [/I][/B] [4]", "source": "mediaplaybox", "parts": "4", "provider": "PlayIndiaFilms", "quality": "HD"}]', 'imdb': 'tt3767372', 'year': '2015', 'action': 'playItem'}
   # params = {'action': 'movies', 'lang': 'hi', 'url': '/browse/hindi?order=desc&sort=date&page=2', 'provider': 'apnaview_mv'}
    #params =  {'action': 'movies', 'lang': 'tamil', 'url': 'HD', 'provider': 'playindiafilms_mv'}
    params = {'tmdb': '362136', 'name': 'Prem Ratan Dhan Payo (2015)', 'title': 'Prem Ratan Dhan Payo', 'meta': '{"rating": "6.6", "tmdb": "362136", "code": "tt3595298", "imdb": "tt3595298", "year": "2015", "duration": "10440", "plot": "Loosely based on the novel The prince and the Pauper. Ever loving Prem is respected and loved by all and Vijay (also played by Salman Khan) is in the world of hatred and violence. They change their identities temporarily to discover the other side of the world.", "votes": "11", "title": "Prem Ratan Dhan Payo", "fanart": "http://image.tmdb.org/t/p/original/9fVjhznaYPcQF7eHZ08CkytmTbL.jpg", "mpaa": "NR", "writer": "Sooraj R. Barjatya", "poster": "http://image.tmdb.org/t/p/w500/8mfZyMKdyXGjwr27dCCBUp4fwVG.jpg", "director": "Sooraj R. Barjatya", "studio": "Fox Star Studios", "genre": "Drama / Action / Romance", "metacache": false, "lang": "hindi", "name": "Prem Ratan Dhan Payo (2015)", "premiered": "2015-11-11", "originaltitle": "Prem Ratan Dhan Payo", "cast": [["Salman Khan", "Prem/Vijay"], ["Sonam Kapoor", "Maithili"], ["Neil Nitin Mukesh", "Yuvraj Ajay Singh"], ["Anupam Kher", "Diwan"], ["Swara Bhaskar", "Chandrika"], ["Deepak Dobriyal", "Kanhaiya"], ["Arman Kohli", "Chirag Singh"], ["Manoj Joshi", "Bhandari"]], "tagline": "Loosely based on the novel The prince and the Pauper", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Prem+Ratan+Dhan+Payo+%282015%29"}', 'imdb': 'tt3595298', 'year': '2015', 'action': 'sources'}


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

    try:
        lang = params['lang']
    except:
        lang = None

    from resources.lib.indexers import movies

    # test search sources
    from resources.lib.sources import einthusan_mv
    from resources.lib.sources import playindiafilms_mv
    from resources.lib.sources import client
    from resources.lib.indexers import movies

    #movies.movies().get(url, provider=provider, lang=lang)

    #playindiafilms_mv.source().get_movie("", "welcome back", "2015")
    #playindiafilms_mv.source().get_sources("piku-2015", [], [], [])
    #einthusan_mv.source().get_movie(imdb, title, year)

    from resources.lib.sources import sources
    #movies.movies().get(url, provider=provider, lang=lang)
    sources().addItem(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta)
    #sources().playItem(content, name, year, imdb, tvdb, source)

except:
    from resources.lib.libraries import client
    client.printException('aftershock-testharness')