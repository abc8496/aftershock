import sys, re

sys.argv = ['plugin.video.aftershock', '1']


try :
    # addItem
    params = {'tmdb': '375290', 'name': 'Airlift (2016)', 'title': 'Airlift', 'meta': '{"rating": "5.3", "code": "tt4387040", "tmdb": "375290", "imdb": "tt4387040", "year": "2016", "duration": "7320", "plot": "Airlift is an uplifting and entertaining edge-of-the-seat thriller and is the story of the biggest ever human evacuation in the history of mankind", "votes": "15", "title": "Airlift", "fanart": "http://image.tmdb.org/t/p/original/cXFL4UUpsj2asWbMhSBwxpkndSW.jpg", "tagline": "170,000 Refugees, 488 Flights, 59 Days, 1 Man", "writer": "Ritesh Shah / Suresh Nair", "next": "", "poster": "http://image.tmdb.org/t/p/w500/f5ebYXP28qYzqZwLDQLc4tHR40U.jpg", "director": "Raja Menon", "studio": "T-Series", "genre": "Thriller / Action / Drama / History", "metacache": true, "lang": "en", "name": "Airlift (2016)", "premiered": "2016-01-22", "originaltitle": "Airlift", "cast": [["Akshay Kumar", "Ranjit Katyal"], ["Nimrat Kaur", "Amrita Katyal"], ["Feryna Wazheir", "Tasneem"], ["Lena", "Deepti Jayarajan"], ["Purab Kohli", "Ibrahim Durrani"], ["Pawan Chopra", "Brij"], ["Kaizaad Kotwal", "Poonawalla"], ["Sameer Ali Khan", "Prince"]], "mpaa": "U", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Airlift+%282016%29"}', 'imdb': 'tt4387040', 'year': '2016', 'action': 'sources'}
    params = {'tmdb': '332835', 'name': 'Piku (2015)', 'title': 'Piku', 'meta': '{"rating": "6.5", "code": "tt3767372", "tmdb": "332835", "imdb": "tt3767372", "year": "2015", "duration": "7380", "plot": "Piku is an Indian comedy-drama film directed by Shoojit Sircar. Deepika Padukone portrays the titular protagonist, a Bengali architect living in New Delhi, and Amitabh Bachchan plays her hypochondriac father. Irrfan Khan, Moushumi Chatterjee and Jishu Sengupta portray supporting roles", "votes": "13", "title": "Piku", "fanart": "http://image.tmdb.org/t/p/original/9KtXu0KGqR5siwUIdYRB2HlOyn1.jpg", "tagline": "Motion Se Hi Emotion", "writer": "Juhi Chaturvedi", "next": "", "poster": "http://image.tmdb.org/t/p/w500/3AiMCKSLxpYsjP3eQFg3FG3a9OW.jpg", "director": "Shoojit Sircar", "studio": "Rising Sun Films", "genre": "Drama / Comedy", "metacache": false, "name": "Piku (2015)", "premiered": "2015-05-08", "originaltitle": "Piku", "cast": [["Amitabh Bachchan", "Bashkor Banerjee"], ["Deepika Padukone", "Piku"], ["Irrfan Khan", "Rana"], ["Jisshu Sengupta", ""]], "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Piku+%282015%29"}', 'imdb': 'tt3767372', 'year': '2015', 'action': 'sources'}
    params = {'action': 'movies', 'lang': 'tamil', 'url': 'added', 'provider': 'apnaview_mv'}

    # playItem
    #params = {'name': 'Piku (2015)', 'tvdb': '0', 'content': 'movie', 'source': '[{"url": "http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_1##http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_2##http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_3##http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_4", "label": "02 | [B]PLAYINDIAFILMS[/B] | MEDIAPLAYBOX | [B][I]HD [/I][/B] [4]", "source": "mediaplaybox", "parts": "4", "provider": "PlayIndiaFilms", "quality": "HD"}]', 'imdb': 'tt3767372', 'year': '2015', 'action': 'playItem'}
   # params = {'action': 'movies', 'lang': 'hi', 'url': '/browse/hindi?order=desc&sort=date&page=2', 'provider': 'apnaview_mv'}
    params =  {'tmdb': '362136', 'name': 'Prem Ratan Dhan Payo (2015)', 'title': 'Prem Ratan Dhan Payo', 'meta': '{"lang": "hindi", "tmdb": "362136", "name": "Prem Ratan Dhan Payo (2015)", "title": "Prem Ratan Dhan Payo", "poster": "http://www.apnaview.com/img/poster/62bc4f3f39685cff7cd28e96866a09be.jpg", "next": "", "originaltitle": "Prem Ratan Dhan Payo", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Prem+Ratan+Dhan+Payo+%282015%29", "year": "2015", "duration": "0", "metacache": false}', 'imdb': '0', 'year': '2015', 'action': 'sources'}
    #params =  {'action': 'movies', 'lang': 'tamil', 'url': 'HD', 'provider': 'playindiafilms_mv'}
    params = {'action': 'movies', 'lang': 'hindi', 'url': 'added', 'provider': 'apnaview_mv'}
    params = {'action': 'movies', 'lang': 'hindi', 'url': '/browse/hindi?order=desc&sort=date&page=2', 'provider': 'apnaview_mv'}
    params = {'tmdb': '362136', 'name': 'Prem Ratan Dhan Payo (2015)', 'title': 'Prem Ratan Dhan Payo', 'meta': '{"rating": "6.9", "code": "tt3595298", "tmdb": "362136", "imdb": "tt3595298", "year": "2015", "duration": "10440", "plot": "Loosely based on the novel The prince and the Pauper. Ever loving Prem is respected and loved by all and Vijay (also played by Salman Khan) is in the world of hatred and violence. They change their identities temporarily to discover the other side of the world.", "votes": "10", "title": "Prem Ratan Dhan Payo", "fanart": "http://image.tmdb.org/t/p/original/9fVjhznaYPcQF7eHZ08CkytmTbL.jpg", "mpaa": "NR", "writer": "Sooraj R. Barjatya", "poster": "http://image.tmdb.org/t/p/w500/8mfZyMKdyXGjwr27dCCBUp4fwVG.jpg", "director": "Sooraj R. Barjatya", "studio": "Fox Star Studios", "genre": "Drama / Action / Romance", "metacache": false, "name": "Prem Ratan Dhan Payo (2015)", "premiered": "2015-11-11", "originaltitle": "Prem Ratan Dhan Payo", "cast": [["Salman Khan", "Prem/Vijay"], ["Sonam Kapoor", "Maithili"], ["Neil Nitin Mukesh", "Yuvraj Ajay Singh"], ["Anupam Kher", "Diwan"], ["Swara Bhaskar", "Chandrika"], ["Deepak Dobriyal", "Kanhaiya"], ["Arman Kohli", "Chirag Singh"], ["Manoj Joshi", "Bhandari"]], "tagline": "Loosely based on the novel The prince and the Pauper", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Prem+Ratan+Dhan+Payo+%282015%29"}', 'imdb': 'tt3595298', 'year': '2015', 'action': 'sources'}
    params = {'name': 'Prem Ratan Dhan Payo (2015)', 'tvdb': '0', 'content': 'movie', 'source': '[{"url": "http://www.mediaplaybox.com/video/Prem_Ratan_Dhan_Payo_Eng_Sub_Part_1##http://www.mediaplaybox.com/video/Prem_Ratan_Dhan_Payo_Eng_Sub_Part_2##http://www.mediaplaybox.com/video/Prem_Ratan_Dhan_Payo_Eng_Sub_Part_3##http://www.mediaplaybox.com/video/Prem_Ratan_Dhan_Payo_Eng_Sub_Part_4##http://www.mediaplaybox.com/video/Prem_Ratan_Dhan_Payo_Eng_Sub_Part_5##http://www.mediaplaybox.com/video/Prem_Ratan_Dhan_Payo_Eng_Sub_Part_6", "direct": "false", "label": "02 | [B]PLAYINDIAFILMS[/B] | MEDIAPLAYBOX | [B][I]HD [/I][/B] [6]", "source": "mediaplaybox", "parts": "6", "provider": "PlayIndiaFilms", "quality": "HD"}]', 'imdb': 'tt3595298', 'year': '2015', 'action': 'playItem'}
    params = {'tmdb': '362136', 'name': 'Prem Ratan Dhan Payo (2015)', 'title': 'Prem Ratan Dhan Payo', 'meta': '{"rating": "6.9", "code": "tt3595298", "tmdb": "362136", "imdb": "tt3595298", "year": "2015", "duration": "10440", "plot": "Loosely based on the novel The prince and the Pauper. Ever loving Prem is respected and loved by all and Vijay (also played by Salman Khan) is in the world of hatred and violence. They change their identities temporarily to discover the other side of the world.", "votes": "10", "title": "Prem Ratan Dhan Payo", "fanart": "http://image.tmdb.org/t/p/original/9fVjhznaYPcQF7eHZ08CkytmTbL.jpg", "tagline": "Loosely based on the novel The prince and the Pauper", "writer": "Sooraj R. Barjatya", "poster": "http://image.tmdb.org/t/p/w500/8mfZyMKdyXGjwr27dCCBUp4fwVG.jpg", "director": "Sooraj R. Barjatya", "studio": "Fox Star Studios", "genre": "Drama / Action / Romance", "metacache": true, "name": "Prem Ratan Dhan Payo (2015)", "premiered": "2015-11-11", "originaltitle": "Prem Ratan Dhan Payo", "cast": [["Salman Khan", "Prem/Vijay"], ["Sonam Kapoor", "Maithili"], ["Neil Nitin Mukesh", "Yuvraj Ajay Singh"], ["Anupam Kher", "Diwan"], ["Swara Bhaskar", "Chandrika"], ["Deepak Dobriyal", "Kanhaiya"], ["Arman Kohli", "Chirag Singh"], ["Manoj Joshi", "Bhandari"]], "mpaa": "NR", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Prem+Ratan+Dhan+Payo+%282015%29"}', 'imdb': 'tt3595298', 'year': '2015', 'action': 'sources'}
    params = {'tmdb': '0', 'episode': '0', 'name': '23rd February 2016', 'title': '23rd February 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Sasural Simar Ka', 'year': '0', 'date': '0', 'meta': '{"tvshowurl": "forums/2498-Sasural-Simar-Ka?s=6fedc4714fca7647c475b927ce952eeb", "title": "23rd February 2016", "url": "threads/859260-Sasural-Simar-Ka-23rd-February-2016-Watch-Online?s=6fedc4714fca7647c475b927ce952eeb", "tvshowtitle": "Sasural Simar Ka", "provider": "desirulez_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Sasural+Simar+Ka", "name": "23rd February 2016"}', 'imdb': '0', 'provider': 'desirulez_tv', 'action': 'sources', 'tvrage': '0', 'alter': '0'}
    params = {'tmdb': '362136', 'name': 'Prem Ratan Dhan Payo (2015)', 'title': 'Prem Ratan Dhan Payo', 'meta': '{"rating": "6.9", "tmdb": "362136", "code": "tt3595298", "imdb": "tt3595298", "year": "2015", "duration": "10440", "plot": "Loosely based on the novel The prince and the Pauper. Ever loving Prem is respected and loved by all and Vijay (also played by Salman Khan) is in the world of hatred and violence. They change their identities temporarily to discover the other side of the world.", "votes": "10", "title": "Prem Ratan Dhan Payo", "fanart": "http://image.tmdb.org/t/p/original/9fVjhznaYPcQF7eHZ08CkytmTbL.jpg", "tagline": "Loosely based on the novel The prince and the Pauper", "writer": "Sooraj R. Barjatya", "poster": "http://image.tmdb.org/t/p/w500/8mfZyMKdyXGjwr27dCCBUp4fwVG.jpg", "director": "Sooraj R. Barjatya", "studio": "Fox Star Studios", "genre": "Drama / Action / Romance", "metacache": true, "lang": "hindi", "name": "Prem Ratan Dhan Payo (2015)", "premiered": "2015-11-11", "originaltitle": "Prem Ratan Dhan Payo", "cast": [["Salman Khan", "Prem/Vijay"], ["Sonam Kapoor", "Maithili"], ["Neil Nitin Mukesh", "Yuvraj Ajay Singh"], ["Anupam Kher", "Diwan"], ["Swara Bhaskar", "Chandrika"], ["Deepak Dobriyal", "Kanhaiya"], ["Arman Kohli", "Chirag Singh"], ["Manoj Joshi", "Bhandari"]], "mpaa": "NR", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Prem+Ratan+Dhan+Payo+%282015%29"}', 'imdb': 'tt3595298', 'year': '2015', 'action': 'sources'}



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
    sources().addItem(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta)
    #sources().playItem(content, name, year, imdb, tvdb, source)

except:
    from resources.lib.libraries import client
    client.printException('aftershock-testharness')