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

import re

def resolve(url):
    try:
        import urlresolver
        url = 'http://www.dailymotion.com/embed/video/' + str(getVideoID(url))
        url = urlresolver.resolve(url)
        return url
    except:
        return

def getVideoID(self, url):
    try :
        return re.compile('(id|url|v|si|sim|data-config)=(.+?)/').findall(url + '/')[0][1]
    except:
        return