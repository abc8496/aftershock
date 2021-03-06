# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2017 Aftershockpy

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

import time

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

from . import control


def fetch(items, lang):
    try:
        t2 = int(time.time())
        dbcon = database.connect(control.metacacheFile)
        dbcur = dbcon.cursor()
    except:
        return items

    for i in range(0, len(items)):
        try:
            dbcur.execute("SELECT * FROM meta WHERE (imdb = '%s' and not imdb = '0') or (tmdb = '%s' and not tmdb = '0') or (tvdb = '%s' and not tvdb = '0')" % (items[i]['imdb'], items[i]['tmdb'], items[i]['tvdb']))
            match = dbcur.fetchone()

            t1 = int(match[5])
            update = (abs(t2 - t1) / 3600) >= 720
            if update == True: raise Exception()

            item = eval(match[4].encode('utf-8'))
            item = dict((k,v) for k, v in item.iteritems() if not v == '0')

            try: items[i].update({'poster': item['poster']})
            except: pass
            try: items[i].update({'banner': item['banner']})
            except: pass
            if items[i]['fanart'] == '0':
                try: items[i].update({'fanart': item['fanart']})
                except: pass

            item = dict((k,v) for k, v in item.iteritems() if not k == 'poster' and not k == 'banner' and not k == 'fanart')
            items[i].update(item)

            items[i].update({'metacache': True})
        except:
            pass

    return items

def insert(meta):
    try:
        control.makeFile(control.dataPath)
        dbcon = database.connect(control.metacacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS meta (""imdb TEXT, ""tmdb TEXT, ""tvdb TEXT, ""lang TEXT, ""item TEXT, ""time TEXT, ""UNIQUE(imdb, tmdb, tvdb, lang)"");")
        t = int(time.time())
        for m in meta:
            try:
                i = repr(m['item'])
                try: dbcur.execute("DELETE * FROM meta WHERE (imdb = '%s' and not imdb = '0') or (tmdb = '%s' and not tmdb = '0') or (tvdb = '%s' and and not tvdb = '0')" % (m['imdb'], m['tmdb'], m['tvdb']))
                except: pass
                dbcur.execute("INSERT INTO meta Values (?, ?, ?, ?, ?, ?)", (m['imdb'], m['tmdb'], m['tvdb'], m['lang'], i, t))
            except:
                #import traceback
                #traceback.print_exc()
                pass

        dbcon.commit()
    except:
        #import traceback
        #traceback.print_exc()
        return

def insertImdb(items):
    try :
        control.makeFile(control.dataPath)
        dbcon = database.connect(control.metacacheFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS meta_imdb ("" title TEXT, ""imdb TEXT, ""tmdb TEXT, ""time TEXT,""UNIQUE(imdb, tmdb, title)"");")
        t = int(time.time())

        for item in items:
            if not item['imdb'] == '0' or not item['tmdb'] == '0':
                try:
                    try: dbcur.execute("DELETE FROM meta_imdb WHERE title = '%s'" % (item['title']))
                    except:
                        pass
                    dbcur.execute("INSERT INTO meta_imdb Values (?, ?, ?, ?)", (item['title'], item['imdb'], item['tmdb'], t))
                except:
                    pass
        dbcon.commit()
    except:
        return

def fetchImdb(items):
    try:
        control.makeFile(control.dataPath)
        dbcon = database.connect(control.metacacheFile)
        dbcur = dbcon.cursor()
        for i in range(0, len(items)):
            try:
                dbcur.execute("SELECT imdb, tmdb FROM meta_imdb WHERE (title = '%s')" % (items[i]['title']))
                item = dbcur.fetchone()

                try :items[i].update({'imdb':item[0], 'tmdb': item[1]})
                except: pass
            except:
                pass
        dbcur.close()
        dbcon.close()
    except:
        pass
    return items