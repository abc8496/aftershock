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
    try :
        from resources.lib.indexers import movies
        from resources.lib.sources import sources
    except:
        traceback.print_exc()
        pass

    name = 'Daredevil'
    title = 'Pilot'
    year = '2015'
    imdb = None
    tmdb = None
    tvdb = None
    tvrage = None
    season = '1'
    episode = '1'
    tvshowtitle = 'Daredevil'
    alter = None
    date = None
    meta = None
    url = None
    #action [play] name [Game of Thrones S04E09] title [The Watchers on the Wall] year [2011] imdb [0944947] tvdb [121361] tvrage [0] season [4] episode [9] tvshowtitle [Game of Thrones] alter [Adventure / Drama / Fantasy] date [2014-06-08] url [http://www.imdb.com/title/tt0944947/] image [None] meta [None] query [None] source [None] content [None] provider [None]
    #print movies.movies().get('featured')
    print sources().addItem(name, title, year, imdb, tmdb, tvdb, tvrage, season, episode, tvshowtitle, alter, date, meta)