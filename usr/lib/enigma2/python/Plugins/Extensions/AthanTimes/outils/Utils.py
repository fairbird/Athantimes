# -*- coding: utf-8 -*-
from Components.config import config
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest, MultiContentEntryPixmapAlphaBlend
from enigma import gFont, eTimer, eConsoleAppContainer, ePicLoad, loadPNG, loadJPG, getDesktop, eServiceReference, iPlayableService, eListboxPythonMultiContent, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER
from Components.MenuList import MenuList
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS, pathExists
from os import path as os_path, system as os_system, unlink, stat, mkdir, popen, makedirs, listdir, access, rename, remove, W_OK, R_OK, F_OK
from Screens.Screen import Screen
from xml.etree.cElementTree import fromstring, ElementTree
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS
from twisted.web.client import downloadPage, getPage
from enigma import getDesktop
from enigma import eListboxPythonMultiContent, gFont
from enigma import gRGB
from Components.Sources.List import List
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest
from enigma import eListboxPythonMultiContent, eListbox, gFont, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_WRAP
from Components.Pixmap import Pixmap, MovingPixmap
from Components.Label import Label
from datetime import date, datetime
import os, re, sys, time, random
from Plugins.Extensions.AthanTimes.outils.Utils import *

#Add By RAED for py2 & py3
from Plugins.Extensions.AthanTimes.outils.compat import compat_urlopen, compat_Request, compat_HTTPError, PY3

#Agent = {'User-agent': 'Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.0.15) Gecko/2009102815 Ubuntu/9.04 (jaunty) Firefox/3.', 'Connection': 'Close'}
Agent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}

wsize = getDesktop(0).size().width()
hsize = getDesktop(0).size().height()
dwidth = getDesktop(0).size().width()

def show_listiptv2(cityId, countryId, cityName, countryName):
    if dwidth == 1280:
        res = [
         (
          cityId,
          countryId,
          cityName,
          countryName)]
        res.append(MultiContentEntryText(pos=(2, 2), size=(425, 30), font=5, text=cityId, backcolor_sel=26214, backcolor=22503, flags=RT_HALIGN_CENTER))
        return res
    else:
        res = [
         (
          cityId,
          countryId,
          cityName,
          countryName)]
        res.append(MultiContentEntryText(pos=(2, 2), size=(459, 30), font=7, text=cityId, backcolor_sel=26214, backcolor=22503, flags=RT_HALIGN_CENTER))
        return res

def XML_Country(Mylist, Contnt, Contr):
    Path_1 = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Choice/' + Contr + '.xml'
    if fileExists(Path_1):
        os.remove(Path_1)
        outfile = open(Path_1, 'a')
        outfile.write('<?xml version="1.0"?>\n<!-- List of ' + Contnt + ' -->\n<stream>\n')
        for x in Mylist:
            outfile.write('<Contry>\n\t<name>' + str(x[0][0]) + '</name>\n' + '\t<url>' + str(x[0][1]) + '</url>\n\t<Id>' + str(x[0][2]) + '</Id>\n</Contry>\n')

        outfile.write('</stream>')
        outfile.close()
    else:
        outfile = open(Path_1, 'a')
        outfile.write('<?xml version="1.0"?>\n<!-- List of ' + Contnt + ' -->\n<stream>\n')
        for x in Mylist:
            outfile.write('<Contry>\n\t<name>' + str(x[0][0]) + '</name>\n' + '\t<url>' + str(x[0][1]) + '</url>\n\t<Id>' + str(x[0][2]) + '</Id>\n</Contry>\n')

        outfile.write('</stream>')
        outfile.close()

def XML_Continent(Mylist, Contry):
    Path_1 = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/' + Contry + '/' + Contry + '.xml'
    if fileExists(Path_1):
        os.remove(Path_1)
        outfile = open(Path_1, 'a')
        outfile.write('<?xml version="1.0"?>\n<!-- List of ' + Contry + ' -->\n<stream>\n')
        for x in Mylist:
            outfile.write('<Contry>\n\t<name>' + str(x[0][0]) + '</name>\n' + '\t<url>' + str(x[0][1]) + '</url>\n</Contry>\n')

        outfile.write('</stream>')
        outfile.close()
    else:
        outfile = open(Path_1, 'a')
        outfile.write('<?xml version="1.0"?>\n<!-- List of ' + Contry + ' -->\n<stream>\n')
        for x in Mylist:
            outfile.write('<Contry>\n\t<name>' + str(x[0][0]) + '</name>\n' + '\t<url>' + str(x[0][1]) + '</url>\n</Contry>\n')

        outfile.write('</stream>')
        outfile.close()

def XML_Choice(Mylist):
    try:
        Path = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes.xml'
        Patho = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Prayer.txt'
        Pathoo = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/city.txt'
        try:
        	os.remove(Path)
        except:
        	pass
        try:
        	os.remove(Patho)
        except:
        	pass
        try:
        	os.remove(Pathoo)
        except:
        	pass
        outfile = open(Path, 'a')
        outfileo = open(Patho, 'a')
        outfileoo = open(Pathoo, 'a')
        outfile.write('<?xml version="1.0"?>\n<stream>\n')
        correction = config.plugins.AthanTimes.correctiontime.value
        for x in Mylist:
            txt_1 = str(x[0][8]).split()
            First = int(txt_1[0][:2]) + int(correction)
            if len(str(First)) == 1:
            	First = str('0') + str(First)
            QIYAM = str(First) + str(":") + txt_1[0][-2:] + str(" ") + txt_1[1]
            outfile.write('<Choice>\n\t<Contnt>' + str(x[0][0]) + '</Contnt>\n' + '\t<Contr>' + str(x[0][1]) + '</Contr>\n' + '\t<fajr>' + str(Change_times_2(x[0][2])) + '</fajr>\n' + '\t<sunrise>' + str(Change_times_2(x[0][3])) + '</sunrise>\n' + '\t<dhuhr>' + str(Change_times_2(x[0][4])) + '</dhuhr>\n' + '\t<asr>' + str(Change_times_2(x[0][5])) + '</asr>\n' + '\t<maghrib>' + str(Change_times_2(x[0][6])) + '</maghrib>\n' + '\t<isha>' + str(Change_times_2(x[0][7])) + '</isha>\n' + '\t<qiyam>' + str(QIYAM) + '</qiyam>\n' + '\t<url>' + str(x[0][9]).replace('\n', '').replace('\t', '').replace('\r', '') + '</url>\n' + '\t<Id>' + str(x[0][10]) + '</Id>\n' + '\t<Lati>' + str(x[0][11]) + '</Lati>\n' + '\t<Longit>' + str(x[0][12]) + '</Longit>\n' + '\t<hijri>' + str(x[0][13]) + '</hijri>\n' + '\t<clac>' + str(x[0][14]) + '</clac>\n' + '\t<next>' + str(x[0][15]) + '</next>\n' + '\t<bled>' + str(x[0][16]) + '</bled>\n' + '\t<haiaa>' + str(x[0][17]) + '</haiaa>\n</Choice>\n')
            outfileo.write(str(x[0][1]) + '\n' + str(x[0][16]) + '\n' + str(Change_times(x[0][2])) + '\n' + str(Change_times(x[0][3])) + '\n' + str(Change_times(x[0][4])) + '\n' + str(Change_times(x[0][5])) + '\n' + str(Change_times(x[0][6])) + '\n' + str(Change_times(x[0][7])))
            outfileoo.write(str(x[0][1]) + ',' + str(x[0][16]))
            Favo = '<Contry>\n' + '\t<Contnt>' + str(x[0][0]) + '</Contnt>\n' + '\t<Contr>' + str(x[0][1]) + '</Contr>\n' + '\t<name>' + str(x[0][16]) + '</name>\n' + '\t<url>' + str(x[0][9]).replace('\n', '').replace('\t', '').replace('\r', '') + '</url>\n' + '\t<Id>' + str(x[0][10]) + '</Id>\n' + '</Contry>\n'
            name = str(x[0][16])
            XML_Replace_Line(Favo, name)

        outfile.write('</stream>')
        outfile.close()
        outfileo.close()
        outfileo.close()
        outfileoo.close()
    except compat_HTTPError as e:
        print('XML_Choice: error reading files')

def XML_AudioAthan(Mylist):
    try:
        Path = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Flash/audiop.xml'
        os.remove(Path)
        outfile = open(Path, 'a')
        outfile.write('<?xml version="1.0"?>\n<stream>\n')
        for x in Mylist:
                outfile.write('<flash>\n\t<name>' + str(x[0][0]) + '</name>\n' + '\t<url>' + str(x[0][1]) + '</url>\n' + '</flash>\n')
        outfile.write('</stream>')
        outfile.close()
    except compat_HTTPError as e:
        print('XML_AudioAthan: error reading (/Flash/audiop.xml) file')

def XML_Replace_Line(line, name):
    try:
        f = open('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Flash/Favos.xml', 'r')
        chaine = f.read()
        f.close()
        if '<name>' + name + '</name>' in chaine:
                pass
        else:
                result = chaine.replace('</stream>', line + '</stream>')
                f = open('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Flash/Favos.xml', 'w')
                f.write(result)
                f.close()
    except compat_HTTPError as e:
        print('XML_Replace_Line: error reading (/Flash/Favos.xml) file')

def XML_Replace_Line_1(line):
    try:
        messg = ''
        f = open('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Flash/Favos.xml', 'r')
        chaine = f.read()
        f.close()
        if line in chaine:
                messg = 'Oui'
        else:
                messg = 'Non'
        return messg
    except compat_HTTPError as e:
        print('XML_Replace_Line_1: error reading (/Flash/audiop.xml) file')

def XML_Delet_Line_Favos(line):
    try:
        messg = ''
        f = open('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Flash/Favos.xml', 'r')
        chaine = f.read()
        f.close()
        result = chaine.replace(line, '')
        f = open('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Flash/Favos.xml', 'w')
        f.write(result)
        f.close()
        return messg
    except compat_HTTPError as e:
        print('XML_Delet_Line_Favos: error reading (/Flash/Favos.xml) file')

def Upcoming_Line():
    try:
        nomsalat = ''
        f = open('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Flash/Upcoming.txt', 'r')
        chaine = f.read()
        f.close()
        if chaine == 'Fajr':
            nomsalat = 'الفجر'
        elif chaine == 'Zuhr':
            nomsalat = 'الظهر'
        elif chaine == 'Asr':
            nomsalat = 'العصر'
        elif chaine == 'Maghrb':
            nomsalat = 'المغرب'
        elif chaine == 'Esha':
            nomsalat = 'العشاء'
        return nomsalat
    except compat_HTTPError as e:
        print('Upcoming_Line: error reading (/Flash/Upcoming.xml) file')

class StreamURIParserAthanmenu_1():

    def __init__(self, xml):
        self.xml = xml

    def parseStreamListAthanmenu_1(self):
        try:
                Athanlist1 = []
                tree = ElementTree()
                tree.parse(self.xml)
                for Athan in tree.findall('Contry'):
                        name = str(Athan.findtext('name'))
                        url = str(Athan.findtext('url'))
                        Id = str(Athan.findtext('Id'))
                        Athanlist1.append({'name': name, 'url': url, 'Id': Id})
                return Athanlist1
        except compat_HTTPError as e:
                print('parseStreamListAthanmenu_1: error reading file')

class StreamURIParserAthanmenu_2():

    def __init__(self, xml):
        self.xml = xml

    def parseStreamListAthanmenu_2(self):
        try:
                Athanlist1 = []
                tree = ElementTree()
                tree.parse(self.xml)
                for Athan in tree.findall('Contry'):
                        Contnt = str(Athan.findtext('Contnt'))
                        Contr = str(Athan.findtext('Contr'))
                        name = str(Athan.findtext('name'))
                        url = str(Athan.findtext('url'))
                        Id = str(Athan.findtext('Id'))
                        Athanlist1.append({'Contnt': Contnt, 'Contr': Contr, 
                                'name': name, 
                                'url': url, 
                                'Id': Id})
                return Athanlist1
        except compat_HTTPError as e:
                print('parseStreamListAthanmenu_2: error reading file')

class ParserAthanFlash():

    def __init__(self, xml):
        self.xml = xml

    def parseListAthanFlash(self):
        try:
                Athanlist1 = []
                tree = ElementTree()
                tree.parse(self.xml)
                for Athan in tree.findall('flash'):
                        name = str(Athan.findtext('name'))
                        url = str(Athan.findtext('url'))
                        urimg = str(Athan.findtext('urimg'))
                        Athanlist1.append({'name': name, 'url': url, 
                                'urimg': urimg})
                return Athanlist1
        except compat_HTTPError as e:
                print('parseListAthanFlash: error reading file')

class ParserAthanAyames():

    def __init__(self, xml):
        self.xml = xml

    def parseListAthanAyames(self):
        try:
                Athanlist1 = []
                tree = ElementTree()
                tree.parse(self.xml)
                for Athan in tree.findall('ayames'):
                        name = str(Athan.findtext('name'))
                        date1 = str(Athan.findtext('date1'))
                        date2 = str(Athan.findtext('date2'))
                        Athanlist1.append({'name': name, 'date1': date1, 
                                'date2': date2})
                return Athanlist1
        except compat_HTTPError as e:
                print('parseListAthanAyames: error reading file')

class StreamURIParserAthanmenu():

    def __init__(self, xml):
        self.xml = xml

    def parseStreamListAthanmenu(self):
        try:
                Athanlist1 = []
                tree = ElementTree()
                tree.parse(self.xml)
                for Athan in tree.findall('Choice'):
                        Contnt = str(Athan.findtext('Contnt'))
                        name = str(Athan.findtext('name'))
                        Athanlist1.append({'Contnt': Contnt, 'name': name})
                return Athanlist1
        except compat_HTTPError as e:
                print('parseStreamListAthanmenu: error reading file')

class StreamURIParserAthan():

    def __init__(self, xml):
        self.xml = xml

    def parseStreamListAthan(self):
        try:
                Athanlist = []
                im = 0
                tree = ElementTree()
                tree.parse(self.xml)
                for Athan in tree.findall('Choice'):
                        Contnt = str(Athan.findtext('Contnt'))
                        Contr = str(Athan.findtext('Contr'))
                        fajr = str(Athan.findtext('fajr'))
                        sunrise = str(Athan.findtext('sunrise'))
                        dhuhr = str(Athan.findtext('dhuhr'))
                        asr = str(Athan.findtext('asr'))
                        maghrib = str(Athan.findtext('maghrib'))
                        isha = str(Athan.findtext('isha'))
                        qiyam = str(Athan.findtext('qiyam'))
                        url = str(Athan.findtext('url'))
                        Id = str(Athan.findtext('Id'))
                        Lati = str(Athan.findtext('Lati'))
                        Longit = str(Athan.findtext('Longit'))
                        hijri = str(Athan.findtext('hijri'))
                        clac = str(Athan.findtext('clac'))
                        next = str(Athan.findtext('next'))
                        bled = str(Athan.findtext('bled'))
                        haiaa = str(Athan.findtext('haiaa'))
                        WeatheId = str(Athan.findtext('WeatheId'))
                        Athanlist.append({'Contnt': Contnt, 'Contr': Contr, 
                                'fajr': fajr, 
                                'sunrise': sunrise, 
                                'sunrise': sunrise, 
                                'dhuhr': dhuhr, 
                                'asr': asr, 
                                'maghrib': maghrib, 
                                'isha': isha, 
                                'qiyam': qiyam, 
                                'url': url, 
                                'Id': Id, 
                                'Lati': Lati, 
                                'Longit': Longit, 
                                'hijri': hijri, 
                                'clac': clac, 
                                'next': next, 
                                'bled': bled, 
                                'haiaa': haiaa, 
                                'WeatheId': WeatheId})
                return Athanlist
        except compat_HTTPError as e:
                print('parseStreamListAthan: error reading file')

def extr_url(cnd):
    try:
        HH = ''
        ecmf = open('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Choice/Choice.txt', 'r')
        ecm = ecmf.readlines()
        for line in ecm:
                if cnd in line:
                        HH = line.split('=')[1].replace('\n', '').replace('\t', '').replace('\r', '')
                        if '=ar' in HH:
                                HH = HH
                        else:
                                HH = HH + '=ar'
        return HH
    except compat_HTTPError as e:
        print('XML_AudioAthan: error reading (/Choice/Choice.txt) file')

def get_remaining_time(h, m):
    #from .datetime import datetime
    maintenant = datetime.now()
    H = maintenant.hour
    M = maintenant.minute
    S = maintenant.second
    if int(H) == 0:
        H = 24
    else:
        H = H
    if int(H) >= 12:
        if int(h) >= 12:
            Act_1 = int(H) * 60 + int(M)
            Act_2 = int(h) * 60 + int(m)
        if int(h) < 12:
            Act_1 = int(H) * 60 + int(M)
            Act_2 = (int(h) + 24) * 60 + int(m)
    else:
        Act_1 = int(H) * 60 + int(M)
        Act_2 = int(h) * 60 + int(m)
    rest = abs(Act_1 - Act_2)
    if rest >= 60:
        if PY3:
            rest_1 = float(rest) // 60
        else:
            rest_1 = float(rest) / 60
        rest_2 = round(rest_1, 2)
        if PY3:
            rest_3 = rest // 60
        else:
            rest_3 = rest / 60
        rest_4 = (rest_2 - rest_3) * 60
        rest_4 = round(rest_4, 0)
        if rest_4 >= 60:
            rest_4 = rest_4 - 60
            rest = str(rest_3 + 1) + ' (h)سا ' + ':' + str(format(rest_4, '.0f')) + ' (m)د'
        else:
            rest = str(rest_3) + ' (h)سا ' + ':' + str(format(rest_4, '.0f')) + ' (m)د'
    else:
        rest = str(rest) + ' (m)د '
    return str(rest) + ' '

def Change_times(txt):
    correction = config.plugins.AthanTimes.correctiontime.value
    txt_1 = int(txt.split(':')[:1][0]) + int(correction)
    if len(str(txt_1)) == 1:
    	txt_1 = str('0') + str(txt_1)
    txt_2 = txt.split(':')[1:][0]
    if 'PM' in txt_2:
        if int(txt.split(':')[:1][0]) < 12:
            txt_1 = int(txt.split(':')[:1][0]) + 12 + int(correction)
            if len(str(txt_1)) == 1:
            	txt_1 = str('0') + str(txt_1)
            txt_2 = txt.split(':')[1:][0]
        else:
            txt_1 = int(txt.split(':')[:1][0]) + int(correction)
            if len(str(txt_1)) == 1:
            	txt_1 = str('0') + str(txt_1)
            txt_2 = txt.split(':')[1:][0]
    if 'AM' in txt_2:
        txt_1 = int(txt.split(':')[:1][0]) + int(correction)
        if len(str(txt_1)) == 1:
        	txt_1 = str('0') + str(txt_1)
        txt_2 = txt.split(':')[1:][0]
    return str(txt_1) + ':' + str(txt_2).replace('PM', '').replace('AM', '')

def Change_times_2(txt):
    correction = config.plugins.AthanTimes.correctiontime.value
    txt_1 = int(txt.split(':')[:1][0]) + int(correction)
    if len(str(txt_1)) == 1:
    	txt_1 = str('0') + str(txt_1)
    txt_2 = txt.split(':')[1:][0]
    if 'PM' in txt_2:
        if int(txt.split(':')[:1][0]) < 12:
            txt_1 = int(txt.split(':')[:1][0]) + 12 + int(correction)
            if len(str(txt_1)) == 1:
            	txt_1 = str('0') + str(txt_1)
            txt_2 = txt.split(':')[1:][0]
        else:
            txt_1 = int(txt.split(':')[:1][0]) + int(correction)
            if len(str(txt_1)) == 1:
            	txt_1 = str('0') + str(txt_1)
            txt_2 = txt.split(':')[1:][0]
    if 'AM' in txt_2:
        txt_1 = int(txt.split(':')[:1][0]) + int(correction)
        if len(str(txt_1)) == 1:
        	txt_1 = str('0') + str(txt_1)
        txt_2 = txt.split(':')[1:][0]
    return str(txt_1) + ':' + str(txt_2)

def Change_times_1(txt):
    correction = config.plugins.AthanTimes.correctiontime.value
    txt_1 = int(txt.split(':')[:1][0]) + int(correction)
    if len(str(txt_1)) == 1:
    	txt_1 = str('0') + str(txt_1)
    txt_2 = txt.split(':')[1:][0]
    return str(txt_1) + ':' + str(txt_2).replace('PM', '').replace('AM', '')

def Search_City(txt):
    txt_1 = txt.split(':')[:1][0]
    txt_2 = txt.split(':')[1:][0]
    if 'PM' in txt_2:
        if int(txt.split(':')[:1][0]) < 12:
            txt_1 = int(txt.split(':')[:1][0]) + 12
            txt_2 = txt.split(':')[1:][0]
        else:
            txt_1 = txt.split(':')[:1][0]
            txt_2 = txt.split(':')[1:][0]
    if 'AM' in txt_2:
        txt_1 = txt.split(':')[:1][0]
        txt_2 = txt.split(':')[1:][0]
    return str(txt_1) + ':' + str(txt_2).replace('PM', '').replace('AM', '')


class SearchAthan():

    def __init__(self, city, id):
        self.city = city
        self.id = id
        self.bilad = ''

    def SearchAthan_1(self):
        self.letter_list = []
        self.limit = 0
        main_url = 'https://www.islamicfinder.org/world/search-city?keyword=' + self.city + '&countryId=' + str(self.id)
        req = compat_Request(main_url)
        try:
            response = compat_urlopen(req)
            Test_page = response.read()
        except compat_HTTPError as e:
            print(e.code)
            Test_page = 'HTTP download ERROR: %s' % str(e.code)

        if isinstance(Test_page, bytes):
            Test_page = Test_page.decode('utf-8', 'ignore')
        if Test_page.startswith('HTTP download ERROR:'):
            self.bilad = Test_page
        else:
            request = compat_Request(main_url, None, Agent)
            if PY3:
            	data = compat_urlopen(request).read().decode('utf-8')
            else:
            	data = compat_urlopen(request).read()
            bilad = re.findall('"cityId":(.*?),"countryId":(.*?),"cityName":"(.*?)"', data)
            self.limit = len(bilad)
            for i in range(self.limit):
                try:
                    self.letter_list.append(show_listiptv2(bilad[i][2], bilad[i][0], bilad[i][1], ''))
                except IndexError:
                    pass

            if bilad == []:
                self.bilad = 'City Not Found'
            else:
                self.bilad = self.letter_list
        return self.bilad

def Search_idCtr(txt):
    idCtr = ''
    try:
        for line in open('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/countryId.txt'):
            if txt in line:
                idCtr = line.split('=')[1].replace('\n', '').replace('\t', '').replace(' ', '')
    except:
        return
    return idCtr


class SearchAthanConvert():

    def __init__(self, Day, Month, Year):
        self.Day = Day
        self.Month = Month
        self.Year = Year
        self.bilad = ''

    def SearchAthanConvert_1(self):
        self.limit = 0
        main_url = 'http://www.islamicfinder.org/dateConversion.php?mode=ger-hij&day=' + str(self.Day) + '&month=' + str(self.Month) + '&year=' + str(self.Year) + '&date_result=1&lang=arabic'
        req = compat_Request(main_url)
        try:
            response = compat_urlopen(req)
            Test_page = response.read()
        except compat_HTTPError as e:
            print(e.code)
            Test_page = 'HTTP download ERROR: %s' % str(e.code)

        if isinstance(Test_page, bytes):
            Test_page = Test_page.decode('utf-8', 'ignore')
        if Test_page.startswith('HTTP download ERROR:'):
            self.bilad = Test_page
        else:
            request = compat_Request(main_url, None, Agent)
            if PY3:
            	data = compat_urlopen(request).read().decode('utf-8')
            else:
            	data = compat_urlopen(request).read()
            bilad = re.findall('<span class="date-converted-date">(.+?)</span><span.+?class="date-converted-day">(.+?)</span><span class="note">.+?</span> <br>', data, re.S)
            self.limit = len(bilad)
            for i in range(self.limit):
                try:
                    self.bilad = Change_TXTDay(str(bilad[0][1])) + '_' + Change_TXT(str(bilad[0][0]))
                except IndexError:
                    pass

            if bilad == []:
                self.bilad = 'City Not Found'
            else:
                self.bilad = self.bilad
        return self.bilad

def Change_TXT(txt):
    TXT = txt
    if 'محرم' in TXT:
        TXT = TXT.replace('محرم', 'محرم_Muharram_')
    elif 'صفر' in TXT:
        TXT = TXT.replace('صفر', 'صفر_Safar_')
    elif 'ربيع الأول' in TXT:
        TXT = TXT.replace('ربيع الأول', 'ربيع الأول_Rabi Al-Awwal_')
    elif 'ربيع الآخرة' in TXT:
        TXT = TXT.replace('ربيع الآخرة', 'ربيع الآخرة_Rabi Al-Akhar_')
    elif 'جمادى الأولى' in TXT:
        TXT = TXT.replace('جمادى الأولى', 'جمادى الأولى_Jumada Al-Awwal_')
    elif 'جمادى الآخرة' in TXT:
        TXT = TXT.replace('جمادى الآخرة', 'جمادى الآخرة_Jumada Al-Akhirah_')
    elif 'رجب' in TXT:
        TXT = TXT.replace('رجب', 'رجب_Rajab_')
    elif 'شعبان' in TXT:
        TXT = TXT.replace('شعبان', 'شعبان_Shaban_')
    elif 'رمضان' in TXT:
        TXT = TXT.replace('رمضان', 'رمضان_Ramadan_')
    elif 'شوال' in TXT:
        TXT = TXT.replace('شوال', 'شوال_Shawwal_')
    elif 'ذي القعدة' in TXT:
        TXT = TXT.replace('ذي القعدة', 'ذي القعدة_Dhul Qadah_')
    elif 'ذي الحجة' in TXT:
        TXT = TXT.replace('ذي الحجة', 'ذي الحجة_Dhul Hiijah_')
    else:
        TXT = TXT
    return TXT

def Change_TXTDay(txt):
    TXT = txt
    if 'الجمعة' in TXT:
        TXT = TXT.replace('الجمعة', 'الجمعة_Friday_')
    elif 'السبت' in TXT:
        TXT = TXT.replace('السبت', 'السبت_Saturday_')
    elif 'الأحد' in TXT:
        TXT = TXT.replace('الأحد', 'الأحد_Sunday_')
    elif 'الاثنين' in TXT:
        TXT = TXT.replace('الاثنين', 'الاثنين_Monday_')
    elif 'الثلاثاء' in TXT:
        TXT = TXT.replace('الثلاثاء', 'الثلاثاء_Tuesday_')
    elif 'الأربعاء' in TXT:
        TXT = TXT.replace('الأربعاء', 'الأربعاء_Wednesday_')
    elif 'الخميس' in TXT:
        TXT = TXT.replace('الخميس', 'الخميس_Thursday_')
    else:
        TXT = TXT
    return TXT

def Change_TXTDay_2(txt):
    TXT = txt
    if 'Friday' in TXT:
        TXT = TXT.replace('Friday', '_Friday_الجمعة')
    elif 'Saturday' in TXT:
        TXT = TXT.replace('Saturday', '_Saturday_السبت')
    elif 'Sunday' in TXT:
        TXT = TXT.replace('Sunday', '_Sunday_الأحد')
    elif 'Monday' in TXT:
        TXT = TXT.replace('Monday', 'الاثنين_Monday_')
    elif 'Tuesday' in TXT:
        TXT = TXT.replace('Tuesday', '_Tuesday_الثلاثاء')
    elif 'Wednesday' in TXT:
        TXT = TXT.replace('Wednesday', '_Wednesday_الأربعاء')
    elif 'Thursday' in TXT:
        TXT = TXT.replace('Thursday', '_Thursday_الخميس')
    elif 'Mardi' in TXT:
        TXT = TXT.replace('Mardi', '_Mardi_الثلاثاء')
    elif 'Mercredi' in TXT:
        TXT = TXT.replace('Mercredi', '_Mercredi_الاربعاء')
    elif 'Jeudi' in TXT:
        TXT = TXT.replace('Jeudi', '_Jeudi_الخميس')
    elif 'Vendredi' in TXT:
        TXT = TXT.replace('Vendredi', '_Vendredi_الجمعة')
    elif 'Samedi' in TXT:
        TXT = TXT.replace('Samedi', '_Samedi_السبت')
    elif 'Dimanche' in TXT:
        TXT = TXT.replace('Dimanche', '_Dimanche_الاحد')
    elif 'Lundi' in TXT:
        TXT = TXT.replace('Lundi', '_Lundi_الاثنين')
    else:
        TXT = TXT
    return TXT


def Copyurlvideo(txt):
    try:
        Path = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/video.txt'
        os.remove(Path)
        outfile = open(Path, 'a')
        outfile.write('url =' + txt)
        outfile.close()
        return 'Video link recorded   تم تسجيل رابط الفيديو'
    except compat_HTTPError as e:
        print('Copyurlvideo: error reading file (AthanTimes/video.txt)')

class SearchAthanWeather():

    def __init__(self, city, contr):
        self.city = city
        self.contr = contr
        self.bilad = ''

    def SearchWeather(self):
        if self.city == 'Algiers' or self.city == 'الجزائر' or self.city == 'Alger' or self.city == 'Algiers Bay' or self.city == 'Algiers Station':
            self.bilad = str(1253079)
            CopyidWeathe(self.bilad)
        else:
            main_url = 'https://www.yahoo.com/news/_td/api/resource/WeatherSearch;text=%s' % self.city.replace(' ', '%20')
            req = compat_Request(main_url)
            try:
                response = compat_urlopen(req)
                Test_page = response.read()
            except compat_HTTPError as e:
                print(e.code)
                Test_page = 'HTTP download ERROR: %s' % str(e.code)

            if isinstance(Test_page, bytes):
                Test_page = Test_page.decode('utf-8', 'ignore')
            if Test_page.startswith('HTTP download ERROR:'):
                self.bilad = Test_page
                CopyidWeathe('City Not Found')
            else:
                request = compat_Request(main_url, None, Agent)
                if PY3:
                	data = compat_urlopen(request).read().decode('utf-8')
                else:
                	data = compat_urlopen(request).read()
                bilado = re.findall('woeid":(.+?),"lat":.*?,"lon":.*?,"country":"' + self.contr + '"', data)
            if bilado == [] or len(bilado) == 0:
                self.bilad = 'City Not Found'
                CopyidWeathe(self.bilad)
            else:
                self.bilad = str(bilado[0])
                CopyidWeathe(self.bilad)
        return

def CopyidWeathe(txt):
    try:
        Path = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/outils/YahooWeather/Config/Location_id'
        os.remove(Path)
        outfile = open(Path, 'a')
        outfile.write(txt)
        outfile.close()
        XML_ADD_Line_WeatheId(txt)
    except compat_HTTPError as e:
        print('CopyidWeathe: error reading file (Config/Location_id)')

def XML_ADD_Line_WeatheId(line):
    try:
        f = open('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes.xml', 'r')
        chaine = f.read()
        f.close()
        result = chaine.replace('</Choice>', '\t<WeatheId>' + str(line) + '</WeatheId>\n</Choice>')
    except compat_HTTPError as e:
        print('XML_ADD_Line_WeatheId: error reading file (AthanTimes/PrayerTimes.xml)')
    try:
        f = open('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes.xml', 'w')
        f.write(result)
        f.close()
    except compat_HTTPError as e:
        print('XML_ADD_Line_WeatheId: error writing file (AthanTimes/PrayerTimes.xml)')

def Prayer_txt(a, b, c, d, e, f, g):
    try:
        Patho = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Prayer.txt'
        os.remove(Patho)
        outfileo = open(Patho, 'a')
        outfileo.write(a + '\n' + b + '\n' + c + '\n' + d + '\n' + e + '\n' + f + '\n' + g)
        outfileo.close()
    except compat_HTTPError as e:
        print('Prayer_txt: error reading file (AthanTimes/Prayer.txt)')

def XML_Choice_Contr_bled(Mylist):
    ZZZ = ''
    for x in Mylist:
        ZZZ = str(x[0][1]) + '\n' + str(x[0][16])
    return ZZZ

def Import_times_Salat(a):
    try:
        ptimesfile = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Prayer.txt'
        if not os.path.exists(ptimesfile):
            os.system('touch ' + ptimesfile)
            open(ptimesfile, 'w').write('Algeria\nbab-ezzouar\n06:20:00\n07:48:00\n15:52:00\n15:52:00\n18:14:00\n19:37:00\n')
        ptfile = open(ptimesfile, 'r')
        data = ptfile.readlines()
        ptfile.close()
        country = str(data[0]).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        city = str(data[1]).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        fajr = str(data[2]).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        sunrise = str(data[3]).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        dhur = str(data[4]).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        asr = str(data[5]).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        maghrib = str(data[6]).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        isha = str(data[7]).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        if a == 'fajr':
            return fajr
        if a == 'sunrise':
            return sunrise
        if a == 'dhur' or a == 'dhuhr' or a == 'Zuhr':
            return dhur
        if a == 'asr':
            return asr
        if a == 'maghrib':
            return maghrib
        if a == 'isha':
            return isha
    except compat_HTTPError as e:
        print('Import_times_Salat: File (AthanTimes/Prayer.txt) empty')

def Import_times_Upadat_Salat():
    try:
        ptimesfile = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Prayer.txt'
        ptfile = open(ptimesfile, 'r')
        data = ptfile.readlines()
        ptfile.close()
        fajr = str(data[2]).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        f = []
        f = fajr.split(':')
        fhour = f[0]
        fminute = f[1]
        fajr_1 = [fhour, fminute]
        sunrise = str(data[3]).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        g = []
        g = sunrise.split(':')
        ghour = g[0]
        gminute = g[1]
        sunrise_1 = [ghour, gminute]
        dhur = str(data[4]).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        h = []
        h = dhur.split(':')
        hhour = h[0]
        hminute = h[1]
        dhur_1 = [hhour, hminute]
        asr = str(data[5]).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        i = []
        i = asr.split(':')
        ihour = i[0]
        iminute = i[1]
        asr_1 = [ihour, iminute]
        maghrib = str(data[6]).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        j = []
        j = maghrib.split(':')
        jhour = j[0]
        jminute = j[1]
        maghrib_1 = [jhour, jminute]
        isha = str(data[7]).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        k = []
        k = isha.split(':')
        khour = k[0]
        kminute = k[1]
        isha_1 = [khour, kminute]
        return (fajr_1,sunrise_1,dhur_1,asr_1,maghrib_1,isha_1)
    except compat_HTTPError as e:
        print('Import_times_Upadat_Salat: error reading file (AthanTimes/Prayer.txt)')

def Nmbrs_lines():
    if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/messageupdat.txt'):
        file = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/messageupdat.txt'
        n = sum(1 for _ in open(file))
        return n
    else:
        return 0

def Nmbrs_lines_2():
    if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Times.txt'):
        file = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Times.txt'
        n = sum(1 for _ in open(file))
        return n
    else:
        return 0

def Import_Datetime_Updat():
    message_1 = ''
    message_2 = ''
    message_3 = ''
    message_4 = ''
    n = Nmbrs_lines()
    if int(n) != 0:
        ptimesfile = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/messageupdat.txt'
        ptfile = open(ptimesfile, 'r')
        data = ptfile.readlines()
        ptfile.close()
        message_1 = str(data[0]).replace('\n', '').replace('\t', '').replace('\r', '')
        message_2 = str(data[1]).replace('\n', '').replace('\t', '').replace('\r', '')
        if int(message_2) < 10:
            message_2 = '0' + str(message_2)
        message_3 = str(data[2]).replace('\n', '').replace('\t', '').replace('\r', '')
        if int(message_3) < 10:
            message_3 = '0' + str(message_3)
        message_4 = str(data[3]).replace('\n', '').replace('\t', '').replace('\r', '')
        return (
         message_1,
         message_2,
         message_3,
         message_4)
    else:
        message_1 = '....'
        message_2 = '....'
        message_3 = '....'
        message_4 = '....'
        return (message_1,
         message_2,
         message_3,
         message_4)

def Import_time_Updat():
    timupdat = ''
    ptimesfile = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Times.txt'
    ptfile = open(ptimesfile, 'r')
    data = ptfile.readlines()
    ptfile.close()
    n = Nmbrs_lines_2()
    if int(n) != 0:
        timupdat = str(data[0]).replace('\n', '').replace('\t', '').replace('\r', '')
    else:
        timupdat = ''
    return timupdat

def Replace_time_Line_Updat(line):
    filepath = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/ChoiceTime.txt'
    if not os.path.exists(filepath) or len(open(filepath, 'r').readlines()) < 5:
        os.system('touch ' + filepath)
        open(filepath, 'w').write('\n\n\n\ntimeupdat=\n')
    try:
        f = open(filepath, 'r')
        chaine = f.readlines()
        f.close()
        lin0 = chaine[0].replace('\n', '').replace('\t', '').replace('\r', '')
        lin1 = chaine[1].replace('\n', '').replace('\t', '').replace('\r', '')
        lin2 = chaine[2].replace('\n', '').replace('\t', '').replace('\r', '')
        lin3 = chaine[3].replace('\n', '').replace('\t', '').replace('\r', '')
        lin4 = 'timeupdat=' + str(line)
        result = lin0 + '\n' + lin1 + '\n' + lin2 + '\n' + lin3 + '\n' + lin4
    except:
        print('Replace_time_Line_Updat: error reading file PrayerTimes/ChoiceTime.txt')
        return
    try:
        f = open(filepath, 'w')
        f.write(result)
        f.close()
    except:
        print('Replace_time_Line_Updat: error writing file PrayerTimes/ChoiceTime.txt')

def ImportDataInfos(data):
    if PY3:
        data = data.decode('utf-8', 'ignore')

    data = data.replace('&nbsp;', ' ')

    bilad = ''
    m = re.search(r'"canonical"\s*:\s*"([^"]+)"', data)
    if m:
        url = m.group(1)
    else:
        m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', data, re.I)
        url = m.group(1) if m else ''
    if url:
        m = re.search(r'/(\d+)/([^/?]+)-prayer-times/?(?:\?|$)', url)
        if m:
            bilad = m.group(2).replace('-', ' ').strip()

    fajr = re.findall(r'"fajr"\s*:\s*"([^"]+)"', data, re.I)
    if not fajr:
        fajr = re.findall(r'prayerTiles.*?fajar.*?prayertime[^>]*>\s*([^<]+)', data, re.S | re.I)

    sunrise = re.findall(r'sunrise-tile.*?<span class="prayertime[^"]*">\s*([0-9: ]+[AP]M)', data, re.S | re.I)

    dhuhr = re.findall(r'dhuhar-tile.*?<span class="prayertime[^"]*">\s*([0-9: ]+[AP]M)', data, re.S | re.I)

    asr = re.findall(r'asr-tile.*?<span class="prayertime[^"]*">\s*([0-9: ]+[AP]M)', data, re.S | re.I)

    maghrib = re.findall(r'maghrib-tile.*?<span class="prayertime[^"]*">\s*([0-9: ]+[AP]M)', data, re.S | re.I)

    isha = re.findall(r'isha-tile.*?<span class="prayertime[^"]*">\s*([0-9: ]+[AP]M)', data, re.S | re.I)

    qiyam = ['02:18 AM']

    Id = re.findall(r'"locationId"\s*:\s*"([^"]+)"', data)

    haiaa = re.findall(r'<p class="pt-method-text">\s*(.*?)\s*<a', data, re.S)
    haiaa = haiaa[0].strip() if haiaa else ''

    Calc = re.findall(r'<p class="pt-method-desc">\s*(.*?)\s*</p>', data, re.S)
    Calc = re.sub(r'<.*?>', '', Calc[0]).replace('\n', '').replace('\r', '').replace('\t', '').strip() if Calc else ''

    hijri = re.findall(r'<span class="pt-date-hijri">\s*(.*?)\s*</span>', data, re.S)
    hijri = re.sub(r'<.*?>', '', hijri[0]).strip() if hijri else ''

    NextSalat = re.findall(r'"nextPrayer"\s*:\s*"lang\.([^"]+)".*?"nextPrayerRemainingTime"\s*:\s*"([^:"]+):([^:"]+):', data, re.S)

    Posit = re.findall(r'id="user-manual-latitude".*?value="([^"]+)".*?id="user-manual-longitude".*?value="([^"]+)"', data, re.S)

    return (
        bilad,
        fajr,
        sunrise,
        dhuhr,
        asr,
        maghrib,
        isha,
        qiyam,
        Id,
        haiaa,
        Calc,
        Calc,
        hijri,
        NextSalat,
        Posit
    )

def show_listiptv0(h, p, u, pw):
    png = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry.png'
    if dwidth == 1280:
        res = [(h, p, u, pw)]
        res.append(MultiContentEntryPixmapAlphaTest(pos=(2, 2), size=(380, 31), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(45, 2), size=(380, 31), font=8, text=h, flags=RT_HALIGN_CENTER))
        return res
    else:
        res = [(h, p, u, pw)]
        res.append(MultiContentEntryPixmapAlphaTest(pos=(2, 2), size=(380, 31), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(45, 2), size=(380, 31), font=8, text=h, flags=RT_HALIGN_CENTER))
        return res

def show_listiptv(h, p, u, pw):
    if dwidth == 1280:
        res = [(h,p,u,pw)]
        if 'Free Server Cccam' in h:
            res.append(MultiContentEntryText(pos=(2, 2), size=(425, 30), font=5, text=h, backcolor_sel=26214, backcolor=22503, flags=RT_HALIGN_CENTER))
            return res
        res.append(MultiContentEntryText(pos=(2, 2), size=(425, 30), font=5, text=h, backcolor_sel=26214, backcolor=1090519040, flags=RT_HALIGN_CENTER))
        return res
    else:
        res = [(h,p,u,pw)]
        if 'Free Server Cccam' in h:
            res.append(MultiContentEntryText(pos=(2, 2), size=(402, 30), font=7, text=h, backcolor_sel=26214, backcolor=22503, flags=RT_HALIGN_CENTER))
            return res
        res.append(MultiContentEntryText(pos=(2, 2), size=(402, 30), font=7, text=h, backcolor_sel=26214, backcolor=1090519040, flags=RT_HALIGN_CENTER))
        return res

def streamListEntry_2(entry):
    uriInfo = entry[1].get('name')
    return [entry,
     (eListboxPythonMultiContent.TYPE_TEXT,34,4,380,31,0,RT_HALIGN_LEFT,entry[0])]


class m2list(MenuList):

    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 14))
        self.l.setFont(1, gFont('Regular', 16))
        self.l.setFont(2, gFont('Regular', 18))
        self.l.setFont(3, gFont('Regular', 20))
        self.l.setFont(4, gFont('Regular', 22))
        self.l.setFont(5, gFont('Regular', 24))
        self.l.setFont(6, gFont('Regular', 26))
        self.l.setFont(7, gFont('Regular', 28))
        self.l.setFont(8, gFont('Regular', 30))

def show_listiptv1(Contnt, Contr, fajr, sunrise, dhuhr, asr, maghrib, isha, qiyam, urlop, Id, Posit1, Posit2, hijri, Calcule, Next, bilad, haiaa):
    if dwidth == 1280:
        res = [(Contnt,Contr,fajr,sunrise,dhuhr,asr,maghrib,isha,qiyam,urlop,Id,Posit1,Posit2,hijri,Calcule,Next,bilad,haiaa)]
        res.append(MultiContentEntryText(pos=(2, 2), size=(425, 30), font=5, text=Contnt, backcolor_sel=26214, backcolor=22503, flags=RT_HALIGN_CENTER))
        return res
    else:
        res = [(Contnt,Contr,fajr,sunrise,dhuhr,asr,maghrib,isha,qiyam,urlop,Id,Posit1,Posit2,hijri,Calcule,Next,bilad,haiaa)]
        res.append(MultiContentEntryText(pos=(2, 2), size=(459, 30), font=7, text=Contnt, backcolor_sel=26214, backcolor=22503, flags=RT_HALIGN_CENTER))
        return res

def streamListEntry(entry):
    uriInfo = entry[1].get('url')
    return [entry,(eListboxPythonMultiContent.TYPE_TEXT,80,15,880,50,0,RT_HALIGN_CENTER,entry[0])]

def openfile():
    cityfile = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/city.txt'
    if not os.path.exists(cityfile):
        os.system('touch ' + cityfile)
        open(cityfile, 'w').write('none')
    try:
        fp = open(cityfile, 'r')
        line = fp.read()
        fp.close()
        return line
    except:
        cname = 'none'
        return cname

def geturlvideo():
    urlname = ''
    pathname = open('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/video.txt', 'r')
    getname = pathname.readlines()
    for line in getname:
        if 'url' in line:
            urlname = line.split('=')[1].replace('\n', '').replace('\t', '').replace('\r', '')

    return urlname

def Verif():
    verifrslt = ''
    if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Flash/audio/adhan.mp3'):
        verifrslt = 'yes'
    else:
        verifrslt = 'no'
    return verifrslt

def Upcoming(txt):
    Path = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Flash/Upcoming.txt'
    if fileExists(Path):
        os.remove(Path)
        outfile = open(Path, 'a')
        outfile.write(txt)
        outfile.close()

def Verif_1(Valist):
    if int(Valist[0]) < 10:
        if int(Valist[1]) < 10:
            Valist = ['0' + str(Valist[0]), '0' + str(Valist[1])]
        else:
            Valist = ['0' + str(Valist[0]), Valist[1]]
    elif int(Valist[1]) < 10:
        Valist = [Valist[0], '0' + str(Valist[1])]
    else:
        Valist = [Valist[0], Valist[1]]
    return Valist
