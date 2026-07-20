# -*- coding: utf-8 -*-
from enigma import eTimer
from Screens.Screen import Screen
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Sources.StaticText import StaticText
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Sources.StaticText import StaticText
from Components.MenuList import MenuList
from enigma import eTimer
from enigma import getDesktop, eListboxPythonMultiContent, eListbox, eTimer, gFont, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_WRAP, loadPNG

dwidth = getDesktop(0).size().width()

Version = 'Update..'


class MessageAthanTimes(Screen):
    TYPE_YESNO = 0
    TYPE_INFO = 1
    TYPE_WARNING = 2
    TYPE_ERROR = 3
    TYPE_MESSAGE = 4

    def __init__(self, session, text, type=TYPE_YESNO, timeout=-1, close_on_any_key=False, default=True, enable_input=True, msgBoxID=None, picon=None, simple=True, list=[], timeout_default=None):
        self.type = type
        BeauteFHD = '<screen name="MessageBoxSimple" position="425,215" size="550,350" title="Message"><widget name="text" position="1,75" size="550,176" font="Regular;28" /><widget name="ErrorPixmap" pixmap="/usr/share/enigma2/skin_default/icons/input_error.png" position="26,16" size="53,53" alphatest="blend" /><widget name="QuestionPixmap" pixmap="/usr/share/enigma2/skin_default/icons/input_question.png" position="26,16" size="53,53" alphatest="blend" /><widget name="InfoPixmap" pixmap="/usr/share/enigma2/skin_default/icons/input_info.png" position="26,16" size="53,53" alphatest="blend" /><widget name="list" position="1,250" font="Regular;30" itemHeight="35" scrollbarMode="showNever" size="550,98" foregroundColor="white" backgroundColor="#80000000" transparent="1" /></screen>'
        BeauteHD = '<screen name="MessageBoxSimple" position="425,215" size="550,350" title="Message"><widget name="text" position="1,75" size="550,176" font="Regular;28" /><widget name="ErrorPixmap" pixmap="/usr/share/enigma2/skin_default/icons/input_error.png" position="26,16" size="53,53" alphatest="blend" /><widget name="QuestionPixmap" pixmap="/usr/share/enigma2/skin_default/icons/input_question.png" position="26,16" size="53,53" alphatest="blend" /><widget name="InfoPixmap" pixmap="/usr/share/enigma2/skin_default/icons/input_info.png" position="26,16" size="53,53" alphatest="blend" /><widget name="list" position="1,250" font="Regular;30" itemHeight="35" scrollbarMode="showNever" size="550,98" foregroundColor="white" backgroundColor="#80000000" transparent="1" /></screen>'
        Screen.__init__(self, session)
        if dwidth == 1280:
            self.skin = BeauteHD
        else:
            self.skin = BeauteFHD
        self.msgBoxID = msgBoxID
        self['text'] = Label(text)
        self['Text'] = StaticText(text)
        self['selectedChoice'] = StaticText()
        self.text = text
        self.close_on_any_key = close_on_any_key
        self.timeout_default = timeout_default
        self['ErrorPixmap'] = Pixmap()
        self['QuestionPixmap'] = Pixmap()
        self['InfoPixmap'] = Pixmap()
        self.timerRunning = False
        self.initTimeout(timeout)
        picon = picon or type
        if picon != self.TYPE_ERROR:
            self['ErrorPixmap'].hide()
        if picon != self.TYPE_YESNO:
            self['QuestionPixmap'].hide()
        if picon != self.TYPE_INFO:
            self['InfoPixmap'].hide()
        self.title = self.type < self.TYPE_MESSAGE and [Version,
         'Information',
         'Warning',
         'Error'][self.type] or 'Message'
        if type == self.TYPE_YESNO:
            if list:
                self.list = list
            elif default == True:
                self.list = [
                 (
                  _('    Oui_نعم'), True), (_('    Non_لا'), False)]
            else:
                self.list = [
                 (
                  _('    Non_لا'), False), (_('    Oui_نعم'), True)]
        else:
            self.list = []
        self['list'] = MenuList(self.list)
        if self.list:
            self['selectedChoice'].setText(self.list[0][0])
        else:
            self['list'].hide()
        if enable_input:
            self['actions'] = ActionMap(['MsgBoxActions', 'DirectionActions'], {'cancel': self.cancel, 'ok': self.ok, 
               'alwaysOK': self.alwaysOK, 
               'up': self.up, 
               'down': self.down, 
               'left': self.left, 
               'right': self.right, 
               'upRepeated': self.up, 
               'downRepeated': self.down, 
               'leftRepeated': self.left, 
               'rightRepeated': self.right}, -1)
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        self.setTitle(_(self.title))

    def initTimeout(self, timeout):
        self.timeout = timeout
        if timeout > 0:
            self.timer = eTimer()
            try:
                self.timer.callback.append(self.timerTick)
            except:
                self.time_conn = self.timer.timeout.connect(self.timerTick)

            self.onExecBegin.append(self.startTimer)
            self.origTitle = None
            if self.execing:
                self.timerTick()
            else:
                self.onShown.append(self.__onShown)
            self.timerRunning = True
        else:
            self.timerRunning = False
        return

    def __onShown(self):
        self.onShown.remove(self.__onShown)
        self.timerTick()

    def startTimer(self):
        self.timer.start(1000)

    def stopTimer(self):
        if self.timerRunning:
            del self.timer
            self.onExecBegin.remove(self.startTimer)
            self.setTitle(self.origTitle)
            self.timerRunning = False

    def timerTick(self):
        if self.execing:
            self.timeout -= 1
            if self.origTitle is None:
                self.origTitle = self.instance.getTitle()
            self.setTitle(self.origTitle + ' (' + str(self.timeout) + ')')
            if self.timeout == 0:
                self.timer.stop()
                self.timerRunning = False
                self.timeoutCallback()
        return

    def timeoutCallback(self):
        print('Timeout!')
        if self.timeout_default is not None:
            self.close(self.timeout_default)
        else:
            self.ok()
        return

    def cancel(self):
        self.close(False)

    def ok(self):
        if self.list:
            self.close(self['list'].getCurrent()[1])
        else:
            self.close(True)

    def alwaysOK(self):
        self.close(True)

    def up(self):
        self.move(self['list'].instance.moveUp)

    def down(self):
        self.move(self['list'].instance.moveDown)

    def left(self):
        self.move(self['list'].instance.pageUp)

    def right(self):
        self.move(self['list'].instance.pageDown)

    def move(self, direction):
        if self.close_on_any_key:
            self.close(True)
        self['list'].instance.moveSelection(direction)
        if self.list:
            self['selectedChoice'].setText(self['list'].getCurrent()[0])
        self.stopTimer()

    def __repr__(self):
        return str(type(self)) + '(' + self.text + ')'
# okay decompiling /home/raed/Desktop/1.pyo
