# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2015 Innovate

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import urlparse,sys, xbmcaddon
params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

print params

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

print "action [%s] name [%s] title [%s] year [%s] imdb [%s] tvdb [%s] tvrage [%s] season [%s] episode [%s] tvshowtitle [%s] alter [%s] date [%s] url [%s] image [%s] meta [%s] query [%s] source [%s] content [%s] provider [%s]" % (action, name, title, year, imdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, url, image, meta, query, source, content, provider)

if action == None:
    from resources.lib.indexers import navigator
    navigator.navigator().root()

elif action == 'movieNavigator':
    from resources.lib.indexers import navigator
    # change to show language selection
    navigator.navigator().desiMovies()

elif action == 'desiTVNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().desiTV()

elif action == 'desiLiveNavigator':
    from resources.lib.indexers import livetv
    livetv.channels().get()


elif action == 'movieGenres':
    from resources.lib.indexers import movies
    movies.movies().genres()

elif action == 'movieYears':
    from resources.lib.indexers import movies
    movies.movies().years()

elif action == 'movies':
    from resources.lib.indexers import movies
    movies.movies().get(url, provider=provider)

elif action == 'movieSearch':
    from resources.lib.indexers import movies
    movies.movies().search(query)

elif action == 'tvshows':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url, provider=provider, network=name)

elif action == 'seasons':
    from resources.lib.indexers import episodes
    episodes.seasons().get(tvshowtitle, year, imdb, tmdb, tvdb, tvrage)

elif action == 'episodes':
    from resources.lib.indexers import episodes
    episodes.episodes().get(tvshowtitle, year, imdb, tmdb, tvdb, tvrage, season, episode, provider=provider, url=url)

elif action == 'sources':
    from resources.lib.sources import sources
    sources().addItem(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta)

elif action == 'play':
    from resources.lib.sources import sources
    sources().play(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta, url)

elif action == 'playItem':
    from resources.lib.sources import sources
    sources().playItem(content, name, year, imdb, tvdb, source)

elif action == 'trailer':
    from resources.lib.libraries import trailer
    trailer.trailer().play(name, url)

elif action == 'addView':
    from resources.lib.libraries import views
    views.addView(content)

elif action == 'refresh':
    from resources.lib.libraries import control
    control.refresh()

elif action == 'queueItem':
    from resources.lib.libraries import control
    control.queueItem()

elif action == 'moviePlaycount':
    from resources.lib.libraries import playcount
    playcount.movies(title, year, imdb, query)

elif action == 'episodePlaycount':
    from resources.lib.libraries import playcount
    playcount.episodes(imdb, tvdb, season, episode, query)

elif action == 'tvPlaycount':
    from resources.lib.libraries import playcount
    playcount.tvshows(name, year, imdb, tvdb, season, query)

elif action == 'trailer':
    from resources.lib.libraries import trailer
    trailer.trailer().play(name, url)

elif action == 'openSettings':
    from resources.lib.libraries import control
    control.openSettings(query)

elif action == 'clearCache':
    from resources.lib.libraries import cache
    from resources.lib import sources
    cache.clear()
    sources.sources().clearSources()

'''
elif action == 'libtoolNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().library()

elif action == 'movieWidget':
    from resources.lib.indexers import movies
    movies.movies().widget()

elif action == 'movieFavourites':
    from resources.lib.indexers import movies
    movies.movies().favourites()

elif action == 'moviePerson':
    from resources.lib.indexers import movies
    movies.movies().person(query)
elif action == 'movieCertificates':
    from resources.lib.indexers import movies
    movies.movies().certifications()

elif action == 'moviePersons':
    from resources.lib.indexers import movies
    movies.movies().persons()

elif action == 'movieUserlists':
    from resources.lib.indexers import movies
    movies.movies().userlists()

elif action == 'channels':
    from resources.lib.indexers import channels
    channels.channels().get()

elif action == 'tvshows':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvFavourites':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().favourites()

elif action == 'tvSearch':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search(query)

elif action == 'tvPerson':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().person(query)

elif action == 'tvGenres':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().genres()

elif action == 'tvNetworks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().networks()

elif action == 'tvYears':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().years()

elif action == 'tvUserlists':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().userlists()

elif action == 'seasons':
    from resources.lib.indexers import episodes
    episodes.seasons().get(tvshowtitle, year, imdb, tmdb, tvdb, tvrage)

elif action == 'calendar':
    from resources.lib.indexers import episodes
    episodes.episodes().calendar(url)

elif action == 'tvWidget':
    from resources.lib.indexers import episodes
    episodes.episodes().widget()

elif action == 'episodeFavourites':
    from resources.lib.indexers import episodes
    episodes.episodes().favourites()

elif action == 'calendars':
    from resources.lib.indexers import episodes
    episodes.episodes().calendars()

elif action == 'openPlaylist':
    from resources.lib.libraries import control
    control.openPlaylist()

elif action == 'openSettings':
    from resources.lib.libraries import control
    control.openSettings(query)

elif action == 'addFavourite':
    from resources.lib.libraries import favourites
    favourites.addFavourite(meta, content, query)

elif action == 'deleteFavourite':
    from resources.lib.libraries import favourites
    favourites.deleteFavourite(meta, content)

elif action == 'traktManager':
    from resources.lib.libraries import trakt
    trakt.manager(name, imdb, tvdb, content)

elif action == 'movieToLibrary':
    from resources.lib.libraries import libtools
    libtools.libmovies().add(name, title, year, imdb, tmdb)

elif action == 'moviesToLibrary':
    from resources.lib.libraries import libtools
    libtools.libmovies().range(url)

elif action == 'tvshowToLibrary':
    from resources.lib.libraries import libtools
    libtools.libtvshows().add(tvshowtitle, year, imdb, tmdb, tvdb, tvrage)

elif action == 'tvshowsToLibrary':
    from resources.lib.libraries import libtools
    libtools.libtvshows().range(url)

elif action == 'updateLibrary':
    from resources.lib.libraries import libtools
    libtools.libepisodes().update(query)

elif action == 'service':
    from resources.lib.libraries import libtools
    libtools.libepisodes().service()

elif action == 'resolve':
    from resources.lib.sources import sources
    from resources.lib.libraries import control
    url = sources().sourcesResolve(url, provider)
    control.addItem(handle=int(sys.argv[1]), url=url, listitem=control.item(name))
    control.directory(int(sys.argv[1]))

elif action == 'download':
    from resources.lib.sources import sources
    from resources.lib.libraries import simpledownloader
    url = sources().sourcesResolve(url, provider)
    simpledownloader.download(name, image, url)

elif action == 'play':
    from resources.lib.sources import sources
    sources().play(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta, url)

elif action == 'alterSources':
    from resources.lib.sources import sources
    sources().alterSources(url, meta)

'''