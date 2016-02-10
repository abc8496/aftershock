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

from resources.lib.libraries import client
from resources.lib import resolvers

def resolve(url):
    try:
        rUrl = None
        result = client.source(url)
        item = client.parseDOM(result, name="div", attrs={"style":"float:right;margin-bottom:10px"})[0]
        item = item.lower()
        try :
            rUrl = client.parseDOM(item, name="iframe", ret="src")[0]
        except:
            pass

        if rUrl == None:
            try :
                rUrl = client.parseDOM(item, name="script", ret="data-config")[0]
            except:
                pass
        return resolvers.request(rUrl)
    except:
        client.printException('tellycolors.resolve(url=%s)' % url)
        return