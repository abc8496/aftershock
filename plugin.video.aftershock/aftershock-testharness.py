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
    # addItem
    params = {'tmdb': '332835', 'name': 'Piku (2015)', 'title': 'Piku', 'meta': '{"rating": "6.5", "code": "tt3767372", "tmdb": "332835", "imdb": "tt3767372", "year": "2015", "duration": "7380", "plot": "Piku is an Indian comedy-drama film directed by Shoojit Sircar. Deepika Padukone portrays the titular protagonist, a Bengali architect living in New Delhi, and Amitabh Bachchan plays her hypochondriac father. Irrfan Khan, Moushumi Chatterjee and Jishu Sengupta portray supporting roles", "votes": "13", "title": "Piku", "fanart": "http://image.tmdb.org/t/p/original/9KtXu0KGqR5siwUIdYRB2HlOyn1.jpg", "tagline": "Motion Se Hi Emotion", "writer": "Juhi Chaturvedi", "next": "", "poster": "http://image.tmdb.org/t/p/w500/3AiMCKSLxpYsjP3eQFg3FG3a9OW.jpg", "director": "Shoojit Sircar", "studio": "Rising Sun Films", "genre": "Drama / Comedy", "metacache": false, "lang": "en", "name": "Piku (2015)", "premiered": "2015-05-08", "originaltitle": "Piku", "cast": [["Amitabh Bachchan", "Bashkor Banerjee"], ["Deepika Padukone", "Piku"], ["Irrfan Khan", "Rana"], ["Jisshu Sengupta", ""]], "mpaa": "", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Piku+%282015%29"}', 'imdb': 'tt3767372', 'year': '2015', 'action': 'sources'}

    # playItem
    params = {'name': 'Piku (2015)', 'tvdb': '0', 'content': 'movie', 'source': '[{"url": "http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_1##http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_2##http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_3##http://www.mediaplaybox.com/video/Piku_Eng_Sub_Part_4", "label": "02 | [B]PLAYINDIAFILMS[/B] | MEDIAPLAYBOX | [B][I]HD [/I][/B] [4]", "source": "mediaplaybox", "parts": "4", "provider": "PlayIndiaFilms", "quality": "HD"}]', 'imdb': 'tt3767372', 'year': '2015', 'action': 'playItem'}

    params = {'tmdb': '353464', 'name': 'Talvar (2015)', 'title': 'Talvar', 'meta': '{"rating": "8.3", "code": "tt4934950", "tmdb": "353464", "imdb": "tt4934950", "year": "2015", "duration": "7920", "plot": "Dramatization of the notorious \\"Noida Double Murder Case\\", which set off a media frenzy around the world in 2008.", "votes": "10", "title": "Talvar", "fanart": "http://image.tmdb.org/t/p/original/hT118jQAcrCMDVrwduhQGfps4Uj.jpg", "tagline": "Dramatization of the notorious \\"Noida Double Murder Case\\", which set off a media frenzy around the world in 2008.", "writer": "Vishal Bhardwaj", "next": "", "poster": "http://image.tmdb.org/t/p/w500/ctOxiFFWrhyP4XG8QtrcyCZA4uG.jpg", "director": "Meghna Gulzar", "studio": "Vishal Bhardwaj Pictures", "genre": "Thriller / Drama / Mystery", "metacache": false, "name": "Talvar (2015)", "premiered": "2015-09-14", "originaltitle": "Talvar", "cast": [["Irrfan Khan", "Ashwin Kumar (Investigation officer of CDI)"], ["Konkona Sen Sharma", "Nutan Tandon"], ["Neeraj Kabi", "Ramesh Tandon"], ["Sohum Shah", "Vedant Mishra (ACP)"], ["Atul Kumar", "Paul (Investigation officer of CDI)"], ["Gajraj Rao", "Dhaniram (Inspector)"], ["Ayesha Parveen", "Shruti Tandon"], ["Tabu", "Reema Kumar"], ["Sumit Gulati", "Kanhaiya"], ["Prakash Belawadi", "Ramshankar Pillai (CDI Director)"], ["Shishir Sharma", "JK Dixit (CDI Director)"]], "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Talvar+%282015%29"}', 'imdb': 'tt4934950', 'year': '2015', 'action': 'sources'}


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

    #from resources.lib.sources import hotstar_mv
    #hotstar_mv.source().get_movie(imdb, title, year)

    # test search sources
    from resources.lib.sources import sources
    sources().addItem(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta)
    #sources().playItem(content, name, year, imdb, tvdb, source)


except:
    from resources.lib.libraries import client
    client.printException('aftershock-testharness')