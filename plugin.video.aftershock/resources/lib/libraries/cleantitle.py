# -*- coding: utf-8 -*-

'''
    Copyright (C) 2015 lamdba

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


import re,unicodedata

def movie(title):
    title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title

def tv(title):
    title = re.sub('\n|\s(|[(])(UK|US|AU|\d{4})(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title

def live(title):
    title = title.upper()
    title = title.strip()
    try : tmpTitle = cleanedNames[title]
    except: tmpTitle = None
    if not tmpTitle == None:
        title = tmpTitle
    return title

def get(title):
    if title == None: return
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title

def get_simple(title):
    if title == None: return
    title = title.lower()
    title = re.sub('(\d{4})', '', title)
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\n|\(|\)|\[|\]|\{|\}|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title


def getsearch(title):
    if title == None: return
    title = title.lower()
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\\\|/|-|:|;|\*|\?|"|\'|<|>|\|', '', title).lower()
    return title


def query(title):
    if title == None: return
    title = title.replace('\'', '').rsplit(':', 1)[0]
    return title


def normalize(title):
    try:
        try: return title.decode('ascii').encode("utf-8")
        except: pass

        return str( ''.join(c for c in unicodedata.normalize('NFKD', unicode( title.decode('utf-8') )) if unicodedata.category(c) != 'Mn') )
    except:
        return title

cleanedNames = {'& PICTURE':'AND PICTURE HD',
                '&TV HD':'AND TV HD',
                '9X M':'9X MUSIC',
                'AAJ TAK NEWS':'AAJ TAK',
                'AAJ TAKK':'AAJ TAK',
                'AASTHA TV':'AASHTA BHAJAN',
                'AND PIC SD':'& PICTURE',
                'AND PIC HD':'& PICTURE HD',
                'AND TV HD (LOCAL TIME)':'AND TV HD',
                'AND PICTURE HD (INDIA )':'AND PICTURE HD',
                'ASTHA BHAJAN':'AASTHA BHAJAN',
                'ASTHA TV':'AASTHA BHAJAN',
                'AASHTA BHAJAN':'AASTHA BHAJAN',
                'BHOJPURI CINEMA':'SKIP',
                'BOLLYWOOD MASALA':'SKIP',
                'CARE WORLD':'SKIP',
                'CARTOON NETWORK HINDI':'CARTOON NETWORK',
                'CINEMA TV':'SKIP',
                'COLORS EU':'COLORS',
                'COLORS IN':'COLORS',
                'COLORS TV':'COLORS',
                'COLORS TV HD':'COLORS HD',
                'COLORS TV HD ( ENTERTAINMENT )':'COLORS HD',
                'COLORS TV INDIA':'COLORS',
                'COLORS TV APAC':'COLORS',
                'COLORS UK':'COLORS',
                'DANGAL TV':'DANGAL',
                'DELHI AAJ TAK':'AAJ AAJ TAK DELHI',
                'DESI TV PUNJABI':'SKIP',
                'DILLAGI':'SKIP',
                'DISCOVERY HD HINDI':'DISCOVERY HD',
                'ENTERR 10':'ENTER 10',
                'ENTERR10 MOVIES':'ENTER 10',
                'JUS PUNJABI':'JUS ONE TV PUNJABI',
                'LIFE OK SD':'LIFE OK',
                'LIFE OK HD (LOCAL TIME)':'LIFE OK HD',
                'MOVIE OK':'MOVIES OK',
                'NATIONAL GEOGRAPHIC HD HINDI':'NATIONAL GEOGRAPHIC HD',
                'NATIONAL GEOGRAPHIC HINDI':'NATIONAL GEOGRAPHIC',
                'NDTV 24x7 NEWS':'NDTV 24X7',
                'NDTV NEWS ENGLISH':'NDTV NEWS',
                'NEWS18':'NEWS 18',
                'RAJ MUSIX':'RAJ MUSIC',
                'RISHTAY ASIA':'RISHTEY',
                'RISHTAY CINEPLEX':'RISHTEY CINEPLEX',
                'SAB TV HD INDIA':'SAB TV HD',
                'SONY ENTERTAINMENT HD (LOCAL TIME)':'SONY ENTERTAINMENT HD',
                'SONY MAX2':'SONY MAX 2',
                'SONY SAB IN':'SONY SAB',
                'SONY SET MAX HD (LOCAL TIME)':'SONY SET MAX HD',
                'SONY SIX HD (INDIA )':'SONY SIX HD',
                'SONY TV IN':'SONY TV',
                'STAR GOLD SD':'STAR GOLD',
                'STAR JALSHA US':'STAR JALSHA',
                'STAR PLUS IND':'STAR PLUS',
                'STAR PLUS SD':'STAR PLUS',
                'STAR PRAVAAHMARATHI':'STAR PRAVAH',
                'STAR PRAVAAH US MARATHI':'STAR PRAVAH',
                'STAR SPORTS1-SD':'STAR SPORTS',
                'STAR SPORTS2-SD':'STAR SPORTS',
                'STAR USTUV':'STAR UTSAV',
                'TEZ NEWS':'AAJ TAK TEZ',
                'TIMES NOW NEWS':'TIMES NOW',
                'UTV MOVIES INTERNATIONAL':'UTV MOVIES',
                'ZEE ANMOL CINE':'ZEE ANMOL',
                'ZEE CINEMA HD (LOCAL TIME)':'ZEE CINEMA HD',
                'ZEE CINEMA INTERNATIONAL':'ZEE CINEMA',
                'ZEE SALAM' : 'ZEE SALAAM',
                'ZEE TV HD (LOCAL TIME)':'ZEE TV HD',
                'ZEE TV SD':'ZEE TV',
                'ZINDAGI':'ZEE ZINDAGI',
                'ZING TV':'ZING'}

