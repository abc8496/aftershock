#!/usr/bin/python

import sys, traceback

import xbmcaddon, xbmc

try :
    from resources.lib.sources import sources
    from resources.lib.indexers import movies
except:
    traceback.print_exc()
    pass


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
    print movies.movies().get('featured')