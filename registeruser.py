# -*- coding: utf-8 -*-

'''
    Copyright (C) 2017 IDev

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


import re,hashlib,time, base64

from fileFetcher import *
import control
import cache

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

def registerUser(user, emailAddress, expiresInDays=180):
    try:
        control.makeFile(control.dataPath)
        userFile = os.path.join(control.dataPath, control.userFile.split('/')[-1])
        dbcon = database.connect(userFile)
        dbcur = dbcon.cursor()

        dbcur.execute("CREATE TABLE IF NOT EXISTS af_users (""user TEXT, ""email TEXT, ""reg_date TEXT, ""expires TEXT, ""added TEXT, ""UNIQUE(user, email)"");")
        t = int(time.time())
        expires = t + (int(expiresInDays) * 3600 * 24)

        import hashlib
        m = hashlib.md5()
        m.update(emailAddress.lower())
        emailMd5 = m.hexdigest()

        dbcur.execute("INSERT INTO af_users Values (?, ?, ?, ?, ?)", (user, emailMd5, t, expires, t))
        dbcon.commit()
    except Exception as e:
        logger.error(e)
        pass
