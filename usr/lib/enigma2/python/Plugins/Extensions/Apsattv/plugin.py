# -*- coding: utf-8 -*-
from __future__ import print_function

"""
#########################################################
#                                                       #
#  Apsattv Plugin                                       #
#  Version: 1.6                                         #
#  Created by Lululla (https://github.com/Belfagor2005) #
#  License: CC BY-NC-SA 4.0                             #
#  https://creativecommons.org/licenses/by-nc-sa/4.0    #
#  Last Modified: "09:25 - 20250514"                    #
#                                                       #
#  Credits:                                             #
#  - Original concept by Lululla                        #
#  Usage of this code without proper attribution        #
#  is strictly prohibited.                              #
#  For modifications and redistribution,                #
#  please maintain this credit header.                  #
#########################################################
"""
__author__ = "Lululla"

from datetime import datetime

from enigma import (
	RT_HALIGN_LEFT,
	RT_VALIGN_CENTER,
	eListboxPythonMultiContent,
	eServiceReference,
	eTimer,
	gFont,
	getDesktop,
	iPlayableService,
	loadPNG,
)

from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryPixmapAlphaTest, MultiContentEntryText
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Components.config import config
from os.path import exists, join, isfile, splitext
from os import listdir, rename, remove, stat
from json import loads
from re import findall, DOTALL, compile, sub
from sys import version_info
from Plugins.Plugin import PluginDescriptor

from Screens.InfoBarGenerics import (
	InfoBarAudioSelection,
	InfoBarMenu,
	InfoBarNotifications,
	InfoBarSeek,
	InfoBarSubtitleSupport,
)
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.VirtualKeyBoard import VirtualKeyBoard

from Tools.Directories import SCOPE_PLUGINS, resolveFilename

from . import _, host22, paypal
from .lib import Utils, html_conv
from .lib.Console import Console as xConsole

global skin_path, search, dowm3u


try:
	aspect_manager = Utils.AspectManager()
	current_aspect = aspect_manager.get_current_aspect()
except:
	pass


try:
	from os.path import isdir
except ImportError:
	from os import isdir


PY3 = version_info.major >= 3
if PY3:
	from urllib.request import urlopen, Request
	from urllib.error import URLError, HTTPError
	unicode = str
	unichr = chr
	long = int
else:
	from urllib2 import urlopen, Request
	from urllib2 import URLError, HTTPError


currversion = '1.3'
name_plugin = 'Apsattv Plugin'
desc_plugin = ('..:: Apsat Tv International Channel List V. %s ::.. ' % currversion)
PLUGIN_PATH = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('Apsattv'))
res_plugin_path = join(PLUGIN_PATH, 'skin')
installer_url = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0JlbGZhZ29yMjAwNS9BcHNhdHR2L21haW4vaW5zdGFsbGVyLnNo'
developer_url = 'aHR0cHM6Ly9hcGkuZ2l0aHViLmNvbS9yZXBvcy9CZWxmYWdvcjIwMDUvQXBzYXR0dg=='
search = False
dowm3u = '/media/hdd/movie/'
enigma_path = '/etc/enigma2/'
Panel_list = [('PLAYLISTS ONLINE')]

screen_width = getDesktop(0).size()
if screen_width == 2560:
	skin_path = join(PLUGIN_PATH, 'skin/uhd')
elif screen_width == 1920:
	skin_path = join(PLUGIN_PATH, 'skin/fhd')
else:
	skin_path = PLUGIN_PATH + '/skin/hd'

if exists('/usr/bin/apt-get'):
	skin_path = join(skin_path, 'dreamOs')


def pngassign(name):
	name_lower = name.lower()
	png = join(res_plugin_path, "pic/tv.png")  # default image

	categories = {
		"webcam": ["webcam"],
		"music": [
			"music", "mtv", "deluxe", "djing", "fashion", "kiss", "sluhay",
			"stingray", "techno", "viva", "country", "vevo"
		],
		"sport": [
			"spor", "boxing", "racing", "fight", "golf", "knock", "harley",
			"futbool", "motor", "nba", "nfl", "bull", "poker", "billiar", "fite"
		],
		"xxx": ["adult", "xxx"],
		"relax": ["relax", "nature", "escape"],
		"weather": ["weather"],
		"radio": ["radio"],
		"family": ["family"],
		"religious": ["religious"],
		"shop": ["shop"],
		"movie": ["movie"],
		"plutotv": ["pluto"],
		"tvplus": ["tvplus"]
	}

	for category, keywords in categories.items():
		if any(keyword in name_lower for keyword in keywords):
			png = join(res_plugin_path, 'pic/%s.png' % category)
			break

	return png


def defaultMoviePath():
	result = config.usage.default_path.value
	if not isdir(result):
		from Tools import Directories
		return Directories.defaultRecordingLocation(config.usage.default_path.value)
	return result


if not isdir(config.movielist.last_videodir.value):
	try:
		config.movielist.last_videodir.value = defaultMoviePath()
		config.movielist.last_videodir.save()
	except:
		pass

dowm3u = config.movielist.last_videodir.value


class free2list(MenuList):
	def __init__(self, items):
		"""
		Initialize the webcam list with appropriate font size and item height based on screen width.
		"""
		MenuList.__init__(self, items, True, eListboxPythonMultiContent)
		self.configureList()

	def configureList(self):
		"""
		Configure font size and item height based on the screen width.
		"""
		if screen_width == 2560:
			self.l.setFont(0, gFont('Regular', 50))
			self.l.setItemHeight(60)
		elif screen_width == 1920:
			self.l.setFont(0, gFont('Regular', 46))
			self.l.setItemHeight(50)
		else:
			self.l.setFont(0, gFont('Regular', 24))
			self.l.setItemHeight(45)


def show_(name, link):
	"""
	Creates a webcam list entry with text and icon based on screen resolution.

	:param name: Name of the webcam.
	:param link: Link associated with the webcam.
	:return: List representing the entry.
	"""
	png = pngassign(name)
	res = [(name, link)]

	if screen_width == 2560:
		icon_pos, icon_size = (5, 2), (70, 50)
		text_pos, text_size = (90, 0), (1200, 60)
	elif screen_width == 1920:
		icon_pos, icon_size = (5, 0), (54, 40)
		text_pos, text_size = (90, 0), (950, 50)
	else:
		icon_pos, icon_size = (3, 0), (54, 40)
		text_pos, text_size = (65, 0), (500, 50)

	res.append(MultiContentEntryPixmapAlphaTest(pos=icon_pos, size=icon_size, png=loadPNG(png)))
	res.append(MultiContentEntryText(pos=text_pos, size=text_size, font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
	return res


def returnIMDB(text_clear):
	text = html_conv.html_unescape(text_clear)

	if Utils.is_TMDB and Utils.TMDB:
		try:
			_session.open(Utils.TMDB.tmdbScreen, text, 0)
		except Exception as e:
			print("[XCF] TMDB error:", str(e))
		return True

	elif Utils.is_tmdb and Utils.tmdb:
		try:
			_session.open(Utils.tmdb.tmdbScreen, text, 0)
		except Exception as e:
			print("[XCF] tmdb error:", str(e))
		return True

	elif Utils.is_imdb and Utils.imdb:
		try:
			Utils.imdb(_session, text)
		except Exception as e:
			print("[XCF] IMDb error:", str(e))
		return True

	_session.open(MessageBox, text, MessageBox.TYPE_INFO)
	return True


def filter_channels(url, result, menu_list, show_):
	"""
	Filter channels based on search result.
	"""
	items = []
	try:
		menu_list.clear()

		req = Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
		r = urlopen(req, None, 15)
		content = r.read()
		r.close()

		if isinstance(content, bytes):
			content = content.decode("utf-8")

		regexcat = r"#EXTINF.*?,(.*?)\n(.*?)\n"
		match = findall(regexcat, content, DOTALL)

		for name, url in match:
			if str(result).lower() in name.lower():
				name = name.capitalize()
				url = url.replace('\\n', '').strip()
				item = name + "###" + url
				if item not in items:
					items.append(item)

		items.sort()
		for item in items:
			name, url = item.split("###")
			menu_list.append(show_(name, url))

		if menu_list:
			auswahl = menu_list[0][0]  # Adjust this to your specific widget or list reference
			return auswahl
		else:
			return 'No results found'

	except (URLError, HTTPError) as e:
		print('Error with URL request: %s' % str(e))
	except Exception as e:
		print('Generic error: %s' % str(e))


class Apsattv(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		skin = join(skin_path, 'defaultListScreen.xml')
		with open(skin, 'r') as f:
			self.skin = f.read()
		global _session
		_session = session
		self.setTitle("Thank's Apsattv")
		self.currentList = 'menulist'
		self.menulist = []
		self.loading_ok = False
		self.count = 0
		self.loading = 0
		self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
		self['menulist'] = free2list([])
		self["paypal"] = Label()
		self['key_red'] = Label(_('Exit'))
		self['key_green'] = Label('Select')
		self['key_yellow'] = Label(_('Update'))
		self['key_blue'] = Label()
		self['category'] = Label("Plugins Channels Free by Lululla")
		self['title'] = Label("Thank's Apsattv")
		self['name'] = Label('')
		self.Update = False
		self['actions'] = ActionMap(
			[
				'OkCancelActions',
				'DirectionActions',
				'HotkeyActions',
				'InfobarEPGActions',
				'ChannelSelectBaseActions'
			],
			{
				'up': self.up,
				'down': self.down,
				'left': self.left,
				'right': self.right,
				'ok': self.ok,
				'cancel': self.exitx,
				'yellow': self.update_me,  # update_me,
				'green': self.ok,
				'yellow_long': self.update_dev,
				'info_long': self.update_dev,
				'infolong': self.update_dev,
				'showEventInfoPlugin': self.update_dev,
				'red': self.exitx,
			},
			-1
		)
		self.timer = eTimer()
		if exists("/usr/bin/apt-get"):
			self.timer_conn = self.timer.timeout.connect(self.check_vers)
		else:
			self.timer.callback.append(self.check_vers)
		self.timer.start(500, 1)
		self.onLayoutFinish.append(self.updateMenuList)
		self.onLayoutFinish.append(self.layoutFinished)

	def check_vers(self):
		"""
		Check the latest version and changelog from the remote installer URL.
		If a new version is available, notify the user.
		"""
		remote_version = '0.0'
		remote_changelog = ''
		try:

			def feth(url):
				try:
					req = Request('http://example.com')
					response = urlopen(req)
					content = response.read()
					response.close()
					return content
				except HTTPError as e:
					print('Errore HTTP: %s' % str(e))
				except URLError as e:
					print('Errore URL: %s' % str(e))
				except Exception as e:
					print('Errore generico: %s' % str(e))
				return None

			req = Utils.Request(Utils.b64decoder(installer_url), headers={'User-Agent': 'Mozilla/5.0'})
			page = Utils.urlopen(req).read()
			# data = page.decode("utf-8") if PY3 else page.encode("utf-8")
			page = feth(installer_url)
			data = page.decode("utf-8") if PY3 else page.encode("utf-8")
			if data:
				lines = data.split("\n")
				for line in lines:
					if line.startswith("version"):
						remote_version = line.split("'")[1] if "'" in line else '0.0'
					elif line.startswith("changelog"):
						remote_changelog = line.split("'")[1] if "'" in line else ''
						break
		except Exception as e:
			self.session.open(MessageBox, _('Error checking version: %s') % str(e), MessageBox.TYPE_ERROR, timeout=5)
			return
		self.new_version = remote_version
		self.new_changelog = remote_changelog
		# if float(currversion) < float(remote_version):
		if currversion < remote_version:
			self.Update = True
			self.session.open(
				MessageBox,
				_('New version %s is available\n\nChangelog: %s\n\nPress info_long or yellow_long button to start force updating.') % (self.new_version, self.new_changelog),
				MessageBox.TYPE_INFO,
				timeout=5
			)

	def update_me(self):
		if self.Update is True:
			self.session.openWithCallback(self.install_update, MessageBox, _("New version %s is available.\n\nChangelog: %s\n\nDo you want to install it now?") % (self.new_version, self.new_changelog), MessageBox.TYPE_YESNO)
		else:
			self.session.open(MessageBox, _("Congrats! You already have the latest version..."),  MessageBox.TYPE_INFO, timeout=4)

	def update_dev(self):
		"""
		Check for updates from the developer's URL and prompt the user to install the latest update.
		"""
		try:
			req = Utils.Request(Utils.b64decoder(developer_url), headers={'User-Agent': 'Mozilla/5.0'})
			page = Utils.urlopen(req).read()
			data = loads(page)
			remote_date = data['pushed_at']
			strp_remote_date = datetime.strptime(remote_date, '%Y-%m-%dT%H:%M:%SZ')
			remote_date = strp_remote_date.strftime('%Y-%m-%d')
			self.session.openWithCallback(self.install_update, MessageBox, _("Do you want to install update ( %s ) now?") % (remote_date), MessageBox.TYPE_YESNO)
		except Exception as e:
			print('error xcons:', e)

	def install_update(self, answer=False):
		if answer:
			cmd1 = 'wget -q "--no-check-certificate" ' + Utils.b64decoder(installer_url) + ' -O - | /bin/sh'
			self.session.open(xConsole, 'Upgrading...', cmdlist=[cmd1], finishedCallback=self.myCallback, closeOnSuccess=False)
		else:
			self.session.open(MessageBox, _("Update Aborted!"),  MessageBox.TYPE_INFO, timeout=3)

	def myCallback(self, result=None):
		print('result:', result)
		return

	def layoutFinished(self):
		payp = paypal()
		self["paypal"].setText(payp)

	def updateMenuList(self):
		self.menu_list = []
		for x in self.menu_list:
			del self.menu_list[0]
		list = []
		idx = 0
		png = join(res_plugin_path, 'pic/tv.png')
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
		namex = "Directy"
		sel = self.menu_list[idx]
		if sel == ("PLAYLISTS ONLINE"):
			lnk = Utils.b64decoder(host22)
			self.session.open(selectplay, namex, lnk)

	def up(self):
		try:
			self[self.currentList].up()
			auswahl = self['menulist'].getCurrent()[0][0]
			self['name'].setText(str(auswahl))
		except Exception as e:
			print("Error occurred:", e)

	def down(self):
		try:
			self[self.currentList].down()
			auswahl = self['menulist'].getCurrent()[0][0]
			self['name'].setText(str(auswahl))
		except Exception as e:
			print("Error occurred:", e)

	def left(self):
		try:
			self[self.currentList].pageUp()
			auswahl = self['menulist'].getCurrent()[0][0]
			self['name'].setText(str(auswahl))
		except Exception as e:
			print("Error occurred:", e)

	def right(self):
		try:
			self[self.currentList].pageDown()
			auswahl = self['menulist'].getCurrent()[0][0]
			self['name'].setText(str(auswahl))
		except Exception as e:
			print("Error occurred:", e)

	def exitx(self):
		self.close()


class selectplay(Screen):
	def __init__(self, session, namex, lnk):
		Screen.__init__(self, session)
		skin = join(skin_path, 'defaultListScreen.xml')
		with open(skin, 'r') as f:
			self.skin = f.read()
		self.session = session
		self.menulist = []
		self.loading_ok = False
		self.count = 0
		self.loading = 0
		self.name = namex
		self.url = lnk
		self.search = ''
		self.currentList = 'menulist'
		self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
		self['menulist'] = free2list([])
		self["paypal"] = Label()
		self['key_red'] = Label(_('Exit'))
		self['key_green'] = Label(_('Search'))
		self['key_yellow'] = Label()
		self['key_blue'] = Label(_('Remove Bouquet'))
		self['title'] = Label("Thank's Apsattv")
		self['category'] = Label('')
		self['category'].setText(namex)
		self['name'] = Label('')
		self['actions'] = ActionMap(
			['OkCancelActions', 'DirectionActions', 'ColorActions'],
			{
				'up': self.up,
				'down': self.down,
				'left': self.left,
				'right': self.right,
				'ok': self.ok,
				'green': self.search_text,
				'blue': self.msgdeleteBouquets,
				'cancel': self.returnback,
				'red': self.returnback
			},
			-1
		)

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
		"""
		Filter channels based on search result.
		"""
		if not result:
			self.resetSearch()
			return

		self.menu_list = []
		try:
			auswahl = filter_channels(self.url, result, self.menu_list, show_)

			if self.menu_list:
				self['name'].setText(str(auswahl))
			else:
				self['name'].setText('No results found')
				self.resetSearch()
				return
		except Exception as e:
			print('Error finder', e)

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
		"""
		Updates the menu list by downloading and parsing the content from the specified URL.
		"""
		self.menu_list = []
		items = []
		try:
			req = Request(self.url)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
			r = urlopen(req, None, 15)
			content = r.read()
			r.close()
			if isinstance(content, bytes):
				try:
					content = content.decode("utf-8")
				except Exception as e:
					print("Error decoding content: %s" % str(e))
					return

			regexcat = r'https://www.apsattv.com/(.+?).m3u<'
			match = compile(regexcat, DOTALL).findall(content)

			for name in match:
				url = 'https://www.apsattv.com/' + name + '.m3u'
				name = name.capitalize()
				item = name + "###" + url + '\n'
				items.append(item)

			for item in sorted(items):
				name, url = item.split('###')
				self.menu_list.append(show_(name, url))

			self['menulist'].l.setList(self.menu_list)
			if self.menu_list:
				auswahl = self['menulist'].getCurrent()[0][0]
				self['name'].setText(str(auswahl))
			else:
				self['name'].setText("No items found.")

		except (URLError, HTTPError) as e:
			print("Error HTTP/URL: %s" % str(e))
		except Exception as e:
			print("Error generic: %s" % str(e))

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
			print("Error occurred:", e)

	def down(self):
		try:
			self[self.currentList].down()
			auswahl = self['menulist'].getCurrent()[0][0]
			self['name'].setText(str(auswahl))
		except Exception as e:
			print("Error occurred:", e)

	def left(self):
		try:
			self[self.currentList].pageUp()
			auswahl = self['menulist'].getCurrent()[0][0]
			self['name'].setText(str(auswahl))
		except Exception as e:
			print("Error occurred:", e)

	def right(self):
		try:
			self[self.currentList].pageDown()
			auswahl = self['menulist'].getCurrent()[0][0]
			self['name'].setText(str(auswahl))
		except Exception as e:
			print("Error occurred:", e)

	def msgdeleteBouquets(self):
		self.session.openWithCallback(self.deleteBouquets, MessageBox, _("Remove all APSATTV Favorite Bouquet?"), MessageBox.TYPE_YESNO, timeout=5, default=True)

	def deleteBouquets(self, result):
		"""
		Cleaning routine to remove any previously made changes to bouquets.
		"""
		if result:
			try:
				for fname in listdir(enigma_path):
					if 'userbouquet.wrd_' in fname or 'bouquets.tv.bak' in fname:
						Utils.purge(enigma_path, fname)
				bouquets_tv = join(enigma_path, 'bouquets.tv')
				bouquets_bak = join(enigma_path, 'bouquets.tv.bak')
				if exists(bouquets_tv):
					rename(bouquets_tv, bouquets_bak)
				else:
					print("The file 'bouquets.tv' does not exist. No changes made.")
					return
				with open(bouquets_bak, 'r') as bakfile, open(bouquets_tv, 'w') as tvfile:
					for line in bakfile:
						if '.astv_' not in line:
							tvfile.write(line)
				self.session.open(
					MessageBox,
					_('APSATTV Favorites List have been removed'),
					MessageBox.TYPE_INFO,
					timeout=5
				)
				Utils.ReloadBouquets()
			except OSError as e:
				print("OS error while editing bouquets: %s" % str(e))
			except Exception as ex:
				print("Error generic: %s" % str(ex))


class main2(Screen):
	def __init__(self, session, namex, lnk):
		Screen.__init__(self, session)
		self.session = session
		self.setup_title = ('Apsattv')
		skin = join(skin_path, 'defaultListScreen.xml')
		with open(skin, 'r') as f:
			self.skin = f.read()
		self.menulist = []
		self.currentList = 'menulist'
		self.loading_ok = False
		self.count = 0
		self.loading = 0
		# self.selectplay = selectplay()
		self.name = namex
		self.url = lnk
		self.search = ''
		self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
		self['menulist'] = free2list([])
		self["paypal"] = Label()
		self['key_red'] = Label(_('Back'))
		self['key_green'] = Label(_('Search'))
		self['key_blue'] = Label(_('Export'))
		self['key_yellow'] = Label()
		self['category'] = Label('')
		self['category'].setText(namex)
		self['title'] = Label("Thank's Apsattv")
		self['name'] = Label('')
		self['actions'] = ActionMap(
			[
				'OkCancelActions',
				'ColorActions',
				'ButtonSetupActions',
				'DirectionActions'
			],
			{
				'up': self.up,
				'down': self.down,
				'left': self.left,
				'right': self.right,
				'ok': self.ok,
				'blue': self.message2,
				'green': self.search_text,
				'cancel': self.closex,
				'red': self.closex
			},
			-1
		)

		self.timer = eTimer()
		if exists('/usr/bin/apt-get'):
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

	# use menultist for search
	def filterChannels(self, result):
		"""
		Filter channels based on search result.
		"""
		if not result:
			self.resetSearch()
			return

		self.menu_list = []
		try:
			auswahl = filter_channels(self.url, result, self.menu_list, show_)

			if self.menu_list:
				# auswahl = self['menulist'].getCurrent()[0][0]
				self['name'].setText(str(auswahl))
			else:
				self['name'].setText('No results found')
				self.resetSearch()
				return
		except Exception as e:
			print('Error finder:', e)

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
		"""
		Update channel list by reading data from m3u URL and parsing it.
		"""
		self.menu_list = []
		items = []
		try:
			req = Request(self.url)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
			r = urlopen(req, None, 15)
			content = r.read()
			r.close()

			if isinstance(content, bytes):
				try:
					content = content.decode("utf-8")
				except Exception as e:
					print("Error decoding content: %s" % str(e))
					return

			regex_with_logo = r'EXTINF.*?tvg-logo="(.*?)".*?,(.*?)\n(.*?)\n'
			regex_without_logo = r'#EXTINF.*?,(.*?)\n(.*?)\n'
			match = findall(regex_with_logo, content, DOTALL) if 'tvg-logo' in content else findall(regex_without_logo, content, DOTALL)

			for entry in match:
				if len(entry) == 3:
					pic, name, url = entry
				else:
					name, url = entry

				url = url.replace(' ', '').replace('\\n', '').strip()
				item = name.capitalize() + "###" + url + '\n'
				if item not in items:
					items.append(item)

			items.sort()
			for item in items:
				name, url = item.split("###")
				self.menu_list.append(show_(name, url))

			self['menulist'].l.setList(self.menu_list)

			if self.menu_list:
				auswahl = self['menulist'].getCurrent()[0][0]
				self['name'].setText(str(auswahl))
			else:
				self['name'].setText('No results found')

		except URLError as e:
			print("URL connection error: %s" % str(e))
		except Exception as e:
			print("Error generic: %s" % str(e))

	def ok(self):
		try:
			i = self['menulist'].getSelectedIndex()
			self.currentindex = i
			selection = self['menulist'].l.getCurrentSelection()
			if selection is not None:
				item = self.menu_list[i][0]
				name = item[0]
				url = item[1]
			self.play_that_shit(url, name, self.currentindex, item, self.menu_list)
		except Exception as error:
			print('error as:', error)

	def play_that_shit(self, url, name, index, item, menu_list):
		self.session.open(Playstream2, name, url, index, item, menu_list)

	def up(self):
		try:
			self[self.currentList].up()
			auswahl = self['menulist'].getCurrent()[0][0]
			self['name'].setText(str(auswahl))
		except Exception as e:
			print("Error occurred:", e)

	def down(self):
		try:
			self[self.currentList].down()
			auswahl = self['menulist'].getCurrent()[0][0]
			self['name'].setText(str(auswahl))
		except Exception as e:
			print("Error occurred:", e)

	def left(self):
		try:
			self[self.currentList].pageUp()
			auswahl = self['menulist'].getCurrent()[0][0]
			self['name'].setText(str(auswahl))
		except Exception as e:
			print("Error occurred:", e)

	def right(self):
		try:
			self[self.currentList].pageDown()
			auswahl = self['menulist'].getCurrent()[0][0]
			self['name'].setText(str(auswahl))
		except Exception as e:
			print("Error occurred:", e)

	def message2(self, answer=None):
		if answer is None:
			self.session.openWithCallback(self.message2, MessageBox, _('Do you want to Convert to favorite .tv ?\n\nAttention!! It may take some time depending\non the number of streams contained !!!'))
		elif answer:
			print('url: ', self.url)
			service = '4097'
			ch = 0
			ch = self.convert_bouquet(service)
			if ch > 0:
				_session.open(MessageBox, _('bouquets reloaded..\nWith %s channel' % str(ch)), MessageBox.TYPE_INFO, timeout=5)
			else:
				_session.open(MessageBox, _('Download Error'), MessageBox.TYPE_INFO, timeout=5)

	def convert_bouquet(self, service):
		from time import sleep
		type = 'tv'
		if "radio" in self.name.lower():
			type = "radio"
		name_file = self.name.replace('/', '_').replace(',', '').replace('hasbahca', 'hbc')
		clean_name = sub(r'[\<\>\:\"\/\\\|\?\*]', '_', str(name_file))
		clean_name = sub(r' ', '_', clean_name)
		clean_name = sub(r'\d+:\d+:[\d.]+', '_', clean_name)
		name_file = sub(r'_+', '_', clean_name)
		bouquet_name = 'userbouquet.astv_%s.%s' % (name_file.lower(), type.lower())
		files = ''
		if exists(str(dowm3u)):
			files = str(dowm3u) + str(name_file) + '.m3u'
		else:
			files = '/tmp/' + str(name_file) + '.m3u'
		if isfile(files):
			remove(files)
		url_m3u = self.url.strip()
		if PY3:
			url_m3u.encode()
		import six
		content = Utils.getUrl(url_m3u)
		if six.PY3:
			content = six.ensure_str(content)
		with open(files, 'wb') as f1:
			f1.write(content.encode())
			f1.close()
		sleep(5)
		ch = 0

		try:
			if isfile(files) and stat(files).st_size > 0:
				print('ChannelList is_tmp exist in playlist')
				desk_tmp = ''
				in_bouquets = 0
				with open('%s%s' % (enigma_path, bouquet_name), 'w') as outfile:
					outfile.write('#NAME %s\r\n' % name_file.capitalize())
					for line in open(files):
						if line.startswith('http://') or line.startswith('https'):
							outfile.write('#SERVICE %s:0:1:1:0:0:0:0:0:0:%s' % (service, line.replace(':', '%3a')))
							outfile.write('#DESCRIPTION %s' % desk_tmp)
						elif line.startswith('#EXTINF'):
							desk_tmp = '%s' % line.split(',')[-1]
						elif '<stream_url><![CDATA' in line:
							outfile.write('#SERVICE %s:0:1:1:0:0:0:0:0:0:%s\r\n' % (service, line.split('[')[-1].split(']')[0].replace(':', '%3a')))
							outfile.write('#DESCRIPTION %s\r\n' % desk_tmp)
						elif '<title>' in line:
							if '<![CDATA[' in line:
								desk_tmp = '%s\r\n' % line.split('[')[-1].split(']')[0]
							else:
								desk_tmp = '%s\r\n' % line.split('<')[1].split('>')[1]
						ch += 1
					outfile.close()
				if isfile('/etc/enigma2/bouquets.tv'):
					for line in open('/etc/enigma2/bouquets.tv'):
						if bouquet_name in line:
							in_bouquets = 1
					if in_bouquets == 0:
						if isfile('%s%s' % (enigma_path, bouquet_name)) and isfile('/etc/enigma2/bouquets.tv'):
							Utils.remove_line('/etc/enigma2/bouquets.tv', bouquet_name)
							with open('/etc/enigma2/bouquets.tv', 'a+') as outfile:
								outfile.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "%s" ORDER BY bouquet\r\n' % bouquet_name)
								outfile.close()
								in_bouquets = 1
					Utils.ReloadBouquets()
			return ch
		except Exception as e:
			print('error convert iptv ', str(e))


class TvInfoBarShowHide():
	""" InfoBar show/hide control, accepts toggleShow and hide actions, might start
	fancy animations. """
	STATE_HIDDEN = 0
	STATE_HIDING = 1
	STATE_SHOWING = 2
	STATE_SHOWN = 3
	skipToggleShow = False

	def __init__(self):
		self["ShowHideActions"] = ActionMap(
			["InfobarShowHideActions"],
			{
				"toggleShow": self.OkPressed,
				"hide": self.hide
			},
			0
		)
		self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evStart: self.serviceStarted})
		self.__state = self.STATE_SHOWN
		self.__locked = 0
		self.hideTimer = eTimer()
		try:
			self.hideTimer_conn = self.hideTimer.timeout.connect(self.doTimerHide)
		except:
			self.hideTimer.callback.append(self.doTimerHide)
		self.hideTimer.start(3000, True)
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

	def debug(self, obj, text=""):
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

	def __init__(self, session, name, url, index, item, menu_list):
		global streaml
		Screen.__init__(self, session)
		self.session = session
		self.skinName = 'MoviePlayer'
		streaml = False
		self.current_channel_index = index
		self.item = item
		self.itemscount = len(menu_list)
		self.menu_list = menu_list
		self.name = html_conv.html_unescape(name)
		self.url = url.replace('%0a', '').replace('%0A', '')
		self.state = self.STATE_PLAYING
		self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
		"""Initialize infobar components."""
		for x in (
			InfoBarBase,
			InfoBarMenu,
			InfoBarSeek,
			InfoBarAudioSelection,
			InfoBarSubtitleSupport,
			InfoBarNotifications,
			TvInfoBarShowHide,
		):
			x.__init__(self)
		self.service = None
		self['actions'] = ActionMap(
			[
				'ChannelSelectBaseActions',
				'ButtonSetupActions',
				'ColorActions',
				'InfobarActions',
				'InfobarEPGActions',
				'InfobarSeekActions',
				'InfobarShowHideActions',
				'MoviePlayerActions',
				'MediaPlayerSeekActions',
				'MovieSelectionActions',
				'OkCancelActions'
			],
			{
				'leavePlayer': self.cancel,
				'prevBouquet': self.keyDown,
				'nextBouquet': self.keyUp,
				'epg': self.showIMDB,
				'info': self.showIMDB,
				'tv': self.cicleStreamType,
				'stop': self.leavePlayer,
				'playpauseService': self.playpauseService,
				'red': self.cicleStreamType,
				'cancel': self.cancel,
				'exit': self.leavePlayer,
				'yellow': self.subtitles,
				'back': self.cancel,
				'keyUDown': self.keyDown,
				'keyUp': self.keyUp,
			},
			-1
		)

		if '8088' in str(self.url):
			# self.onLayoutFinish.append(self.slinkPlay)
			self.onFirstExecBegin.append(self.slinkPlay)
		else:
			# self.onLayoutFinish.append(self.cicleStreamType)
			self.onFirstExecBegin.append(self.cicleStreamType)
		self.onClose.append(self.cancel)

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
		sref.setName(str(name))
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
		sref.setName(str(name))
		self.session.nav.stopService()
		self.session.nav.playService(sref)

	def subtitles(self):
		self.session.open(MessageBox, _('Please install SubSupport Plugins'), MessageBox.TYPE_ERROR, timeout=10)

	def keyUp(self):
		currentindex = int(self.current_channel_index) + 1
		if currentindex == self.itemscount:
			currentindex = 0
		self.current_channel_index = currentindex
		i = self.current_channel_index
		item = self.menu_list[i][0]
		self.name = item[0]
		self.url = item[1]
		self.cicleStreamType()

	def keyDown(self):
		currentindex = int(self.current_channel_index) - 1
		if currentindex < 0:
			currentindex = self.itemscount - 1
		self.current_channel_index = currentindex
		i = self.current_channel_index
		item = self.menu_list[i][0]
		self.name = item[0]
		self.url = item[1]
		self.cicleStreamType()

	def cicleStreamType(self):
		self.servicetype = '4097'
		if not self.url.startswith('http'):
			self.url = 'http://' + self.url
		url = str(self.url)
		if str(splitext(self.url)[-1]) == ".m3u8":
			if self.servicetype == "1":
				self.servicetype = "4097"
		self.openTest(self.servicetype, url)

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
		if exists('/tmp/hls.avi'):
			remove('/tmp/hls.avi')
		self.session.nav.stopService()
		self.session.nav.playService(self.srefInit)
		aspect_manager.restore_aspect()
		self.close()

	def leavePlayer(self):
		self.cancel()


def main(session, **kwargs):
	try:
		session.open(Apsattv)
	except:
		import traceback
		traceback.print_exc()


def Plugins(**kwargs):
	ico_path = 'plugin.png'
	# extDescriptor = PluginDescriptor(name=name_plugin, description=desc_plugin, where=[PluginDescriptor.WHERE_EXTENSIONSMENU], icon=ico_path, fnc=main)
	result = [PluginDescriptor(name=name_plugin, description=desc_plugin, where=PluginDescriptor.WHERE_PLUGINMENU, icon=ico_path, fnc=main)]
	# result.append(extDescriptor)
	return result
