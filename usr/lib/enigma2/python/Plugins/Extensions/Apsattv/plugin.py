#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
****************************************
*        coded by Lululla              *
*             02/07/2023               *
*       skin by MMark                  *
****************************************
Info http://t.me/tivustream
'''
# 03/06/2023 init
# ######################################################################
#   Enigma2 plugin Apsattv is coded by Lululla                         #
#   This is free software; you can redistribute it and/or modify it.   #
#   But no delete this message & support on forum linuxsat-support     #
# ######################################################################
from __future__ import print_function
from . import _, isDreamOS, paypal, host22
from . import Utils
from . import html_conv
from Components.AVSwitch import AVSwitch
from Components.ActionMap import ActionMap
from Components.config import config
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText
from Components.MultiContent import MultiContentEntryPixmapAlphaTest
from Components.Pixmap import Pixmap
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Plugins.Plugin import PluginDescriptor
from Screens.InfoBarGenerics import InfoBarSubtitleSupport, InfoBarMenu
from Screens.InfoBarGenerics import InfoBarSeek, InfoBarAudioSelection
from Screens.InfoBarGenerics import InfoBarNotifications
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import SCOPE_PLUGINS
from Tools.Directories import resolveFilename
from Screens.VirtualKeyBoard import VirtualKeyBoard
from enigma import RT_VALIGN_CENTER
from enigma import RT_HALIGN_LEFT
from enigma import eListboxPythonMultiContent
from enigma import loadPNG, gFont  # ePicLoad
from enigma import eServiceReference
from enigma import eTimer
from enigma import getDesktop
from enigma import iPlayableService
import os
import re
import sys

PY3 = sys.version_info.major >= 3
if PY3:
    from urllib.request import urlopen, Request
    unicode = str
    unichr = chr
    long = int
    PY3 = True
else:
    from urllib2 import urlopen, Request

global skin_path, search, downloadm3u
currversion = '1.0'
name_plugin = 'Apsattv Plugin'
desc_plugin = ('..:: Apsat Tv International Channel List V. %s ::.. ' % currversion)
PLUGIN_PATH = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('Apsattv'))
res_plugin_path = os.path.join(PLUGIN_PATH, 'skin')
_firstStartfh = True
search = False
downloadm3u = '/media/hdd/movie/'
Panel_list = [('PLAYLISTS ONLINE')]
screenwidth = getDesktop(0).size()
if screenwidth.width() == 2560:
    skin_path = PLUGIN_PATH + '/skin/uhd'
elif screenwidth.width() == 1920:
    skin_path = PLUGIN_PATH + '/skin//fhd'
else:
    skin_path = PLUGIN_PATH + '/skin//hd'

if os.path.exists('/var/lib/dpkg/info'):
    skin_path = skin_path + '/dreamOs'


try:
    from Components.UsageConfig import defaultMoviePath
    downloadm3u = defaultMoviePath()
except:
    if os.path.exists("/usr/bin/apt-get"):
        downloadm3u = ('/media/hdd/movie/')


def pngassign(name):
    png = os.path.join(res_plugin_path, 'pic/tv.png')
    if 'webcam' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/webcam.png')
    elif 'music' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/music.png')
    elif 'spor' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/sport.png')
    elif 'mtv' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/music.png')
    elif 'deluxe' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/music.png')
    elif 'djing' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/music.png')
    elif 'fashion' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/music.png')
    elif 'kiss' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/music.png')
    elif 'sluhay' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/music.png')
    elif 'stingray' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/music.png')
    elif 'techno' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/music.png')
    elif 'viva' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/music.png')
    elif 'country' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/music.png')
    elif 'vevo' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/music.png')
    elif 'spor' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/sport.png')
    elif 'boxing' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/sport.png')
    elif 'racing' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/sport.png')
    elif 'fight' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/sport.png')
    elif 'golf' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/sport.png')
    elif 'knock' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/sport.png')
    elif 'harley' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/sport.png')
    elif 'futbool' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/sport.png')
    elif 'motor' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/sport.png')
    elif 'nba' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/sport.png')
    elif 'nfl' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/sport.png')
    elif 'bull' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/sport.png')
    elif 'poker' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/sport.png')
    elif 'billiar' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/sport.png')
    elif 'fite' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/sport.png')
    elif 'adult' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/xxx.png')
    elif 'xxx' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/xxx.png')
    elif 'weather' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/weather.png')
    elif 'radio' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/radio.png')
    elif 'family' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/family.png')
    elif 'relax' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/relax.png')
    elif 'nature' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/relax.png')
    elif 'escape' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/relax.png')
    elif 'religious' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/religious.png')
    elif 'shop' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/shop.png')
    elif 'movie' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/movie.png')
    elif 'pluto' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/plutotv.png')
    elif 'tvplus' in name.lower():
        png = os.path.join(res_plugin_path, 'pic/tvplus.png')
    else:
        png = os.path.join(res_plugin_path, 'pic/tv.png')
    return png


class free2list(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        if screenwidth.width() == 2560:
            self.l.setItemHeight(60)
            textfont = int(42)
            self.l.setFont(0, gFont('Regular', textfont))
        elif screenwidth.width() == 1920:
            self.l.setItemHeight(50)
            textfont = int(30)
            self.l.setFont(0, gFont('Regular', textfont))
        else:
            self.l.setItemHeight(50)
            textfont = int(24)
            self.l.setFont(0, gFont('Regular', textfont))


def show_(name, link):
    res = [(name, link)]
    png = pngassign(name)
    if screenwidth.width() == 2560:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 5), size=(70, 56), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(90, 0), size=(1200, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    elif screenwidth.width() == 1920:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 5), size=(54, 40), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(70, 0), size=(1000, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(3, 10), size=(54, 40), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(50, 0), size=(500, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    return res


def returnIMDB(text_clear):
    TMDB = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('TMDB'))
    IMDb = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('IMDb'))
    if os.path.exists(TMDB):
        try:
            from Plugins.Extensions.TMBD.plugin import TMBD
            text = html_conv.html_unescape(text_clear)
            _session.open(TMBD.tmdbScreen, text, 0)
        except Exception as e:
            print("[XCF] Tmdb: ", str(e))
        return True
    elif os.path.exists(IMDb):
        try:
            from Plugins.Extensions.IMDb.plugin import main as imdb
            text = html_conv.html_unescape(text_clear)
            imdb(_session, text)
        except Exception as e:
            print("[XCF] imdb: ", str(e))
        return True
    else:
        text_clear = html_conv.html_unescape(text_clear)
        _session.open(MessageBox, text_clear, MessageBox.TYPE_INFO)
        return True
    return False


class Apsattv(Screen):
    def __init__(self, session):
        self.session = session
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        with open(skin, 'r') as f:
            self.skin = f.read()
        Screen.__init__(self, session)
        global _session
        _session = session
        self.setTitle("Thank's Apsattv")
        self['menulist'] = free2list([])
        self['key_red'] = Label(_('Exit'))
        self['key_green'] = Label('Select')
        self['category'] = Label("Plugins Channels Free by Lululla")
        self['title'] = Label("Thank's Apsattv")
        self['name'] = Label('')
        self["paypal"] = Label()
        # self.picload = ePicLoad()
        # self.picfile = ''
        self.currentList = 'menulist'
        self.menulist = []
        self.loading_ok = False
        self.count = 0
        self.loading = 0
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     # 'ButtonSetupActions',
                                     'DirectionActions'], {'up': self.up,
                                                           'down': self.down,
                                                           'left': self.left,
                                                           'right': self.right,
                                                           'ok': self.ok,
                                                           'green': self.ok,
                                                           'cancel': self.exit,
                                                           'red': self.exit}, -1)
        self.onLayoutFinish.append(self.updateMenuList)
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        payp = paypal()
        self["paypal"].setText(payp)

    def updateMenuList(self):
        self.menu_list = []
        for x in self.menu_list:
            del self.menu_list[0]
        list = []
        idx = 0
        png = os.path.join(res_plugin_path, 'pic/tv.png')
        for x in Panel_list:
            list.append(show_(x, png))
            self.menu_list.append(x)
            idx += 1
        self['menulist'].setList(list)
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def ok(self):
        self.keyNumberGlobalCB(self['menulist'].getSelectedIndex())

    def keyNumberGlobalCB(self, idx):
        global namex, lnk
        namex = ''
        lnk = Utils.b64decoder(host22)
        sel = self.menu_list[idx]
        if sel == ("PLAYLISTS ONLINE"):
            namex = "Directy"
            lnk = Utils.b64decoder(host22)
            self.session.open(selectplay, namex, lnk)

    def adultonly(self, namex, lnk):
        self.session.openWithCallback(self.cancelConfirm, MessageBox, _('These streams may contain Adult content\n\nare you sure you want to continue??'))

    def cancelConfirm(self, result):
        if not result:
            return
        else:
            self.session.open(selectplay, namex, lnk)

    def up(self):
        try:
            self[self.currentList].up()
            auswahl = self['menulist'].getCurrent()[0][0]
            self['name'].setText(str(auswahl))
        except Exception as e:
            print(e)

    def down(self):
        try:
            self[self.currentList].down()
            auswahl = self['menulist'].getCurrent()[0][0]
            self['name'].setText(str(auswahl))
        except Exception as e:
            print(e)

    def left(self):
        try:
            self[self.currentList].pageUp()
            auswahl = self['menulist'].getCurrent()[0][0]
            self['name'].setText(str(auswahl))
        except Exception as e:
            print(e)

    def right(self):
        try:
            self[self.currentList].pageDown()
            auswahl = self['menulist'].getCurrent()[0][0]
            self['name'].setText(str(auswahl))
        except Exception as e:
            print(e)

    def exit(self):
        self.close()


class selectplay(Screen):
    def __init__(self, session, namex, lnk):
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.session = session
        Screen.__init__(self, session)
        self.menulist = []
        self.loading_ok = False
        self.count = 0
        self.loading = 0
        self.name = namex
        self.url = lnk
        self.search = ''
        # self.picload = ePicLoad()
        # self.picfile = ''
        self.currentList = 'menulist'
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self['menulist'] = free2list([])
        self["paypal"] = Label()
        self['key_red'] = Label(_('Exit'))
        self['key_green'] = Label(_('Search'))
        self['key_blue'] = Label(_('Export'))
        self['title'] = Label("Thank's Apsattv")
        self['category'] = Label('')
        self['category'].setText(namex)
        self['name'] = Label('')
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     # 'ButtonSetupActions',
                                     'DirectionActions'], {'up': self.up,
                                                           'down': self.down,
                                                           'left': self.left,
                                                           'right': self.right,
                                                           'ok': self.ok,
                                                           'green': self.search_text,
                                                           'blue': self.maincnv,
                                                           'cancel': self.returnback,
                                                           'red': self.returnback}, -1)

        self.onLayoutFinish.append(self.updateMenuList)
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        payp = paypal()
        self["paypal"].setText(payp)

    def maincnv(self):
        try:
            name = self['menulist'].getCurrent()[0][0]
            url = self['menulist'].getCurrent()[0][1]
            conv = main2(self.session, name, url)
            conv.message2()
        except:
            pass

    def search_text(self):
        from Screens.VirtualKeyBoard import VirtualKeyBoard
        self.session.openWithCallback(self.filterChannels, VirtualKeyBoard, title=_("Search"), text='')

    def filterChannels(self, result):
        global search
        if result:
            try:
                self.menu_list = []
                if result is not None and len(result):
                    req = Request(self.url)
                    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                    r = urlopen(req, None, 15)
                    link = r.read()
                    r.close()
                    content = link
                    if str(type(content)).find('bytes') != -1:
                        try:
                            content = content.decode("utf-8")
                        except Exception as e:
                            print("Error: %s." % str(e))
                    regexcat = 'https://www.apsattv.com/(.+?).m3u<'
                    match = re.compile(regexcat, re.DOTALL).findall(content)
                    for name in match:
                        if str(result).lower() in name.lower():
                            search = True
                            url = 'https://www.apsattv.com/' + name + '.m3u'
                            name = name.capitalize()
                            self.menu_list.append(show_(name, url))
                        self['menulist'].l.setList(self.menu_list)
                    auswahl = self['menulist'].getCurrent()[0][0]
                    self['name'].setText(str(auswahl))
            except Exception as e:
                print('error ', str(e))
        else:
            self.resetSearch()

    def returnback(self):
        global search
        if search is True:
            search = False
            del self.menu_list
            self.updateMenuList()
        else:
            search = False
            del self.menu_list
            self.close()

    def resetSearch(self):
        global search
        search = False
        del self.menu_list
        self.updateMenuList()

    def updateMenuList(self):
        self.menu_list = []
        items = []
        try:
            req = Request(self.url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
            r = urlopen(req, None, 15)
            link = r.read()
            r.close()
            content = link
            if str(type(content)).find('bytes') != -1:
                try:
                    content = content.decode("utf-8")
                except Exception as e:
                    print("Error: %s." % str(e))
            regexcat = 'https://www.apsattv.com/(.+?).m3u<'
            match = re.compile(regexcat, re.DOTALL).findall(content)
            for name in match:
                url = 'https://www.apsattv.com/' + name + '.m3u'
                name = name.capitalize()
                item = name + "###" + url + '\n'
                items.append(item)
            items.sort()
            for item in items:
                name = item.split('###')[0]
                url = item.split('###')[1]
                self.menu_list.append(show_(name, url))
            self['menulist'].l.setList(self.menu_list)
            auswahl = self['menulist'].getCurrent()[0][0]
            self['name'].setText(str(auswahl))
        except Exception as e:
            print('exception error II ', str(e))

    def ok(self):
        name = self['menulist'].getCurrent()[0][0]
        url = self['menulist'].getCurrent()[0][1]
        self.session.open(main2, name, url)

    def up(self):
        try:
            self[self.currentList].up()
            auswahl = self['menulist'].getCurrent()[0][0]
            self['name'].setText(str(auswahl))
        except Exception as e:
            print(e)

    def down(self):
        try:
            self[self.currentList].down()
            auswahl = self['menulist'].getCurrent()[0][0]
            self['name'].setText(str(auswahl))
        except Exception as e:
            print(e)

    def left(self):
        try:
            self[self.currentList].pageUp()
            auswahl = self['menulist'].getCurrent()[0][0]
            self['name'].setText(str(auswahl))
        except Exception as e:
            print(e)

    def right(self):
        try:
            self[self.currentList].pageDown()
            auswahl = self['menulist'].getCurrent()[0][0]
            self['name'].setText(str(auswahl))
        except Exception as e:
            print(e)


class main2(Screen):
    def __init__(self, session, namex, lnk):
        self.session = session
        Screen.__init__(self, session)
        self.setup_title = ('Apsattv')
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.menulist = []
        # self.picload = ePicLoad()
        # self.picfile = ''
        self.currentList = 'menulist'
        self.loading_ok = False
        self.count = 0
        self.loading = 0
        self.name = namex
        self.url = lnk
        self.search = ''
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self['menulist'] = free2list([])
        self["paypal"] = Label()
        self['key_red'] = Label(_('Back'))
        self['key_green'] = Label(_('Search'))
        self['key_blue'] = Label(_('Export'))
        self['category'] = Label('')
        self['category'].setText(namex)
        self['title'] = Label("Thank's Apsattv")
        self['name'] = Label('')
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'ButtonSetupActions',
                                     'DirectionActions'], {'up': self.up,
                                                           'down': self.down,
                                                           'left': self.left,
                                                           'right': self.right,
                                                           'ok': self.ok,
                                                           'blue': self.message2,
                                                           'green': self.search_text,
                                                           'cancel': self.closex,
                                                           'red': self.closex}, -1)
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self.updateMenuList)
        else:
            self.timer.callback.append(self.updateMenuList)
        self.timer.start(100, True)
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        payp = paypal()
        self["paypal"].setText(payp)
        self.setTitle(self.setup_title)

    def search_text(self):
        global search
        if search is True:
            search = False
        self.session.openWithCallback(self.filterChannels, VirtualKeyBoard, title=_("Filter this category..."), text=self.search)

    def filterChannels(self, result):
        if result:
            i = len(self.menu_list)
            del self.menu_list[0:i]
            self.menu_list = []
            items = []
            pic = os.path.join(res_plugin_path, 'pic/tv.png')
            try:
                req = Request(self.url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                r = urlopen(req, None, 15)
                content = r.read()
                r.close()
                if str(type(content)).find('bytes') != -1:
                    try:
                        content = content.decode("utf-8")
                    except Exception as e:
                        print("Error: %s." % str(e))
                regexcat = '#EXTINF.*?,(.*?)\\n(.*?)\\n'
                match = re.compile(regexcat, re.DOTALL).findall(content)
                for name, url in match:
                    if str(result).lower() in name.lower():
                        global search
                        search = True
                        name = name.capitalize()
                        url = url.replace(' ', '')
                        url = url.replace('\\n', '')
                        pic = pic
                        item = name + "###" + url + '\n'
                        if item not in items:
                            items.append(item)
                items.sort()
                for item in items:
                    name = item.split("###")[0]
                    url = item.split("###")[1]
                    name = name.capitalize()
                    self.menu_list.append(show_(name, url))
                    self['menulist'].l.setList(self.menu_list)
                auswahl = self['menulist'].getCurrent()[0][0]
                self['name'].setText(str(auswahl))
            except Exception as e:
                print('error ', str(e))
        else:
            self.resetSearch()

    def closex(self):
        if search is True:
            self.resetSearch()
        else:
            self.close()

    def resetSearch(self):
        global search
        search = False
        del self.menu_list
        self.updateMenuList()

    def updateMenuList(self):
        self.menu_list = []
        items = []
        pic = os.path.join(res_plugin_path, 'pic/tv.png')
        try:
            req = Request(self.url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
            r = urlopen(req, None, 15)
            content = r.read()
            r.close()
            if str(type(content)).find('bytes') != -1:
                try:
                    content = content.decode("utf-8")
                except Exception as e:
                    print("Error: %s." % str(e))
            if 'tvg-logo' in content:
                regexcat = 'EXTINF.*?tvg-logo="(.*?)".*?,(.*?)\\n(.*?)\\n'
                match = re.compile(regexcat, re.DOTALL).findall(content)
                for pic, name, url in match:
                    url = url.replace(' ', '')
                    url = url.replace('\\n', '')
                    pic = pic
                    item = name + "###" + url + '\n'
                    if item not in items:
                        items.append(item)
            else:
                regexcat = '#EXTINF.*?,(.*?)\\n(.*?)\\n'
                match = re.compile(regexcat, re.DOTALL).findall(content)
                for name, url in match:
                    url = url.replace(' ', '')
                    url = url.replace('\\n', '')
                    pic = pic

                    item = name + "###" + url + '\n'
                    if item not in items:
                        items.append(item)
            items.sort()
            for item in items:
                name = item.split("###")[0]
                url = item.split("###")[1]
                name = name.capitalize()
                self.menu_list.append(show_(name, url))
                self['menulist'].l.setList(self.menu_list)
            auswahl = self['menulist'].getCurrent()[0][0]
            self['name'].setText(str(auswahl))
        except Exception as e:
            print('error ', str(e))

    def ok(self):
        name = self['menulist'].getCurrent()[0][0]
        url = self['menulist'].getCurrent()[0][1]
        self.play_that_shit(name, url)

    def play_that_shit(self, name, url):
        self.session.open(Playstream2, name, url)

    def up(self):
        try:
            self[self.currentList].up()
            auswahl = self['menulist'].getCurrent()[0][0]
            self['name'].setText(str(auswahl))
        except Exception as e:
            print(e)

    def down(self):
        try:
            self[self.currentList].down()
            auswahl = self['menulist'].getCurrent()[0][0]
            self['name'].setText(str(auswahl))
        except Exception as e:
            print(e)

    def left(self):
        try:
            self[self.currentList].pageUp()
            auswahl = self['menulist'].getCurrent()[0][0]
            self['name'].setText(str(auswahl))
        except Exception as e:
            print(e)

    def right(self):
        try:
            self[self.currentList].pageDown()
            auswahl = self['menulist'].getCurrent()[0][0]
            self['name'].setText(str(auswahl))
        except Exception as e:
            print(e)

    def message2(self, answer=None):
        if answer is None:
            self.session.openWithCallback(self.message2, MessageBox, _('Do you want to Convert to favorite .tv ?\n\nAttention!! It may take some time depending\non the number of streams contained !!!'))
        elif answer:
            name = self.name
            url = self.url
            self.convert_bouquet(url, name)

    def convert_bouquet(self, url, namex):
        type = 'tv'
        if "radio" in namex.lower():
            type = "radio"
        name_file = namex.replace('/', '_').replace(',', '').replace(' ', '-')
        cleanName = re.sub(r'[\<\>\:\"\/\\\|\?\*]', '_', str(name_file))
        cleanName = re.sub(r' ', '_', cleanName)
        cleanName = re.sub(r'\d+:\d+:[\d.]+', '_', cleanName)
        name_file = re.sub(r'_+', '_', cleanName)
        name_file = name_file.lower()
        # downloadm3u = mountipkpth()
        xxxname = '/tmp/' + name_file + '.m3u'
        # if os.path.exists(downloadm3u):
            # xxxname = downloadm3u + name_file + '.m3u'
        # else:
            # xxxname = '/tmp/' + name_file + '.m3u'
        # print('path m3u: ', xxxname)
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        r = urlopen(req, None, 15)
        content = r.read()
        r.close()
        with open(xxxname, 'wb') as output:
            output.write(content)
        bouquetname = 'userbouquet.%s.%s' % (name_file.lower(), type.lower())
        path1 = '/etc/enigma2/' + str(bouquetname)
        path2 = '/etc/enigma2/bouquets.' + str(type.lower())
        if os.path.exists(xxxname) and os.stat(xxxname).st_size > 0:
            tmplist = []
            tmplist.append('#NAME %s (%s)' % (name_file.upper(), type.upper()))
            tmplist.append('#SERVICE 1:64:0:0:0:0:0:0:0:0::%s CHANNELS' % name_file)
            tmplist.append('#DESCRIPTION --- %s ---' % name_file)
            namel = ''
            servicez = ''
            descriptionz = ''
            for line in open(xxxname):
                if line.startswith("#EXTINF"):
                    namel = '%s' % line.split(',')[-1]
                    descriptiona = ('#DESCRIPTION %s' % namel).splitlines()
                    descriptionz = ''.join(descriptiona)
                elif line.startswith('http'):
                    tag = '1'
                    if type.upper() == 'RADIO':
                        tag = '2'
                    servicea = ('#SERVICE 4097:0:%s:0:0:0:0:0:0:0:%s' % (tag, line.replace(':', '%3a')))  # .rstrip('\r').rstrip('\n')
                    servicez = (servicea + ':' + namel).splitlines()
                    servicez = ''.join(servicez)

                if servicez not in tmplist:
                    tmplist.append(servicez)
                    tmplist.append(descriptionz)

            with open(path1, 'w+') as f:
                for item in tmplist:
                    if item not in f.read():
                        f.write("%s\n" % item)
                        # print('item  -------- ', item)
            in_bouquets = 0
            for line in open('/etc/enigma2/bouquets.%s' % type.lower()):
                if bouquetname in line:
                    in_bouquets = 1
            if in_bouquets == 0:
                '''
                Rename unlinked bouquet file /etc/enigma2/userbouquet.webcam.tv to /etc/enigma2/userbouquet.webcam.tv.del
                '''
                with open(path2, 'a+') as f:
                    bouquetTvString = '#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "' + str(bouquetname) + '" ORDER BY bouquet\n'
                    f.write(str(bouquetTvString))
            try:
                from enigma import eDVBDB
                eDVBDB.getInstance().reloadServicelist()
                eDVBDB.getInstance().reloadBouquets()
                print('all bouquets reloaded...')
            except:
                eDVBDB = None
                os.system('wget -qO - http://127.0.0.1/web/servicelistreload?mode=2 > /dev/null 2>&1 &')
                print('bouquets reloaded...')
            mbox = _session.open(MessageBox, _('bouquets reloaded..'), MessageBox.TYPE_INFO, timeout=5)


class TvInfoBarShowHide():
    """ InfoBar show/hide control, accepts toggleShow and hide actions, might start
    fancy animations. """
    STATE_HIDDEN = 0
    STATE_HIDING = 1
    STATE_SHOWING = 2
    STATE_SHOWN = 3
    skipToggleShow = False

    def __init__(self):
        self["ShowHideActions"] = ActionMap(["InfobarShowHideActions"], {"toggleShow": self.OkPressed, "hide": self.hide}, 1)
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={
            iPlayableService.evStart: self.serviceStarted,
        })
        self.__state = self.STATE_SHOWN
        self.__locked = 0
        self.hideTimer = eTimer()
        try:
            self.hideTimer_conn = self.hideTimer.timeout.connect(self.doTimerHide)
        except:
            self.hideTimer.callback.append(self.doTimerHide)
        self.hideTimer.start(5000, True)
        self.onShow.append(self.__onShow)
        self.onHide.append(self.__onHide)

    def OkPressed(self):
        self.toggleShow()

    def __onShow(self):
        self.__state = self.STATE_SHOWN
        self.startHideTimer()

    def __onHide(self):
        self.__state = self.STATE_HIDDEN

    def serviceStarted(self):
        if self.execing:
            if config.usage.show_infobar_on_zap.value:
                self.doShow()

    def startHideTimer(self):
        if self.__state == self.STATE_SHOWN and not self.__locked:
            self.hideTimer.stop()
            idx = config.usage.infobar_timeout.index
            if idx:
                self.hideTimer.start(idx * 1500, True)

    def doShow(self):
        self.hideTimer.stop()
        self.show()
        self.startHideTimer()

    def doTimerHide(self):
        self.hideTimer.stop()
        if self.__state == self.STATE_SHOWN:
            self.hide()

    def toggleShow(self):
        if self.skipToggleShow:
            self.skipToggleShow = False
            return
        if self.__state == self.STATE_HIDDEN:
            self.show()
            self.hideTimer.stop()
        else:
            self.hide()
            self.startHideTimer()

    def lockShow(self):
        try:
            self.__locked += 1
        except:
            self.__locked = 0
        if self.execing:
            self.show()
            self.hideTimer.stop()
            self.skipToggleShow = False

    def unlockShow(self):
        try:
            self.__locked -= 1
        except:
            self.__locked = 0
        if self.__locked < 0:
            self.__locked = 0
        if self.execing:
            self.startHideTimer()

    def debug(obj, text=""):
        print(text + " %s\n" % obj)


class Playstream2(
                  InfoBarBase,
                  InfoBarMenu,
                  InfoBarSeek,
                  InfoBarAudioSelection,
                  InfoBarSubtitleSupport,
                  InfoBarNotifications,
                  TvInfoBarShowHide,
                  Screen
                  ):
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    screen_timeout = 5000

    def __init__(self, session, name, url):
        global streaml
        Screen.__init__(self, session)
        self.session = session
        self.skinName = 'MoviePlayer'
        streaml = False
        for x in InfoBarBase, \
                InfoBarMenu, \
                InfoBarSeek, \
                InfoBarAudioSelection, \
                InfoBarSubtitleSupport, \
                InfoBarNotifications, \
                TvInfoBarShowHide:
            x.__init__(self)
        try:
            self.init_aspect = int(self.getAspect())
        except:
            self.init_aspect = 0
        self.new_aspect = self.init_aspect
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self.service = None
        self.name = html_conv.html_unescape(name)
        self.icount = 0
        self.url = url
        self.state = self.STATE_PLAYING
        self['actions'] = ActionMap(['MoviePlayerActions',
                                     'MovieSelectionActions',
                                     'MediaPlayerActions',
                                     'EPGSelectActions',
                                     'MediaPlayerSeekActions',
                                     'ColorActions',
                                     'ButtonSetupActions',
                                     'OkCancelActions',
                                     'InfobarShowHideActions',
                                     'InfobarActions',
                                     'InfobarSeekActions'], {'leavePlayer': self.cancel,
                                                             'epg': self.showIMDB,
                                                             'info': self.showIMDB,
                                                             'tv': self.cicleStreamType,
                                                             'stop': self.leavePlayer,
                                                             'playpauseService': self.playpauseService,
                                                             'red': self.cicleStreamType,
                                                             'cancel': self.cancel,
                                                             'exit': self.leavePlayer,
                                                             'yellow': self.subtitles,
                                                             'down': self.av,
                                                             'back': self.cancel}, -1)
        if '8088' in str(self.url):
            # self.onLayoutFinish.append(self.slinkPlay)
            self.onFirstExecBegin.append(self.slinkPlay)
        else:
            # self.onLayoutFinish.append(self.cicleStreamType)
            self.onFirstExecBegin.append(self.cicleStreamType)
        self.onClose.append(self.cancel)

    def getAspect(self):
        return AVSwitch().getAspectRatioSetting()

    def getAspectString(self, aspectnum):
        return {
            0: '4:3 Letterbox',
            1: '4:3 PanScan',
            2: '16:9',
            3: '16:9 always',
            4: '16:10 Letterbox',
            5: '16:10 PanScan',
            6: '16:9 Letterbox'
        }[aspectnum]

    def setAspect(self, aspect):
        map = {
            0: '4_3_letterbox',
            1: '4_3_panscan',
            2: '16_9',
            3: '16_9_always',
            4: '16_10_letterbox',
            5: '16_10_panscan',
            6: '16_9_letterbox'
        }
        config.av.aspectratio.setValue(map[aspect])
        try:
            AVSwitch().setAspectRatio(aspect)
        except:
            pass

    def av(self):
        temp = int(self.getAspect())
        temp = temp + 1
        if temp > 6:
            temp = 0
        self.new_aspect = temp
        self.setAspect(temp)

    def showIMDB(self):
        try:
            text_clear = self.name
            if returnIMDB(text_clear):
                print('show imdb/tmdb')
        except Exception as ex:
            print(str(ex))
            print("Error: can't find Playstream2 in live_to_stream")

    def slinkPlay(self, url):
        name = self.name
        ref = "{0}:{1}".format(url.replace(":", "%3a"), name.replace(":", "%3a"))
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def openTest(self, servicetype, url):
        name = self.name
        ref = "{0}:0:1:0:0:0:0:0:0:0:{1}:{2}".format(servicetype, url.replace(":", "%3a"), name.replace(":", "%3a"))
        print('reference:   ', ref)
        if streaml is True:
            url = 'http://127.0.0.1:8088/' + str(url)
            ref = "{0}:0:1:0:0:0:0:0:0:0:{1}:{2}".format(servicetype, url.replace(":", "%3a"), name.replace(":", "%3a"))
            print('streaml reference:   ', ref)
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def subtitles(self):
        self.session.open(MessageBox, _('Please install SubSupport Plugins'), MessageBox.TYPE_ERROR, timeout=10)

    def cicleStreamType(self):
        global streaml
        streaml = False
        from itertools import cycle, islice
        self.servicetype = '4097'
        print('servicetype1: ', self.servicetype)
        url = str(self.url)
        if str(os.path.splitext(self.url)[-1]) == ".m3u8":
            if self.servicetype == "1":
                self.servicetype = "4097"
        currentindex = 0
        streamtypelist = ["4097"]
        '''
        if Utils.isStreamlinkAvailable():
            streamtypelist.append("5002")  # ref = '5002:0:1:0:0:0:0:0:0:0:http%3a//127.0.0.1%3a8088/' + url
            streaml = True
        if os.path.exists("/usr/bin/gstplayer"):
            streamtypelist.append("5001")
        if os.path.exists("/usr/bin/exteplayer3"):
            streamtypelist.append("5002")
        '''
        if os.path.exists("/usr/bin/apt-get"):
            streamtypelist.append("8193")
        for index, item in enumerate(streamtypelist, start=0):
            if str(item) == str(self.servicetype):
                currentindex = index
                break
        nextStreamType = islice(cycle(streamtypelist), currentindex + 1, None)
        self.servicetype = str(next(nextStreamType))
        print('servicetype2: ', self.servicetype)
        self.openTest(self.servicetype, url)

    def up(self):
        pass

    def down(self):
        self.up()

    def doEofInternal(self, playing):
        self.close()

    def __evEOF(self):
        self.end = True

    def showVideoInfo(self):
        if self.shown:
            self.hideInfobar()
        if self.infoCallback is not None:
            self.infoCallback()
        return

    def showAfterSeek(self):
        if isinstance(self, TvInfoBarShowHide):
            self.doShow()

    def cancel(self):
        if os.path.isfile('/tmp/hls.avi'):
            os.remove('/tmp/hls.avi')
        self.session.nav.stopService()
        self.session.nav.playService(self.srefInit)
        if not self.new_aspect == self.init_aspect:
            try:
                self.setAspect(self.init_aspect)
            except:
                pass
        streaml = False
        self.close()

    def leavePlayer(self):
        self.close()


class AutoStartTimerFh:

    def __init__(self, session):
        self.session = session
        global _firstStartfh
        print("*** running AutoStartTimerFh ***")
        if _firstStartfh:
            self.runUpdate()

    def runUpdate(self):
        print("*** running update ***")
        try:
            from . import Update
            Update.upd_done()
            _firstStartfh = False
        except Exception as e:
            print('error Fxy', str(e))


def autostart(reason, session=None, **kwargs):
    print("*** running autostart ***")
    global autoStartTimerFh
    global _firstStartfh
    if reason == 0:
        if session is not None:
            _firstStartfh = True
            autoStartTimerFh = AutoStartTimerFh(session)
    return


def main(session, **kwargs):
    try:
        session.open(Apsattv)
    except:
        import traceback
        traceback.print_exc


def Plugins(**kwargs):
    ico_path = 'plugin.png'
    # extDescriptor = PluginDescriptor(name=name_plugin, description=desc_plugin, where=[PluginDescriptor.WHERE_EXTENSIONSMENU], icon=ico_path, fnc=main)
    result = [PluginDescriptor(name=name_plugin, description=desc_plugin, where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=autostart),
              PluginDescriptor(name=name_plugin, description=desc_plugin, where=PluginDescriptor.WHERE_PLUGINMENU, icon=ico_path, fnc=main)]
    # result.append(extDescriptor)
    return result
