import sys

sys.argv = ['plugin.video.aftershock', '1']
try :
    # addItem
    params = {'tmdb': '375290', 'name': 'Airlift (2016)', 'title': 'Airlift', 'meta': '{"rating": "5.3", "code": "tt4387040", "tmdb": "375290", "imdb": "tt4387040", "year": "2016", "duration": "7320", "plot": "Airlift is an uplifting and entertaining edge-of-the-seat thriller and is the story of the biggest ever human evacuation in the history of mankind", "votes": "15", "title": "Airlift", "fanart": "http://image.tmdb.org/t/p/original/cXFL4UUpsj2asWbMhSBwxpkndSW.jpg", "tagline": "170,000 Refugees, 488 Flights, 59 Days, 1 Man", "writer": "Ritesh Shah / Suresh Nair", "next": "", "poster": "http://image.tmdb.org/t/p/w500/f5ebYXP28qYzqZwLDQLc4tHR40U.jpg", "director": "Raja Menon", "studio": "T-Series", "genre": "Thriller / Action / Drama / History", "metacache": true, "lang": "en", "name": "Airlift (2016)", "premiered": "2016-01-22", "originaltitle": "Airlift", "cast": [["Akshay Kumar", "Ranjit Katyal"], ["Nimrat Kaur", "Amrita Katyal"], ["Feryna Wazheir", "Tasneem"], ["Lena", "Deepti Jayarajan"], ["Purab Kohli", "Ibrahim Durrani"], ["Pawan Chopra", "Brij"], ["Kaizaad Kotwal", "Poonawalla"], ["Sameer Ali Khan", "Prince"]], "mpaa": "U", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Airlift+%282016%29"}', 'imdb': 'tt4387040', 'year': '2016', 'action': 'sources'}
    params = {'tmdb': '332835', 'name': 'Piku (2015)', 'title': 'Piku', 'meta': '{"rating": "6.5", "code": "tt3767372", "tmdb": "332835", "imdb": "tt3767372", "year": "2015", "duration": "7380", "plot": "Piku is an Indian comedy-drama film directed by Shoojit Sircar. Deepika Padukone portrays the titular protagonist, a Bengali architect living in New Delhi, and Amitabh Bachchan plays her hypochondriac father. Irrfan Khan, Moushumi Chatterjee and Jishu Sengupta portray supporting roles", "votes": "13", "title": "Piku", "fanart": "http://image.tmdb.org/t/p/original/9KtXu0KGqR5siwUIdYRB2HlOyn1.jpg", "tagline": "Motion Se Hi Emotion", "writer": "Juhi Chaturvedi", "next": "", "poster": "http://image.tmdb.org/t/p/w500/3AiMCKSLxpYsjP3eQFg3FG3a9OW.jpg", "director": "Shoojit Sircar", "studio": "Rising Sun Films", "genre": "Drama / Comedy", "metacache": false, "name": "Piku (2015)", "premiered": "2015-05-08", "originaltitle": "Piku", "cast": [["Amitabh Bachchan", "Bashkor Banerjee"], ["Deepika Padukone", "Piku"], ["Irrfan Khan", "Rana"], ["Jisshu Sengupta", ""]], "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Piku+%282015%29"}', 'imdb': 'tt3767372', 'year': '2015', 'action': 'sources'}

    # playItem
    #params = {'name': 'Piku (2015)', 'tvdb': '0', 'content': 'movie', 'source': '[{"url": "http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_1##http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_2##http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_3##http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_4", "label": "02 | [B]PLAYINDIAFILMS[/B] | MEDIAPLAYBOX | [B][I]HD [/I][/B] [4]", "source": "mediaplaybox", "parts": "4", "provider": "PlayIndiaFilms", "quality": "HD"}]', 'imdb': 'tt3767372', 'year': '2015', 'action': 'playItem'}

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

    from resources.lib.indexers import movies

    # test search sources
    from resources.lib.sources import einthusan_mv
    from resources.lib.sources import playindiafilms_mv
    from resources.lib.sources import client
    client.source('http://stream.zeefamily.tv/zeecinema/playlist.m3u8')
    #playindiafilms_mv.source().get_movie("", "welcome back", "2015")
    #playindiafilms_mv.source().get_sources("piku-2015", [], [], [])
    #einthusan_mv.source().get_movie(imdb, title, year)

    from resources.lib.sources import sources
    #sources().addItem(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta)
    #sources().playItem(content, name, year, imdb, tvdb, source)


except:
    from resources.lib.libraries import client
    client.printException('aftershock-testharness')