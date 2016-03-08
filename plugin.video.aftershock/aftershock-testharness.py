import sys, re

sys.argv = ['plugin.video.aftershock', '1']


try :
    # playItem
    #params = {'name': 'Piku (2015)', 'tvdb': '0', 'content': 'movie', 'source': '[{"url": "http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_1##http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_2##http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_3##http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_4", "label": "02 | [B]PLAYINDIAFILMS[/B] | MEDIAPLAYBOX | [B][I]HD [/I][/B] [4]", "source": "mediaplaybox", "parts": "4", "provider": "PlayIndiaFilms", "quality": "HD"}]', 'imdb': 'tt3767372', 'year': '2015', 'action': 'playItem'}
   # params = {'action': 'movies', 'lang': 'hi', 'url': '/browse/hindi?order=desc&sort=date&page=2', 'provider': 'apnaview_mv'}
    #params =  {'action': 'movies', 'lang': 'tamil', 'url': 'HD', 'provider': 'playindiafilms_mv'}
    params = {'tmdb': '362136', 'name': 'Prem Ratan Dhan Payo (2015)', 'title': 'Prem Ratan Dhan Payo', 'meta': '{"rating": "6.6", "tmdb": "362136", "code": "tt3595298", "imdb": "tt3595298", "year": "2015", "duration": "10440", "plot": "Loosely based on the novel The prince and the Pauper. Ever loving Prem is respected and loved by all and Vijay (also played by Salman Khan) is in the world of hatred and violence. They change their identities temporarily to discover the other side of the world.", "votes": "11", "title": "Prem Ratan Dhan Payo", "fanart": "http://image.tmdb.org/t/p/original/9fVjhznaYPcQF7eHZ08CkytmTbL.jpg", "mpaa": "NR", "writer": "Sooraj R. Barjatya", "poster": "http://image.tmdb.org/t/p/w500/8mfZyMKdyXGjwr27dCCBUp4fwVG.jpg", "director": "Sooraj R. Barjatya", "studio": "Fox Star Studios", "genre": "Drama / Action / Romance", "metacache": false, "lang": "hindi", "name": "Prem Ratan Dhan Payo (2015)", "premiered": "2015-11-11", "originaltitle": "Prem Ratan Dhan Payo", "cast": [["Salman Khan", "Prem/Vijay"], ["Sonam Kapoor", "Maithili"], ["Neil Nitin Mukesh", "Yuvraj Ajay Singh"], ["Anupam Kher", "Diwan"], ["Swara Bhaskar", "Chandrika"], ["Deepak Dobriyal", "Kanhaiya"], ["Arman Kohli", "Chirag Singh"], ["Manoj Joshi", "Bhandari"]], "tagline": "Loosely based on the novel The prince and the Pauper", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Prem+Ratan+Dhan+Payo+%282015%29"}', 'imdb': 'tt3595298', 'year': '2015', 'action': 'sources'}
    #params = {'tmdb': '0', 'tvdb': '0', 'tvshowtitle': 'Fear Factor Khatron Ke Khiladi Season 7', 'year': '0', 'url': 'forums/3683-Fear-Factor-Khatron-Ke-Khiladi-Season-7?s=faad8efe3f12248ca229f8be39eb3035', 'imdb': '0', 'provider': 'desirulez_tv', 'action': 'episodes', 'tvrage': '0'}
    #params = {'tmdb': '0', 'episode': '0', 'name': '1st March 2016', 'title': '1st March 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Yeh Rishta Kya Kehlata Hai', 'year': '0', 'date': '0', 'meta': '{"tvshowurl": "forums/3699-Yeh-Rishta-Kya-Kehlata-Hai?s=333166e47513e1996d0c8fde0871acc2", "title": "1st March 2016", "url": "threads/861109-Yeh-Rishta-Kya-Kehlata-Hai-1st-March-2016-Watch-Online?s=333166e47513e1996d0c8fde0871acc2", "tvshowtitle": "Yeh Rishta Kya Kehlata Hai", "provider": "desirulez_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Yeh+Rishta+Kya+Kehlata+Hai", "name": "1st March 2016"}', 'imdb': '0', 'provider': 'desirulez_tv', 'action': 'sources', 'tvrage': '0', 'alter': '0'}
    params = {'action': 'movies', 'lang': 'marathi', 'url': 'added', 'provider': 'ibollytv_mv'}
    params = {'action': 'movies', 'lang': 'marathi', 'url': '/watch-marathi-movies-online?page=2&', 'provider': 'ibollytv_mv'}
    params = {'tmdb': '0', 'name': 'Shasan (2016)', 'title': 'Shasan', 'meta': '{"name": "Shasan (2016)", "title": "Shasan", "poster": "http://cdn1.marathistars.com/wp-content/uploads/2015/09/Shasan-Marathi-Movie-Poster.jpg", "next": "/watch-marathi-movies-online?page=2&", "originaltitle": "Shasan", "imdb": "tt5061416", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Shasan+%282016%29", "year": "2016", "duration": "7200", "metacache": false}', 'imdb': 'tt5061416', 'year': '2016', 'action': 'sources'}
    params = {'tmdb': '0', 'name': 'Aligrah (2016)', 'title': 'Aligrah', 'meta': '{"name": "Aligrah (2016)", "title": "Aligrah", "poster": "http://www.apnaview.com/img/poster/50cd90328418ef3d066268408804b78b.jpg", "originaltitle": "Aligrah", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Aligrah+%282016%29", "year": "2016", "duration": "7200", "metacache": false}', 'imdb': '0', 'year': '2016', 'action': 'sources'}
    params = {'tmdb': '376869', 'name': 'Neerja (2016)', 'title': 'Neerja', 'meta': '{"rating": "8.5", "code": "tt5286444", "tmdb": "376869", "imdb": "tt5286444", "year": "2016", "duration": "7320", "plot": "Neerja is a portrayal on the life of the courageous Neerja Bhanot, who sacrificed her life while protecting the lives of 359 passengers on the Pan Am flight 73 in 1986. The flight was hijacked by a terrorist organization.", "votes": "3", "title": "Neerja", "fanart": "http://image.tmdb.org/t/p/original/sJbviiOJ15k4gcaDrdRDmyjvJvh.jpg", "tagline": "Fear Gave Her Courage", "writer": "Saiwyn Qadras", "poster": "http://image.tmdb.org/t/p/w500/97qsAXZ31E2VYfQY2zgy4djxOWE.jpg", "director": "Ram Madhvani", "studio": "T-Series", "genre": "Drama / History", "metacache": true, "name": "Neerja (2016)", "premiered": "2016-02-19", "originaltitle": "Neerja", "cast": [["Sonam Kapoor", "Neerja Bhanot"], ["Shabana Azmi", "Rama Bhanot"], ["Shekhar Ravjiani", "Jaideep"]], "mpaa": "UA", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Neerja+%282016%29"}', 'imdb': 'tt5286444', 'year': '2016', 'action': 'sources'}
    params = {'action': 'movies', 'lang': 'marathi', 'url': 'theaters', 'provider': 'ibollytv_mv'}
    params = {'action': 'movies', 'lang': 'marathi', 'url': '/watch-marathi-movies-online?sort=latest&year=2016&page=2', 'provider': 'ibollytv_mv'}
    params = {'action': 'movies', 'lang': 'punjabi', 'url': 'theaters', 'provider': 'ibollytv_mv'}
    params = {'action': 'movies', 'lang': 'kannada', 'url': 'added', 'provider': 'ibollytv_mv'}




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
    from resources.lib.indexers import episodes

    #movies.movies().get(url, provider=provider, lang=lang)

    #playindiafilms_mv.source().get_movie("", "welcome back", "2015")
    #playindiafilms_mv.source().get_sources("piku-2015", [], [], [])
    #einthusan_mv.source().get_movie(imdb, title, year)

    from resources.lib.sources import sources
    movies.movies().get(url, provider=provider, lang=lang)
    #episodes.episodes().get(tvshowtitle, year, imdb, tmdb, tvdb, tvrage, season, episode, provider=provider, url=url)
    sources().addItem(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta)
    #sources().playItem(content, name, year, imdb, tvdb, source)

except:
    from resources.lib.libraries import client
    client.printException('aftershock-testharness')