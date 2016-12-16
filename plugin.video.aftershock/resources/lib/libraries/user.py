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


import re,hashlib,time

from resources.lib.libraries.fileFetcher import *

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

from resources.lib.libraries import control

def registerUser(emailAddress, expiresInDays=30):
    try:
        control.makeFile(control.dataPath)
        dbcon = database.connect(control.userFile)
        dbcur = dbcon.cursor()

        dbcur.execute("CREATE TABLE IF NOT EXISTS af_users (""email TEXT, ""reg_date TEXT, ""expires TEXT, ""added TEXT, ""UNIQUE(email)"");")
        t = int(time.time())
        expires = t + (int(expiresInDays) * 3600 * 24)

        dbcur.execute("INSERT INTO af_users Values (?, ?, ?, ?)", (emailAddress.lower(), t, expires, t))
        dbcon.commit()
    except:
        pass

def validateUser(emailAddress, showRegisteration=False):
    try:
        if (emailAddress == None or emailAddress == ''):
            emailAddress = control.setting('user.email')
        if (emailAddress == None or emailAddress == '') and showRegisteration:
            t = control.lang(30275).encode('utf-8')
            k = control.keyboard('', t) ; k.doModal()
            emailAddress = k.getText() if k.isConfirmed() else None
        elif (emailAddress == None or emailAddress == ''):
            return control.INVALID

        fileFetcher = FileFetcher(control.userFile, control.addon)
        retValue = fileFetcher.fetchFile()
        control.makeFile(control.dataPath)

        userFile = os.path.join(control.dataPath, control.userFile.split('/')[-1])
        dbcon = database.connect(userFile)
        dbcur = dbcon.cursor()

        dbcur.execute("SELECT * FROM af_users WHERE email = '%s'" % (emailAddress.lower()))
        match = dbcur.fetchone()

        logger.debug('emailAddress : %s Match : %s' % (emailAddress, match))

        t1 = int(match[2])
        t2 = int(time.time())
        expired = t1 - t2
        expiredDays = expired / (3600 * 24)
        if expired <= 0 :
            control.dialog.ok(control.addonInfo('name'), "Your access has expired. Please make a donation (min. $5) to aftershockpy@gmail.com via PayPal to get access !!")
            return control.EXPIRED
        else:
            control.setSetting('user.email', emailAddress)
            return control.VALID
    except Exception as e:
        logger.error(e)
        control.dialog.ok(control.addonInfo('name'), "User not registered. Please make a donation (min. $5) to aftershockpy@gmail.com via PayPal to get access !!")
        return control.INVALID