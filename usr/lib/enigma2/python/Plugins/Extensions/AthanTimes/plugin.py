# -*- coding: utf-8 -*-
# Plugin codes for Aime_Jeux
# Update by RAED (fairbird) support py3

from Components.config import config, ConfigSubsection, ConfigSelection, getConfigListEntry, configfile, ConfigClock, NoSave
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.Pixmap import Pixmap, MovingPixmap
from Components.Label import Label
from Components.Sources.List import List
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest, MultiContentEntryPixmapAlphaBlend
from Components.Pixmap import Pixmap
from Components.ActionMap import *
from Components.Input import Input
from Components.Sources.StaticText import StaticText
from Components.AVSwitch import AVSwitch
from Components.ServiceEventTracker import ServiceEventTracker
from Components.ScrollLabel import ScrollLabel
from enigma import gFont, eTimer, eConsoleAppContainer, ePicLoad, loadPNG, loadJPG, getDesktop, eServiceReference, iPlayableService, eListboxPythonMultiContent, RT_HALIGN_LEFT, gRGB, gPixmapPtr
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.InputBox import InputBox
from Screens.Standby import TryQuitMainloop
from Screens.Screen import Screen
from Screens.InfoBar import MoviePlayer
from Screens.InfoBarGenerics import InfoBarSeek, InfoBarNotifications
from Plugins.Plugin import PluginDescriptor
from time import time
from datetime import date, datetime
import base64, time, shutil, os, time, re, io, random

from Plugins.Extensions.AthanTimes.outils.Console import Console
from Plugins.Extensions.AthanTimes.outils.Utils import *
from Plugins.Extensions.AthanTimes.outils.About import AthanTimes_About, Updat_AthanTimes
#Add By RAED for py2 & py3
from Plugins.Extensions.AthanTimes.outils.compat import compat_urlopen, compat_Request, compat_HTTPError, compat_urlretrieve, compat_urlparse, PY3
if PY3:
	from Components.config import ConfigIP
else:
	from Plugins.Extensions.AthanTimes.outils.config import ConfigIP

session = None

dwidth = getDesktop(0).size().width()
wsize = getDesktop(0).size().width()
hsize = getDesktop(0).size().height()

Agent = {'User-agent': 'Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.0.15) Gecko/2009102815 Ubuntu/9.04 (jaunty) Firefox/3.', 'Connection': 'Close'}

#UserAgent2 = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0', 'Accept': 'text/html'}
UserAgent2 = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}
AGENT = b'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
AGENT_STR = AGENT.decode('utf-8', 'ignore')
#Valeurs = '00:00'

NV = 'V3.3'
currversion = '3.3'
Version = 'AthanTimes(مواقيت الصلاة)' + ' _' + NV
Version_1 = 'prayer times for many cities_مواقيت الصلاة لعديد المدن'

config.plugins.AthanTimes = ConfigSubsection()
config.plugins.AthanTimesScreen = ConfigSubsection()
config.plugins.AthanTimesSetup = ConfigSubsection()
config.plugins.AthanTimesUpcoming = ConfigSubsection()
config.plugins.AthanTimesRefresh = ConfigSubsection()
config.plugins.AthanTimes.showplugin = ConfigSelection(default='all', choices=[('all', _('all')), ('only_plugin', _('only plugin'))])
#config.plugins.AthanTimes.SearchUpdat = ConfigSelection(default='no', choices=[('yes', _('Yes')), ('no', _('No'))])
config.plugins.AthanTimes.onlineupdate = ConfigYesNo(default=True)
config.plugins.AthanTimesScreen.Screeno = ConfigSelection(default='more', choices=[('more', _('More')), ('less', _('Less'))])
config.plugins.AthanTimes.notification = ConfigSelection(default='disabled', choices=[('disabled', _('Disabled')), ('enabled', _('Enabled'))])
config.plugins.AthanTimesSetup.flash = ConfigSelection(default='flash', choices=[('flash', _('Flash')), ('audio', _('Audio')), ('video', _('Video'))])
config.plugins.AthanTimesUpcoming.Upcoming = ConfigSelection(default='yes', choices=[('yes', _('Yes')), ('no', _('No'))])
config.plugins.AthanTimesRefresh.Refresh = ConfigSelection(default='2mn', choices=[('2mn', _('2Mn')), ('3mn', _('3Mn')), ('5mn', _('5Mn'))])
config.plugins.AthanTimes.Salat = ConfigSelection(default='no', choices=[('yes', _('Yes')), ('no', _('No'))])
config.plugins.AthanTimes.UpdatSalat = ConfigSelection(default='yes', choices=[('yes', _('Yes')), ('no', _('No'))])
config.plugins.AthanTimes.correctiontime = ConfigSelection(default = "0", choices = [
	("-3", _("-3 Hour")),
	("-2", _("-2 Hour")),
	("-1", _("-1 Hour")),
	("0", _("No Change")),
	("+1", _("+1 Hour")),
	("+2", _("+2 Hour")),
	("+3", _("+3 Hour")),
	]) # int(config.plugins.AthanTimes.correctiontime.value) * 60

##### change by RAED for py2 & 3 and more stable ...
#config.plugins.AthanTimes.fajr = ConfigIP(default=[0, 0])
#config.plugins.AthanTimes.sunrise = ConfigIP(default=[0, 0])
#config.plugins.AthanTimes.dohr = ConfigIP(default=[0, 0])
#config.plugins.AthanTimes.asr = ConfigIP(default=[0, 0])
#config.plugins.AthanTimes.maghrib = ConfigIP(default=[0, 0])
#config.plugins.AthanTimes.isha = ConfigIP(default=[0, 0])
#config.plugins.AthanTimes.UpdatSalattime = ConfigIP(default=[0, 0])
config.AthanTimes = ConfigSubsection()
### fajr
config.AthanTimes.fajr = NoSave(ConfigClock(default=0))
config.AthanTimes.fajr.value, mytmpt = ([0, 0], [0, 0])
### sunrise
config.AthanTimes.sunrise = NoSave(ConfigClock(default=0))
config.AthanTimes.sunrise.value, mytmpt = ([0, 0], [0, 0])
### dohr
config.AthanTimes.dohr = NoSave(ConfigClock(default=0))
config.AthanTimes.dohr.value, mytmpt = ([0, 0], [0, 0])
### asr
config.AthanTimes.asr = NoSave(ConfigClock(default=0))
config.AthanTimes.asr.value, mytmpt = ([0, 0], [0, 0])
### maghrib
config.AthanTimes.maghrib = NoSave(ConfigClock(default=0))
config.AthanTimes.maghrib.value, mytmpt = ([0, 0], [0, 0])
### isha
config.AthanTimes.isha = NoSave(ConfigClock(default=0))
config.AthanTimes.isha.value, mytmpt = ([0, 0], [0, 0])
### UpdatSalattime
config.AthanTimes.UpdatSalattime = NoSave(ConfigClock(default=0))
config.AthanTimes.UpdatSalattime.value, mytmpt = ([0, 0], [0, 0])
##############

logfile="/tmp/Athantimes.log"

def logdata(label='', data=None):
    try:
    	bfile=open(logfile, 'a')
    	bfile.write( str(label) + ' : ' + str(data) + "\n")
    	bfile.close()
    except:
    	pass

def trace_error():
    try:
    	traceback.print_exc(file=sys.stdout)
    	if os.path.exists(logfile):
    		pass
    	else:
    		return
    	traceback.print_exc(file=open(logfile, 'a'))
    except:
    	pass

# Add By RAED to Fix (urlopen error [SSL: CERTIFICATE_VERIFY_FAILED])
import ssl
from twisted.internet.ssl import ClientContextFactory
from twisted.internet._sslverify import ClientTLSOptions
try:
    from twisted.internet.ssl import optionsForClientTLS
except ImportError:
    optionsForClientTLS = None
from twisted.web.client import getPage, downloadPage
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

# The CRITICAL class for TLS SNI support
if PY3:
	from OpenSSL import SSL
	from zope.interface import implementer
	from twisted.internet.interfaces import IOpenSSLClientConnectionCreator

	@implementer(IOpenSSLClientConnectionCreator)
	class WebClientContextFactory(ClientContextFactory):
		def __init__(self, url=None):
			domain = compat_urlparse(url).netloc
			if isinstance(domain, bytes):
				domain = domain.decode('utf-8')
			self.hostname = domain

		def getContext(self, hostname=None, port=None):
			return ClientContextFactory.getContext(self)

		def clientConnectionForTLS(self, tlsProtocol):
			ctx = ClientContextFactory.getContext(self)
			connection = SSL.Connection(ctx, None)
			if self.hostname:
				try:
					connection.set_tlsext_host_name(self.hostname.encode('ascii'))
				except Exception:
					pass
			connection.set_app_data(tlsProtocol)
			return connection
else:
	class WebClientContextFactory(ClientContextFactory):
		def __init__(self, url=None):
			domain = compat_urlparse(url).netloc
			self.hostname = domain

		def getContext(self, hostname=None, port=None):
			ctx = ClientContextFactory.getContext(self)
			if self.hostname and ClientTLSOptions is not None:
				ClientTLSOptions(self.hostname, ctx)
			return ctx
#########################

def getColor(str):
    return gRGB(int(str[1:], 16))

def Updat_Plugin():
    lstvrs = []
    lnkvers = 'aHR0cDovL3d3dy5tZWRpYWZpcmUuY29tL2ZpbGUvdTg4ZzFuM21uODZsYXE0L2N1cnJ2ZXJzaW9uLnR4dA=='
    Link = base64.b64decode(lnkvers)
    NomFichier = 'currversion.txt'
    Distnt = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/outils'
    sniFactory = WebClientContextFactory(lnkvers)
    if PY3:
    	getPage(Link.encode('utf-8'), contextFactory=sniFactory, timeout=5,agent=AGENT)
    else:
    	getPage(Link, method='GET', contextFactory=sniFactory, headers=Agent)
    request = compat_Request(Link, None, Agent)
    data = compat_urlopen(request).read()
    url1 = re.findall('"Download file"\n.*?href="(.*?)">', data)
    URL = url1[0].replace("'", '')
    compat_urlretrieve(URL, os.path.join(Distnt, NomFichier))
    MyNewVersion = ''
    Path_version = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/outils/currversion.txt'
    if fileExists(Path_version):
        ptfile = open(Path_version, 'r')
        data = ptfile.readlines()
        ptfile.close()
        MyNewVersion = str(data[0]).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
    else:
        MyNewVersion = currversion
    return MyNewVersion

def Change_times_3(txt):
    correction = config.plugins.AthanTimes.correctiontime.value
    txt_1 = txt.split()
    First = int(txt_1[0][:2]) + int(correction)
    if len(str(First)) == 1:
    	First = str('0') + str(First)
    txt_2 = str(First) + str(txt[-6:])
    return str(txt_2)


class ScreenAthanTimesSetup(Screen, ConfigListScreen):
    if dwidth == 1280:
        skin = '''
<screen name="ScreenAthanTimesSetup" position="3,0" size="602,675" title="Prayer Times Setup" flags="wfNoBorder" backgroundColor="transparent">
<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/setup.png" position="44,551" zPosition="5" size="518,45" transparent="1" alphatest="blend" />
<widget render="Label" source="key_red" position="60,557" size="145,34" zPosition="5" valign="center" halign="center" backgroundColor="#80000000" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
<widget render="Label" source="key_green" position="413,557" size="145,34" zPosition="5" valign="center" halign="center" backgroundColor="#80000000" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
<widget name="config" position="44,138" size="518,250" itemHeight="32" scrollbarMode="showOnDemand" zPosition="4" transparent="1" backgroundColor="#80000000" foregroundColor="#999999" foregroundColorSelected="white" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/setup_fhd2.png" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/setup_fhd.png"/>
<widget render="Label" source="key_blue" position="238,557" size="145,34" zPosition="5" valign="center" halign="center" backgroundColor="#80000000" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
<eLabel text="Athan Times Setup" position="44,84" size="518,32" font="Regular; 35" halign="center" transparent="0" foregroundColor="white" backgroundColor="#011f4b" zPosition="3" />
<eLabel text="إعدادات مواقيت الصلاة" position="44,50" size="518,32" font="Regular; 30" halign="center" transparent="0" foregroundColor="white" backgroundColor="#011f4b" zPosition="3" />
<eLabel position="30,123" size="545,406" backgroundColor="#80000000" zPosition="2" />
<eLabel position="30,45" size="545,75" backgroundColor="#80000000" zPosition="2" />
<eLabel position="30,535" size="545,75" backgroundColor="#80000000" zPosition="2" />
<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/DecosSetup.png" position="40,132" zPosition="3" size="528,390" transparent="1" alphatest="blend" />
</screen>'''
    else:
        skin = '''
<screen name="ScreenAthanTimesSetup" position="3,0" size="602,775" title="Prayer Times Setup" flags="wfNoBorder" backgroundColor="transparent">
<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/setup.png" position="44,676" zPosition="5" size="518,45" transparent="1" alphatest="blend" />
<widget render="Label" source="key_red" position="60,682" size="145,34" zPosition="6" valign="center" halign="center" backgroundColor="#80000000" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
<widget render="Label" source="key_green" position="413,682" size="145,34" zPosition="6" valign="center" halign="center" backgroundColor="#80000000" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
<widget name="config" position="44,138" size="518,515" itemHeight="32" scrollbarMode="showOnDemand" zPosition="4" transparent="1" backgroundColor="#80000000" foregroundColor="#999999" foregroundColorSelected="white" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/setup_fhd2.png" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/setup_fhd.png" />
<widget render="Label" source="key_blue" position="238,682" size="145,34" zPosition="6" valign="center" halign="center" backgroundColor="#80000000" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
<eLabel text="Athan Times Setup" position="44,84" size="518,32" font="Regular; 35" halign="center" transparent="0" foregroundColor="white" backgroundColor="#011f4b" zPosition="3" />
<eLabel text="إعدادات مواقيت الصلاة" position="44,50" size="518,32" font="Regular; 30" halign="center" transparent="0" foregroundColor="white" backgroundColor="#011f4b" zPosition="3" />
<eLabel position="30,123" size="545,535" backgroundColor="#80000000" zPosition="2" />
<eLabel position="30,45" size="545,75" backgroundColor="#80000000" zPosition="2" />
<eLabel position="30,660" size="545,75" backgroundColor="#80000000" zPosition="2" />
<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/DecosSetup.png" position="40,267" zPosition="3" size="528,390" transparent="1" alphatest="blend" />
</screen>'''

    def __init__(self, session, lista):
        Screen.__init__(self, session)
        self.session = session
        self.onChangedEntry = []
        self.list = []
        ConfigListScreen.__init__(self, self.list, session=session, on_change=self.changedEntry)
        self['key_red'] = StaticText(_('Cancel'))
        self['key_green'] = StaticText(_('OK'))
        self['key_blue'] = StaticText(_(''))
        self.fajr, self.sunrise, self.dohr, self.asr, self.maghrib, self.isha = Import_times_Upadat_Salat()
        self.oldvalue = config.plugins.AthanTimes.notification.value
        self.flashvalue = config.plugins.AthanTimesSetup.flash.value
        self.Upcoming = config.plugins.AthanTimesUpcoming.Upcoming.value
        self.UpcomingRefresh = config.plugins.AthanTimesRefresh.Refresh.value
        self.Screeno = config.plugins.AthanTimesScreen.Screeno.value
        self.showplugin = config.plugins.AthanTimes.showplugin.value
        #config.plugin.AthanTimes.fajr.value = self.Verif(self.fajr)
        #config.plugin.AthanTimes.sunrise.value = self.Verif(self.sunrise)
        #config.plugin.AthanTimes.dohr.value = self.Verif(self.dohr)
        #config.plugin.AthanTimes.asr.value = self.Verif(self.asr)
        #config.plugin.AthanTimes.maghrib.value = self.Verif(self.maghrib)
        #config.plugin.AthanTimes.isha.value = self.Verif(self.isha)
        #config.plugin.AthanTimes.UpdatSalattime.value = self.Verif(config.plugin.AthanTimes.UpdatSalattime.value)
        self.lista = lista
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions'],
        	{
        		'green': self.keySave,
         		'blue': self.KeyBlue,
         		'cancel': self.keyClose,
         		'ok': self.keySave
         	}, -2)
        if self.oldvalue == 'enabled':
            self['key_blue'].setText(self.flashvalue)
        else:
            self['key_blue'].setText('.....')
        self.runSetup()

    def Verif(self, Valist):
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

    def timeSalat(self):
        if config.plugins.AthanTimes.Salat.value == 'yes':
            self.fajr = config.AthanTimes.fajr.value
            self.sunrise = config.AthanTimes.sunrise.value
            self.dohr = config.AthanTimes.dohr.value
            self.asr = config.AthanTimes.asr.value
            self.maghrib = config.AthanTimes.maghrib.value
            self.isha = config.AthanTimes.isha.value
            self.UpdatSalattime = config.AthanTimes.UpdatSalattime.value
            for x in self.lista:
                ZZZ = x[0][0] + '\n' + x[0][1]
            Prayer_txt(ZZZ, str(self.fajr[0]) + ':' + str(self.fajr[1]), str(self.sunrise[0]) + ':' + str(self.sunrise[1]), str(self.dohr[0]) + ':' + str(self.dohr[1]), str(self.asr[0]) + ':' + str(self.asr[1]), str(self.maghrib[0]) + ':' + str(self.maghrib[1]), str(self.isha[0]) + ':' + str(self.isha[1]))

    def keySave(self):
        self.timeSalat()
        for x in self['config'].list:
            x[1].save()
        configfile.save()
        if not config.plugins.AthanTimes.notification.value == self.oldvalue or not config.plugins.AthanTimesSetup.flash.value == self.flashvalue or not config.plugins.AthanTimesUpcoming.Upcoming.value == self.Upcoming or not config.plugins.AthanTimesScreen.Screeno.value == self.Screeno or not config.plugins.AthanTimes.showplugin.value == self.showplugin:
            self.session.openWithCallback(self.restartenigma, MessageBox, _('Restart enigma2 to load new settings?'), MessageBox.TYPE_YESNO)
            return
        self.session.openWithCallback(self.close, ScreenPrayerTimes_Show)
        if config.plugins.AthanTimes.UpdatSalat.value == 'yes':
            self.UpdatSalattime = config.AthanTimes.UpdatSalattime.value
            f = open('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Times.txt', 'w')
            f.write(str(self.UpdatSalattime[0]) + ':' + str(self.UpdatSalattime[1]))
            f.close()
            Replace_time_Line_Updat(str(self.UpdatSalattime[0]) + ':' + str(self.UpdatSalattime[1]))
        else:
            f = open('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Times.txt', 'w')
            f.write('vide')
            f.close()
            Replace_time_Line_Updat('')

    def keyClose(self):
        for x in self['config'].list:
            x[1].cancel()
        self.session.openWithCallback(self.close, ScreenPrayerTimes_Show)

    def restartenigma(self, result):
        if result:
            self.session.open(TryQuitMainloop, 3)
        else:
            self.session.openWithCallback(self.close, ScreenPrayerTimes_Show)

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        if config.plugins.AthanTimes.notification.value == 'enabled':
            self['key_blue'].setText(config.plugins.AthanTimesSetup.flash.value)
            self.runSetup()
        else:
            self['key_blue'].setText('.....')
            self.runSetup()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        if config.plugins.AthanTimes.notification.value == 'enabled':
            self['key_blue'].setText(config.plugins.AthanTimesSetup.flash.value)
            self.runSetup()
        else:
            self['key_blue'].setText('.....')
            self.runSetup()

    def KeyBlue(self):
        if config.plugins.AthanTimes.notification.value == 'disabled':
            self.session.open(MessageBox, 'notification not activated  لم يتم تنشيط الإشعار', MessageBox.TYPE_INFO)
        else:
            selection = config.plugins.AthanTimesSetup.flash.value
            if selection == 'flash':
                self.session.open(PrayerTimes_Flash, 'flash')
            if selection == 'audio':
                self.session.open(PrayerTimes_Flash, 'audio')
            if selection == 'video':
                self.session.open(PrayerTimes_Flash, 'video')

    def runSetup(self):
        self.list = []
        self.list.append(getConfigListEntry(_('Show_Plugin_(ظهور البلجن)'), config.plugins.AthanTimes.showplugin))
        self.list.append(getConfigListEntry(_('Notify on_off_(فتح غلق)'), config.plugins.AthanTimes.notification))
        if config.plugins.AthanTimes.notification.value == 'enabled':
            #self.list.append(getConfigListEntry(_('AutoUpdat_(تحديث تلقائي)'), config.plugins.AthanTimes.SearchUpdat))
            self.list.append(getConfigListEntry(_('AutoUpdat_(تحديث تلقائي)'), config.plugins.AthanTimes.onlineupdate))
            self.list.append(getConfigListEntry(_('Data_Screen_(شاشة البيانات)'), config.plugins.AthanTimesScreen.Screeno))
            self.list.append(getConfigListEntry(_('Choose flash_(اختر التنبيه)'), config.plugins.AthanTimesSetup.flash))
            self.list.append(getConfigListEntry(_('Upcoming Prayer(الصلاة التالية)'), config.plugins.AthanTimesUpcoming.Upcoming))
            self.list.append(getConfigListEntry(_('Correction time(تصحيح الوقت)'), config.plugins.AthanTimes.correctiontime))
            if config.plugins.AthanTimesUpcoming.Upcoming.value == 'yes':
                self.list.append(getConfigListEntry(_('Refresh time(وقت التحديث)'), config.plugins.AthanTimesRefresh.Refresh))
            self.list.append(getConfigListEntry(_('Select Times(تحديد الأوقات)'), config.plugins.AthanTimes.Salat))
            if config.plugins.AthanTimes.Salat.value == 'yes':
                self.list.append(getConfigListEntry(_('Fajr(الفجر)'), config.AthanTimes.fajr))
                self.list.append(getConfigListEntry(_('sunrise(الشروق)'), config.AthanTimes.sunrise))
                self.list.append(getConfigListEntry(_('Dhur(الظهر)'), config.AthanTimes.dohr))
                self.list.append(getConfigListEntry(_('Asr(العصر)'), config.AthanTimes.asr))
                self.list.append(getConfigListEntry(_('Maghrib(المغرب)'), config.AthanTimes.maghrib))
                self.list.append(getConfigListEntry(_('Isha(العشاء)'), config.AthanTimes.isha))
            self.list.append(getConfigListEntry(_('Updat Times(تحديث الأوقات)'), config.plugins.AthanTimes.UpdatSalat))
            if config.plugins.AthanTimes.UpdatSalat.value == 'yes':
                self.list.append(getConfigListEntry(_('Select Times(تحديد الوقت)'), config.AthanTimes.UpdatSalattime))
        self['config'].list = self.list
        self['config'].setList(self.list)

    def changedEntry(self):
        for x in self.onChangedEntry:
            x()

class PrayerTimes_Flash(Screen):
    skinfhd = '<screen name="PrayerTimes_Flash" position="0,0" size="1920,1082" title="" flags="wfNoBorder" backgroundColor="transparent"><ePixmap position="0,0" size="478,720" zPosition="5" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/plan1.png" /><widget source="global.CurrentTime" render="Label" position="4,98" size="100,27" zPosition="6" font="Regular; 20" backgroundColor="black" transparent="1" halign="left"><convert type="ClockToText">Format:%H:%M:%S</convert></widget><widget name="streamlist" zPosition="6" foregroundColorSelected="white" position="43,127" size="380,465" enableWrapAround="1" scrollbarMode="showNever" transparent="1" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry.png" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry_on.png" /><widget name="Box" position="43,595" zPosition="6" size="380,72" font="Regular;25" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget render="Label" source="key_red" position="25,736" size="130,34" zPosition="6" valign="center" halign="center" backgroundColor="#80000000" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" /><widget render="Label" source="key_blue" position="176,736" size="130,34" zPosition="6" valign="center" halign="center" backgroundColor="#80000000" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" /><widget render="Label" source="key_green" position="332,734" size="130,34" zPosition="6" valign="center" halign="center" backgroundColor="#80000000" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" /><ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/setupflash.png" position="3,730" zPosition="5" size="472,45" transparent="1" alphatest="blend" /><eLabel position="3,716" size="472,75" backgroundColor="#80000000" zPosition="2" /><widget name="Box1" position="9,672" zPosition="6" size="450,35" font="Regular;20" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="myPic" position="116,799" size="150,150" zPosition="-1" alphatest="on" transparent="0" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Flash/icons/athan0.png"/><widget name="Box2" position="495,561" zPosition="6" size="610,150" font="Regular;20" foregroundColor="white" backgroundColor="#80000000" transparent="0" halign="center" valign="center" /></screen>'
    skinhd = '<screen name="PrayerTimes_Flash" position="0,0" size="1920,1082" title="" flags="wfNoBorder" backgroundColor="transparent"><ePixmap position="0,0" size="478,720" zPosition="5" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/plan1.png" /><widget source="global.CurrentTime" render="Label" position="4,98" size="100,27" zPosition="6" font="Regular; 20" backgroundColor="black" transparent="1" halign="left"><convert type="ClockToText">Format:%H:%M:%S</convert></widget><widget name="streamlist" zPosition="6" foregroundColorSelected="white" position="43,127" size="380,465" enableWrapAround="1" scrollbarMode="showNever" transparent="1" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry.png" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry_on.png" /><widget name="Box" position="43,595" zPosition="6" size="380,72" font="Regular;25" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget render="Label" source="key_red" position="503,668" size="130,34" zPosition="6" valign="center" halign="center" backgroundColor="#80000000" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" /><widget render="Label" source="key_blue" position="658,668" size="130,34" zPosition="6" valign="center" halign="center" backgroundColor="#80000000" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" /><widget render="Label" source="key_green" position="807,668" size="130,34" zPosition="6" valign="center" halign="center" backgroundColor="#80000000" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" /><ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/setupflash.png" position="481,662" zPosition="5" size="472,45" transparent="1" alphatest="blend" /><eLabel position="481,644" size="472,75" backgroundColor="#80000000" zPosition="2" /><widget name="Box1" position="9,672" zPosition="6" size="450,35" font="Regular;20" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="myPic" position="619,487" size="150,150" zPosition="-1" alphatest="on" transparent="0" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Flash/icons/athan0.png" /></screen>'

    def __init__(self, session, namexml):
        Screen.__init__(self, session)
        if dwidth == 1280:
            self.skin = PrayerTimes_Flash.skinhd
        else:
            self.skin = PrayerTimes_Flash.skinfhd
        self['actions'] = ActionMap(['OkCancelActions',
         'ColorActions',
         'DirectionActions',
         'SetupActions',
         'MovieSelectionActions'], {'up': self.keyUp,
         'down': self.keyDown,
         'left': self.keyLeft,
         'right': self.keyRight,
         'cancel': self.End,
         'green': self.Key_Green,
         'red': self.End,
         'blue': self.Key_Blue,
         'ok': self.okbuttonClick}, -1)
        self.timer = eTimer()
        self.initialservice = session.nav.getCurrentlyPlayingServiceReference()
        self['Box'] = Label()
        self['Box1'] = Label()
        self['Box1'].setText('.............')
        self['Box2'] = Label()
        self['Box2'].setText('Your Audio File Is Empty\nملف الصوت فارغ\nyou have to download an audio file to activate the audio\nيجب تحميل ملف صوتي للتفعيل')
        self['myPic'] = Pixmap()
        self['myPic'].show()
        self.name = ''
        self.picPath = ''
        self.urlInfo = ''
        self.nameCtry = ''
        self['key_red'] = StaticText(_('Cancel'))
        self['key_green'] = StaticText(_('Play'))
        self['key_blue'] = StaticText(_('Download'))
        self.letter_list4 = []
        self.name = namexml
        if self.name == 'flash':
            self['Box'].setText('Choose Your Flash\nاختر الومضة')
            self['Box1'].setText('.............')
            self['key_green'] = StaticText(_('Test'))
            self['key_blue'] = StaticText(_('Change'))
            self['myPic'].show()
            self.Verif()
        if self.name == 'audio':
            self['Box'].setText('Choose Your Athan\nاختر الآذان')
            self['Box1'].setText('.............')
            self['myPic'].hide()
            self['key_green'] = StaticText(_('Play'))
            self['key_blue'] = StaticText(_('Download'))
            self.Verif()
        if self.name == 'video':
            self['Box'].setText('Choose Your Video\nاختر الفيديو')
            self['Box1'].setText('To record the video link Ok  لتسجيل رابط الفيديو')
            self['myPic'].hide()
            self['key_green'] = StaticText(_('Play'))
            self['key_blue'] = StaticText(_('Download'))
            self.Verif()
        self.NameXML()

    def NameXML(self):
        self.streamAthan = resolveFilename(SCOPE_PLUGINS, 'Extensions/AthanTimes/Flash/' + self.name + '.xml')
        self.streamListAthan = []
        self.makeStreamListAthan()
        self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self.streamMenuList.l.setFont(0, gFont('Regular', 20))
        self.streamMenuList.l.setFont(1, gFont('Regular', 18))
        self.streamMenuList.l.setItemHeight(31)
        self['streamlist'] = self.streamMenuList
        self.streamMenuList.setList(list(map(streamListEntry_2, self.streamListAthan)))

    def makeStreamListAthan(self):
        self.streamDBAthan = ParserAthanFlash(self.streamAthan).parseListAthanFlash()
        for x in self.streamDBAthan:
            self.streamListAthan.append((x.get('name'), x))

    def okbuttonClick(self):
        if self.name == 'audio':
            streamInfo = self['streamlist'].getCurrent()[0][1]
            self.urlInfo = streamInfo.get('url')
            self.nameAthan = streamInfo.get('name')
            self.Tilawa(self.urlInfo, self.nameAthan)
        if self.name == 'flash':
            streamInfo = self['streamlist'].getCurrent()[0][1]
            self.urlInfo = streamInfo.get('url')
            self.session.open(athantimeTestScreen, 'Athan Times  مواقيت الصلاة' + '\nok To Exit   للخروج ok', self.urlInfo)
#        if self.name == 'video':
#            streamInfo = self['streamlist'].getCurrent()[0][1]
#            self.urlInfo = streamInfo.get('url')
#            messag = Copyurlvideo(self.urlInfo)
#            self.session.open(MessageBox, messag, MessageBox.TYPE_INFO, timeout=5)
        if self.name == 'video':
            self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
            URL = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Flash/video/Adhan.mp4'
            sref = eServiceReference(4097, 0, URL)
            sref.setName('Adhan Video أذان')
            self.session.openWithCallback(self.backToIntialService, AthanTimesStreamVideo, sref)

    def Key_Green(self):
        if self.name == 'audio':
            self.okbuttonClick()
        if self.name == 'flash':
            streamInfo = self['streamlist'].getCurrent()[0][1]
            self.urlInfo = streamInfo.get('url')
            self.session.open(athantimeTestScreen, 'Athan Times  مواقيت الصلاة' + '\nok To Exit   للخروج ok', self.urlInfo)
        if self.name == 'video':
            self.UpdatALAJRETxt()

    def Key_Blue(self):
        if self.name == 'audio':
            self['Box1'].setText('Wait Download   أنتظر تحميل الملف')
            try: # Edit By RAED For DreamOS
                self.timer.callback.append(self.Key_Blue_1)
            except:
                self.time_conn = self.timer.timeout.connect(self.Key_Blue_1)
            self.timer.start(1000, True)
        if self.name == 'flash':
            streamInfo = self['streamlist'].getCurrent()[0][1]
            self.urimg = streamInfo.get('urimg')
            self.urlInfo = streamInfo.get('url')
            shutil.copy2(self.urlInfo, self.urimg)
            self.session.open(MessageBox, 'replaced file  تم استبدال الملف', MessageBox.TYPE_INFO, timeout=5)
        if self.name == 'video':
            self.session.open(MessageBox, 'The file size is large so when the video is activated it is broadcast directly from the link\nحجم الملف كبير ولهذا عند تفعيل الفيديو يتم إذاعه مباشرة من الرابط', MessageBox.TYPE_INFO, timeout=15)

    def Key_Blue_1(self):
        self.timer.stop()
        file_size = 0
        NomFichier = 'adhan.mp3'
        streamInfo = self['streamlist'].getCurrent()[0][1]
        self.urlInfo = streamInfo.get('url')
        self.audioPath = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Flash/audio/'
        try:
            compat_urlretrieve(self.urlInfo, os.path.join(self.audioPath, NomFichier))
        except Exception as e:
            print(e)
            return self.session.open(MessageBox, 'Problem withe\n' + str(e), type=MessageBox.TYPE_INFO)
        meta = os.path.getsize(self.audioPath + '/' + NomFichier)
        meta1 = float(os.stat(self.audioPath + '/' + NomFichier).st_size / 1000)
        self.session.open(MessageBox, 'Downloaded  ' + '  تم تنزيله', type=MessageBox.TYPE_INFO)
        self.NameBox()

    def NameBox(self):
        self['Box1'].setText('.............')
        if self.name == 'flash':
            self['Box'].setText('Choose Your Flash\nاختر الومضة')
        if self.name == 'audio':
            self['Box'].setText('Choose Your Athan\nاختر الآذان')
            self.Verif()

    def Tilawa(self, url, name):
        url = url
        ref = eServiceReference(4097, 0, url)
        ref.setName(name)

        self.session.openWithCallback(self.backToIntialService, AthanTimesStream, ref, 'essai')
    def backToIntialService(self, ret = None):
        self.session.nav.stopService()
        self.session.nav.playService(self.initialservice)

    def Fetch_URL(self, url):
        req = compat_Request(url)
        try:
            response = compat_urlopen(req)
            the_page = response.read()
        except compat_HTTPError as e:
            print(e.code)
            the_page = 'HTTP download ERROR: %s' % e.code
        return the_page

    def showPic(self):
        picfile = self.picPath
        picobject = self['myPic']
        picobject.instance.setPixmap(gPixmapPtr())
        self.scale = AVSwitch().getFramebufferScale()
        self.picload = ePicLoad()
        size = picobject.instance.size()
        self.picload.setPara((size.width(),
         size.height(),
         self.scale[0],
         self.scale[0],
         False,
         1,
         '#80000000'))
        if self.picload.startDecode(picfile, 0, 0, False) == 0:
            ptr = self.picload.getData()
            if ptr != None:
                picobject.instance.setPixmap(ptr)
                picobject.show()
                del self.picload
        return

    def keyUp(self):
        self['streamlist'].up()
        if self.name == 'flash':
            streamInfo = self['streamlist'].getCurrent()[0][1]
            self.picPath = streamInfo.get('url')
            self.showPic()

    def keyDown(self):
        self['streamlist'].down()
        if self.name == 'flash':
            streamInfo = self['streamlist'].getCurrent()[0][1]
            self.picPath = streamInfo.get('url')
            self.showPic()

    def keyLeft(self):
        self['streamlist'].pageUp()
        if self.name == 'flash':
            streamInfo = self['streamlist'].getCurrent()[0][1]
            self.picPath = streamInfo.get('url')
            self.showPic()

    def keyRight(self):
        self['streamlist'].pageDown()
        if self.name == 'flash':
            streamInfo = self['streamlist'].getCurrent()[0][1]
            self.picPath = streamInfo.get('url')
            self.showPic()

    def UpdatALAJRETxt(self):
        streamInfo = self['streamlist'].getCurrent()[0][1]
        LienUpd = streamInfo.get('url')
        sniFactory = WebClientContextFactory(LienUpd)
        if PY3:
        	getPage(LienUpd.encode('utf-8'), contextFactory=sniFactory, timeout=5,agent=AGENT).addCallback(self.load_updtTxt, LienUpd.encode('utf-8'))
        else:
        	getPage(LienUpd, method='GET', headers=Agent, contextFactory=sniFactory).addCallback(self.load_updtTxt, LienUpd)

    def load_updtTxt(self, data, LienUpd):
        if PY3:
        	url1 = re.findall('"Download file" .*?href="(.*?)">', data.decode('utf-8'))
        else:
        	url1 = re.findall('"Download file" .*?href="(.*?)">', data)
        if url1 != []:
            URL = url1[0]
            sref = eServiceReference(4097, 0, URL)
            sref.setName('AthanTimes مواقيت الصلاة')
            self.session.open(MoviePlayer, sref)
        else:
            self.session.open(MessageBox, 'Link error or connection problem \n' + 'خطأ في الارتباط أو مشكلة في الاتصال', type=MessageBox.TYPE_INFO)

    def Verif(self):
        if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Flash/audio/adhan.mp3'):
            self['Box2'].hide()
        else:
            self['Box2'].show()

    def End(self):
        self.close()

class ScreenPrayerTimes(Screen):
    skinfhd = '<screen name="ScreenPrayerTimes" position="0,0" size="1920,1064" title="" flags="wfNoBorder" backgroundColor="transparent"><widget name="ProgramTv" zPosition="2" foregroundColorSelected="white" position="112,66" size="402,720" enableWrapAround="1" scrollbarMode="showNever" transparent="1" /><widget name="ProgramTv2" zPosition="2" foregroundColorSelected="white" position="58,66" size="50,720" enableWrapAround="1" scrollbarMode="showNever" transparent="1" /><widget name="List" zPosition="2" foregroundColorSelected="white" position="1403,119" size="459,771" enableWrapAround="1" scrollbarMode="showNever" transparent="1" /></screen>'
    skinhd = '<screen name="ScreenPrayerTimes" position="0,0" size="1280,720" title="" flags="wfNoBorder" backgroundColor="transparent">  <widget name="ProgramTv" zPosition="1" foregroundColorSelected="white" position="6,1" size="425,480" enableWrapAround="1" scrollbarMode="showNever" transparent="0" /><widget name="List" zPosition="1" foregroundColorSelected="white" position="841,1" size="425,620" enableWrapAround="1" scrollbarMode="showNever" transparent="0" /></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        if dwidth == 1280:
            self.skin = ScreenPrayerTimes.skinhd
        else:
            self.skin = ScreenPrayerTimes.skinfhd
        self['actions'] = ActionMap(['OkCancelActions',
         'ColorActions',
         'DirectionActions',
         'SetupActions',
         'MovieSelectionActions'], {'cancel': self.End,
         'ok': self.Choice_Continent,
         'blue': self.list_iptv_2,
         'up': self.up,
         'down': self.down,
         'left': self.left,
         'right': self.right}, -1)
        self['EPGSelectActions'] = HelpableActionMap(self, 'EPGSelectActions', {'nextBouquet': self.switchList,
         'prevBouquet': self.switchList}, -1)
        self.List = []
        self.letter_list = []
        self['List'] = m2list([])
        self.ProgramTv = []
        self.letter_list2 = []
        self['ProgramTv'] = m2list([])
        self.ProgramTv2 = []
        self.letter_list3 = []
        self['ProgramTv2'] = m2list([])
        self.currentList = 'ProgramTv'
        self['ProgramTv'].selectionEnabled(0)
        self.updateTimer = eTimer()
        self.initial()
        self.letter_list4 = []
        self.Nomdujour = ''
        self.Jourdumois = ''
        self.Nomdumois = ''
        self.Annee = ''
        self.Heure = ''
        self.Minute = ''
        self.Seconde = ''
        self.Hadira = ''

    def switchList(self):
        if self.currentList == 'List':
            self['List'].selectionEnabled(1)
            self['ProgramTv'].selectionEnabled(1)
            self.currentList = 'ProgramTv'
        else:
            self['ProgramTv'].selectionEnabled(1)
            self['List'].selectionEnabled(1)
            self.currentList = 'List'

    def up(self):
        self[self.currentList].up()
        InDex = self['ProgramTv'].getSelectionIndex()
        self['ProgramTv2'].moveToIndex(InDex)
        self.updateTimer.stop()

    def down(self):
        self[self.currentList].down()
        InDex = self['ProgramTv'].getSelectionIndex()
        self['ProgramTv2'].moveToIndex(InDex)
        self.updateTimer.stop()

    def left(self):
        self[self.currentList].pageUp()
        InDex = self['ProgramTv'].getSelectionIndex()
        self['ProgramTv2'].moveToIndex(InDex)
        self.updateTimer.stop()

    def right(self):
        self[self.currentList].pageDown()
        InDex = self['ProgramTv'].getSelectionIndex()
        self['ProgramTv2'].moveToIndex(InDex)
        self.updateTimer.stop()

    def Choice_Continent(self):
        if self.currentList == 'ProgramTv':
            self.List_Contry()
        else:
            self.list_iptv()

    def List_Contry(self):
        self.letter_list = []
        Dex = self['ProgramTv'].getSelectionIndex()
        rabit = b'https://www.islamicfinder.org/world/?language=ar'
        request = compat_Request(rabit, None, UserAgent2)
        data = compat_urlopen(request).read()
        if Dex == len(self.letter_list2) - 1:
            AA = self.letter_list2[Dex][0][0]
            BB = BB = '<div class="large-4 medium-4 columns full" id="sidebar">'
        else:
            AA = self.letter_list2[Dex][0][0]
            BB = self.letter_list2[Dex + 1][0][0]
        debut = data.find('<strong>' + AA + '</strong>')
        fin = data.find('<strong>' + BB + '</strong>')
        zone = data[debut:fin]
        titreS = re.findall('<div class="large-10 medium-11 small-11 column">\n.*?<a href="(.*?)"\n.*?' + "title='(.*?)'>", zone)
        self.limita = len(titreS)
        for y in range(self.limita):
            try:
                self.letter_list.append(show_listiptv0(titreS[y][1], 'https://www.islamicfinder.org' + titreS[y][0], '', ''))
            except IndexError:
                pass

        self['List'].l.setList(self.letter_list)
        self['List'].l.setItemHeight(30)
        BVG = self['ProgramTv'].getCurrent()[0][0]
        XML_Continent(self.letter_list, BVG)
        return

    def initial(self):
        letter_list2 = []
        self.List = []
        rabit = 'https://www.islamicfinder.org/world/?language=ar'
        request = compat_Request(rabit, None, UserAgent2)
        data = compat_urlopen(request).read()
        Contn = re.findall('<h4>\n.*?<strong>(.*?)</strong>\n.*?\n.*?</h4>', data)
        self.limit = len(Contn)
        for i in range(self.limit):
            try:
                self.letter_list2.append(show_listiptv(Contn[i], Contn[i].replace(' ', '_'), '', ''))
            except IndexError:
                pass

        self['ProgramTv'].l.setList(self.letter_list2)
        self['ProgramTv'].l.setItemHeight(30)
        return

    def list_iptv(self):
        main_url = self['List'].getCurrent()[0][1]
        sniFactory = WebClientContextFactory(main_url)
        if PY3:
        	getPage(main_url.encode('utf-8'), contextFactory=sniFactory, timeout=5,agent=AGENT).addCallback(self.load_iptv, main_url.encode('utf-8'))
        else:
        	getPage(main_url, method='GET', headers=UserAgent2, contextFactory=sniFactory).addCallback(self.load_iptv, main_url)

    def load_iptv(self, data, main_url):
        self.letter_list3 = []
        Contnt = self['ProgramTv'].getCurrent()[0][0]
        Contr = self['List'].getCurrent()[0][0]
        Contry = re.findall('class="underlined"\n.*?href="(.*?)"\n.*?' + "title= '.*?'>(.*?)</a></td>", data)
        ID_Contry = re.findall('class="underlined"\n.*?href="/world/.*?/(.*?)/', data)
        self.limito = len(Contry)
        for x in range(self.limito):
            try:
                self.letter_list3.append(show_listiptv0(Contry[x][1], 'https://www.islamicfinder.org' + Contry[x][0], ID_Contry[x], ''))
            except IndexError:
                pass

        self['List'].l.setList(self.letter_list3)
        self['List'].l.setItemHeight(30)
        XML_Country(self.letter_list3, Contnt, Contr)
    def dataError(self, data):
        self.session.open(MessageBox, 'login problem try again later', MessageBox.TYPE_INFO, timeout=10)

    def list_iptv_2(self):
        main_url = self['List'].getCurrent()[0][1]
        sniFactory = WebClientContextFactory(main_url)
        try:
        	if PY3:
        		getPage(main_url.encode('utf-8'), contextFactory=sniFactory, timeout=5,agent=AGENT).addCallback(self.load_iptv_2, main_url.encode('utf-8'))
        	else:
        		getPage(main_url, method='GET', headers=UserAgent2, contextFactory=sniFactory).addCallback(self.load_iptv_2, main_url).addErrback(self.dataError)
        except:
        	print("[AthanTimes] Connection error")

    def load_iptv_2(self, data, main_url):
        urlop = main_url
        self.letter_list4 = []
        Contnt = self['ProgramTv'].getCurrent()[0][0]
        Contr = self['List'].getCurrent()[0][0]
        bilad,fajr,sunrise,dhuhr,asr,maghrib,isha,qiyam,Id,haiaa,Calc,Calcule,hijri,NextSalat,Posit = ImportDataInfos(data)
        Next = (NextSalat[0][0] + ' ' + NextSalat[0][1] + ':' + NextSalat[0][2]).replace('\n', '').replace('\t', '').replace('\r', '')
        self.Hadira = NextSalat[0][0]
        lat = Posit[0][0] if Posit else ''
        lon = Posit[0][1] if Posit else ''
        # self.session.open(MessageBox,Contnt+','+Contr+','+fajr[0]+','+sunrise[0]+','+dhuhr[0]+','+asr[0]+','+maghrib[0]+','+isha[0]+','+qiyam[0]+','+urlop+','+Id[0]+','+lat+','+lon+','+hijri+','+Calcule+','+Next+','+bilad+','+haiaa, MessageBox.TYPE_INFO)
        self.letter_list4.append(show_listiptv1(Contnt, Contr, fajr[0], sunrise[0], dhuhr[0], asr[0], maghrib[0], isha[0], qiyam[0], urlop, Id[0], lat, lon, hijri, Calcule, Next, bilad, haiaa))
        self.FAJR = 'Contnt=' + Contnt + '\nContr=' + Contr + '\nfajr=' + Change_times_3(fajr[0]) + '\nsunrise=' + Change_times_3(sunrise[0]) + '\ndhuhr=' + Change_times_3(dhuhr[0]) + '\nasr=' + Change_times_3(asr[0]) + '\nmaghrib:' + Change_times_3(maghrib[0]) + '\nisha=' + Change_times_3(isha[0]) + '\nqiyam=' + Change_times_3(qiyam[0]) + '\nurl=' + urlop + '\nId=' + Id[0] + '\nLatitude=' + lat + '\nLongitude=' + lon + '\ndate=' + hijri + '\nCalc=' + Calcule + '\nNextSalat=' + Next + '\nbilad=' + bilad + '\nhaiaa=' + haiaa + '\nsalathadira='
        self.FAJR_1 = 'Contnt=' + Contnt + '\nContr=' + Contr + '\nfajr=' + Change_times_3(fajr[0]) + '\nsunrise=' + Change_times_3(sunrise[0]) + '\ndhuhr=' + Change_times_3(dhuhr[0]) + '\nasr=' + Change_times_3(asr[0]) + '\nmaghrib:' + Change_times_3(maghrib[0]) + '\nisha=' + Change_times_3(isha[0]) + '\nqiyam=' + Change_times_3(qiyam[0]) + '\nId=' + Id[0] + '\nLatitude=' + lat + '\nLongitude=' + lon + '\ndate=' + hijri + '\nCalc=' + Calcule + '\nNextSalat=' + Next + '\nbilad=' + bilad + '\nhaiaa=' + haiaa
        Path_2 = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Choice/Choice.txt'
        os.remove(Path_2)
        outfile = open(Path_2, 'a')
        outfile.write(self.FAJR)
        outfile.close()
        XML_Choice(self.letter_list4)
        main_url = self['List'].getCurrent()[0][1]

    def Importtime(self):
        self.Nomdujour = time.strftime('%A')
        self.Jourdumois = time.strftime('%d')
        self.Nomdumois = time.strftime('%B')
        self.Annee = time.strftime('%Y')
        self.Heure = time.strftime('%H')
        self.Minute = time.strftime('%M:%S')
        self.Seconde = time.strftime('%S')

    def Importtime_1(self):
        maintenant = datetime.now()
        self.Jour = maintenant.day
        self.mois = maintenant.month
        self.Annee = maintenant.year
        self.Heure = maintenant.hour
        self.Minute = maintenant.minute
        self.Seconde = maintenant.second

    def End(self):
        self.session.openWithCallback(self.close, ScreenPrayerTimes_Show)

class ScreenPrayerTimes_Show(Screen):
    if config.plugins.AthanTimesScreen.Screeno.value == 'less':
        skinfhd = '''<screen name="ScreenPrayerTimes_Show" position="0,0" size="1920,1082" title="" flags="wfNoBorder" backgroundColor="transparent"><widget name="Box_0" position="8,938" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_3" position="1137,1025" zPosition="5" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_2" position="983,1025" zPosition="5" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_1" position="829,1025" zPosition="5" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_6" position="1602,1025" zPosition="5" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_5" position="1447,1025" zPosition="5" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_4" position="1292,1025" zPosition="5" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_7" position="1757,1025" zPosition="5" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_8" position="8,985" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_9" position="8,1033" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_10" position="405,938" zPosition="5" size="390,40" font="Regular;20" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_11" position="405,985" zPosition="5" size="390,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_12" position="1292,938" zPosition="5" size="390,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_17" position="829,938" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget source="global.CurrentTime" render="Label" position="1780,938" size="127,40" zPosition="5" font="Regular; 26" backgroundColor="#111111" transparent="0" halign="center" foregroundColor="white"><convert type="ClockToText">Format:%H:%M:%S</convert></widget><eLabel position="5,935" size="1907,140" backgroundColor="#80000000" /><eLabel text="Fajr الفجر" zPosition="5" position="829,988" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Sunrise الشروق" zPosition="5" position="983,988" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Dhur الظهر" zPosition="5" position="1137,988" size="150,35" font="Regular; 23" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Asr العصر" zPosition="5" position="1292,988" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Maghrib المغرب" zPosition="5" position="1447,988" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Isha العشاء" zPosition="5" position="1602,988" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Qiyam القيام" zPosition="5" position="1757,988" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Athan Timesمواقيت الصلاة" zPosition="5" position="405,1033" size="390,40" font="Regular; 25" transparent="0" backgroundColor="#333333" halign="center" valign="center" foregroundColor="white" /><eLabel position="5,935" size="1907,140" backgroundColor="#80000000" /><eLabel position="5,893" size="432,40" backgroundColor="#80000000" /><eLabel position="5,893" size="432,40" backgroundColor="#80000000" /><eLabel text="Exit(خروج)" zPosition="5" position="8,896" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#bf0000" halign="center" valign="center" foregroundColor="#333333" /><eLabel text="Converter Date(محول التاريخ)" zPosition="5" position="162,896" size="270,35" font="Regular; 20" transparent="0" backgroundColor="#028900" halign="center" valign="center" foregroundColor="#333333" /><eLabel text="Setup(الإعدادات)" zPosition="5" position="1485,896" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#fdfe02" halign="center" valign="center" foregroundColor="#333333" /><eLabel text="Choose city (اختر المدينة)" zPosition="5" position="1657,896" size="250,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel position="1480,893" size="432,40" backgroundColor="#80000000" /><eLabel position="1480,893" size="432,40" backgroundColor="#80000000" /><ePixmap position="2,2" size="400,100" zPosition="4" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/LOGOPlug.png" /><widget name="Box_23" position="1657,856" zPosition="5" size="250,35" font="Regular;20" foregroundColor="#777777" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_24" position="1657,817" zPosition="5" size="250,35" font="Regular;20" foregroundColor="#777777" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_25" position="1657,778" zPosition="5" size="250,35" font="Regular;20" foregroundColor="#777777" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><eLabel text=" 5.Islamic days(أيام إسلامية)" position="1657,740" size="250,35" font="Regular; 22" halign="left" transparent="0" foregroundColor="#777777" backgroundColor="#111111" zPosition="5" /><eLabel text=" 6.Weather(الطقس)" position="1657,702" size="250,35" font="Regular; 21" halign="left" transparent="0" foregroundColor="#777777" backgroundColor="#111111" zPosition="5" /><widget name="Box_27" position="877,4" zPosition="5" size="1039,100" font="Regular;26" foregroundColor="#ffbf00" backgroundColor="#111111" transparent="1" halign="center" valign="center" /></screen>'''
        skinhd = '''<screen name="ScreenPrayerTimes_Show" position="0,0" size="1280,720" title="" flags="wfNoBorder" backgroundColor="transparent"><widget name="Box_0" position="6,6" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_3" position="244,467" zPosition="5" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_2" position="6,381" zPosition="5" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_1" position="244,381" zPosition="5" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_6" position="6,552" zPosition="5" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_5" position="244,552" zPosition="5" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_4" position="6,467" zPosition="5" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_7" position="6,637" zPosition="5" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_8" position="6,49" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_9" position="6,91" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_10" position="6,133" zPosition="5" size="388,40" font="Regular;20" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_11" position="6,175" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_12" position="6,260" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_17" position="6,217" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget source="global.CurrentTime" render="Label" position="268,656" size="127,40" zPosition="5" font="Regular; 26" backgroundColor="#111111" transparent="0" halign="center" foregroundColor="white"><convert type="ClockToText">Format:%H:%M:%S</convert></widget><eLabel position="4,3" size="393,695" backgroundColor="#80000000" /><eLabel text="Fajr الفجر" zPosition="5" position="244,344" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Sunrise الشروق" zPosition="5" position="6,344" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Dhur الظهر" zPosition="5" position="244,430" size="150,35" font="Regular; 23" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Asr العصر" zPosition="5" position="6,430" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Maghrib المغرب" zPosition="5" position="244,515" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Isha العشاء" zPosition="5" position="6,515" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Qiyam القيام" zPosition="5" position="6,600" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Athan Timesمواقيت الصلاة" zPosition="5" position="6,302" size="388,40" font="Regular; 25" transparent="0" backgroundColor="#333333" halign="center" valign="center" foregroundColor="white" /><eLabel position="401,658" size="863,40" backgroundColor="#80000000" /><eLabel text="Exit(خروج)" zPosition="5" position="403,661" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#bf0000" halign="center" valign="center" foregroundColor="#333333" /><eLabel text="Converter Date(تحويل الوقت)" zPosition="5" position="563,661" size="270,35" font="Regular; 20" transparent="0" backgroundColor="#028900" halign="center" valign="center" foregroundColor="#333333" /><eLabel text="Setup(الإعدادات)" zPosition="5" position="842,661" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#fdfe02" halign="center" valign="center" foregroundColor="#333333" /><eLabel text="Choose city (اختر المدينة)" zPosition="5" position="1002,661" size="250,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel position="4,3" size="393,695" backgroundColor="#80000000" /><eLabel text="1.dates_(التاريخ)" position="401,631" size="165,25" font="Regular; 20" halign="center" transparent="0" foregroundColor="white" backgroundColor="#80000000" zPosition="5" /><eLabel text="2. List Favoris(قائمة المفضلة)" position="568,631" size="266,25" font="Regular; 20" halign="center" transparent="0" foregroundColor="white" backgroundColor="#80000000" zPosition="5" /><eLabel text="3. Update(التحديث)" position="837,631" size="197,25" font="Regular; 20" halign="left" transparent="0" foregroundColor="white" backgroundColor="#80000000" zPosition="5" /><eLabel text="4. About(عن البرنامج)" position="1037,631" size="227,25" font="Regular; 20" halign="left" transparent="0" foregroundColor="white" backgroundColor="#80000000" zPosition="5" /><eLabel text="5.Islamic days(أيام إسلامية)" position="401,604" size="228,25" font="Regular; 20" halign="left" transparent="0" foregroundColor="white" backgroundColor="#80000000" zPosition="5" /><eLabel text="6.Weather(الطقس)" position="631,604" size="228,25" font="Regular; 20" halign="left" transparent="0" foregroundColor="white" backgroundColor="#80000000" zPosition="5" /><widget name="Box_27" position="575,5" zPosition="5" size="700,85" font="Regular;19" foregroundColor="#ffbf00" backgroundColor="#111111" transparent="1" halign="center" valign="center" /></screen>'''
    if config.plugins.AthanTimesScreen.Screeno.value == 'more':
        if config.plugins.AthanTimesUpcoming.Upcoming.value == 'yes':
            skinfhd = '''<screen name="ScreenPrayerTimes_Show" position="0,0" size="1920,1082" title="" flags="wfNoBorder" backgroundColor="transparent"><widget name="Box_0" position="8,938" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="1" halign="center" valign="center" /><ePixmap position="8,938" size="388,40" zPosition="4" alphatest="blend" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/coool.png" /><widget name="Box_3" position="1137,1025" zPosition="6" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="1" halign="center" valign="center" /><widget name="Box_2" position="983,1025" zPosition="6" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="1" halign="center" valign="center" /><widget name="Box_1" position="829,1025" zPosition="6" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="1" halign="center" valign="center" /><widget name="Box_6" position="1602,1025" zPosition="6" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="1" halign="center" valign="center" /><widget name="Box_5" position="1447,1025" zPosition="6" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="1" halign="center" valign="center" /><widget name="Box_4" position="1292,1025" zPosition="6" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="1" halign="center" valign="center" /><widget name="Box_7" position="1757,1025" zPosition="6" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="1" halign="center" valign="center" /><widget name="Box_8" position="8,985" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="1" halign="center" valign="center" /><ePixmap position="8,985" size="388,40" zPosition="4" alphatest="blend" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/coool.png" /><widget name="Box_9" position="8,1033" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="1" halign="center" valign="center" /><ePixmap position="8,1033" size="388,40" zPosition="4" alphatest="blend" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/coool.png" /><widget name="Box_10" position="405,938" zPosition="5" size="390,40" font="Regular;20" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_11" position="405,985" zPosition="5" size="390,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_12" position="1292,938" zPosition="5" size="390,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_17" position="829,938" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget source="global.CurrentTime" render="Label" position="1780,938" size="127,40" zPosition="5" font="Regular; 26" backgroundColor="#111111" transparent="0" halign="center" foregroundColor="white"><convert type="ClockToText">Format:%H:%M:%S</convert></widget><eLabel position="5,935" size="1907,140" backgroundColor="#80000000" /><eLabel text="Fajr الفجر" zPosition="5" position="829,988" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Sunrise الشروق" zPosition="5" position="983,988" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Dhur الظهر" zPosition="5" position="1137,988" size="150,35" font="Regular; 23" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Asr العصر" zPosition="5" position="1292,988" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Maghrib المغرب" zPosition="5" position="1447,988" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Isha العشاء" zPosition="5" position="1602,988" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Qiyam القيام" zPosition="5" position="1757,988" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Athan Timesمواقيت الصلاة" zPosition="5" position="405,1033" size="390,40" font="Regular; 25" transparent="0" backgroundColor="#333333" halign="center" valign="center" foregroundColor="white" /><eLabel position="5,935" size="1907,140" backgroundColor="#80000000" /><eLabel position="5,893" size="432,40" backgroundColor="#80000000" /><eLabel position="5,893" size="432,40" backgroundColor="#80000000" /><eLabel text="Exit(خروج)" zPosition="5" position="8,896" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#bf0000" halign="center" valign="center" foregroundColor="#333333" /><eLabel text="Converter Date(تحويل الوقت)" zPosition="5" position="162,896" size="270,35" font="Regular; 20" transparent="0" backgroundColor="#028900" halign="center" valign="center" foregroundColor="#333333" /><eLabel text="Setup(الإعدادات)" zPosition="5" position="1485,896" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#fdfe02" halign="center" valign="center" foregroundColor="#333333" /><eLabel text="Choose city (اختر المدينة)" zPosition="5" position="1657,896" size="250,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel position="1480,893" size="432,40" backgroundColor="#80000000" /><eLabel position="1480,893" size="432,40" backgroundColor="#80000000" /><eLabel position="5,750" size="432,140" backgroundColor="#80000000" /><widget name="Box_14" position="8,858" zPosition="5" size="190,30" font="Regular;18" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_15" position="8,784" zPosition="5" size="190,30" font="Regular;20" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_16" position="244,784" zPosition="5" size="190,30" font="Regular;20" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><eLabel text="Longitude (خط الطول)" zPosition="5" position="8,752" size="190,30" font="Regular; 18" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Latitude (خط العرض)" zPosition="5" position="244,752" size="190,30" font="Regular; 18" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Id City (الرقم الاستدلالي)" zPosition="5" position="8,820" size="190,35" font="Regular; 18" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="قياسي_مالكي ,حنبلي ,شافعي" zPosition="5" position="244,820" size="190,30" font="Regular; 18" transparent="0" backgroundColor="#333333" halign="center" valign="center" foregroundColor="white" /><eLabel text="Standard (Hanbali, Maliki, Shafi)" zPosition="5" position="244,857" size="190,30" font="Regular; 16" transparent="0" backgroundColor="#333333" halign="center" valign="center" foregroundColor="white" /><eLabel position="5,750" size="432,140" backgroundColor="#80000000" /><widget name="Box_18" position="439,893" zPosition="5" size="1039,40" font="Regular;24" foregroundColor="#9afe2e" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="frame" position="250,1093" size="150,46" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/frame.png" zPosition="6" alphatest="on" transparent="1" /><widget source="global.CurrentTime" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/salat.png" position="1292,938" size="390,40" zPosition="6" alphatest="blend"><convert type="AthanTimesAlwaysTrue" /><convert type="AthanTimesConditionalShowHide">Blink</convert></widget><ePixmap position="2,2" size="400,100" zPosition="4" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/LOGOPlug.png" /><ePixmap position="829,1025" size="150,46" zPosition="5" alphatest="blend" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/frameColl.png" /><ePixmap position="983,1025" size="150,46" zPosition="5" alphatest="blend" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/frameColl.png" /><ePixmap position="1137,1025" size="150,46" zPosition="5" alphatest="blend" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/frameColl.png" /><ePixmap position="1292,1025" size="150,46" zPosition="5" alphatest="blend" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/frameColl.png" /><ePixmap position="1447,1025" size="150,46" zPosition="5" alphatest="blend" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/frameColl.png" /><ePixmap position="1602,1025" size="150,46" zPosition="5" alphatest="blend" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/frameColl.png" /><ePixmap position="1757,1025" size="150,46" zPosition="5" alphatest="blend" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/frameColl.png" /><widget name="Box_19" position="439,850" zPosition="5" size="1039,40" font="Regular;24" foregroundColor="#777777" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_20" position="439,800" zPosition="5" size="1039,40" font="Regular;24" foregroundColor="#777777" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_21" position="439,750" zPosition="5" size="1039,40" font="Regular;24" foregroundColor="#777777" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_22" position="1657,856" zPosition="5" size="250,35" font="Regular;20" foregroundColor="#777777" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_23" position="1657,819" zPosition="5" size="250,35" font="Regular;20" foregroundColor="#777777" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_24" position="1657,782" zPosition="5" size="250,35" font="Regular;20" foregroundColor="#777777" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_25" position="1657,745" zPosition="5" size="250,35" font="Regular;20" foregroundColor="#777777" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><eLabel text=" 5.Islamic days(أيام إسلامية)" position="1657,708" size="250,35" font="Regular; 22" halign="left" transparent="0" foregroundColor="#777777" backgroundColor="#111111" zPosition="5" /><eLabel text=" 6.Weather(الطقس)" position="1657,671" size="250,35" font="Regular; 21" halign="left" transparent="0" foregroundColor="#777777" backgroundColor="#111111" zPosition="5" /><widget name="Box_26" position="5,710" zPosition="5" size="432,35" font="Regular;20" foregroundColor="#777777" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_27" position="877,4" zPosition="5" size="1039,100" font="Regular;26" foregroundColor="#ffbf00" backgroundColor="#111111" transparent="1" halign="center" valign="center" /></screen>'''
            skinhd = '''<screen name="ScreenPrayerTimes_Show" position="0,0" size="1920,1082" title="" flags="wfNoBorder" backgroundColor="transparent"><widget name="Box_0" position="125,141" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_1" position="1099,614" zPosition="5" size="165,65" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_2" position="919,614" zPosition="5" size="165,65" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_3" position="739,614" zPosition="5" size="165,65" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_4" position="559,614" zPosition="5" size="165,65" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_5" position="378,614" zPosition="5" size="165,65" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_6" position="197,614" zPosition="5" size="165,65" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_7" position="16,614" zPosition="5" size="165,65" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_8" position="125,196" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_9" position="125,249" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_10" position="123,302" zPosition="5" size="390,40" font="Regular;20" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_11" position="125,357" zPosition="5" size="390,40" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_12" position="125,414" zPosition="5" size="390,40" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_13" position="124,468" zPosition="5" size="390,28" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_14" position="123,511" zPosition="5" size="97,29" font="Regular;18" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_15" position="287,511" zPosition="5" size="97,29" font="Regular;20" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_16" position="460,511" zPosition="5" size="97,29" font="Regular;20" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_17" position="123,92" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget source="session.VideoPicture" render="Pig" position="774,140" size="485,387" zPosition="5" backgroundColor="#df0b1300" /><ePixmap position="0,0" size="1280,720" zPosition="4" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/prayer.png" /><widget source="global.CurrentTime" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/salathds.png" position="118,408" size="402,50" zPosition="5" alphatest="blend"><convert type="AthanTimesAlwaysTrue" /><convert type="AthanTimesConditionalShowHide">Blink</convert></widget><widget source="global.CurrentTime" render="Label" position="833,534" size="388,30" zPosition="5" font="Regular; 26" backgroundColor="black" transparent="1" halign="center"><convert type="ClockToText">Format:%H:%M:%S</convert></widget><widget name="frame" position="1300,565" size="175,120" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/framhd.png" zPosition="5" alphatest="on" transparent="1" /><eLabel text="1.dates_(التاريخ)" position="10,687" size="235,39" font="Regular; 23" halign="left" transparent="1" foregroundColor="white" backgroundColor="#11f4b" zPosition="5" /><eLabel text="2. List Favoris(قائمة المفضلة)" position="198,687" size="380,39" font="Regular; 23" halign="left" transparent="1" foregroundColor="white" backgroundColor="#11f4b" zPosition="5" /><eLabel text="3. Update(التحديث)" position="488,687" size="260,39" font="Regular; 23" halign="left" transparent="1" foregroundColor="white" backgroundColor="#11f4b" zPosition="5" /><eLabel text="4. About(عن البرنامج)" position="686,687" size="228,39" font="Regular; 23" halign="left" transparent="1" foregroundColor="white" backgroundColor="#11f4b" zPosition="5" /><eLabel text="5.Islamic days(أيام إسلامية)" position="909,687" size="228,39" font="Regular; 22" halign="left" transparent="1" foregroundColor="white" backgroundColor="#11f4b" zPosition="5" /><eLabel text="6.Weather(الطقس)" position="1108,687" size="228,39" font="Regular; 21" halign="left" transparent="1" foregroundColor="white" backgroundColor="#11f4b" zPosition="5" /><widget name="Box_27" position="0,2" zPosition="5" size="600,50" font="Regular;18" foregroundColor="#ffbf00" backgroundColor="#111111" transparent="1" halign="center" valign="center" /></screen>'''
        else:
            skinfhd = '''<screen name="ScreenPrayerTimes_Show" position="0,0" size="1920,1082" title="" flags="wfNoBorder" backgroundColor="transparent"><widget name="Box_0" position="8,938" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_3" position="1137,1025" zPosition="6" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="1" halign="center" valign="center" /><widget name="Box_2" position="983,1025" zPosition="6" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="1" halign="center" valign="center" /><widget name="Box_1" position="829,1025" zPosition="6" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="1" halign="center" valign="center" /><widget name="Box_6" position="1602,1025" zPosition="6" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="1" halign="center" valign="center" /><widget name="Box_5" position="1447,1025" zPosition="6" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="1" halign="center" valign="center" /><widget name="Box_4" position="1292,1025" zPosition="6" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="1" halign="center" valign="center" /><widget name="Box_7" position="1757,1025" zPosition="6" size="150,46" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="1" halign="center" valign="center" /><widget name="Box_8" position="8,985" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_9" position="8,1033" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_10" position="405,938" zPosition="5" size="390,40" font="Regular;20" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_11" position="405,985" zPosition="5" size="390,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_12" position="1292,938" zPosition="5" size="390,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_17" position="829,938" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget source="global.CurrentTime" render="Label" position="1780,938" size="127,40" zPosition="5" font="Regular; 26" backgroundColor="#111111" transparent="0" halign="center" foregroundColor="white"><convert type="ClockToText">Format:%H:%M:%S</convert></widget><eLabel position="5,935" size="1907,140" backgroundColor="#80000000" /><eLabel text="Fajr الفجر" zPosition="5" position="829,988" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Sunrise الشروق" zPosition="5" position="983,988" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Dhur الظهر" zPosition="5" position="1137,988" size="150,35" font="Regular; 23" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Asr العصر" zPosition="5" position="1292,988" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Maghrib المغرب" zPosition="5" position="1447,988" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Isha العشاء" zPosition="5" position="1602,988" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Qiyam القيام" zPosition="5" position="1757,988" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Athan Timesمواقيت الصلاة" zPosition="5" position="405,1033" size="390,40" font="Regular; 25" transparent="0" backgroundColor="#333333" halign="center" valign="center" foregroundColor="white" /><eLabel position="5,935" size="1907,140" backgroundColor="#80000000" /><eLabel position="5,893" size="432,40" backgroundColor="#80000000" /><eLabel position="5,893" size="432,40" backgroundColor="#80000000" /><eLabel text="Exit(خروج)" zPosition="5" position="8,896" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#bf0000" halign="center" valign="center" foregroundColor="#333333" /><eLabel text="Converter Date(تحويل الوقت)" zPosition="5" position="162,896" size="270,35" font="Regular; 20" transparent="0" backgroundColor="#028900" halign="center" valign="center" foregroundColor="#333333" /><eLabel text="Setup(الإعدادات)" zPosition="5" position="1485,896" size="150,35" font="Regular; 20" transparent="0" backgroundColor="#fdfe02" halign="center" valign="center" foregroundColor="#333333" /><eLabel text="Choose city (اختر المدينة)" zPosition="5" position="1657,896" size="250,35" font="Regular; 20" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel position="1480,893" size="432,40" backgroundColor="#80000000" /><eLabel position="1480,893" size="432,40" backgroundColor="#80000000" /><eLabel position="5,750" size="432,140" backgroundColor="#80000000" /><widget name="Box_14" position="8,858" zPosition="5" size="190,30" font="Regular;18" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_15" position="8,784" zPosition="5" size="190,30" font="Regular;20" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_16" position="244,784" zPosition="5" size="190,30" font="Regular;20" foregroundColor="white" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><eLabel text="Longitude (خط الطول)" zPosition="5" position="8,752" size="190,30" font="Regular; 18" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Latitude (خط العرض)" zPosition="5" position="244,752" size="190,30" font="Regular; 18" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="Id City (الرقم الاستدلالي)" zPosition="5" position="8,820" size="190,35" font="Regular; 18" transparent="0" backgroundColor="#011efe" halign="center" valign="center" foregroundColor="white" /><eLabel text="قياسي_مالكي ,حنبلي ,شافعي" zPosition="5" position="244,820" size="190,30" font="Regular; 18" transparent="0" backgroundColor="#333333" halign="center" valign="center" foregroundColor="white" /><eLabel text="Standard (Hanbali, Maliki, Shafi)" zPosition="5" position="244,857" size="190,30" font="Regular; 16" transparent="0" backgroundColor="#333333" halign="center" valign="center" foregroundColor="white" /><eLabel position="5,750" size="432,140" backgroundColor="#80000000" /><widget name="Box_18" position="439,893" zPosition="5" size="1039,40" font="Regular;24" foregroundColor="#9afe2e" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="frame" position="250,1093" size="150,46" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/frame.png" zPosition="6" alphatest="on" transparent="1" /><ePixmap position="2,2" size="400,100" zPosition="4" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/LOGOPlug.png" /><ePixmap position="829,1025" size="150,46" zPosition="5" alphatest="blend" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/frameColl.png" /><ePixmap position="983,1025" size="150,46" zPosition="5" alphatest="blend" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/frameColl.png" /><ePixmap position="1137,1025" size="150,46" zPosition="5" alphatest="blend" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/frameColl.png" /><ePixmap position="1292,1025" size="150,46" zPosition="5" alphatest="blend" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/frameColl.png" /><ePixmap position="1447,1025" size="150,46" zPosition="5" alphatest="blend" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/frameColl.png" /><ePixmap position="1602,1025" size="150,46" zPosition="5" alphatest="blend" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/frameColl.png" /><ePixmap position="1757,1025" size="150,46" zPosition="5" alphatest="blend" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/frameColl.png" /><widget name="Box_23" position="1657,855" zPosition="5" size="250,35" font="Regular;20" foregroundColor="#777777" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_24" position="1657,818" zPosition="5" size="250,35" font="Regular;20" foregroundColor="#777777" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><widget name="Box_25" position="1657,781" zPosition="5" size="250,35" font="Regular;20" foregroundColor="#777777" backgroundColor="#111111" transparent="0" halign="center" valign="center" /><eLabel text=" 5.Islamic days(أيام إسلامية)" position="1657,744" size="250,35" font="Regular; 22" halign="left" transparent="0" foregroundColor="#777777" backgroundColor="#111111" zPosition="5" /><eLabel text=" 6.Weather(الطقس)" position="1657,707" size="250,35" font="Regular; 21" halign="left" transparent="0" foregroundColor="#777777" backgroundColor="#111111" zPosition="5" /><widget name="Box_27" position="877,4" zPosition="5" size="1039,100" font="Regular;26" foregroundColor="#ffbf00" backgroundColor="#111111" transparent="1" halign="center" valign="center" /></screen>'''
            skinhd = '''<screen name="ScreenPrayerTimes_Show" position="0,0" size="1920,1082" title="" flags="wfNoBorder" backgroundColor="transparent"><widget name="Box_0" position="125,141" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_1" position="1099,614" zPosition="5" size="165,65" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_2" position="919,614" zPosition="5" size="165,65" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_3" position="739,614" zPosition="5" size="165,65" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_4" position="559,614" zPosition="5" size="165,65" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_5" position="378,614" zPosition="5" size="165,65" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_6" position="197,614" zPosition="5" size="165,65" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_7" position="16,614" zPosition="5" size="165,65" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_8" position="125,196" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_9" position="125,249" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_10" position="123,302" zPosition="5" size="390,40" font="Regular;20" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_11" position="125,357" zPosition="5" size="390,40" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_12" position="125,414" zPosition="5" size="390,40" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_13" position="124,468" zPosition="5" size="390,28" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_14" position="123,511" zPosition="5" size="97,29" font="Regular;18" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_15" position="287,511" zPosition="5" size="97,29" font="Regular;20" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_16" position="460,511" zPosition="5" size="97,29" font="Regular;20" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_17" position="123,92" zPosition="5" size="388,40" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget source="session.VideoPicture" render="Pig" position="774,140" size="485,387" zPosition="5" backgroundColor="#df0b1300" /><ePixmap position="0,0" size="1280,720" zPosition="4" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/prayer.png" /><widget source="global.CurrentTime" render="Label" position="833,534" size="388,30" zPosition="5" font="Regular; 26" backgroundColor="black" transparent="1" halign="center"><convert type="ClockToText">Format:%H:%M:%S</convert></widget><eLabel text="1.dates_(التاريخ)" position="10,687" size="235,39" font="Regular; 23" halign="left" transparent="1" foregroundColor="white" backgroundColor="#11f4b" zPosition="5" /><eLabel text="2. List Favoris(قائمة المفضلة)" position="198,687" size="380,39" font="Regular; 23" halign="left" transparent="1" foregroundColor="white" backgroundColor="#11f4b" zPosition="5" /><eLabel text="3. Update(التحديث)" position="488,687" size="260,39" font="Regular; 23" halign="left" transparent="1" foregroundColor="white" backgroundColor="#11f4b" zPosition="5" /><eLabel text="4. About(عن البرنامج)" position="686,687" size="228,39" font="Regular; 23" halign="left" transparent="1" foregroundColor="white" backgroundColor="#11f4b" zPosition="5" /><eLabel text="5.Islamic days(أيام إسلامية)" position="909,687" size="228,39" font="Regular; 22" halign="left" transparent="1" foregroundColor="white" backgroundColor="#11f4b" zPosition="5" /><eLabel text="6.Weather(الطقس)" position="1108,687" size="228,39" font="Regular; 21" halign="left" transparent="1" foregroundColor="white" backgroundColor="#11f4b" zPosition="5" /><widget name="Box_27" position="0,4" zPosition="5" size="600,50" font="Regular;19" foregroundColor="#ffbf00" backgroundColor="#111111" transparent="1" halign="center" valign="center" /></screen>'''

    def __init__(self, session):
        Screen.__init__(self, session)
        if dwidth == 1280:
            self.skin = ScreenPrayerTimes_Show.skinhd
        else:
            self.skin = ScreenPrayerTimes_Show.skinfhd
        self['actions'] = ActionMap(['OkCancelActions',
         'ColorActions',
         'DirectionActions',
         'SetupActions',
         'MovieSelectionActions'], {'cancel': self.End,
         '1': self.Calendaro,
         '2': self.FAvorit,
         '3': self.Update,
         '4': self.About,
         '5': self.Ayames,
         '6': self.Weather,
         'blue': self.ChooseCity,
         'yellow': self.configPlugin,
         'green': self.Converter_Date,
         'ok': self.End}, -1)
        self.timer = eTimer()
        self.timerupdat = eTimer()
        self.Nomdujour = ''
        self.Jourdumois = ''
        self.Nomdumois = ''
        self.Annee = ''
        self.Heure = ''
        self.Minute = ''
        self.Seconde = ''
        self.Hadira = ''
        self.Had_H = ''
        self.Had_M = ''
        self.salathadira = ''
        self.Condition = ''
        self.date = ''
        self.Calendar = False
        self.Formehadira = False
        self['frame'] = MovingPixmap()
        self.letter_list4 = []
        for i in range(26):
            try:
                self['Box_' + str(i)] = Label()
            except IndexError:
                pass

        self['Box_19'].hide()
        self['Box_20'].hide()
        self['Box_21'].hide()
        self['Box_22'] = Label('1. Show dates(اظهار التاريخ)')
        self['Box_23'] = Label('2. List Favoris(قائمة المفضلة)')
        self['Box_24'] = Label('3. Update(التحديث)             ')
        self['Box_25'] = Label('4. About(عن البرنامج)          ')
        self['Box_26'] = Label('البحث عن الجديد')
        self['Box_27'] = Label('Look for the latest update of times_البحث عن آخر تحديث للأوقات')
        self.Importtime_1()
        self.updateTimer = eTimer()
        self.Vers = ''
        self.NameXML()

    def VerifVersion(self):
        messageversion = Updat_Plugin()
        if float(messageversion) == float(currversion):
            self.timerupdat.stop()
            self['Box_26'].setText('Your_Version_إصدارك_%s' % str(currversion))
        else:
            self.timerupdat.stop()
            self.session.open(Updat_AthanTimes)
            self.session.open(MessageBox, _('There_is_a_new_version_هناك إصدار جديد_%s' % str(messageversion)), MessageBox.TYPE_INFO, timeout=10)
            self['Box_26'].setText('New Version ' + str(messageversion))

    def Weather(self):
        self.session.open(MessageBox, _('معذرة .. فقد توقف دعم ياهوو لأحوال الطقس'), MessageBox.TYPE_INFO, timeout=10)
        # self.timer.stop()
        # self.timerupdat.stop()
        # streamInfo = self['streamlist'].getCurrent()[0][1]
        # city = streamInfo.get('bled')
        # self.session.openWithCallback(self.close, MeteoMain, city)

    def FAvorit(self):
        self.timer.stop()
        self.session.openWithCallback(self.close, PrayerTimes_Favoris)

    def About(self):
        self.timer.stop()
        self.timerupdat.stop()
        self.session.open(AthanTimes_About)

    def Update(self):
        self.timer.stop()
        self.timerupdat.stop()
        self.session.open(Updat_AthanTimes)

    def Ayames(self):
        self.ayamesStreamListAthan()
        ayameinfos = self.ayamestreamListAthan[0][0] + '\n' + self.ayamestreamListAthan[1][0] + '\n' + self.ayamestreamListAthan[2][0] + '\n' + self.ayamestreamListAthan[3][0] + '\n' + self.ayamestreamListAthan[4][0] + '\n' + self.ayamestreamListAthan[5][0] + '\n' + self.ayamestreamListAthan[6][0]
        self.session.open(MessageBox, str(ayameinfos), type=MessageBox.TYPE_INFO)

    def ChooseCity(self):
        self.timer.stop()
        self.timerupdat.stop()
        self.session.openWithCallback(self.close, ScreenPrayerTimes_menu)

    def configPlugin(self):
        self.timer.stop()
        self.timerupdat.stop()
        self.session.openWithCallback(self.close, ScreenAthanTimesSetup, self.letter_list4)

    def Converter_Date(self):
        self.timer.stop()
        self.timerupdat.stop()
        self.session.openWithCallback(self.close, ScreenPrayerTimes_Converter)

    def getsalat(self):
        self.Minute1 = time.strftime('%M')
        streamInfo = self['streamlist'].getCurrent()[0][1]
        uriInfo = streamInfo.get('Contnt')
        maghrib = streamInfo.get('maghrib')
        f = maghrib.split(':')[:1][0]
        g = maghrib.split(':')[1:][0].replace('AM', '').replace('PM', '')
        self.session.open(MessageBox, str(f) + '\n' + str(g) + '\n\n' + str(self.Heure) + '\n' + str(self.Minute1), type=MessageBox.TYPE_INFO)

    def NameXML(self):
        if config.plugins.AthanTimes.onlineupdate.value:
        	self.checkupdates()
        self.streamAthan = resolveFilename(SCOPE_PLUGINS, 'Extensions/AthanTimes/PrayerTimes.xml')
        self.streamListAthan = []
        self.makeStreamListAthan()
        self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self.streamMenuList.l.setFont(0, gFont('Regular', 38))
        self.streamMenuList.l.setFont(1, gFont('Regular', 18))
        self.streamMenuList.l.setItemHeight(92)
        self['streamlist'] = self.streamMenuList
        self.streamMenuList.setList(list(map(streamListEntry, self.streamListAthan)))
        self.Choice_Show()

    def NameVille(self):
        self.B = ''
        ecmf = open('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Choice/Choice.txt', 'r')
        ecm = ecmf.readlines()
        for line in ecm:
            if 'url' in line:
                self.B = line.split('=')[1]

        return self.B

    def makeStreamListAthan(self):
        dirname = os.path.dirname(self.streamAthan)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)
        if not os.path.exists(self.streamAthan) or os.path.getsize(self.streamAthan) == 0:
            xml_data = '<?xml version="1.0"?>\n<stream>\n<Choice>\n\t<Contnt>Africa</Contnt>\n\t<Contr>Algeria</Contr>\n\t<fajr>06:20 AM</fajr>\n\t<sunrise>07:48 AM</sunrise>\n\t<dhuhr>03:52 PM</dhuhr>\n\t<asr>03:52 PM</asr>\n\t<maghrib>06:14 PM</maghrib>\n\t<isha>07:37 PM</isha>\n\t<qiyam>02:18 AM</qiyam>\n\t<url>https://www.islamicfinder.org/world/Algeria/2505854/Bab%20Ezzouar-prayer-times/?language=ar</url>\n\t<Id>2505854</Id>\n\t<Lati>36.7167</Lati>\n\t<Longit>3.1833</Longit>\n\t<hijri>7 جمادى الآخرة, 1441</hijri>\n\t<clac>الفجر 18.0 درجة, العشاء 17.0 درجة, مالكي,حنبلي,شافعي </clac>\n\t<next>asr 0:45</next>\n\t<bled>bab-ezzouar</bled>\n\t<haiaa>وزارة الشؤون الدينية والأوقاف الجزائرية </haiaa>\n\t<WeatheId>1253199</WeatheId>\n</Choice>\n</stream>'
            with open(self.streamAthan, 'w', encoding='utf-8') as f:
                f.write(xml_data)
        self.streamDBAthan = StreamURIParserAthan(self.streamAthan).parseStreamListAthan()
        self.streamListAthan = []
        for x in self.streamDBAthan:
            self.streamListAthan.append((x.get('Contnt'), x))

    def Choice_Show(self):
        curr = self['streamlist'].getCurrent()
        if curr and len(curr) > 0:
            streamInfo = curr[0][1]
        else:
            streamInfo = {}

    def ayamesStreamListAthan(self):
        self.ayamestreamAthan = resolveFilename(SCOPE_PLUGINS, 'Extensions/AthanTimes/Flash/ayames.xml')
        self.ayamestreamDBAthan = ParserAthanAyames(self.ayamestreamAthan).parseListAthanAyames()
        self.ayamestreamListAthan = []
        for x in self.ayamestreamDBAthan:
            AA = x.get('name') + '_' + x.get('date1') + '_' + x.get('date2')
            self.ayamestreamListAthan.append((AA, x))

    def Choice_Show(self):
        streamInfo = self['streamlist'].getCurrent()[0][1]
        uriInfo = streamInfo.get('Contnt')
        fajr = streamInfo.get('fajr')
        fajr = self.Change(fajr)
        sunrise = streamInfo.get('sunrise')
        sunrise = self.Change(sunrise)
        dhuhr = streamInfo.get('dhuhr')
        dhuhr = self.Change(dhuhr)
        asr = streamInfo.get('asr')
        asr = self.Change(asr)
        maghrib = streamInfo.get('maghrib')
        maghrib = self.Change(maghrib)
        isha = streamInfo.get('isha')
        isha = self.Change(isha)
        Contnt = streamInfo.get('Contnt')
        bled = streamInfo.get('Contr')
        qiyam = streamInfo.get('qiyam')
        qiyam = self.Change(qiyam)
        Id = streamInfo.get('Id')
        Pos1 = streamInfo.get('Lati')
        Pos2 = streamInfo.get('Longit')
        hijri = streamInfo.get('hijri')
        clac = streamInfo.get('clac')
        Contr = streamInfo.get('bled')
        haiaa = streamInfo.get('haiaa')
        self.letter_list4.append(show_listiptv1(bled, Contr, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''))
        self['Box_0'] = Label(str(Contnt))
        fajr_1 = Import_times_Salat('fajr')
        self['Box_1'] = Label(str(fajr_1))
        sunrise_1 = Import_times_Salat('sunrise')
        self['Box_2'] = Label(str(sunrise_1))
        dhuhr_1 = Import_times_Salat('dhur')
        self['Box_3'] = Label(str(dhuhr_1))
        asr_1 = Import_times_Salat('asr')
        self['Box_4'] = Label(str(asr_1))
        maghrib_1 = Import_times_Salat('maghrib')
        self['Box_5'] = Label(str(maghrib_1))
        isha_1 = Import_times_Salat('isha')
        self['Box_6'] = Label(str(isha_1))
        self['Box_7'] = Label(str(qiyam))
        self['Box_8'] = Label(str(bled))
        self['Box_9'] = Label(str(Contr))
        self['Box_10'].setText('.......')
        self['Box_13'] = Label(str(clac))
        self['Box_14'] = Label(str(Id))
        self['Box_15'] = Label(str(Pos2))
        self['Box_16'] = Label(str(Pos1))
        self['Box_17'] = Label(str(haiaa))
        self.list_iptv_2()
        self.list_Hadira()
        #if config.plugins.AthanTimes.SearchUpdat.value == 'yes':
        #    try: # Edit By RAED For DreamOS
        #        self.timerupdat.callback.append(self.VerifVersion)
        #    except:
        #        self.timerupdat_conn = self.timer.timeout.connect(self.VerifVersion)
        #    self.timerupdat.start(10000, True)
        #else:
            #self.timerupdat.stop()
            #self['Box_26'].setText('Your_Version_إصدارك_%s' % str(currversion))
        self.timerupdat.stop()
        self['Box_26'].setText('Your_Version_إصدارك_%s' % str(currversion))
        message1, message2, message3, message4 = Import_Datetime_Updat()
        messageUpdattimes = message1 + '\nDay_' + message2 + ':' + message3 + ':' + message4 + '_يوم'
        self['Box_27'].setText(messageUpdattimes)

    def Importtime(self):
        self.Nomdujour = time.strftime('%A / %d / %Y')
        self['Box_9'] = Label(str(self.Nomdujour))

    def Importtime_1(self):
        maintenant = datetime.now()
        self.Jour = maintenant.day
        self.NameJour = maintenant.strftime('%A')
        self.NameJour = Change_TXTDay_2(self.NameJour)
        if int(self.Jour) < 10:
            self.Jour = '0' + str(self.Jour)
        else:
            self.Jour = self.Jour
        self.mois = maintenant.month
        self.Annee = maintenant.year
        self.Heure = maintenant.hour
        self.Minute = maintenant.minute
        self.Seconde = maintenant.second
        Date = str(self.NameJour) + '/' + str(self.Jour) + ' / ' + str(self.mois) + ' / ' + str(self.Annee)
        self['Box_11'] = Label(Date)

    def End(self):
        self.timer.stop()
        files = os.listdir('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Choice')
        for i in range(0, len(files)):
            os.remove('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Choice' + '/' + files[i])
        self.close()

    def list_iptv_2(self):
        self.date = ''
        streamInfo = self['streamlist'].getCurrent()[0][1]
        main_url = streamInfo.get('url')
        main_url = main_url.replace('\n', '').replace('\t', '').replace('\r', '')
        if '=ar' in str(main_url):
            main_url = main_url
        else:
            main_url = main_url + '=ar'
        sniFactory = WebClientContextFactory(main_url)
        try:
        	if PY3:
        		getPage(main_url.encode('utf-8'), contextFactory=sniFactory, timeout=5,agent=AGENT).addCallback(self.load_iptv_2, main_url.encode('utf-8'))
        	else:
        		getPage(main_url, method='GET', headers=UserAgent2, contextFactory=sniFactory).addCallback(self.load_iptv_2, main_url)
        except:
        	print("[AthanTimes] Connection error")

    def load_iptv_2(self, data, main_url):
        if PY3:
            hijri = re.findall('<p class="font-weight-bold pt-date-right">(.+?)</p>', data.decode('utf-8'))
        else:            
            hijri = re.findall('<p class="font-weight-bold pt-date-right">(.+?)</p>', data)
        if hijri != []:
            hijri = hijri[0].replace('&nbsp;', ' ')
            hijri = Change_TXT(hijri)
            self['Box_10'].setText(str(hijri))
            self.date = str(hijri)
        else:
            self['Box_10'].setText('Not Found(غير متوفرة)')

    def Contnt_1(self):
        self.B = ''
        ecmf = open('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Choice/Choice.txt', 'r')
        ecm = ecmf.readlines()
        for line in ecm:
            if 'Contnt' in line:
                self.B = line.split('=')[1]

        return self.B

    def Contr_1(self):
        self.C = ''
        ecmf = open('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Choice/Choice.txt', 'r')
        ecm = ecmf.readlines()
        for line in ecm:
            if 'Contr' in line:
                self.C = line.split('=')[1]

        return self.C

    def Change(self, txt):
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

    def Next_Salat(self, txt):
        txt_1 = txt.split(':')[:1][0]
        txt_2 = txt.split(':')[1:][0]
        return str(txt_1)

    def list_Hadira(self):
        if config.plugins.AthanTimesUpcoming.Upcoming.value == 'no':
            self['Box_12'].setText('Not activated... غير مفعلة')
            self['Box_18'].setText('Not activated... غير مفعلة')
        else:
            self.Upcoming_Salat()

    def Upcoming_Salat(self):
        self.salathadira = Upcoming_Line()
        try: # Edit By RAED For DreamOS
                self.timer.callback.append(self.set_Color_Salat)
        except:
                self.timer_conn = self.timer.timeout.connect(self.set_Color_Salat)
        self.timer.start(1500, True)

    def set_Color_Salat(self):
        self.timer.stop()
        self['Box_12'].instance.setForegroundColor(getColor('#8ae429'))
        if 'الفجر' in str(self.salathadira):
            self['Box_1'].instance.setForegroundColor(getColor('#8ae429'))
            self['Box_6'].instance.setForegroundColor(getColor('#f9f9f9'))
            if dwidth > 1280:
                self['frame'].moveTo(829, 1025, 1)
            else:
                self['frame'].moveTo(1094, 565, 1)
            self['frame'].startMoving()
            self.get_you('fajr')
        if 'الظهر' in str(self.salathadira):
            self['Box_3'].instance.setForegroundColor(getColor('#8ae429'))
            self['Box_1'].instance.setForegroundColor(getColor('#f9f9f9'))
            if dwidth > 1280:
                self['frame'].moveTo(1137, 1025, 1)
            else:
                self['frame'].moveTo(734, 565, 1)
            self['frame'].startMoving()
            self.get_you('dhuhr')
        if 'العصر' in str(self.salathadira):
            self['Box_4'].instance.setForegroundColor(getColor('#8ae429'))
            self['Box_3'].instance.setForegroundColor(getColor('#f9f9f9'))
            if dwidth > 1280:
                self['frame'].moveTo(1292, 1025, 1)
            else:
                self['frame'].moveTo(554, 565, 1)
            self['frame'].startMoving()
            self.get_you('asr')
        if 'المغرب' in str(self.salathadira):
            self['Box_5'].instance.setForegroundColor(getColor('#8ae429'))
            self['Box_4'].instance.setForegroundColor(getColor('#f9f9f9'))
            if dwidth > 1280:
                self['frame'].moveTo(1447, 1025, 1)
            else:
                self['frame'].moveTo(373, 565, 1)
            self['frame'].startMoving()
            self.get_you('maghrib')
        if 'العشاء' in str(self.salathadira):
            self['Box_6'].instance.setForegroundColor(getColor('#8ae429'))
            self['Box_5'].instance.setForegroundColor(getColor('#f9f9f9'))
            if dwidth > 1280:
                self['frame'].moveTo(1602, 1025, 1)
            else:
                self['frame'].moveTo(192, 565, 1)
            self['frame'].startMoving()
            self.get_you('isha')

    def get_move(self):
        self.Condition = Cond

    def get_you(self, Cond):
        self.Condition = Cond
        streamInfo = self['streamlist'].getCurrent()[0][1]
        Get = Import_times_Salat(Cond)
        Actuel = Change_times_1(Get)
        txt_1 = Actuel.split(':')[:1][0]
        txt_2 = Actuel.split(':')[1:][0]
        enfi = get_remaining_time(txt_1, txt_2)
        self['Box_12'].setText(str(self.salathadira) + '  ' + str(enfi) + '  (' + Cond + ')')
        self['Box_18'].setText('  _متوافق مع ساعة الجهاز_According To Your Time_' + str(self.salathadira) + ' ' + str(enfi) + ' ' + Cond)
        if config.plugins.AthanTimesUpcoming.Upcoming.value == 'yes':
            try: # Edit By RAED For DreamOS
                self.timer.callback.append(self.get_refresh)
            except:
                self.timer_conn = self.timer.timeout.connect(self.get_refresh)
            if config.plugins.AthanTimesRefresh.Refresh.value == '2mn':
                Timesrfch = 120000
            if config.plugins.AthanTimesRefresh.Refresh.value == '3mn':
                Timesrfch = 180000
            if config.plugins.AthanTimesRefresh.Refresh.value == '5mn':
                Timesrfch = 300000
            self.timer.start(Timesrfch, True)

    def get_refresh(self):
        self.timer.stop()
        self.list_Hadira()

    def Condition0(self, Npage):
        if Npage is None:
            self.cancelCondition()
        elif str(Npage) == '':
            self.cancelCondition()
        else:
            self.Day = Npage
            self.configMonth()
        return

    def configMonth(self):
        self.Month = ''
        self.session.openWithCallback(self.Condition1, InputBox, title=_('The Month(الشهر)'), windowTitle=_('AthanTimes (مواقيت الصلاة)  ' + NV), text='', maxSize=False, type=Input.NUMBER)

    def Condition1(self, Npage):
        if Npage is None:
            self.cancelCondition()
        elif str(Npage) == '':
            self.cancelCondition()
        else:
            self.Month = Npage
            self.configYear()
        return

    def configYear(self):
        self.Year = ''
        self.session.openWithCallback(self.Condition2, InputBox, title=_('The Year(السنة)'), windowTitle=_('AthanTimes (مواقيت الصلاة)  ' + NV), text='', maxSize=False, type=Input.NUMBER)

    def Condition2(self, Npage):
        if Npage is None:
            self.cancelCondition()
        elif str(Npage) == '':
            self.cancelCondition()
        else:
            self.Year = Npage
            self.convert()
        return

    def cancelCondition(self):
        pass

    def convert(self):
        urlConvert = SearchAthanConvert(self.Day, self.Month, self.Year).SearchAthanConvert_1()

    def ImportHadira(self):
        streamInfo = self['streamlist'].getCurrent()[0][1]
        GeturlHadira = streamInfo.get('url')
        sniFactory = WebClientContextFactory(GeturlHadira)
        if PY3:
        	getPage(GeturlHadira.encode('utf-8'), contextFactory=sniFactory, timeout=5,agent=AGENT).addCallback(self.load_ImportHadira, GeturlHadira.encode('utf-8'))
        else:
        	getPage(GeturlHadira, method='GET', headers=UserAgent2, contextFactory=sniFactory).addCallback(self.load_ImportHadira, GeturlHadira)

    def load_ImportHadira(self, data, main_url):
        NextSalat = re.findall('<span class="xxl uppercase margin-right">(.*?)</span> <span\n.*?class="text-light margin-left" id="clockdiv">\n.*?<div>\n.*?(.*?):(.*?):.*?\n.*?</div>', data)
        self.Hadira = (NextSalat[0][0] + ':' + NextSalat[0][1]).replace('\n', '').replace('\t', '').replace('\r', '').replace('<', '').replace('>', '')
        Next = (NextSalat[0][0] + ' ' + NextSalat[0][1] + ':' + NextSalat[0][2]).replace('\n', '').replace('\t', '').replace('\r', '')
        self.salathadira = NextSalat[0][0].replace('\n', '').replace('\t', '').replace('\r', '')
        if str(self.salathadira) != '':
            self.Formehadira = True
        else:
            self.Formehadira = False

    def Calendaro(self):
        if config.plugins.AthanTimesScreen.Screeno.value == 'more' and config.plugins.AthanTimesUpcoming.Upcoming.value == 'yes' and dwidth > 1280:
            if self.Calendar == False:
                url = 'http://v22v.net/services/calendar.html'
                request = compat_Request(url, None, Agent)
                data = compat_urlopen(request).read()
                Info2 = re.findall('<div class="FCalendar">.*?<p>(.*?)</p>.*?<ul>.*?<li>(.*?)</il>.*?<li>(.*?)</li>.*?<li>.*?(.*?).*?</li>', data.decode('utf-8'))
                Info3 = re.findall('<div class="hijrito-gregorian">.*?<label>(.*?)</label>.*?<label>(.*?)</label>.*?<span>(.*?)</span>.*?</div>.*?<div class="hijrito-gregorian">.*?<label>.*?</label>.*?<label>.*?</label>.*?<span>.*?</span>.*?</div>.*?<div class="clearfix">', data.decode('utf-8'))
                Info4 = re.findall('<div class="hijrito-gregorian">.*?<label>.*?</label>.*?<label>.*?</label>.*?<span>.*?</span>.*?</div>.*?<div class="hijrito-gregorian">.*?<label>(.*?)</label>.*?<label>(.*?)</label>.*?<span>(.*?)</span>.*?</div>.*?<div class="clearfix">', data.decode('utf-8'))
                for day, NdayH, NdayM, Sana in Info2:
                    day = Change_TXTDay(day)
                    self['Box_19'].setText(day + ' ' + NdayH + ' ' + NdayM + ' ' + Sana)

                for day1, NdayH1, NdayM1 in Info3:
                    NdayH1 = Change_TXT(NdayH1)
                    self['Box_20'].setText(day1 + ' ' + NdayH1 + ' ' + NdayM1)

                for day2, NdayH2, NdayM2 in Info4:
                    self['Box_21'].setText(day2 + ' ' + NdayH2 + ' ' + NdayM2)

                self.Calendar = True
                self['Box_19'].show()
                self['Box_20'].show()
                self['Box_21'].show()
                self['Box_22'].setText('1. Hide dates(إخفاء التأريخ)')
            else:
                self.Calendar = False
                self['Box_19'].hide()
                self['Box_20'].hide()
                self['Box_21'].hide()
                self['Box_22'].setText('1.  Show dates(إظهار التاريخ)')
        else:
            self.session.open(MessageBox, 'Reserved Screen more full hd\nخاص الصلاة التالية شاشة عالية الدقة', MessageBox.TYPE_INFO, timeout=5)
        return

    def Calendaro_Background(self):
        if dwidth > 1280:
            self['Box_19'].instance.setBackgroundColor(getColor('#555555'))
            self['Box_20'].instance.setForegroundColor(getColor('#555555'))
            self['Box_21'].instance.setBackgroundColor(getColor('#555555'))

    def checkupdates(self):
    	try:
    		from twisted.web.client import getPage, error
    		url = b'https://raw.githubusercontent.com/fairbird/Athantimes/main/installer.sh'
    		getPage(url, timeout=10).addCallback(self.parseData).addErrback(self.errBack)
    	except Exception as error:
    		trace_error()

    def errBack(self, error=None):
    	logdata("errBack-error", error)

    def parseData(self, data):
    	if PY3:
    		data = data.decode("utf-8")
    	else:
    		data = data.encode("utf-8")
    	if data:
    		lines = data.split("\n")
    		for line in lines:
    			# line=str(line)
    			if line.startswith("version"):
    				self.new_version = line.split("=")[1]
    	if float(Ver) >= float(self.new_version):
    		logdata("Updates", "No new version available")
    	else:
    		new_version = self.new_version
    		self.session.openWithCallback(self.install, MessageBox, _('New version %s is available.\n\nDo want to install now.' % new_version), MessageBox.TYPE_YESNO)

    def install(self, answer=False):
    	try:
    		if answer:
    			cmdlist = []
    			cmd = 'wget https://raw.githubusercontent.com/fairbird/Athantimes/main/installer.sh -O - | /bin/sh'
    			cmdlist.append(cmd)
    			self.session.open(Console, title='Installing last update, enigma will be started after install',
						cmdlist=cmdlist, finishedCallback=self.myCallback, closeOnSuccess=False)
    	except:
    		trace_error()

    def myCallback(self, result = None):
    	return


class ScreenPrayerTimes_menu(Screen):
    skinfhd = '''<screen name="ScreenPrayerTimes_menu" position="0,0" size="1920,1082" title="" flags="wfNoBorder" backgroundColor="transparent">
<ePixmap position="0,0" size="600,720" zPosition="4" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/plan1.png" />
<widget source="global.CurrentTime" render="Label" position="6,671" size="388,40" zPosition="5" font="Regular; 26" foregroundColor="#333333" backgroundColor="black" transparent="1" halign="left">
<convert type="ClockToText">Format:%H:%M:%S</convert>
</widget>
<widget source="streamlist" render="Listbox" backgroundColor="#333333" foregroundColor="#333333" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-select.png" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-select_on.png" position="7,120" scrollbarMode="showNever" size="542,636" transparent="1" zPosition="5" foregroundColorSelected="white">
<convert type="TemplatedMultiContent">{"template": [ MultiContentEntryText(pos = (65, 18), size = (542, 64), flags = RT_HALIGN_LEFT, text = 0) ],"fonts": [gFont("Regular", 30)],"itemHeight": 64}</convert>
</widget>
</screen>'''
    skinhd = '''<screen name="ScreenPrayerTimes_menu" position="0,0" size="1920,1082" title="" flags="wfNoBorder" backgroundColor="transparent">
<ePixmap position="0,0" size="600,720" zPosition="4" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/plan1.png" />
<widget source="global.CurrentTime" render="Label" position="6,671" size="388,40" zPosition="5" font="Regular; 26" foregroundColor="#333333" backgroundColor="black" transparent="1" halign="left">
<convert type="ClockToText">Format:%H:%M:%S</convert>
</widget>
<widget source="streamlist" render="Listbox" backgroundColor="#333333" foregroundColor="#333333" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-select.png" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-select_on.png" position="7,120" scrollbarMode="showNever" size="542,636" transparent="1" zPosition="5" foregroundColorSelected="white">
<convert type="TemplatedMultiContent">{"template": [ MultiContentEntryText(pos = (65, 18), size = (542, 64), flags = RT_HALIGN_LEFT, text = 0) ],"fonts": [gFont("Regular", 30)],"itemHeight": 64}</convert>
</widget>
</screen>'''
    def __init__(self, session):
        Screen.__init__(self, session)
        if dwidth == 1280:
            self.skin = ScreenPrayerTimes_menu.skinhd
        else:
            self.skin = ScreenPrayerTimes_menu.skinfhd
        self['actions'] = ActionMap(['OkCancelActions',
         'ColorActions',
         'DirectionActions',
         'SetupActions',
         'MovieSelectionActions'], {'cancel': self.End,
         'ok': self.okbuttonClick}, -1)
        self.updateTimer = eTimer()
        self.currentList = 'streamlist'
        self.NameXML()

    def NameXML(self):
        self.streamListAthan = []
        self.streamListAthan.append((_('Africa'), 'Africa.xml'))
        self.streamListAthan.append((_('Antarctica'), 'Antarctica.xml'))
        self.streamListAthan.append((_('Asia'), 'Asia.xml'))
        self.streamListAthan.append((_('Europe'), 'Europe.xml'))
        self.streamListAthan.append((_('North America'), 'North America.xml'))
        self.streamListAthan.append((_('Oceania'), 'Oceania.xml'))
        self.streamListAthan.append((_('South America'), 'South America.xml'))
        self['streamlist'] = List(self.streamListAthan)

    def okbuttonClick(self):
        selection = self['streamlist'].getCurrent()
        if selection is not None:
            if selection[1] == 'Africa.xml':
                self.session.open(PrayerTimes_Contry, selection[0])
            elif selection[1] == 'Antarctica.xml':
                self.session.open(PrayerTimes_Contry, selection[0])
            elif selection[1] == 'Asia.xml':
                self.session.open(PrayerTimes_Contry, selection[0])
            elif selection[1] == 'Europe.xml':
                self.session.open(PrayerTimes_Contry, selection[0])
            elif selection[1] == 'North America.xml':
                self.session.open(PrayerTimes_Contry, selection[0])
            elif selection[1] == 'Oceania.xml':
                self.session.open(PrayerTimes_Contry, selection[0])
            elif selection[1] == 'South America.xml':
                self.session.open(PrayerTimes_Contry, selection[0])
            else:
                self.session.open(MessageBox, 'Error: Could not find plugin %s\n next update ... :)' % selection[1], MessageBox.TYPE_INFO)
        return

    def End(self):
        self.session.openWithCallback(self.close, ScreenPrayerTimes_Show)


class PrayerTimes_Contry(Screen):
    skinfhd = '<screen name="PrayerTimes_Contry" position="0,0" size="1920,1082" title="" flags="wfNoBorder" backgroundColor="transparent"><ePixmap position="0,0" size="600,720" zPosition="5" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/plan1.png" /><widget source="global.CurrentTime" render="Label" position="6,671" size="388,40" zPosition="6" font="Regular; 26" backgroundColor="black" transparent="1" halign="left"><convert type="ClockToText">Format:%H:%M:%S</convert></widget><widget name="streamlist" zPosition="6" foregroundColorSelected="white" position="43,127" size="380,465" enableWrapAround="1" scrollbarMode="showNever" transparent="1" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry.png" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry_on.png" /><widget name="Box" position="43,595" zPosition="6" size="380,72" font="Regular;25" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /></screen>'
    skinhd = '<screen name="PrayerTimes_Contry" position="0,0" size="1920,1082" title="" flags="wfNoBorder" backgroundColor="transparent"><ePixmap position="0,0" size="600,720" zPosition="5" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/plan1.png" /><widget source="global.CurrentTime" render="Label" position="6,671" size="388,40" zPosition="6" font="Regular; 26" backgroundColor="black" transparent="1" halign="left"><convert type="ClockToText">Format:%H:%M:%S</convert></widget><widget name="streamlist" zPosition="6" foregroundColorSelected="white" position="43,127" size="380,465" enableWrapAround="1" scrollbarMode="showNever" transparent="1" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry.png" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry_on.png" /><widget name="Box" position="43,595" zPosition="6" size="380,72" font="Regular;25" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /></screen>'

    def __init__(self, session, fil):
        Screen.__init__(self, session)
        if dwidth == 1280:
            self.skin = PrayerTimes_Contry.skinhd
        else:
            self.skin = PrayerTimes_Contry.skinfhd
        self['actions'] = ActionMap(['OkCancelActions','ColorActions','SetupActions','MovieSelectionActions','DirectionActions'],
        	{
        		'cancel': self.End,
         		'ok': self.okbuttonClick,
			'down': self.down,
			'up': self.up
         	}, -1)
        self.updateTimer = eTimer()
        self['Box'] = Label()
        self['Box'].setText('Choose Your Country\nاختر دولتك')
        self.fil = fil
        self.urlInfo = ''
        self.nameCtry = ''
        self['List'] = m2list([])
        self.currentList = 'streamlist'
        self['streamlist'] = ScrollLabel()
        self.NameXML()

    def up(self):
        self['streamlist'].up()

    def down(self):
        self['streamlist'].down()

    def NameXML(self):
        self.streamAthan = resolveFilename(SCOPE_PLUGINS, 'Extensions/AthanTimes/PrayerTimes/' + self.fil + '/' + self.fil + '.xml')
        self.streamListAthan = []
        self.makeStreamListAthan()
        self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self.streamMenuList.l.setFont(0, gFont('Regular', 20))
        self.streamMenuList.l.setFont(1, gFont('Regular', 18))
        self.streamMenuList.l.setItemHeight(31)
        self['streamlist'] = self.streamMenuList
        self.streamMenuList.setList(list(map(streamListEntry_2, self.streamListAthan)))

    def makeStreamListAthan(self):
        self.streamDBAthan = StreamURIParserAthanmenu_1(self.streamAthan).parseStreamListAthanmenu_1()
        for x in self.streamDBAthan:
            self.streamListAthan.append((x.get('name'), x))

    def okbuttonClick(self):
        self.Free_Space()
        self['Box'].setText('Wait...\nانتظر تحميل المدن')
        streamInfo = self['streamlist'].getCurrent()[0][1]
        self.urlInfo = streamInfo.get('url')
        self.nameCtry = streamInfo.get('name')
        self.list_iptv()

    def list_iptv(self):
        main_url = self.urlInfo
        # # self.session.open(MessageBox, main_url, MessageBox.TYPE_INFO, timeout=5)
        # r = Demande.get(main_url,headers=UserAgent2)
        # data = r.text
        # self.load_iptv(data,main_url)
        # self.session.open(MessageBox, data, MessageBox.TYPE_INFO, timeout=5)
        sniFactory = WebClientContextFactory(main_url)
        if PY3:
        	getPage(main_url.encode('utf-8'), contextFactory=sniFactory, timeout=5,agent=AGENT).addCallback(self.load_iptv, main_url.encode('utf-8'))
        else:
        	getPage(main_url, method='GET', headers=UserAgent2, contextFactory=sniFactory).addCallback(self.load_iptv, main_url)
    def remove_extra_whitespace(self,string):
        string = re.sub(r'\s+', ' ', string)
        return re.sub(r'\s{2,}', ' ', string).strip()
    def load_iptv(self, data, main_url):
        self.letter_list3 = []
        Contnt = self.fil
        Contr = self.nameCtry
        if PY3:
            data = data.decode('utf-8')
        else:
            data = data
        Contry = re.findall('class="underli.+?rel="".+?href="(.+?)".+?title.+?>(.+?)</a></td>', data,re.S)
        ID_Contry = re.findall('''class="underli.+?rel="".+?href="/world/.*?/(.*?)/.*?/?language=ar"''', data,re.S)
        self.limito = len(Contry)
        for x in range(self.limito):
            try:
                href = Contry[x][0]
                name = Contry[x][1]
                name = self.remove_extra_whitespace(name)
                self.letter_list3.append(show_listiptv0('A_'+name, 'https://www.islamicfinder.org' + href, ID_Contry[x], ''))
            except IndexError:
                pass
        self['List'].l.setList(self.letter_list3)
        self['List'].l.setItemHeight(30)
        XML_Country(self.letter_list3, self.fil, self.nameCtry)
        self['Box'].setText('Choose Your Country\nاختر دولتك')
        self.session.open(PrayerTimes_Contry_City, self.nameCtry, self.fil)

    def Free_Space(self):
        for element in os.listdir('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Choice'):
            if element.endswith('.xml'):
                os.remove('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Choice/' + element)

    def End(self):
        self.close()


class PrayerTimes_Contry_City(Screen):
    skinfhd = '<screen name="PrayerTimes_Contry_City" position="0,0" size="1920,1082" title="" flags="wfNoBorder" backgroundColor="transparent"><ePixmap position="0,0" size="600,720" zPosition="5" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/plan1.png" /><widget source="global.CurrentTime" render="Label" position="4,98" size="100,27" zPosition="6" font="Regular; 20" backgroundColor="black" transparent="1" halign="left"><convert type="ClockToText">Format:%H:%M:%S</convert></widget><widget name="streamlist" zPosition="6" foregroundColorSelected="white" position="43,127" size="380,465" enableWrapAround="1" scrollbarMode="showNever" transparent="1" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry.png" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry_on.png" /><widget name="Box" position="43,595" zPosition="6" size="380,72" font="Regular;25" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><eLabel text="إذا لم تجد مدينتك استعمل الزر الأزرق" zPosition="6" position="3,665" size="471,25" font="Regular; 19" transparent="1" backgroundColor="#80000000" halign="center" foregroundColor="white" /><eLabel text="If you can not find your city, use the blue button" zPosition="6" position="3,691" size="471,25" font="Regular; 19" transparent="1" backgroundColor="#80000000" halign="center" foregroundColor="white" /></screen>'
    skinhd = '<screen name="PrayerTimes_Contry_City" position="0,0" size="1920,1082" title="" flags="wfNoBorder" backgroundColor="transparent"><ePixmap position="0,0" size="600,720" zPosition="5" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/plan1.png" /><widget source="global.CurrentTime" render="Label" position="4,98" size="100,27" zPosition="6" font="Regular; 20" backgroundColor="black" transparent="1" halign="left"><convert type="ClockToText">Format:%H:%M:%S</convert></widget><widget name="streamlist" zPosition="6" foregroundColorSelected="white" position="43,127" size="380,465" enableWrapAround="1" scrollbarMode="showNever" transparent="1" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry.png" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry_on.png" /><widget name="Box" position="43,595" zPosition="6" size="380,72" font="Regular;25" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><eLabel text="إذا لم تجد مدينتك استعمل الزر الأزرق" zPosition="6" position="3,665" size="471,25" font="Regular; 19" transparent="1" backgroundColor="#80000000" halign="center" foregroundColor="white" /><eLabel text="If you can not find your city, use the blue button" zPosition="6" position="3,691" size="471,25" font="Regular; 19" transparent="1" backgroundColor="#80000000" halign="center" foregroundColor="white" /></screen>'

    def __init__(self, session, name, Contnt):
        Screen.__init__(self, session)
        if dwidth == 1280:
            self.skin = PrayerTimes_Contry_City.skinhd
        else:
            self.skin = PrayerTimes_Contry_City.skinfhd
        self['actions'] = ActionMap(['OkCancelActions',
         'ColorActions',
         'DirectionActions',
         'SetupActions',
         'MovieSelectionActions'], {'cancel': self.End,
         'blue': self.SearchCity,
         'ok': self.okbuttonClick}, -1)
        self.updateTimer = eTimer()
        self['Box'] = Label()
        self['Box'].setText('Choose Your City\nاختر مدينتك')
        self.name = name
        self.Contnt = Contnt
        self.NameXML()

    def NameXML(self):
        self.streamAthan = resolveFilename(SCOPE_PLUGINS, 'Extensions/AthanTimes/PrayerTimes/Choice/' + self.name + '.xml')
        self.streamListAthan = []
        self.makeStreamListAthan()
        self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self.streamMenuList.l.setFont(0, gFont('Regular', 20))
        self.streamMenuList.l.setFont(1, gFont('Regular', 18))
        self.streamMenuList.l.setItemHeight(31)
        self['streamlist'] = self.streamMenuList
        self.streamMenuList.setList(list(map(streamListEntry_2, self.streamListAthan)))

    def makeStreamListAthan(self):
        self.streamDBAthan = StreamURIParserAthanmenu_1(self.streamAthan).parseStreamListAthanmenu_1()
        for x in self.streamDBAthan:
            self.streamListAthan.append((x.get('name'), x))

    def SearchCity(self):
        self.GoToPage()

    def okbuttonClick(self):
        self['Box'].setText('Wait..Download..Information\nتحميل البيانات')
        streamInfo = self['streamlist'].getCurrent()[0][1]
        self.urlInfo = streamInfo.get('url')
        self.nameCtry = streamInfo.get('name')
        self.Avant()

    def Avant(self):
        self.list_iptv_2()

    def dataError(self, data):
        self.session.open(MessageBox, 'login problem try again later', MessageBox.TYPE_INFO, timeout=10)

    def list_iptv_2(self):
        main_url = self.urlInfo
        sniFactory = WebClientContextFactory(main_url)
        try:
        	if PY3:
        		getPage(main_url.encode('utf-8'), contextFactory=sniFactory, timeout=5,agent=AGENT).addCallback(self.load_iptv_2, main_url.encode('utf-8'))
        	else:
        		getPage(main_url, method='GET', headers=UserAgent2, contextFactory=sniFactory).addCallback(self.load_iptv_2, main_url).addErrback(self.dataError)
        except:
        	print("[AthanTimes] Connection error")

    def load_iptv_2(self, data, main_url):
        data = data
        urlop = main_url
        urlop = urlop.decode('utf-8')
#        print("[DEBUG] urlop:", urlop)
#        print("[DEBUG] data len:", len(data) if data else 0)
        self.letter_list4 = []
        Contnt = self.Contnt
        Contr = self.name
        res = ImportDataInfos(data)
#        print("[DEBUG] ImportDataInfos output:", res)
        bilad,fajr,sunrise,dhuhr,asr,maghrib,isha,qiyam,Id,haiaa,Calc,Calcule,hijri,NextSalat,Posit = res
#        print("[DEBUG] bilad:", bilad)
#        print("[DEBUG] fajr:", fajr)
#        print("[DEBUG] sunrise:", sunrise)
#        print("[DEBUG] dhuhr:", dhuhr)
#        print("[DEBUG] asr:", asr)
#        print("[DEBUG] maghrib:", maghrib)
#        print("[DEBUG] isha:", isha)
#        print("[DEBUG] qiyam:", qiyam)
#        print("[DEBUG] Id:", Id)
#        print("[DEBUG] haiaa:", haiaa)
#        print("[DEBUG] Calc:", Calc)
#        print("[DEBUG] Calcule:", Calcule)
#        print("[DEBUG] hijri:", hijri)
#        print("[DEBUG] NextSalat:", NextSalat)
#        print("[DEBUG] Posit:", Posit)
        Next = (NextSalat[0][0] + ' ' + NextSalat[0][1] + ':' + NextSalat[0][2]).replace('\n', '').replace('\t', '').replace('\r', '')
        self.Hadira = NextSalat[0][0]
        lat = Posit[0][0] if Posit else ''
        lon = Posit[0][1] if Posit else ''
        # self.session.open(MessageBox,Contnt+','+Contr+','+fajr[0]+','+sunrise[0]+','+dhuhr[0]+','+asr[0]+','+maghrib[0]+','+isha[0]+','+qiyam[0]+','+urlop+','+Id[0]+','+lat+','+lon+','+hijri+','+Calcule+','+Next+','+bilad+','+haiaa, MessageBox.TYPE_INFO)
        self.letter_list4.append(show_listiptv1(Contnt, Contr, fajr[0], sunrise[0], dhuhr[0], asr[0], maghrib[0], isha[0], qiyam[0], urlop, Id[0], lat, lon, hijri, Calcule, Next, bilad, haiaa))
        self.FAJR = 'Contnt=' + Contnt + '\nContr=' + Contr + '\nfajr=' + Change_times_3(fajr[0]) + '\nsunrise=' + Change_times_3(sunrise[0]) + '\ndhuhr=' + Change_times_3(dhuhr[0]) + '\nasr=' + Change_times_3(asr[0]) + '\nmaghrib:' + Change_times_3(maghrib[0]) + '\nisha=' + Change_times_3(isha[0]) + '\nqiyam=' + Change_times_3(qiyam[0]) + '\nurl=' + urlop + '\nId=' + Id[0] + '\nLatitude=' + lat + '\nLongitude=' + lon + '\ndate=' + hijri + '\nCalc=' + Calcule + '\nNextSalat=' + Next + '\nbilad=' + bilad + '\nhaiaa=' + haiaa + '\nsalathadira='
        self.FAJR_1 = 'Contnt=' + Contnt + '\nContr=' + Contr + '\nfajr=' + Change_times_3(fajr[0]) + '\nsunrise=' + Change_times_3(sunrise[0]) + '\ndhuhr=' + Change_times_3(dhuhr[0]) + '\nasr=' + Change_times_3(asr[0]) + '\nmaghrib:' + Change_times_3(maghrib[0]) + '\nisha=' + Change_times_3(isha[0]) + '\nqiyam=' + Change_times_3(qiyam[0]) + '\nId=' + Id[0] + '\nLatitude=' + lat + '\nLongitude=' + lon + '\ndate=' + hijri + '\nCalc=' + Calcule + '\nNextSalat=' + Next + '\nbilad=' + bilad + '\nhaiaa=' + haiaa
        # AA = str(haiaa) + '\n' + str(Calc) + '\n' + str(Calcule) + '\n' + str(hijri) + '\n' + str(Next) + '\n' + str(Posit)
        Path_2 = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Choice/Choice.txt'
        Path_3 = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/ChoiceTime.txt'
        if fileExists(Path_2):
            os.remove(Path_2)
            outfile = open(Path_2, 'a')
            outfile.write(self.FAJR)
            outfile.close()
            XML_Choice(self.letter_list4)
        else:
            outfile = open(Path_2, 'a')
            outfile.write(self.FAJR)
            outfile.close()
            XML_Choice(self.letter_list4)
        os.remove(Path_3)
        if config.plugins.AthanTimes.UpdatSalat.value == 'yes':
            timeupdat = Verif_1(config.AthanTimes.UpdatSalattime.value)
            Afile = open(Path_3, 'a')
            Afile.write('Contnt=' + Contnt + '\nContr=' + Contr + '\nbilad=' + bilad + '\nUrl=' + urlop + '\ntimeupdat=' + str(timeupdat[0]) + ':' + str(timeupdat[1]))
        else:
            Afile = open(Path_3, 'a')
            Afile.write('Contnt=' + Contnt + '\nContr=' + Contr + '\nbilad=' + bilad + '\nUrl=' + urlop + '\ntimeupdat=vide')
        Afile.close()
        self['Box'].setText('Choose Your City')
        self.session.open(MessageBox, '\tAdded to favorites list(تمت اضافتها الى قائمة المفضلات)\n\t====\n\tData\n\t====\n\tالبيانات\n\t=====\n' + self.FAJR_1, MessageBox.TYPE_INFO, timeout=20)
        SearchAthanWeather(bilad, Contr).SearchWeather()

    def GoToPage(self):
        from Screens.VirtualKeyBoard import VirtualKeyBoard
        self.session.openWithCallback(self.Condition, VirtualKeyBoard, title=_("Name your city(حدد اسم مدينتك)"), text="")
        #self.session.openWithCallback(self.Condition, InputBox, title=_('Name your city(حدد اسم مدينتك)'), windowTitle=_('AthanTimes (مواقيت الصلاة)  ' + NV), text='', maxSize=False, type=Input.TEXT)

    def Condition(self, Npage):
        self.serach_list = []
        self.name = self.name.replace(' ', '%20')
        if Npage is None:
            self.cancelCondition()
        elif str(Npage) == '':
            self.cancelCondition()
        else:
            msgavert = str(Npage)
            Npage = str(Npage).replace(' ', '%20')
            A_1 = Search_idCtr(self.name.replace('%20',' '))
            A_1 = A_1.replace('\t','').replace('\n','').replace('\s','').replace('\d','')
            # self.session.open(MessageBox, self.name+'\n'+str(A_1), MessageBox.TYPE_ERROR)
            H_1 = SearchAthan(Npage, A_1).SearchAthan_1()
            if 'HTTP download ERROR' in H_1 or 'City Not Found' in H_1 or H_1 == []:
                self.GoToPage()
                self.session.open(MessageBox, 'City ' + msgavert + ' Not Found', MessageBox.TYPE_ERROR, timeout=5)
            else:
                self.serach_list = SearchAthan(Npage, A_1).SearchAthan_1()
                self.session.open(Search_City, self.serach_list, self.Contnt, self.name)
        return

    def cancelCondition(self):
        pass

    def End(self):
        self.close()


class Search_City(Screen):
    skinfhd = '<screen name="Search_City" position="0,0" size="1920,1082" title="" flags="wfNoBorder" backgroundColor="transparent"><ePixmap position="0,0" size="600,720" zPosition="5" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/plan1.png" /><widget source="global.CurrentTime" render="Label" position="6,671" size="388,40" zPosition="6" font="Regular; 26" backgroundColor="black" transparent="1" halign="left"><convert type="ClockToText">Format:%H:%M:%S</convert></widget><widget name="List" zPosition="6" foregroundColor="#999999" foregroundColorSelected="white" position="43,127" size="380,452" enableWrapAround="1" scrollbarMode="showNever" transparent="1" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry.png" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry_on.png" /><widget name="Box" position="43,595" zPosition="6" size="380,72" font="Regular;25" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /></screen>'
    skinhd = '<screen name="Search_City" position="0,0" size="1920,1082" title="" flags="wfNoBorder" backgroundColor="transparent"><ePixmap position="0,0" size="600,720" zPosition="5" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/plan1.png" /><widget source="global.CurrentTime" render="Label" position="6,671" size="388,40" zPosition="6" font="Regular; 26" backgroundColor="black" transparent="1" halign="left"><convert type="ClockToText">Format:%H:%M:%S</convert></widget><widget name="List" zPosition="6" foregroundColor="#999999" foregroundColorSelected="white" position="43,127" size="380,452" enableWrapAround="1" scrollbarMode="showNever" transparent="1" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry.png" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry_on.png"/><widget name="Box" position="43,595" zPosition="6" size="380,72" font="Regular;25" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /></screen>'

    def __init__(self, session, listo, Contnt, name):
        Screen.__init__(self, session)
        if dwidth == 1280:
            self.skin = Search_City.skinhd
        else:
            self.skin = Search_City.skinfhd
        self['actions'] = ActionMap(['OkCancelActions',
         'ColorActions',
         'DirectionActions',
         'SetupActions',
         'MovieSelectionActions'], {'cancel': self.End,
         'ok': self.GoToPage}, -1)
        self.updateTimer = eTimer()
        self.Contnt = Contnt
        self.name = name
        self['Box'] = Label()
        self['Box'].setText('Choose Your City\nاختر مدينتك')
        self['List'] = m2list([])
        self.ListSearchCityFinal = []
        for y in listo:
            self.ListSearchCityFinal.append(show_listiptv0(y[0][0], y[0][1], y[0][2], ''))

        self['List'].l.setList(self.ListSearchCityFinal)
        self['List'].l.setItemHeight(30)

    def GoToPage(self):
        self.list_iptv_2()

    def dataError(self, data):
        self.session.open(MessageBox, 'login problem try again later', MessageBox.TYPE_INFO, timeout=10)

    def list_iptv_2(self):
        self['Box'].setText('Wait..Download..Information\nتحميل البيانات')
        self.city = self['List'].getCurrent()[0][0]
        self.id = self['List'].getCurrent()[0][1]
        self.name = self.name.replace(' ', '%20')
        self.city = self.city.replace(' ', '%20')
        main_url = 'https://www.islamicfinder.org/world/' + self.name + '/' + self.id + '/' + self.city + '-prayer-times/?language=ar'
        sniFactory = WebClientContextFactory(main_url)
        try:
        	if PY3:
        		getPage(main_url.encode('utf-8'), contextFactory=sniFactory, timeout=5,agent=AGENT).addCallback(self.load_iptv_2, main_url.encode('utf-8'))
        	else:
        		getPage(main_url, method='GET', headers=UserAgent2, contextFactory=sniFactory).addCallback(self.load_iptv_2, main_url)
        except:
        	print("[AthanTimes] Connection error")

    def load_iptv_2(self, data, main_url):
        urlop = main_url
        urlop = urlop.decode('utf-8')
        self.letter_list4 = []
        Contnt = self.Contnt
        Contr = self.name
        bilad,fajr,sunrise,dhuhr,asr,maghrib,isha,qiyam,Id,haiaa,Calc,Calcule,hijri,NextSalat,Posit = ImportDataInfos(data)
        Next = (NextSalat[0][0] + ' ' + NextSalat[0][1] + ':' + NextSalat[0][2]).replace('\n', '').replace('\t', '').replace('\r', '')
        self.Hadira = NextSalat[0][0]
        lat = Posit[0][0] if Posit else ''
        lon = Posit[0][1] if Posit else ''
        # self.session.open(MessageBox,Contnt+','+Contr+','+fajr[0]+','+sunrise[0]+','+dhuhr[0]+','+asr[0]+','+maghrib[0]+','+isha[0]+','+qiyam[0]+','+urlop+','+Id[0]+','+lat+','+lon+','+hijri+','+Calcule+','+Next+','+bilad+','+haiaa, MessageBox.TYPE_INFO)
        self.letter_list4.append(show_listiptv1(Contnt, Contr, fajr[0], sunrise[0], dhuhr[0], asr[0], maghrib[0], isha[0], qiyam[0], urlop, Id[0], lat, lon, hijri, Calcule, Next, bilad, haiaa))
        self.FAJR = 'Contnt=' + Contnt + '\nContr=' + Contr + '\nfajr=' + Change_times_3(fajr[0]) + '\nsunrise=' + Change_times_3(sunrise[0]) + '\ndhuhr=' + Change_times_3(dhuhr[0]) + '\nasr=' + Change_times_3(asr[0]) + '\nmaghrib:' + Change_times_3(maghrib[0]) + '\nisha=' + Change_times_3(isha[0]) + '\nqiyam=' + Change_times_3(qiyam[0]) + '\nurl=' + urlop + '\nId=' + Id[0] + '\nLatitude=' + lat + '\nLongitude=' + lon + '\ndate=' + hijri + '\nCalc=' + Calcule + '\nNextSalat=' + Next + '\nbilad=' + bilad + '\nhaiaa=' + haiaa + '\nsalathadira='
        self.FAJR_1 = 'Contnt=' + Contnt + '\nContr=' + Contr + '\nfajr=' + Change_times_3(fajr[0]) + '\nsunrise=' + Change_times_3(sunrise[0]) + '\ndhuhr=' + Change_times_3(dhuhr[0]) + '\nasr=' + Change_times_3(asr[0]) + '\nmaghrib:' + Change_times_3(maghrib[0]) + '\nisha=' + Change_times_3(isha[0]) + '\nqiyam=' + Change_times_3(qiyam[0]) + '\nId=' + Id[0] + '\nLatitude=' + lat + '\nLongitude=' + lon + '\ndate=' + hijri + '\nCalc=' + Calcule + '\nNextSalat=' + Next + '\nbilad=' + bilad + '\nhaiaa=' + haiaa
        AA = str(haiaa) + '\n' + str(Calc) + '\n' + str(Calcule) + '\n' + str(hijri) + '\n' + str(Next) + '\n' + str(Posit)
        Path_2 = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Choice/Choice.txt'
        Path_3 = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/ChoiceTime.txt'
        if fileExists(Path_2):
            os.remove(Path_2)
            outfile = open(Path_2, 'a')
            outfile.write(self.FAJR)
            outfile.close()
            XML_Choice(self.letter_list4)
        else:
            outfile = open(Path_2, 'a')
            outfile.write(self.FAJR)
            outfile.close()
            XML_Choice(self.letter_list4)
        os.remove(Path_3)
        if config.plugins.AthanTimes.UpdatSalat.value == 'yes':
            timeupdat = Verif_1(config.AthanTimes.UpdatSalattime.value)
            Afile = open(Path_3, 'a')
            Afile.write('Contnt=' + Contnt + '\nContr=' + Contr + '\nbilad=' + bilad + '\nUrl=' + urlop + '\ntimeupdat=' + str(timeupdat[0]) + ':' + str(timeupdat[1]))
        else:
            Afile = open(Path_3, 'a')
            Afile.write('Contnt=' + Contnt + '\nContr=' + Contr + '\nbilad=' + bilad + '\nUrl=' + urlop + '\ntimeupdat=vide')
        Afile.close()
        self['Box'].setText('Choose Your City')
        self.session.open(MessageBox, '\tAdded to favorites list(تمت اضافتها الى قائمة المفضلات)\n\t====\n\tData\n\t====\n\tالبيانات\n\t=====\n' + self.FAJR_1, MessageBox.TYPE_INFO, timeout=20)
        SearchAthanWeather(self.city, self.name).SearchWeather()

    def End(self):
        self.close()

class PrayerTimes_Favoris(Screen):
    skinfhd = '<screen name="PrayerTimes_Favoris" position="0,0" size="1920,1082" title="" flags="wfNoBorder" backgroundColor="transparent"><ePixmap position="0,0" size="478,720" zPosition="5" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/plan1.png" /><widget source="global.CurrentTime" render="Label" position="3,687" size="388,31" zPosition="6" font="Regular; 26" backgroundColor="black" transparent="1" halign="left"><convert type="ClockToText">Format:%H:%M:%S</convert></widget><widget name="streamlist" zPosition="6" foregroundColorSelected="white" position="43,72" size="380,465" enableWrapAround="1" scrollbarMode="showNever" transparent="1" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry.png" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry_on.png" /><widget name="Box" position="43,539" zPosition="6" size="380,95" font="Regular;25" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><ePixmap position="10,639" size="453,45" zPosition="6" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/setupFavos.png" /><widget render="Label" source="key_red" position="18,645" size="130,34" zPosition="7" valign="center" halign="center" backgroundColor="#80000000" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" /><widget render="Label" source="key_green" position="327,645" size="130,34" zPosition="7" valign="center" halign="center" backgroundColor="#80000000" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" /><widget render="Label" source="key_blue" position="176,645" size="130,34" zPosition="7" valign="center" halign="center" backgroundColor="#80000000" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" /></screen>'
    skinhd = '<screen name="PrayerTimes_Favoris" position="0,0" size="1920,1082" title="" flags="wfNoBorder" backgroundColor="transparent"><ePixmap position="0,0" size="478,720" zPosition="5" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/plan1.png" /><widget source="global.CurrentTime" render="Label" position="3,687" size="388,31" zPosition="6" font="Regular; 26" backgroundColor="black" transparent="1" halign="left"><convert type="ClockToText">Format:%H:%M:%S</convert></widget><widget name="streamlist" zPosition="6" foregroundColorSelected="white" position="43,72" size="380,465" enableWrapAround="1" scrollbarMode="showNever" transparent="1" backgroundPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry.png" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/menu-Contry_on.png" /><widget name="Box" position="43,539" zPosition="6" size="380,95" font="Regular;25" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><ePixmap position="10,639" size="453,45" zPosition="6" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/setupFavos.png" /><widget render="Label" source="key_red" position="18,645" size="130,34" zPosition="7" valign="center" halign="center" backgroundColor="#80000000" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" /><widget render="Label" source="key_green" position="327,645" size="130,34" zPosition="7" valign="center" halign="center" backgroundColor="#80000000" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" /><widget render="Label" source="key_blue" position="176,645" size="130,34" zPosition="7" valign="center" halign="center" backgroundColor="#80000000" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" /></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        if dwidth == 1280:
            self.skin = PrayerTimes_Favoris.skinhd
        else:
            self.skin = PrayerTimes_Favoris.skinfhd
        self['actions'] = ActionMap(['OkCancelActions',
         'ColorActions',
         'DirectionActions',
         'SetupActions',
         'MovieSelectionActions'], {'cancel': self.End,
         'red': self.End,
         'blue': self.Delet_Favoris,
         'ok': self.okbuttonClick,
         'green': self.okbuttonClick,
         'down': self.down,
         'up': self.up}, -1)
        self.updateTimer = eTimer()
        self['Box'] = Label()
        self['Box'].setText('Choose Your City\nاختر مدينتك')
        self['key_red'] = StaticText(_('Cancel'))
        self['key_green'] = StaticText(_('OK'))
        self['key_blue'] = StaticText(_('Delete'))
        self.urlInfo = ''
        self.nameCtry = ''
        self.IdCtry = ''
        self.Favo = ''
        self.WeatherId = ''
        self['List'] = m2list([])
        self.currentList = 'streamlist'
        self['streamlist'] = ScrollLabel()
        self.NameXML()

    def up(self):
        self['streamlist'].up()

    def down(self):
        self['streamlist'].down()

    def NameXML(self):
        self.streamAthan = resolveFilename(SCOPE_PLUGINS, 'Extensions/AthanTimes/Flash/Favos.xml')
        self['streamlist'] = []
        self.streamListAthan = []
        self.makeStreamListAthan()
        self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self.streamMenuList.l.setFont(0, gFont('Regular', 20))
        self.streamMenuList.l.setFont(1, gFont('Regular', 18))
        self.streamMenuList.l.setItemHeight(31)
        self['streamlist'] = self.streamMenuList
        self.streamMenuList.setList(list(map(streamListEntry_2, self.streamListAthan)))
        if len(self.streamDBAthan) == 0:
            self['Box'].setText('Once you have chosen your city you will have it here\nعند اختيارك للمدينة ستجدها هنا')
        else:
            self['Box'].setText('Choose Your City\nاختر مدينتك')

    def makeStreamListAthan(self):
        self.streamDBAthan = StreamURIParserAthanmenu_2(self.streamAthan).parseStreamListAthanmenu_2()
        for x in self.streamDBAthan:
            self.streamListAthan.append(('Fav_(' + x.get('name') + ')', x))

    def Delet_Favoris(self):
        if len(self.streamDBAthan) == 0:
            self.session.open(MessageBox, 'delete what? empty list_حذف ماذا؟ قائمة فارغة', MessageBox.TYPE_INFO, timeout=20)
        else:
            streamInfo = self['streamlist'].getCurrent()[0][1]
            self.urlInfo = streamInfo.get('url')
            self.nameCtry = streamInfo.get('name')
            self.IdCtry = streamInfo.get('Id')
            Contnt = streamInfo.get('Contnt')
            Contr = streamInfo.get('Contr')
            self.Favo = '<Contry>\n\t<Contnt>' + Contnt + '</Contnt>\n' + '\t<Contr>' + Contr + '</Contr>\n' + '\t<name>' + str(self.nameCtry) + '</name>\n' + '\t<url>' + str(self.urlInfo) + '</url>\n' + '\t<Id>' + str(self.IdCtry) + '</Id>\n' + '</Contry>'
            chouf = XML_Replace_Line_1(self.Favo)
            if chouf == 'Oui':
                self.session.openWithCallback(self.userIsSure, MessageBox, _('are you sure to delete this Favoris?' + '\nهل أنت متأكد من حذف؟\n\n%s' % self.nameCtry), MessageBox.TYPE_YESNO)
            if chouf == 'Non':
                pass

    def userIsSure(self, answer):
        if answer is None:
            self.cancelWizzard()
        if answer is False:
            self.cancelWizzard()
        elif len(self.streamDBAthan) == 0:
            pass
        else:
            XML_Delet_Line_Favos(self.Favo)
            idic = self['streamlist'].getSelectionIndex()
            del self.streamListAthan[idic]
            self['streamlist'] = self.streamMenuList
            self.streamMenuList.setList(list(map(streamListEntry_2, self.streamListAthan)))
        return

    def cancelWizzard(self):
        pass

    def okbuttonClick(self):
        if len(self.streamDBAthan) == 0:
            self.session.open(MessageBox, 'Once you have chosen your city you will have it here\nعند اختيارك للمدينة ستجدها هنا', MessageBox.TYPE_INFO, timeout=20)
        else:
            self['Box'].setText('Wait..Download..Information\nتحميل البيانات')
            streamInfo = self['streamlist'].getCurrent()[0][1]
            self.urlInfo = streamInfo.get('url')
            self.nameCtry = streamInfo.get('name')
            self.Avant()

    def Avant(self):
        self.list_iptv_2()

    def dataError(self, data):
        self.session.open(MessageBox, 'login problem try again later..........', MessageBox.TYPE_INFO, timeout=10)

    def list_iptv_2(self):
        main_url = self.urlInfo
        sniFactory = WebClientContextFactory(main_url)
        try:
        	if PY3:
        		getPage(main_url.encode('utf-8'), contextFactory=sniFactory, timeout=5,agent=AGENT).addCallback(self.load_iptv_2, main_url.encode('utf-8'))
        	else:
        		getPage(main_url, method='GET', headers=UserAgent2, contextFactory=sniFactory).addCallback(self.load_iptv_2, main_url).addErrback(self.dataError)
        except:
        	print("[AthanTimes] Connection error")

    def load_iptv_2(self, data, main_url):
        urlop = main_url
        timeupdat = ''
        self.letter_list4 = []
        streamInfo = self['streamlist'].getCurrent()[0][1]
        Contnt = streamInfo.get('Contnt')
        Contr = streamInfo.get('Contr')
        bilad,fajr,sunrise,dhuhr,asr,maghrib,isha,qiyam,Id,haiaa,Calc,Calcule,hijri,NextSalat,Posit = ImportDataInfos(data)
        Next = (NextSalat[0][0] + ' ' + NextSalat[0][1] + ':' + NextSalat[0][2]).replace('\n', '').replace('\t', '').replace('\r', '')
        self.Hadira = NextSalat[0][0]
        lat = Posit[0][0] if Posit else ''
        lon = Posit[0][1] if Posit else ''
        # self.session.open(MessageBox,Contnt+','+Contr+','+fajr[0]+','+sunrise[0]+','+dhuhr[0]+','+asr[0]+','+maghrib[0]+','+isha[0]+','+qiyam[0]+','+urlop+','+Id[0]+','+lat+','+lon+','+hijri+','+Calcule+','+Next+','+bilad+','+haiaa, MessageBox.TYPE_INFO)
        self.letter_list4.append(show_listiptv1(Contnt, Contr, fajr[0], sunrise[0], dhuhr[0], asr[0], maghrib[0], isha[0], qiyam[0], urlop, Id[0], lat, lon, hijri, Calcule, Next, bilad, haiaa))
        self.FAJR = 'Contnt=' + Contnt + '\nContr=' + Contr + '\nfajr=' + Change_times_3(fajr[0]) + '\nsunrise=' + Change_times_3(sunrise[0]) + '\ndhuhr=' + Change_times_3(dhuhr[0]) + '\nasr=' + Change_times_3(asr[0]) + '\nmaghrib:' + Change_times_3(maghrib[0]) + '\nisha=' + Change_times_3(isha[0]) + '\nqiyam=' + Change_times_3(qiyam[0]) + '\nurl=' + urlop + '\nId=' + Id[0] + '\nLatitude=' + lat + '\nLongitude=' + lon + '\ndate=' + hijri + '\nCalc=' + Calcule + '\nNextSalat=' + Next + '\nbilad=' + bilad + '\nhaiaa=' + haiaa + '\nsalathadira='
        self.FAJR_1 = 'Contnt=' + Contnt + '\nContr=' + Contr + '\nfajr=' + Change_times_3(fajr[0]) + '\nsunrise=' + Change_times_3(sunrise[0]) + '\ndhuhr=' + Change_times_3(dhuhr[0]) + '\nasr=' + Change_times_3(asr[0]) + '\nmaghrib:' + Change_times_3(maghrib[0]) + '\nisha=' + Change_times_3(isha[0]) + '\nqiyam=' + Change_times_3(qiyam[0]) + '\nId=' + Id[0] + '\nLatitude=' + lat + '\nLongitude=' + lon + '\ndate=' + hijri + '\nCalc=' + Calcule + '\nNextSalat=' + Next + '\nbilad=' + bilad + '\nhaiaa=' + haiaa
        AA = str(haiaa) + '\n' + str(Calc) + '\n' + str(Calcule) + '\n' + str(hijri) + '\n' + str(Next) + '\n' + str(Posit)
        Path_2 = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Choice/Choice.txt'
        Path_3 = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/ChoiceTime.txt'
        if fileExists(Path_2):
            os.remove(Path_2)
            outfile = open(Path_2, 'a')
            outfile.write(self.FAJR)
            outfile.close()
            XML_Choice(self.letter_list4)
        else:
            outfile = open(Path_2, 'a')
            outfile.write(self.FAJR)
            outfile.close()
            XML_Choice(self.letter_list4)
        os.remove(Path_3)
        if config.plugins.AthanTimes.UpdatSalat.value == 'yes':
            timeupdat = Verif_1(config.AthanTimes.UpdatSalattime.value)
            Afile = open(Path_3, 'a')
            Afile.write('Contnt=' + Contnt + '\nContr=' + Contr + '\nbilad=' + bilad + '\nUrl=' + urlop + '\ntimeupdat=' + str(timeupdat[0]) + ':' + str(timeupdat[1]))
        else:
            Afile = open(Path_3, 'a')
            Afile.write('Contnt=' + Contnt + '\nContr=' + Contr + '\nbilad=' + bilad + '\nUrl=' + urlop + '\ntimeupdat=vide')
        Afile.close()
        self['Box'].setText('Choose Your City\nاختر مدينتك')
        self.session.open(MessageBox, '\tData\n\t====\n\tالبيانات\n\t=====\n' + self.FAJR_1, MessageBox.TYPE_INFO, timeout=20)
        SearchAthanWeather(bilad, Contr).SearchWeather()

    def End(self):
        self.session.openWithCallback(self.close, ScreenPrayerTimes_Show)


class ScreenPrayerTimes_Converter(Screen):
    skinfhd = '<screen name="ScreenPrayerTimes_Converter" position="350,0" size="1280,720" title="" flags="wfNoBorder" backgroundColor="transparent"><widget name="Box_0" position="456,342" zPosition="5" size="319,40" font="Regular;24" foregroundColor="#adff00" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_1" position="360,431" zPosition="5" size="512,42" font="Regular;20" foregroundColor="#adff00" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget source="global.CurrentTime" render="Label" position="761,305" size="120,30" zPosition="5" font="Regular; 24" backgroundColor="black" transparent="1" halign="left" foregroundColor="white"><convert type="ClockToText">Format:%H:%M:%S</convert></widget><ePixmap position="342,251" size="547,343" zPosition="4" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/converter.png" /><widget name="Box_4" position="356,305" zPosition="5" size="160,30" font="Regular;20" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="left" valign="center" /></screen>'
    skinhd = '<screen name="ScreenPrayerTimes_Converter" position="0,0" size="1280,720" title="" flags="wfNoBorder" backgroundColor="transparent"><widget name="Box_0" position="456,342" zPosition="5" size="320,40" font="Regular;24" foregroundColor="#adff00" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget name="Box_1" position="356,425" zPosition="5" size="516,51" font="Regular;20" foregroundColor="#adff00" backgroundColor="#80000000" transparent="1" halign="center" valign="center" /><widget source="global.CurrentTime" render="Label" position="761,305" size="120,30" zPosition="5" font="Regular; 24" backgroundColor="black" transparent="1" halign="left" foregroundColor="white"><convert type="ClockToText">Format:%H:%M:%S</convert></widget><ePixmap position="342,251" size="547,343" zPosition="4" alphatest="on" transparent="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/converter.png" /><widget name="Box_4" position="356,305" zPosition="5" size="150,30" font="Regular;20" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="left" valign="center" /></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        if dwidth == 1280:
            self.skin = ScreenPrayerTimes_Converter.skinhd
        else:
            self.skin = ScreenPrayerTimes_Converter.skinfhd
        self['actions'] = ActionMap(['OkCancelActions','ColorActions','DirectionActions','SetupActions','MovieSelectionActions'],
        	{
        		'cancel': self.keyClose,
         		'blue': self.configDay,
         		'ok': self.keyClose,
         	}, -1)
        self.Day = ''
        self.Month = ''
        self.Year = ''
        for i in range(5):
            try:
                self['Box_' + str(i)] = Label()
            except IndexError:
                pass

        self['Box_2'].setText('هناك احتمال صغير من الخطأ بيوم واحد')
        self['Box_3'].setText('There is a small probability of error one day')
        self.Importtime()

    def configDay(self):
        self.Day = ''
        self.session.openWithCallback(self.Condition0, InputBox, title=_('The Day(اليوم)'), windowTitle=_('AthanTimes (مواقيت الصلاة)  ' + NV), text='', maxSize=False, type=Input.NUMBER)

    def Condition0(self, Npage):
        if Npage is None:
            self.cancelCondition()
        elif str(Npage) == '':
            self.cancelCondition()
        elif int(Npage) > 31:
            self.configDay()
            self.session.open(MessageBox, 'The Day =' + str(Npage) + '?!!!', MessageBox.TYPE_INFO, timeout=20)
        else:
            self.Day = Npage
            self.configMonth()
        return

    def configMonth(self):
        self.Month = ''
        self.session.openWithCallback(self.Condition1, InputBox, title=_('The Month(الشهر)'), windowTitle=_('AthanTimes (مواقيت الصلاة)  ' + NV), text='', maxSize=False, type=Input.NUMBER)

    def Condition1(self, Npage):
        if Npage is None:
            self.cancelCondition()
        elif str(Npage) == '':
            self.cancelCondition()
        elif int(Npage) > 12:
            self.configMonth()
            self.session.open(MessageBox, 'The Month =' + str(Npage) + '?!!!', MessageBox.TYPE_INFO, timeout=20)
        else:
            self.Month = Npage
            self.configYear()
        return

    def configYear(self):
        self.Year = ''
        self.session.openWithCallback(self.Condition2, InputBox, title=_('The Year(السنة)'), windowTitle=_('AthanTimes (مواقيت الصلاة)  ' + NV), text='', maxSize=False, type=Input.NUMBER)

    def Condition2(self, Npage):
        if Npage is None:
            self.cancelCondition()
        elif str(Npage) == '':
            self.cancelCondition()
        else:
            self.Year = Npage
            self.convert()
        return

    def cancelCondition(self):
        pass

    def convert(self):
        urlConvert = SearchAthanConvert(self.Day, self.Month, self.Year).SearchAthanConvert_1()
        self['Box_0'].setText(str(self.Day) + '/' + str(self.Month) + '/' + str(self.Year))
        self['Box_1'].setText(str(urlConvert))

    def Importtime(self):
        maintenant = datetime.now()
        self.Jour = maintenant.day
        if int(self.Jour) < 10:
            self.Jour = '0' + str(self.Jour)
        else:
            self.Jour = self.Jour
        self.mois = maintenant.month
        self.Annee = maintenant.year
        self.Heure = maintenant.hour
        self.Minute = maintenant.minute
        self.Seconde = maintenant.second
        Date = str(self.Jour) + ' / ' + str(self.mois) + ' / ' + str(self.Annee)
        self['Box_4'].setText(Date)
        self.convert_1(self.Jour, self.mois, self.Annee)

    def convert_1(self, Jour, mois, Annee):
        urlConvert = SearchAthanConvert(str(Jour), str(mois), str(Annee)).SearchAthanConvert_1()
        self['Box_0'].setText(str(Jour) + '/' + str(mois) + '/' + str(Annee))
        self['Box_1'].setText(str(urlConvert))

    def keyClose(self):
        self.session.openWithCallback(self.close, ScreenPrayerTimes_Show)

def comparetimes():
    msgestr = ''
    try:
        now = datetime.now()
        hr = str(now.hour)
        minute = str(now.minute)
        if len(hr) == 1:
            hr = '0' + hr
        if len(minute) == 1:
            minute = '0' + minute
        hrminute = hr + minute
        hrminute = hrminute.replace(':', '')
        hrminute = hrminute.strip()
        ptimesfile = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Prayer.txt'
        if not os.path.exists(ptimesfile):
            os.system('touch ' + ptimesfile)
            open(ptimesfile, 'w').write('Algeria\nbab-ezzouar\n06:20:00\n07:48:00\n15:52:00\n15:52:00\n18:14:00\n19:37:00\n')
        ptfile = open(ptimesfile, 'r')
        data = ptfile.readlines()
        ptfile.close()
        country = data[0]
        city = data[1]
        fajr_time = data[2]
        fajr_time1 = data[2].replace('\n', '').replace('\t', '').replace('\r', '')
        f = []
        f = fajr_time.split(':')
        fhour = f[0]
        fminute = f[1]
        if len(fhour) == 1:
            fhour = '0' + fhour
        if len(fminute) == 1:
            fminute = '0' + fminute
        fajr_time = str(fhour) + str(fminute)
        zuhr_time = data[4]
        zuhr_time1 = data[4].replace('\n', '').replace('\t', '').replace('\r', '')
        f = []
        f = zuhr_time.split(':')
        fhour = f[0]
        fminute = f[1]
        if len(fhour) == 1:
            fhour = '0' + fhour
        if len(fminute) == 1:
            fminute = '0' + fminute
        zuhr_time = str(fhour) + str(fminute)
        asr_time = data[5]
        asr_time1 = data[5].replace('\n', '').replace('\t', '').replace('\r', '')
        f = []
        f = asr_time.split(':')
        fhour = f[0]
        fminute = f[1]
        if len(fhour) == 1:
            fhour = '0' + fhour
        if len(fminute) == 1:
            fminute = '0' + fminute
        asr_time = str(fhour) + str(fminute)
        maghrb_time = data[6]
        maghrb_time1 = data[6].replace('\n', '').replace('\t', '').replace('\r', '')
        f = []
        f = maghrb_time.split(':')
        fhour = f[0]
        fminute = f[1]
        if len(fhour) == 1:
            fhour = '0' + fhour
        if len(fminute) == 1:
            fminute = '0' + fminute
        maghrb_time = str(fhour) + str(fminute)
        esha_time = data[7]
        esha_time1 = data[7].replace('\n', '').replace('\t', '').replace('\r', '')
        f = []
        f = esha_time.split(':')
        fhour = f[0]
        fminute = f[1]
        if len(fhour) == 1:
            fhour = '0' + fhour
        if len(fminute) == 1:
            fminute = '0' + fminute
        esha_time = str(fhour) + str(fminute)
        fajr_time = fajr_time.strip()
        zuhr_time = zuhr_time.strip()
        asr_time = asr_time.strip()
        maghrb_time = maghrb_time.strip()
        esha_time = esha_time.strip()
        if hrminute == fajr_time:
            msgestr = '\n' + ' حان موعد صلاة الفجر ' + fajr_time1 + '  حسب توقيت  ' + city + "  It's Now Fajr  "
        if hrminute == zuhr_time:
            msgestr = '\n' + ' حان موعد صلاة الظهر ' + zuhr_time1 + ' حسب توقيت ' + city + "  It's Now Zuhr  "
        if hrminute == asr_time:
            msgestr = '\n' + ' حان موعد صلاة العصر ' + asr_time1 + ' حسب توقيت ' + city + "  It's Now Asr  "
        if hrminute == maghrb_time:
            msgestr = '\n' + ' حان موعد صلاة المغرب ' + maghrb_time1 + ' حسب توقيت ' + city + "  It's Now Maghrb  "
        if hrminute == esha_time:
            msgestr = '\n' + 'حان موعد صلاة العشاء ' + esha_time1 + ' حسب توقيت ' + city + "  It's Now Esha  "
        return msgestr
    except:
        return msgestr
def comparetimes_2():
    msgestr_2 = ''
    try:
        now = datetime.now()
        hr = str(now.hour)
        minute = str(now.minute)
        if len(hr) == 1:
            hr = '0' + hr
        if len(minute) == 1:
            minute = '0' + minute
        hrminute = hr + minute
        hrminute = hrminute.replace(':', '')
        hrminute = hrminute.strip()
        ptimesfile = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Times.txt'
        ptfile = open(ptimesfile, 'r')
        data = ptfile.readlines()
        ptfile.close()
        updat_time = data[0]
        if updat_time == 'vide':
            msgestr_2 = ''
        else:
            updat_time1 = data[0].replace('\n', '').replace('\t', '').replace('\r', '')
            f = []
            f = updat_time.split(':')
            fhour = f[0]
            fminute = f[1]
            if len(fhour) == 1:
                fhour = '0' + fhour
            if len(fminute) == 1:
                fminute = '0' + fminute
            updat_time = str(fhour) + str(fminute)
            updat_time = updat_time.strip()
            if hrminute == updat_time:
                msgestr_2 = 'Prayer times have been updated....' + str(updat_time1) + '....تم تحديث اوقات الصلاة'
        return msgestr_2
    except:
        return msgestr_2
class DoPrayerTimesScreen(Screen):
    skin = '\n            <screen position="100,100" size="300,300" title="paryertimes" >\n            </screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        self.msg = ''
        self.minutecount = 30000
        self.TimerPrayerTimes = eTimer()
        self.TimerPrayerTimes.stop()
        try: # Edit By RAED For DreamOS
        	self.TimerPrayerTimes.timeout.get().append(self.CheckPrayerTimes)
        except:
        	self.TimerPrayerTimes_conn = self.TimerPrayerTimes.timeout.connect(self.CheckPrayerTimes)
        self.TimerPrayerTimes.start(self.minutecount, True)

    def repeat(self, result = None):
        self.TimerPrayerTimes = eTimer()
        self.TimerPrayerTimes.stop()
        try: # Edit By RAED For DreamOS
        	self.TimerPrayerTimes.timeout.get().append(self.CheckPrayerTimes)
        except:
        	self.TimerPrayerTimes_conn = self.TimerPrayerTimes.timeout.connect(self.CheckPrayerTimes)
        self.TimerPrayerTimes.start(self.minutecount, True)

    def CheckPrayerTimes(self):
        msg = comparetimes()
        msg_2 = comparetimes_2()
        now = datetime.now()
        if not msg == '':
            self.minutecount = 3600000
            if config.plugins.AthanTimesSetup.flash.value == 'flash':
                self.Verif_msg(msg)
                self.session.openWithCallback(self.repeat, athantimescreen, msg)
            if config.plugins.AthanTimesSetup.flash.value == 'audio':
                if Verif() == 'yes':
                    self.Verif_msg(msg)
                    self.AthanAudio(msg)
                else:
                    self.Verif_msg(msg)
                    self.session.openWithCallback(self.repeat, athantimescreen, msg)
            if config.plugins.AthanTimesSetup.flash.value == 'video':
                self.Verif_msg(msg)
                self.AthanVidio(msg)
        elif not msg_2 == 'vide' and not msg_2 == '':
            self.minutecount = 3600000
            if config.plugins.AthanTimes.UpdatSalat.value == 'yes':
                self.session.openWithCallback(self.repeat, athantimescreen_2, msg_2)
        else:
            self.minutecount = 30000
            self.repeat()

    def Verif_msg(self, msg):
        salathadira = ''
        if 'Fajr' in str(msg):
            salathadira = 'Zuhr'
        elif 'Zuhr' in str(msg):
            salathadira = 'Asr'
        elif 'Asr' in str(msg):
            salathadira = 'Maghrb'
        elif 'Maghrb' in str(msg):
            salathadira = 'Esha'
        elif 'Esha' in str(msg):
            salathadira = 'Fajr'
        Upcoming(salathadira)

    def AthanAudio(self, msg):
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        url = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Flash/audio/adhan.mp3'
        ref = eServiceReference(4097, 0, url)
        ref.setName(msg)
        self.session.openWithCallback(self.backToIntialService, AthanTimesStream, ref, 'athan')

    def AthanAudio_1(self):
        self.initialservice_1 = self.session.nav.getCurrentlyPlayingServiceReference()
        url = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Flash/audio/Dooaa.mp3'
        ref = eServiceReference(4097, 0, url)
        ref.setName('Dooaa دُعاء')
        self.session.openWithCallback(self.backToIntialService_1, AthanTimesStreamDooaa, ref)

#    def AthanVidio(self, msg):
#        self.msg = msg
#        LienUpd = geturlvideo()
#        sniFactory = WebClientContextFactory(LienUpd)
#        if PY3:
#        	getPage(LienUpd.encode('utf-8'), contextFactory=sniFactory, timeout=5,agent=AGENT).addCallback(self.load_AthanVidio, LienUpd.encode('utf-8'))
#        else:
#        	getPage(LienUpd, method='GET', headers=Agent, contextFactory=sniFactory).addCallback(self.load_AthanVidio, LienUpd)

    def AthanVidio(self, msg):
        self.msg = msg
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        URL = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Flash/video/Adhan.mp4'
        sref = eServiceReference(4097, 0, URL)
        sref.setName(self.msg)
        self.session.openWithCallback(self.backToIntialService, AthanTimesStreamVideo, sref)

    def load_AthanVidio(self, data, LienUpd):
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        if PY3:
        	url1 = re.findall('"Download file"\n.*?href="(.*?)">', data.decode('utf-8'))
        else:
        	url1 = re.findall('"Download file"\n.*?href="(.*?)">', data)
        if url1 != []:
            URL = url1[0]
            sref = eServiceReference(4097, 0, URL)
            sref.setName(self.msg)
            self.session.openWithCallback(self.backToIntialService, AthanTimesStreamVideo, sref)
        else:
            self.session.open(MessageBox, 'Link error or connection problem \n' + 'خطأ في الارتباط أو مشكلة في الاتصال', type=MessageBox.TYPE_INFO)

    def backToIntialService(self):
        self.repeat()
        self.session.nav.stopService()
        self.session.nav.playService(self.initialservice)

    def backToIntialService_1(self):
        self.session.nav.stopService()
        self.session.nav.playService(self.initialservice_1)


class athantimescreen(Screen):

    def __init__(self, session, msg = None):
        Screen.__init__(self, session)
        self.dist = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/athan.png'
        skinhd = '<screen name="athantimescreen" position="0,0" size="1280,163" title="" flags="wfNoBorder" backgroundColor="transparent"><widget name="info" position="39,33" size="1029,85" font="Regular;26" zPosition="3" transparent="1" valign="center" halign="center" /><widget source="global.CurrentTime" render="Pixmap" pixmap="' + self.dist + '" position="1120,6" size="150,150" zPosition="4" alphatest="blend"><convert type="AthanTimesAlwaysTrue" /><convert type="AthanTimesConditionalShowHide">Blink</convert></widget><ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/Screenhd.png" position="2,8" zPosition="2" size="1103,132" transparent="1" alphatest="on" /></screen>'
        skinfhd = '<screen name="athantimescreen" position="0,0" size="1920,211" title="" flags="wfNoBorder" backgroundColor="transparent"><widget name="info" position="66,48" size="1617,120" font="Regular;40" zPosition="3" transparent="1" valign="center" halign="center" backgroundColor="#80000000" /><widget source="global.CurrentTime" render="Pixmap" pixmap="' + self.dist + '" position="1748,26" size="150,150" zPosition="4" alphatest="blend"><convert type="AthanTimesAlwaysTrue" /><convert type="AthanTimesConditionalShowHide">Blink</convert></widget><ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/Screen.png" position="4,8" zPosition="2" size="1738,195" transparent="1" alphatest="on" /></screen>'
        if dwidth == 1280:
            self.skin = skinhd
        else:
            self.skin = skinfhd
        self['actions'] = ActionMap(['SetupActions'], {'cancel': self.disappear}, -1)
        self['info'] = Label()
        self['info'].setText(msg)
        self.timer = eTimer()
        try: # Edit By RAED For DreamOS
                self.timer.callback.append(self.disappear)
        except:
                self.timer_conn = self.timer.timeout.connect(self.disappear)
        self.timer.start(50000, True)

    def disappear(self):
        self.timer.stop()
        self.close()
def Nmbrs_lines_1():
    if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/ChoiceTime.txt'):
        file = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/ChoiceTime.txt'
        n = sum((1 for _ in open(file)))
        return n
    else:
        return 0
def Import_Url_Updat_Salat():
    Contnt = ''
    Contr = ''
    bilad = ''
    Url = ''
    timeupdat = ''
    ptimesfile = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/ChoiceTime.txt'
    ptfile = open(ptimesfile, 'r')
    data = ptfile.readlines()
    ptfile.close()
    n = Nmbrs_lines_1()
    if int(n) != 0:
        Contnt = str(data[0]).replace('\n', '').replace('\t', '').replace('\r', '').replace('Contnt=', '')
        Contr = str(data[1]).replace('\n', '').replace('\t', '').replace('\r', '').replace('Contr=', '')
        bilad = str(data[2]).replace('\n', '').replace('\t', '').replace('\r', '').replace('bilad=', '')
        Url = str(data[3]).replace('\n', '').replace('\t', '').replace('\r', '').replace('Url=', '')
        timeupdat = str(data[4]).replace('\n', '').replace('\t', '').replace('\r', '').replace('timeupdat=', '')
        return (Contnt,
         Contr,
         bilad,
         Url,
         timeupdat)
    else:
        Contnt = ''
        Contr = ''
        bilad = ''
        Url = ''
        timeupdat = ''
        return (Contnt,
         Contr,
         bilad,
         Url,
         timeupdat)

def ImportDataInfos_2(data):#
    if PY3:
    	data = data.decode('utf-8')
    else:
    	data = data
    bilad = re.findall("<link rel='canonical' href='https://www.islamicfinder.org/world/.*?/.*?/(.*?)/?language=ar'></link>", data)[0]
    bilad = bilad.replace('-prayer-times', '').replace('/', '').replace('?', '')
    fajr = re.findall('<div class="prayerTiles fajar-tile">.+?<span class="prayername ">.+?</span>.+?<span class="prayertime">(.+?)</span>', data, re.S)
    sunrise = re.findall('<div class="prayerTiles sunrise-tile">.+?<span class="prayername">.+?</span>.+?<span class="prayertime">(.+?)</span>', data, re.S)
    dhuhr = re.findall('<div class="prayerTiles dhuhar-tile">.+?<span class="prayername">.+?</span>.+?<span class="prayertime">(.+?)</span>', data, re.S)
    asr = re.findall('<div class="prayerTiles asr-tile">.+?<span class="prayername">.+?</span>.+?<span class="prayertime">(.+?)</span>', data, re.S)
    maghrib = re.findall('<div class="prayerTiles maghrib-tile">.+?<span class="prayername">.+?</span>.+?<span class="prayertime">(.+?)</span>', data, re.S)
    isha = re.findall('<div class="prayerTiles isha-tile">.+?<span class="prayername">.+?</span>.+?<span class="prayertime">(.+?)</span>', data, re.S)
    qiyam = ['02:18 AM']
    Id = re.findall('"locationId": "(.+?)",', data)
    haiaa = re.findall('<p class="font-sm font-dark">(.+?)<a class=".+?" title="تغيير الإعدادات">يتغيرون</a>', data, re.S)
    haiaa = haiaa[0].replace('\n', '').replace('\t', '').replace('\r', '').replace('&nbsp;', '')
    Calc = re.findall('<p class="font-xs font-muted">(.+?)<span class', data, re.S)
    Calc = Calc[0].replace('&nbsp;', ' ').replace('\n', '').replace('\t', '').replace('\r', '')
    hijri = re.findall('<p class="font-weight-bold pt-date-right">(.+?)</p>', data)[0]
    hijri = hijri.replace('&nbsp;', ' ')
    NextSalat = re.findall('"nextPrayer": "lang.(.+?)", "nextPrayerRemainingTime": "(.+?):(.+?):.+?",', data, re.S)
    Posit = re.findall('id="user-manual-latitude" placeholder=.+?value="(.+?)".+?id="user-manual-longitude" placeholder=.+?name="Longitute" value="(.+?)"', data, re.S)
    return (bilad, fajr, sunrise, dhuhr, asr, maghrib, isha, qiyam, Id, haiaa, Calc, Calc, hijri, NextSalat, Posit)



class athantimescreen_2(Screen):
    def __init__(self, session, msg = None):
        Screen.__init__(self, session)
        self.dist = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/athan.png'
        skinhd = '<screen name="athantimescreen_2" position="0,0" size="1280,720" title="" flags="wfNoBorder" backgroundColor="transparent"><widget name="info" position="39,33" size="1029,85" font="Regular;15" zPosition="3" transparent="1" valign="center" halign="center" /><widget source="global.CurrentTime" render="Pixmap" pixmap="' + self.dist + '" position="1120,6" size="150,150" zPosition="4" alphatest="blend"><convert type="AthanTimesAlwaysTrue" /><convert type="AthanTimesConditionalShowHide">Blink</convert></widget><ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/Screenhd.png" position="2,8" zPosition="2" size="1103,132" transparent="1" alphatest="on" /></screen>'
        skinfhd = '<screen name="athantimescreen_2" position="0,0" size="1920,1080" title="" flags="wfNoBorder" backgroundColor="transparent"><widget name="info" position="66,48" size="1617,120" font="Regular;22" zPosition="3" transparent="1" valign="center" halign="center" backgroundColor="#80000000" /><widget source="global.CurrentTime" render="Pixmap" pixmap="' + self.dist + '" position="1748,26" size="150,150" zPosition="4" alphatest="blend"><convert type="AthanTimesAlwaysTrue" /><convert type="AthanTimesConditionalShowHide">Blink</convert></widget><ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/Screen.png" position="4,8" zPosition="2" size="1738,195" transparent="1" alphatest="on" /></screen>'
        if dwidth == 1280:
            self.skin = skinhd
        else:
            self.skin = skinfhd
        self['actions'] = ActionMap(['SetupActions'], {'ok': self.disappear,
         'cancel': self.disappear}, -1)
        self.messageupdat = msg
        self.Contnt, self.Contr, self.bilad, self.Url, self.timeupdat = Import_Url_Updat_Salat()
        self['info'] = Label()
        self['info'].setText(msg + '\n' + self.Contnt + ' ; ' + self.Contr + ' ; ' + self.bilad + '\nGod accepts your prayers with more reward and forgiveness_تقبل الله صلاتكم بمزيد من الاجر والمغفرة')
        self.list_iptv_2()
        self.timer = eTimer()
        try: # Edit By RAED For DreamOS
                self.timer.callback.append(self.disappear)
        except:
                self.timer_conn = self.timer.timeout.connect(self.disappear)
        self.timer.start(50000, True)

    def disappear(self):
        self.timer.stop()
        self.close()

    def dataError(self, data):
        self['info'].setText('Unfortunately the times have not been updated_للأسف لم يتم تحديث الاوقات' + '\n' + self.Contnt + '\n' + self.Contr + '\n' + self.bilad + '\nGod accepts your prayers with more reward and forgiveness_تقبل الله صلاتكم بمزيد من الاجر والمغفرة')
        self.session.open(MessageBox, 'Sorry a problem with the connection_معذرة مشكل في الاتصال', MessageBox.TYPE_INFO, timeout=10)
        self.Notification_Msg('ko')

    def list_iptv_2(self):
        main_url = self.Url
        sniFactory = WebClientContextFactory(main_url)
        if self.Url != '':
            if PY3:
            	getPage(self.Url.encode('utf-8'), contextFactory=sniFactory, timeout=5,agent=AGENT).addCallback(self.load_iptv_2, self.Url.encode('utf-8'))
            else:
            	getPage(self.Url, method='GET', headers=UserAgent2, contextFactory=sniFactory).addCallback(self.load_iptv_2, self.Url).addErrback(self.dataError)
        else:
            self['info'].setText('Choose your city first so you can update_اختر مدينتك اولاً حتى تتمكن من التحديث')

    def load_iptv_2(self, data, main_url):
        urlop = main_url
        self.letter_list4 = []
        bilad,fajr,sunrise,dhuhr,asr,maghrib,isha,qiyam,Id,haiaa,Calc,Calcule,hijri,NextSalat,Posit = ImportDataInfos_2(data)
        Next = (NextSalat[0][0] + ' ' + NextSalat[0][1] + ':' + NextSalat[0][2]).replace('\n', '').replace('\t', '').replace('\r', '')
        self.Hadira = NextSalat[0][0]
        lat = Posit[0][0] if Posit else ''
        lon = Posit[0][1] if Posit else ''
        self.letter_list4.append(show_listiptv1(self.Contnt, self.Contr, fajr[0], sunrise[0], dhuhr[0], asr[0], maghrib[0], isha[0], qiyam[0], urlop, Id[0], lat, lon, hijri, Calcule, Next, bilad, haiaa))
        self.FAJR = 'Contnt=' + self.Contnt + '\nContr=' + self.Contr + '\nfajr=' + Change_times_3(fajr[0]) + '\nsunrise=' + Change_times_3(sunrise[0]) + '\ndhuhr=' + Change_times_3(dhuhr[0]) + '\nasr=' + Change_times_3(asr[0]) + '\nmaghrib:' + Change_times_3(maghrib[0]) + '\nisha=' + Change_times_3(isha[0]) + '\nqiyam=' + Change_times_3(qiyam[0]) + '\nurl=' + urlop + '\nId=' + Id[0] + '\nLatitude=' + lat + '\nLongitude=' + lon + '\ndate=' + hijri + '\nCalc=' + Calcule + '\nNextSalat=' + Next + '\nbilad=' + bilad + '\nhaiaa=' + haiaa + '\nsalathadira='
        self.FAJR_1 = 'Contnt=' + self.Contnt + '\nContr=' + self.Contr + '\nfajr=' + Change_times_3(fajr[0]) + '\nsunrise=' + Change_times_3(sunrise[0]) + '\ndhuhr=' + Change_times_3(dhuhr[0]) + '\nasr=' + Change_times_3(asr[0]) + '\nmaghrib:' + Change_times_3(maghrib[0]) + '\nisha=' + Change_times_3(isha[0]) + '\nqiyam=' + Change_times_3(qiyam[0]) + '\nId=' + Id[0] + '\nLatitude=' + lat + '\nLongitude=' + lon + '\ndate=' + hijri + '\nCalc=' + Calcule + '\nNextSalat=' + Next + '\nbilad=' + bilad + '\nhaiaa=' + haiaa
        AA = str(haiaa) + '\n' + str(Calc) + '\n' + str(Calcule) + '\n' + str(hijri) + '\n' + str(Next) + '\n' + str(Posit)
        Path_2 = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/Choice/Choice.txt'
        if fileExists(Path_2):
            os.remove(Path_2)
            outfile = open(Path_2, 'a')
            outfile.write(self.FAJR)
            outfile.close()
            XML_Choice(self.letter_list4)
        else:
            outfile = open(Path_2, 'a')
            outfile.write(self.FAJR)
            outfile.close()
            XML_Choice(self.letter_list4)
        self.session.open(MessageBox, '\tData\n\t====\n\tالبيانات\n\t=====\n' + self.FAJR_1, MessageBox.TYPE_INFO, timeout=20)
        SearchAthanWeather(bilad, self.Contr).SearchWeather()
        self.Notification_Msg('ok')

    def Notification_Msg(self, cond):
        self.Path_4 = '/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/PrayerTimes/messageupdat.txt'
        maintenant = datetime.now()
        self.Jour = maintenant.day
        self.mois = maintenant.month
        self.Annee = maintenant.year
        if cond == 'ok':
            if fileExists(self.Path_4):
                os.remove(self.Path_4)
                outfile = open(self.Path_4, 'a')
                outfile.write(self.messageupdat + '\n' + str(self.Jour) + '\n' + str(self.mois) + '\n' + str(self.Annee))
                outfile.close()
        elif fileExists(self.Path_4):
            os.remove(self.Path_4)
            outfile = open(self.Path_4, 'a')
            outfile.write('Unfortunately the times have not been updated_للأسف لم يتم تحديث الاوقات' + '\n' + str(self.Jour) + '\n' + str(self.mois) + '\n' + str(self.Annee))
            outfile.close()

class PrayerTimesBackgroundWorkerScreen(Screen):
    skin = '\n            <screen position="100,100" size="300,300" title="Mountie Plugin Menu" >\n            </screen>'

    def __init__(self, session, args = 0):
        self.skin = PrayerTimesBackgroundWorkerScreen.skin
        self.session = session
        Screen.__init__(self, session)
        self.menu = args
        self.session = session
        self.loop = eTimer()
        try: # Edit By RAED For DreamOS
                self.loop.callback.append(self.ExecTest)
        except:
                self.loop_conn = self.loop.timeout.connect(self.ExecTest)

    def stopTimer(self):
        self.loop.stop()

    def startTimer(self):
        self.loop.start(1, 1)

    def ExecTest(self):
        self.loop.stop()
        self.DebugToLog()
        self.loop.start(3600000, 1)

    def DebugToLog(self):
        now = datetime.now()
        timenow = str(now)


def stoploop():
    StayLoop.stopTimer()

StayLoop = PrayerTimesBackgroundWorkerScreen(session)

class AthanTimesStream(Screen, InfoBarNotifications):
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    PLAYER_STOPS = 3
    skinfhd = '<screen name="AthanTimesStream" flags="wfNoBorder" position="0,0" size="1920,1080" title="AthanTimesStream" backgroundColor="transparent"><widget source="session.CurrentService" render="Label" position="193,826" size="1450,250" font="Regular; 35" backgroundColor="#263c59" shadowColor="#1d354c" shadowOffset="-1,-1" transparent="1" zPosition="1" halign="center"><convert type="ServiceName">Name</convert></widget><widget source="global.CurrentTime" render="Label" position="13,9" size="250,100" font="Regular; 28" halign="left" backgroundColor="black" transparent="1"><convert type="ClockToText">Format:%d.%m.%Y</convert></widget><ePixmap position="388,217" size="1000,600" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/Demar.png" zPosition="-1" transparent="1" alphatest="blend" /><eLabel text="مواقيت الصلاة" position="388,74" size="1000,68" font="Regular; 35" halign="center" transparent="0" foregroundColor="white" backgroundColor="#11f4b" zPosition="3" /><eLabel text="Athan Times" position="388,148" size="1000,68" font="Regular; 35" halign="center" transparent="0" foregroundColor="white" backgroundColor="#11f4b" zPosition="3" /><eLabel text="اللهم رب هذه الدعوة التامة، والصلاة القائمة، آت محمد الوسيلة والفضيلة وابعثه مقاماً محموداً الذي وعدته" position="358,1120" size="1000,68" font="Regular; 30" halign="center" transparent="0" foregroundColor="white" backgroundColor="#11f4b" zPosition="3" /><widget name="Box_0" position="388,0" zPosition="5" size="1000,68" font="Regular;24" foregroundColor="#adff00" backgroundColor="#11f4b" transparent="0" halign="center" valign="center" /></screen>'
    skinhd = '<screen name="AthanTimesStream" flags="wfNoBorder" position="0,0" size="1280,720" title="AthanTimesStream" backgroundColor="transparent"><widget source="session.CurrentService" render="Label" position="-2,616" size="1280,100" font="Regular; 20" backgroundColor="#263c59" shadowColor="#1d354c" shadowOffset="-1,-1" transparent="1" zPosition="1" halign="center"><convert type="ServiceName">Name</convert></widget><widget source="global.CurrentTime" render="Label" position="3,5" size="150,100" font="Regular; 24" halign="left" backgroundColor="black" transparent="1"><convert type="ClockToText">Format:%d.%m.%Y</convert></widget><ePixmap position="165,15" size="1000,600" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/Demar.png" zPosition="-1" transparent="1" alphatest="blend" /></screen>'

    def __init__(self, session, service, cond):
        Screen.__init__(self, session)
        if dwidth == 1280:
            self.skin = AthanTimesStream.skinhd
        else:
            self.skin = AthanTimesStream.skinfhd
        InfoBarNotifications.__init__(self)
        self.session = session
        self.service = service
        self.screen_timeout = 1000
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evSeekableStatusChanged: self.__seekableStatusChanged,
         iPlayableService.evStart: self.__serviceStarted,
         iPlayableService.evEOF: self.__evEOF})
        self['actions'] = ActionMap(['OkCancelActions',
         'InfobarSeekActions',
         'ColorActions',
         'MediaPlayerActions',
         'MovieSelectionActions'], {'ok': self.leavePlayer,
         'cancel': self.leavePlayer,
         'stop': self.leavePlayer}, -2)
        self.cond = cond
        self['pauseplay'] = Label(_('Play'))
        self['Box_0'] = Label(_('اللهم رب هذه الدعوة التامة والصلاة القائمة آت محمدا الوسيلة والفضيلة وابعثه مقاما محمودا الذي وعدته'))
        if self.cond == 'athan':
            self['Box_0'].show()
        if self.cond == 'essai':
            self['Box_0'].hide()
        self.hidetimer = eTimer()
        self.repeter = True
        self.state = self.STATE_PLAYING
        self.onPlayStateChanged = []
        self.play()
        self.onClose.append(self.__onClose)

    def __onClose(self):
        self.session.nav.stopService()

    def __evEOF(self):
        self.STATE_PLAYING = True
        self.state = self.STATE_PLAYING
        self.session.nav.playService(self.service)
        if self.session.nav.stopService():
            self.state = self.STATE_PLAYING
            self.session.nav.playService(self.service)
        else:
            self.leavePlayer()

    def __setHideTimer(self):
        self.hidetimer.start(self.screen_timeout)

    def ok(self):
        self.leavePlayer()

    def playNextFile(self):
        self.session.open(MessageBox, 'only to watch not play Next and Prev File', MessageBox.TYPE_INFO)

    def playPrevFile(self):
        self.session.open(MessageBox, 'only to watch not play Next and Prev File', MessageBox.TYPE_INFO)

    def playService(self, newservice):
        if self.state == self.STATE_IDLE:
            self.play()
        self.service = newservice

    def play(self):
        self.state = self.STATE_PLAYING
        self.session.nav.playService(self.service)
        self.__evEOF

    def __seekableStatusChanged(self):
        service = self.session.nav.getCurrentService()
        if service is not None:
            seek = service.seek()
            if seek is None or not seek.isCurrentlySeekable():
                self.setSeekState(self.STATE_PLAYING)
                self.__evEOF
        return

    def __serviceStarted(self):
        self.state = self.STATE_PLAYING
        self.__evEOF

    def setSeekState(self, wantstate):
        print('setSeekState')
        if wantstate == self.STATE_PAUSED:
            print('trying to switch to Pause- state:', self.STATE_PAUSED)
        elif wantstate == self.STATE_PLAYING:
            print('trying to switch to playing- state:', self.STATE_PLAYING)
        service = self.session.nav.getCurrentService()
        if service is None:
            print('No Service found')
            return False
        else:
            pauseable = service.pause()
            if pauseable is None:
                print('not pauseable.')
                self.state = self.STATE_PLAYING
            if pauseable is not None:
                print('service is pausable')
                if wantstate == self.STATE_PAUSED:
                    print('WANT TO PAUSE')
                    pauseable.pause()
                    self.state = self.STATE_PAUSED
                    if not self.shown:
                        self.hidetimer.stop()
                        self.show()
                elif wantstate == self.STATE_PLAYING:
                    print('WANT TO PLAY')
                    pauseable.unpause()
                    self.state = self.STATE_PLAYING
                    if self.shown:
                        self.__setHideTimer()
            for c in self.onPlayStateChanged:
                c(self.state)

            return True
            return

    def handleLeave(self):
        self.close()

    def leavePlayer(self):
        self.close()


class AthanTimesStreamDooaa(Screen, InfoBarNotifications):
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    PLAYER_STOPS = 3
    skinfhd = '<screen name="AthanTimesStreamDooaa" flags="wfNoBorder" position="0,0" size="1920,1080" title="AthanTimesStreamDooaa" backgroundColor="transparent"><widget source="session.CurrentService" render="Label" position="193,826" size="1450,250" font="Regular; 35" backgroundColor="#263c59" shadowColor="#1d354c" shadowOffset="-1,-1" transparent="1" zPosition="1" halign="center"><convert type="ServiceName">Name</convert></widget><widget source="global.CurrentTime" render="Label" position="13,9" size="250,100" font="Regular; 28" halign="left" backgroundColor="black" transparent="1"><convert type="ClockToText">Format:%d.%m.%Y</convert></widget><ePixmap position="388,217" size="1000,600" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/Demar.png" zPosition="-1" transparent="1" alphatest="blend" /><eLabel text="مواقيت الصلاة" position="388,74" size="1000,68" font="Regular; 35" halign="center" transparent="0" foregroundColor="white" backgroundColor="#11f4b" zPosition="3" /><eLabel text="Athan Times" position="388,148" size="1000,68" font="Regular; 35" halign="center" transparent="0" foregroundColor="white" backgroundColor="#11f4b" zPosition="3" /></screen>'
    skinhd = '<screen name="AthanTimesStreamDooaa" flags="wfNoBorder" position="0,0" size="1280,720" title="AthanTimesStreamDooaa" backgroundColor="transparent"><widget source="session.CurrentService" render="Label" position="-2,616" size="1280,100" font="Regular; 20" backgroundColor="#263c59" shadowColor="#1d354c" shadowOffset="-1,-1" transparent="1" zPosition="1" halign="center"><convert type="ServiceName">Name</convert></widget><widget source="global.CurrentTime" render="Label" position="3,5" size="150,100" font="Regular; 24" halign="left" backgroundColor="black" transparent="1"><convert type="ClockToText">Format:%d.%m.%Y</convert></widget><ePixmap position="165,15" size="1000,600" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/Demar.png" zPosition="-1" transparent="1" alphatest="blend" /></screen>'

    def __init__(self, session, service):
        Screen.__init__(self, session)
        if dwidth == 1280:
            self.skin = AthanTimesStreamDooaa.skinhd
        else:
            self.skin = AthanTimesStreamDooaa.skinfhd
        InfoBarNotifications.__init__(self)
        self.session = session
        self.service = service
        self.screen_timeout = 1000
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evSeekableStatusChanged: self.__seekableStatusChanged,
         iPlayableService.evStart: self.__serviceStarted,
         iPlayableService.evEOF: self.__evEOF})
        self['actions'] = ActionMap(['OkCancelActions',
         'InfobarSeekActions',
         'ColorActions',
         'MediaPlayerActions',
         'MovieSelectionActions'], {'ok': self.leavePlayer,
         'cancel': self.leavePlayer,
         'stop': self.leavePlayer}, -2)
        self['pauseplay'] = Label(_('Play'))
        self.hidetimer = eTimer()
        self.repeter = True
        self.state = self.STATE_PLAYING
        self.onPlayStateChanged = []
        self.play()
        self.onClose.append(self.__onClose)

    def __onClose(self):
        self.session.nav.stopService()

    def __evEOF(self):
        self.STATE_PLAYING = True
        self.state = self.STATE_PLAYING
        self.session.nav.playService(self.service)
        if self.session.nav.stopService():
            self.state = self.STATE_PLAYING
            self.session.nav.playService(self.service)
        else:
            self.leavePlayer()

    def __setHideTimer(self):
        self.hidetimer.start(self.screen_timeout)

    def ok(self):
        self.leavePlayer()

    def playNextFile(self):
        self.session.open(MessageBox, 'only to watch not play Next and Prev File', MessageBox.TYPE_INFO)

    def playPrevFile(self):
        self.session.open(MessageBox, 'only to watch not play Next and Prev File', MessageBox.TYPE_INFO)

    def playService(self, newservice):
        if self.state == self.STATE_IDLE:
            self.play()
        self.service = newservice

    def play(self):
        self.state = self.STATE_PLAYING
        self.session.nav.playService(self.service)
        self.__evEOF

    def __seekableStatusChanged(self):
        service = self.session.nav.getCurrentService()
        if service is not None:
            seek = service.seek()
            if seek is None or not seek.isCurrentlySeekable():
                self.setSeekState(self.STATE_PLAYING)
                self.__evEOF
        return

    def __serviceStarted(self):
        self.state = self.STATE_PLAYING
        self.__evEOF

    def setSeekState(self, wantstate):
        print('setSeekState')
        if wantstate == self.STATE_PAUSED:
            print('trying to switch to Pause- state:', self.STATE_PAUSED)
        elif wantstate == self.STATE_PLAYING:
            print('trying to switch to playing- state:', self.STATE_PLAYING)
        service = self.session.nav.getCurrentService()
        if service is None:
            print('No Service found')
            return False
        else:
            pauseable = service.pause()
            if pauseable is None:
                print('not pauseable.')
                self.state = self.STATE_PLAYING
            if pauseable is not None:
                print('service is pausable')
                if wantstate == self.STATE_PAUSED:
                    print('WANT TO PAUSE')
                    pauseable.pause()
                    self.state = self.STATE_PAUSED
                    if not self.shown:
                        self.hidetimer.stop()
                        self.show()
                elif wantstate == self.STATE_PLAYING:
                    print('WANT TO PLAY')
                    pauseable.unpause()
                    self.state = self.STATE_PLAYING
                    if self.shown:
                        self.__setHideTimer()
            for c in self.onPlayStateChanged:
                c(self.state)

            return True
            return

    def handleLeave(self):
        self.close()

    def leavePlayer(self):
        self.close()


class AthanTimesStreamVideo(Screen, InfoBarNotifications):
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    PLAYER_STOPS = 3
    skinfhd = '<screen name="AthanTimesStreamVideo" flags="wfNoBorder" position="0,0" size="1920,1080" title="AthanTimesStreamVideo" backgroundColor="transparent"><widget source="session.CurrentService" render="Label" position="11,826" size="1902,250" font="Regular; 35" backgroundColor="#263c59" shadowColor="#1d354c" shadowOffset="-1,-1" transparent="1" zPosition="1" halign="center"><convert type="ServiceName">Name</convert></widget><widget source="global.CurrentTime" render="Label" position="13,9" size="250,100" font="Regular; 28" halign="left" backgroundColor="black" transparent="1"><convert type="ClockToText">Format:%d.%m.%Y</convert></widget><eLabel text="اللهم رب هذه الدعوة التامة، والصلاة القائمة، آت محمد الوسيلة والفضيلة وابعثه مقاماً محموداً الذي وعدته" position="273,10" size="1000,90" font="Regular; 30" halign="center" transparent="1" foregroundColor="white" backgroundColor="#11f4b" zPosition="3" /></screen>'
    skinhd = '<screen name="AthanTimesStreamVideo" flags="wfNoBorder" position="0,0" size="1280,720" title="LiveSoccerStream" backgroundColor="transparent"><widget source="session.CurrentService" render="Label" position="-2,581" size="1280,135" font="Regular; 20" backgroundColor="#263c59" shadowColor="#1d354c" shadowOffset="-1,-1" transparent="1" zPosition="1" halign="center"><convert type="ServiceName">Name</convert></widget><widget source="global.CurrentTime" render="Label" position="3,5" size="150,100" font="Regular; 24" halign="left" backgroundColor="black" transparent="1"><convert type="ClockToText">Format:%d.%m.%Y</convert></widget><eLabel text="اللهم رب هذه الدعوة التامة، والصلاة القائمة، آت محمد الوسيلة والفضيلة وابعثه مقاماً محموداً الذي وعدته" position="273,10" size="1000,90" font="Regular; 30" halign="center" transparent="1" foregroundColor="white" backgroundColor="#11f4b" zPosition="3" /></screen>'

    def __init__(self, session, service):
        Screen.__init__(self, session)
        if dwidth == 1280:
            self.skin = AthanTimesStreamVideo.skinhd
        else:
            self.skin = AthanTimesStreamVideo.skinfhd
        InfoBarNotifications.__init__(self)
        self.session = session
        self.service = service
        self.screen_timeout = 1000
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evSeekableStatusChanged: self.__seekableStatusChanged,
         iPlayableService.evStart: self.__serviceStarted,
         iPlayableService.evEOF: self.__evEOF})
        self['actions'] = ActionMap(['OkCancelActions',
         'InfobarSeekActions',
         'ColorActions',
         'MediaPlayerActions',
         'MovieSelectionActions'], {'ok': self.leavePlayer,
         'cancel': self.leavePlayer,
         'stop': self.leavePlayer}, -2)
        self['pauseplay'] = Label(_('Play'))
        self.hidetimer = eTimer()
        self.repeter = True
        self.state = self.STATE_PLAYING
        self.onPlayStateChanged = []
        self.play()
        self.onClose.append(self.__onClose)

    def __onClose(self):
        self.session.nav.stopService()

    def __evEOF(self):
        self.STATE_PLAYING = True
        self.state = self.STATE_PLAYING
        self.session.nav.playService(self.service)
        if self.session.nav.stopService():
            self.state = self.STATE_PLAYING
            self.session.nav.playService(self.service)
        else:
            self.leavePlayer()

    def __setHideTimer(self):
        self.hidetimer.start(self.screen_timeout)

    def ok(self):
        self.leavePlayer()

    def playNextFile(self):
        self.session.open(MessageBox, 'only to watch not play Next and Prev File', MessageBox.TYPE_INFO)

    def playPrevFile(self):
        self.session.open(MessageBox, 'only to watch not play Next and Prev File', MessageBox.TYPE_INFO)

    def playService(self, newservice):
        if self.state == self.STATE_IDLE:
            self.play()
        self.service = newservice

    def play(self):
        self.state = self.STATE_PLAYING
        self['pauseplay'].setText('PLAY')
        self.session.nav.playService(self.service)
        self.__evEOF

    def __seekableStatusChanged(self):
        service = self.session.nav.getCurrentService()
        if service is not None:
            seek = service.seek()
            if seek is None or not seek.isCurrentlySeekable():
                self.setSeekState(self.STATE_PLAYING)
                self.__evEOF
        return

    def __serviceStarted(self):
        self.state = self.STATE_PLAYING
        self.__evEOF

    def setSeekState(self, wantstate):
        print('setSeekState')
        if wantstate == self.STATE_PAUSED:
            print('trying to switch to Pause- state:', self.STATE_PAUSED)
        elif wantstate == self.STATE_PLAYING:
            print('trying to switch to playing- state:', self.STATE_PLAYING)
        service = self.session.nav.getCurrentService()
        if service is None:
            print('No Service found')
            return False
        else:
            pauseable = service.pause()
            if pauseable is None:
                print('not pauseable.')
                self.state = self.STATE_PLAYING
            if pauseable is not None:
                print('service is pausable')
                if wantstate == self.STATE_PAUSED:
                    print('WANT TO PAUSE')
                    pauseable.pause()
                    self.state = self.STATE_PAUSED
                    if not self.shown:
                        self.hidetimer.stop()
                        self.show()
                elif wantstate == self.STATE_PLAYING:
                    print('WANT TO PLAY')
                    pauseable.unpause()
                    self.state = self.STATE_PLAYING
                    if self.shown:
                        self.__setHideTimer()
            for c in self.onPlayStateChanged:
                c(self.state)

            return True
            return

    def handleLeave(self):
        self.close()

    def leavePlayer(self):
        self.close()


class athantimeTestScreen(Screen):

    def __init__(self, session, msg, dist):
        Screen.__init__(self, session)
        self.dist = dist
        skinhd = '<screen name="athantimeTestScreen" position="0,0" size="1280,163" title="" flags="wfNoBorder" backgroundColor="transparent"><widget name="info" position="39,33" size="1029,85" font="Regular;20" zPosition="3" transparent="1" valign="center" halign="center" /><widget source="global.CurrentTime" render="Pixmap" pixmap="' + self.dist + '" position="1120,6" size="150,150" zPosition="4" alphatest="blend"><convert type="AthanTimesAlwaysTrue" /><convert type="AthanTimesConditionalShowHide">Blink</convert></widget><ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/Screenhd.png" position="2,8" zPosition="2" size="1103,132" transparent="1" alphatest="on" /></screen>'
        skinfhd = '<screen name="athantimeTestScreen" position="0,0" size="1920,211" title="" flags="wfNoBorder" backgroundColor="transparent"><widget name="info" position="66,48" size="1617,120" font="Regular;35" zPosition="3" transparent="1" valign="center" halign="center" backgroundColor="#80000000" /><widget source="global.CurrentTime" render="Pixmap" pixmap="' + self.dist + '" position="1748,26" size="150,150" zPosition="4" alphatest="blend"><convert type="AthanTimesAlwaysTrue" /><convert type="AthanTimesConditionalShowHide">Blink</convert></widget><ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/Screen.png" position="4,8" zPosition="2" size="1738,195" transparent="1" alphatest="on" /></screen>'
        if dwidth == 1280:
            self.skin = skinhd
        else:
            self.skin = skinfhd
        self['actions'] = ActionMap(['SetupActions'], {'ok': self.disappear,
         'cancel': self.disappear}, -1)
        self['info'] = Label()
        self['info'].setText(msg)
        self.timer = eTimer()
        try: # Edit By RAED For DreamOS
                self.timer.callback.append(self.disappear)
        except:
                self.timer_conn = self.timer.timeout.connect(self.disappear)
        self.timer.start(20000, True)

    def disappear(self):
        self.timer.stop()
        self.close()

class BooT_AthanTimes(Screen):
    if dwidth == 1280:
        skin = '<screen name="BooT_AthanTimes" position="0,0" size="1280,720" flags="wfNoBorder" title="Boot Logo" backgroundColor="transparent"><ePixmap position="305,188" size="650,290" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/DemarLogo.png" zPosition="-10" transparent="1" /><widget name="Box_1" position="607,632" zPosition="5" size="650,60" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="0" halign="center" valign="center" /></screen>'
    else:
        skin = '<screen name="BooT_ALAJRE" position="0,0" size="1920,1080" flags="wfNoBorder" title="Boot Logo" backgroundColor="transparent"><ePixmap position="607,333" size="650,290" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes/Decos/DemarLogo.png" zPosition="-10" transparent="1" /><widget name="Box_1" position="607,632" zPosition="5" size="650,60" font="Regular;24" foregroundColor="white" backgroundColor="#80000000" transparent="0" halign="center" valign="center" /></screen>'
    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['SetupActions'], {'ok': self.fast,
         'cancel': self.fast}, -1)
        self['Box_1'] = Label(Version_1 + '\n' + Version)
        self.timer = eTimer()
        try: # Edit By RAED For DreamOS
                self.timer.callback.append(self.fast)
        except:
                self.timer_conn = self.timer.timeout.connect(self.fast)
        self.timer.start(1500, True)
    def fast(self):
        self.timer.stop()
        self.session.openWithCallback(self.close, ScreenPrayerTimes_Show)


def main(session, **kwargs):
    session.open(BooT_AthanTimes)

def menu(menuid, **kwargs):
    if menuid == 'mainmenu':
        return [(_('AthanTimes (مواقيت الصلاة)'), main, 'AthanTimes', 44)]
    return []

def Plugins(**kwargs):
    return [PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART, PluginDescriptor.WHERE_AUTOSTART], fnc=autostartAthanTimes),
     PluginDescriptor(name='AthanTimes (مواقيت الصلاة)', description=Version_1, where=[PluginDescriptor.WHERE_PLUGINMENU], icon='AthanTimes.png', fnc=main),
     ] + ([PluginDescriptor(name=_("AthanTimes (مواقيت الصلاة)"), description=_('AthanTimes (مواقيت الصلاة)'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main),
           PluginDescriptor(name=_('AthanTimes (مواقيت الصلاة)'), description=_('AthanTimes (مواقيت الصلاة)'), where=PluginDescriptor.WHERE_MENU, fnc=menu)] if config.plugins.AthanTimes.showplugin.value == "all" else [])


def autostartAthanTimes(reason, **kwargs):
    global session
    try:
        if config.plugins.AthanTimes.notification.value == 'disabled':
            return
    except:
        pass

    if reason == 0:
        if openfile() == 'none':
            StayLoop.stopTimer
        else:
            StayLoop.startTimer()
    if reason == 0 and 'session' in kwargs:
        session = kwargs['session']
        session.open(DoPrayerTimesScreen)
