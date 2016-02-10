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

    params = {'tmdb': '17501', 'name': 'Don 2 (2006)', 'title': 'Don 2', 'meta': '{"rating": "7.4", "code": "tt0461936", "tmdb": "17501", "imdb": "tt0461936", "year": "2006", "duration": "10680", "plot": "A huge South Asian law enforcement contingent embarks on a dangerous cat-and-mouse game of capturing DON (Shah Rukh Khan) - high-ranking member of the ruthless drug mafia in Malaysia. When DON gets seriously injured in a police encounter, the word that he is dead begins to do the rounds. The reality, of course, is that DON is held captive in a secret location, while his bumpkin of a look-alike, Vijay, is polished and sent to infiltrate DON\'s gang. In a bizarre twist of fate, when the policeman shielding the humble street singer Vijay, is killed, the latter comes to terms with the horrifying realization that both the police and the gang are out to get him for different reasons. In a desperate attempt to prove his innocence, he is aided by the glamorous Roma (Priyanka Chopra), and ex-con Jasjit (Arjun Rampal), who owes Vijay a debt for caring for his son during his imprisonment. But will Vijay be successful in his mission?", "votes": "28", "title": "Don", "fanart": "http://image.tmdb.org/t/p/original/wxTpIJn375p8NRSxygS1Dz9UZv.jpg", "tagline": "The Chase Begins Again", "writer": "Farhan Akhtar", "next": "", "poster": "http://image.tmdb.org/t/p/w500/pRlVq9lUEuMv9Fq0t8kpPwfUT6d.jpg", "director": "Farhan Akhtar", "studio": "Excel Entertainment", "genre": "Action / Drama / Thriller", "metacache": false, "name": "Don (2006)", "premiered": "2006-10-20", "originaltitle": "Don", "cast": [["Shahrukh Khan", "Don / Vijay"], ["Priyanka Chopra", "Roma"], ["Arjun Rampal", "Jasjit"], ["Isha Koppikar", "Anita"], ["Boman Irani", "DCP DeSilva / Vardhaan"], ["Om Puri", "Vishal Malik"], ["Diwakar Pundir", "Ramesh"], ["Rajesh Khattar", "Singhania"], ["Kareena Kapoor", "Kamini / Sonia"], ["Tanay Chheda", "Dipu"], ["Sushma Reddy", "Geeta"], ["Chunky Pandey", "Teja (T.J.)"], ["Pavan Malhotra", "Narang"]], "mpaa": "PG-13", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Don+%282006%29"}', 'imdb': 'tt0461936', 'year': '2006', 'action': 'sources'}

    params = {'tmdb': '0', 'episode': '0', 'name': '9th February 2016', 'title': '9th February 2016', 'tvdb': '0', 'season': '0', 'tvshowtitle': 'Sasural Simar Ka', 'year': '0', 'date': '0', 'meta': '{"tvshowurl": "forums/2498-Sasural-Simar-Ka?s=9c7ced9d1acda3921055ec305954891b", "title": "9th February 2016", "url": "threads/853158-Sasural-Simar-Ka-9th-February-2016-Watch-Online?s=9c7ced9d1acda3921055ec305954891b", "tvshowtitle": "Sasural Simar Ka", "provider": "desirulez_tv", "duration": "1800", "trailer": "plugin://plugin.video.aftershock/?action=trailer&name=Sasural+Simar+Ka", "name": "9th February 2016"}', 'imdb': '0', 'provider': 'desirulez_tv', 'action': 'sources', 'tvrage': '0', 'alter': '0'}

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

    from resources.lib.sources import sources
    from resources.lib.indexers import episodes

    #episodes.episodes().get(tvshowtitle, year, imdb, tmdb, tvdb, tvrage, season, episode, provider=provider, url=url)
    #sources().addItem(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta)

    #from resources.lib.sources import desirulez_tv
    #title = 'Sasural Simar Ka'
    #url = 'forums/2498-Sasural-Simar-Ka?s=485267fe875e5e71d08730ed0ad7f24f'
    #url = 'forums/2498-Sasural-Simar-Ka/page2?s=b1b769323933aeeff5c937efd024008a'
    #desirulez_tv.source().get_episodes(title, url)

    # test search sources
    from resources.lib.sources import sources
    sources().addItem(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta)

    from resources.lib.resolvers import tellycolors
    # Playwire
    url = 'http://www.tellycolors.me/balika-vadhu/?si=4576302'

    # vidhsare url
    url = 'http://www.tellycolors.me/colors/?si=v8m8ab3g72bs'
    url = 'http://vidshare.us/embed-v8m8ab3g72bs-595x430.html'
    # DAILYMOTION
    url = 'http://www.tellycolors.me/balika-vadhu/?si=k1xvL0nEgZZNg9flv6Z'
    #IDOWATCH
    url = 'http://bestarticles.me/colors/?si=970446x6ywj7'

    #playu
    url = 'http://xpressvids.info/playu.php?id=bkp9bewk35ex'

    # video
    url = 'http://desimania.net/colors/?si=39wbg65nqzxz'

    # letwatch
    url = 'http://www.tellycolors.me/colors/?si=iyrasrqwffrt'

    # video
    url = 'http://desimania.net/colors/?si=kwgnbk2k2qoq'
    from resources.lib import resolvers
    #resolvers.request(url)
except:
    from resources.lib.libraries import client
    client.printException('aftershock-testharness')