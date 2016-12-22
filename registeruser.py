import sys, re, base64

sys.argv = ['plugin.video.aftershock', '1']
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

'''
import re,hashlib,time, base64

from fileFetcher import *
import control
import cache

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

def registerUser(user, emailAddress, expiresInDays=365):
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
'''

from resources.lib.libraries import user
try :
    # 12/16/2016
    '''
    user.registerUser('Charanjit Singh', 'finetouchconstructions@yahoo.com', 730)
    user.registerUser('Charanjit Singh', 'charanjeet3usa@yahoo.com', 730)
    user.registerUser('Bhaumik Modi', 'klu_9bk@yahoo.com')
    user.registerUser('Nick Vachani', 'tollandtnpk@gmail.com')
    user.registerUser('Anil Jakkaladki', 'anilkuj@yahoo.com')
    user.registerUser('Abhinav Halen', 'ab_hal@hotmail.com')
    user.registerUser('Sougata Deb', 'sdeb7381@gmail.com')
    user.registerUser('Vineet Gupta', 'vineetg@gmail.com', 3650)
    '''
    '''
    #12/18/2016
    #user.registerUser('Vasudevan Kadambi', 'vkadambi@gmail.com')
    #user.registerUser('Sachin Patel', 'sachin27581@gmail.com')
    #user.registerUser('Rajesh Kumar', 'rrajeshh@gmail.com')
    #valid, url = user.validateUser('vineetg@gmail.com')
    #user.registerUser('Arpita Lakhotia', 'arpita1586@yahoo.com')
    #user.registerUser('Rakshit Desai', 'raksspam@yahoo.com')
    #user.registerUser('Yasin Chinoy', 'yasinchinoy@yahoo.com')
    #user.registerUser('Kalyan Makkena', 'ftpkalyan@gmail.com')

    #12/19/2016
    #user.registerUser('Jitesh Ranavaya', 'jiteshranavaya@live.co.uk')
    #user.registerUser('Hiren Patel', 'patel001@me.com')
    #user.registerUser('Priyang Vyas','vyasp13@gmail.com')
    #user.registerUser('Prashant Khatiwada', 'p.khatiwada@outlook.com')
    #user.registerUser('Huzefa Talib','hstalib@hotmail.com')
    #user.registerUser('Hiren Srivastava', 'hirubhaiya@gmail.com')
    #user.registerUser('Sandesh Ghawghawe','sg1851@hotmail.com')
    #user.registerUser('Romi Ahluwalia','romiahluwalia53@gmail.com')

    #12/20/2016
    #user.registerUser('Rajesh Assi','rajeshratna@msn.com')
    #user.registerUser('Jignesh Gohel','jignesh.gohel@gmail.com')
    #user.registerUser('Avinash Kunigal Nagabhushan','avinashkn.infa@gmail.com')
    #user.registerUser('Prasenjit Saha','prasenjitsh@icloud.com')
    #user.registerUser('Amsun','amsun.innovations@gmail.com')
    #user.registerUser('Amit Kopal','ajnabi1975@yahoo.com')
    #user.registerUser('Yadwinder Devgan','luckydevgun@gmail.com')
    '''

    #12/21//2016
    # user.registerUser('Ashish Chapagain','43ashish@gmail.com')
    # user.registerUser('Baneerji Bhat','baneerji.bhat@gmail.com')
    # user.registerUser('Prafulla Pisolkar','prafulla.pisolkar@gmail.com')
    # user.registerUser('Rohan Verma','rohan.615@gmail.com')
    # user.registerUser('Sagar patil','psagar001@gmail.com')
    # user.registerUser('Basant Yadav','yadav.basantkumar83@gmail.com')
    # user.registerUser('Raghu Murthy','raghunmurthy@gmail.com')
    # user.registerUser('satnam singh','satnam1chandi@gmail.com')
    # user.registerUser('Chugh Varun','varun.chugh@hotmail.com')

    #12/22/2016
    # user.registerUser('Udit Meghraj','uditmeghraj@yahoo.com')
    # user.registerUser('Shamoel Faizullabhoy','shamoel@cox.net')
    # #user.registerUser('Vaibhav Zaveri','vaibhavzaveri@gmail.com', expiresInDays=30) # Partial Payment $5
    # #user.registerUser('Amita Narayanan','wear-on-the-web@sympatico.ca', expiresInDays=30) #Partial Payment $7.25
    # user.registerUser('Nishit Rana','NRana14@gmail.com')
    # user.registerUser('Rashmi Khosla','rashmi1.khosla@gmail.com')
    # user.registerUser('Ramesh Govindarajan','rgovindar@gmail.com')
    # #user.registerUser('Theresa Gomboc','janunanu2006@hotmail.com', expiresInDays=30) #Partial Payment $7.25
    # user.registerUser('Karan Sabharwal','karans.aus@gmail.com')
    # user.registerUser('Rafat Nabi','rafpac6@hotmail.com')
    # user.registerUser('THEITCITY', 'accounts@theitcity.com')

    print "All Done"
except:
    import traceback
    traceback.print_exc()