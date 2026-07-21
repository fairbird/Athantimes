# -*- coding: utf-8 -*-
from Components.ActionMap import *
from Screens.Standby import TryQuitMainloop
from Components.ScrollLabel import ScrollLabel
from Screens.Screen import Screen
from Components.Sources.StaticText import StaticText
from twisted.web.client import downloadPage, getPage
from Tools.Directories import resolveFilename, fileExists, SCOPE_PLUGINS
from Plugins.Extensions.AthanTimes.outils.MessagAthanTimes import MessageAthanTimes
from Components.Label import Label
from Plugins.Extensions.AthanTimes.outils.MessageBox import MessageBox
from Screens.Console import Console
from enigma import getDesktop, eServiceReference, iServiceInformation, iPlayableService, eTimer
import os, re, time, base64

#Add By RAED for py2 & py3
from Plugins.Extensions.AthanTimes.outils.compat import compat_urlopen, compat_Request, compat_urlretrieve, compat_HTTPError, PY3

dwidth = getDesktop(0).size().width()

def getversioninfo():
	currversion = '1.0'
	version_file = resolveFilename(SCOPE_PLUGINS, 'Extensions/AthanTimes/Version')
	if os.path.exists(version_file):
		try:
			fp = open(version_file, 'r').readlines()
			for line in fp:
				if 'version' in line.lower():
					currversion = line.split('=')[1].strip()
		except:
			pass
	return currversion

Ver = getversioninfo()

#Agent = {'User-agent': 'Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.0.15) Gecko/2009102815 Ubuntu/9.04 (jaunty) Firefox/3.', 'Connection': 'Close'}
Agent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
Date = ''
NV = '%s' % Ver
Version1 = 'athan times V %s' % Ver
Version = 'athan times for many cities_مواقيت الصلاة لعديد المدن'
LienUpd = base64.b64decode('aHR0cDovL3d3dy5tZWRpYWZpcmUuY29tL2ZpbGUvb2hyOW40eTc2c2RpNjBjL0F0aGFuVGltZXNVcGRhdC50eHQ=')


class AthanTimes_About(Screen):
    skin = '<screen name="AthanTimes_About" position="378,142" size="510,529" title="' + Version1 + '" flags="wfNoBorder" backgroundColor="#41000000"><widget name="text" position="15,10" size="480,482" font="Regular;20" foregroundColor="white" backgroundColor="#80000000" /><ePixmap position="160,291" zPosition="1" size="200,200" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/AthanTimes.png" alphatest="blend" transparent="1" /></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        info = '\n ' + Version + ' \n - أبوياسين الجزائري -  \n --------------------------- \n ' + Version1 + ' ...\n --------------------------- \n Aime_Jeux   \n' + Date
        self['text'] = ScrollLabel(info)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.close, 'cancel': self.close}, -1)


LienTxto = 'http://www.mediafire.com/file/cxggzj3nbyud9yt/NewUpdateAthanTimes.txt'

class AthanTimes_NewUpdate(Screen):
    skinfhd = '<screen name="AthanTimes_NewUpdate" position="16,12" size="632,1044" title="...." flags="wfNoBorder" backgroundColor="#41000000"><widget name="text" position="13,37" size="597,785" font="Regular;20" foregroundColor="white" backgroundColor="#80000000" /><eLabel text="بيانات التحديثات" zPosition="4" position="71,7" size="480,27" font="Regular; 23" transparent="0" backgroundColor="#80000000" halign="center" valign="center" /><ePixmap position="204,834" zPosition="1" size="200,200" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/AthanTimes.png" alphatest="blend" transparent="1" /></screen>'
    skinhd = '<screen name="AthanTimes_NewUpdate" position="16,0" size="632,720" title="...." flags="wfNoBorder" backgroundColor="#41000000"><widget name="text" position="13,37" size="597,450" font="Regular;20" foregroundColor="white" backgroundColor="#80000000" /><eLabel text="بيانات التحديثات" zPosition="4" position="71,7" size="480,27" font="Regular; 23" transparent="0" backgroundColor="#80000000" halign="center" valign="center" /><ePixmap position="206,498" zPosition="1" size="200,200" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/AthanTimes.png" alphatest="blend" transparent="1" /></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        if dwidth == 1280:
            self.skin = AthanTimes_NewUpdate.skinhd
        else:
            self.skin = AthanTimes_NewUpdate.skinfhd
        self['text'] = ScrollLabel('\nصبرا جميلا........\nتحميل البيانلت......')
        req = compat_Request(LienTxto)
        try:
            response = compat_urlopen(req)
            Test_page = response.read()
        except compat_HTTPError as e:
            print(e.code)
            Test_page = 'HTTP download ERROR: %s' % str(e.code)

        if Test_page.startswith(b'HTTP download ERROR:'):
            self['text'] = ScrollLabel('مشكل في الإتصال......\n' + Test_page)
        else:
            UrlFinal = ''
            url1 = ''
            url2 = ''
            URL = ''
            NomFichier = 'NewUpdateAthanTimes.txt'
            Distnt = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/outils'
            if PY3:
            	getPage(LienTxto.encode('utf-8'))
            else:
            	getPage(LienTxto, method='GET', headers=Agent)
            request = compat_Request(LienTxto, None, Agent)
            if PY3:
            	data = compat_urlopen(request).read().decode('utf-8')
            else:
            	data = compat_urlopen(request).read()
            url1 = re.findall('href="http://download(.*?)"', data)
            if len(url1) == 0:
                url2 = re.findall('"Download file"\n.*?href="(.*?)">', data)
                URL = url2[0]
            else:
                URL = 'http://download' + url1[0].replace("'", '')
            compat_urlretrieve(URL, os.path.join(Distnt, NomFichier))
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/outils/NewUpdateAthanTimes.txt'):
                try:
                    mon_fichier = open('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/outils/NewUpdateAthanTimes.txt', 'r')
                    contenu = mon_fichier.read()
                    print(contenu)
                except:
                    return

                self['text'] = ScrollLabel(contenu)
            else:
                self.info1 = 'غير موجود'
                self['text'] = ScrollLabel(str(self.info1))
        os.remove('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/outils/NewUpdateAthanTimes.txt')
        self['actions'] = ActionMap(['SetupActions', 'ColorActions', 'DirectionActions'], {'ok': self.close, 'cancel': self.close, 
           'up': self['text'].pageUp, 
           'down': self['text'].pageDown, 
           'left': self['text'].pageUp, 
           'right': self['text'].pageDown}, -1)
        return


class Updat_AthanTimes(Screen):
    skin = '<screen name="Updat_AthanTimes" position="378,51" size="593,620" title="' + Version1 + '" flags="wfNoBorder" backgroundColor="#41000000"><widget name="text" position="5,7" size="583,570" font="Regular;25" foregroundColor="white" backgroundColor="#80000000" /><ePixmap position="202,374" zPosition="1" size="200,200" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/AthanTimes.png" alphatest="blend" transparent="1" /><eLabel position="5,579" size="200,30" backgroundColor="#ae0001" /><eLabel position="388,579" size="200,30" backgroundColor="#adff00" /><eLabel text="الخروج" zPosition="4" position="10,582" size="190,25" font="Regular; 22" transparent="0" backgroundColor="#80000000" halign="center" /><eLabel text="التحديث" zPosition="4" position="393,582" size="190,25" font="Regular; 22" transparent="0" backgroundColor="#80000000" halign="center" /><widget name="RestarEng" position="68,313" size="480,50" font="Regular;30" foregroundColor="#fdfe02" backgroundColor="#80000000" halign="center" valign="center" /><eLabel position="207,579" size="178,30" backgroundColor="#0000ff" /><eLabel text="الجديد" zPosition="4" position="211,582" size="170,25" font="Regular; 22" transparent="0" backgroundColor="#80000000" halign="center" /></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions', 'DirectionActions'], {'ok': self.close, 'cancel': self.close, 
           'yellow': self.StartEng, 
           'green': self.InfosUpdat, 
           'blue': self.InfosNewsUpdat, 
           'red': self.close}, -1)
        self['text'] = Label()
        self['RestarEng'] = Label()
        self['RestarEng'].setText('إعادة تشغيل الواجهة?')
        self['RestarEng'].hide()
        self.info = '\n ' + Version + ' \n - أبوياسين الجزائري -  \n --------------------------- \n Athan Times(مواقيت الصلاة) ...\n --------------------------- \n Aime_Jeux   ' + Date + '\n --------------------------- \nأدعوا الله تعالى أن ينفع به خلقه \n ---------------------------\nI pray to Allah to benefit from this work......\n --------------------------- '
        self['text'].setText(self.info)
        self.Vers = ''
        self.urlupdt = ''
        self.namedat = ''
        self.Versdat = ''
        self.Dateipk = ''
        self.Cond = False

    def InfosUpdat(self):
        self.info1 = '\nصبرا جميلا........\nتحميل البيانلت......\n wait........\nDownload data......'
        self['text'].setText(self.info1)
        self.UpdatALAJRETxt()

    def InfosNewsUpdat(self):
        self.info1 = '\nصبرا جميلا........\nتحميل البيانلت......\n wait........\nDownload data......'
        self['text'].setText(self.info1)
        self.timer = eTimer()
        try:
            self.timer.callback.append(self.InfosNewsUpdat_3)
        except:
            self.time_conn = self.timer.timeout.connect(self.InfosNewsUpdat_3)

        self.timer.start(100, 1)

    def InfosNewsUpdat_3(self):
        self['text'].setText(self.info)
        self.session.open(AthanTimes_NewUpdate)

    def UpdatALAJRETxt(self):
        if PY3:
        	getPage(LienUpd).addCallback(self.load_updtTxt, LienUpd)
        else:
        	getPage(LienUpd, method='GET', headers=Agent).addCallback(self.load_updtTxt, LienUpd)

    def load_updtTxt(self, data, LienUpd):
        NomFichier = 'AthanTimesUpdat.txt'
        Distnt = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/outils'
        url1 = re.findall('href="http://download(.*?)"', str(data))
        if url1:
            URL = 'http://download' + url1[0].replace("'", '')
            compat_urlretrieve(URL, os.path.join(Distnt, NomFichier))
            self.UpdatDownload()
        else:
            self['text'].setText('خطأ في الارتباط أو مشكلة في الاتصال\nحاول لاحقا ..........\nLink error or connection problem\nTry later..........')

    def UpdatDownload(self):
        self.Vers = ''
        if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/outils/AthanTimesUpdat.txt'):
            try:
                for line in open('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/outils/AthanTimesUpdat.txt'):
                    if 'Version' in line:
                        Vers = line.split('=')[1].replace('\n', '').replace('\t', '').replace(' ', '')
                        self.Vers = Vers
                    if 'Url' in line:
                        UrlVrs = line.split('=')[1].replace('\n', '').replace('\t', '').replace(' ', '')
                    if 'name' in line:
                        name = line.split('=')[1].replace('\n', '').replace('\t', '')
                    if 'Date' in line:
                        Date = line.split('=')[1].replace('\n', '').replace('\t', '')
                    if 'Download' in line:
                        Download = line.split('=')[1].replace('\n', '').replace('..', ' ').replace('\t', '')

            except:
                return

            if float(self.Vers) == float(NV):
                self['text'].setText('Greetings\nYou own the version _' + Vers + '\nUpdate_' + Date)
                self.session.open(MessageBox, 'أنت تملك النسخة _' + Vers + '\nتحديث_' + Date + '\nYou own the version _' + Vers + '\nUpdate_' + Date, type=MessageBox.TYPE_INFO, timeout=10)
                os.remove('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/outils/AthanTimesUpdat.txt')
            else:
                self.session.openWithCallback(self.userIsSure, MessageAthanTimes, _('Your Version is _ ' + NV + '\nYou want to download the new version_' + Vers + ' ?' + '\nUpdate_' + Date + '(' + Download + '(' + '\n%s' % name), MessageAthanTimes.TYPE_YESNO)
                self.urlupdt = UrlVrs
                self.namedat = name
                self.Versdat = Vers
                self.Dateipk = Date
                os.remove('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/outils/AthanTimesUpdat.txt')
        else:
            self['text'].setText('لم يتم العثور على ملف المعلومات\nحاول مرة أخرى في وقت لاحق......\nFile not found\nTry again later')
            self.session.open(MessageBox, 'لم يتم العثور على ملف المعلومات\nFile not found', type=MessageBox.TYPE_INFO, timeout=10)

    def userIsSure(self, answer):
        if answer is None:
            self.cancelWizzard()
        if answer is False:
            self.cancelWizzard()
        else:
            self['RestarEng'].show()
            self.Cond = True
            self.UpdatALAJREIPK(self.urlupdt)
        return

    def cancelWizzard(self):
        self.Cond = False
        self['text'].setText('اخترت عدم تحميل النسخة الجديدة هو اختيارك ..... \nحظا طيبا وفقك الله.......\nYou choose not to download this new version ,\nGood luck, God reward you')

    def UpdatALAJREIPK(self, url):
        if PY3:
        	getPage(url.encode('utf-8')).addCallback(self.load_updtIPK, url.encode('utf-8'))
        else:
        	getPage(url, method='GET', headers=Agent).addCallback(self.load_updtIPK, url)

    def load_updtIPK(self, data, url):
        Distnt = '/tmp'
        url1 = re.findall('href="http://download(.*?)"', str(data))
        if url1:
            self['text'].setText('تم العثور على رابط التحميل..... \nإعداد التثبيت......')
            URL = 'http://download' + url1[0]
            self.namedat
            self.prombt(URL, self.namedat)
        else:
            self['text'].setText('لا يمكن الحصول على الرابط\nخطأ في الارتباط أو مشكلة في الاتصال\nحاول لاحقا ..........\nFile not found\nTry again later')

    def prombt(self, com, dom):
        self.com = com
        self.dom = dom
        if self.com == '':
            self.session.open(MessageBox, 'لم يتم العثور على ملف المعلومات\nFile not found', type=MessageBox.TYPE_INFO, timeout=10)
        else:
            self.session.open(Console, _('downloading-installing: %s') % dom, ['opkg install -force-overwrite %s' % com])
            self['text'].setText('تهانينا قمت بتحميل فقط النسخة الجديدة \n لا تنس إعادة تشغيل IGU\nCongratulations you just downloaded the new version\nDo not forget to restart IGU')

    def StartEng(self):
        if self.Cond == False:
            pass
        else:
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('تحتاج واجهة المستخدم إلى إعادة تشغيل لتطبيق إصدار الاجر الجديد\nهل تريد اعادة تشغيل الواجهة?\nThe user interface needs to be restarted \\ nWould you like to restart the interface?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('إعادة تشغيل واجهة المستخدم الآن?\\Restart the user interface now?'))

    def restartGUI(self, answer):
        if answer is True:
            self.session.open(TryQuitMainloop, 3)
        else:
            self['text'].setText('أنت أردت عدم إعادة تشغيل الواجهة\nهذا اختيارك لكن لا تنسى اعادة تشيغلها\\You do not want to restart the interface. \\ NThis is your choice but do not forget to restart it')
            self['RestarEng'].hide()
            self.Cond
# okay decompiling /home/raed/Desktop/1.pyo
