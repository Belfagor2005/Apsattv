# -*- coding: utf-8 -*-

from __future__ import absolute_import
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
import gettext

__author__ = "Lululla"
__email__ = "ekekaz@gmail.com"
__copyright__ = 'Copyright (c) 2024 Lululla'
__license__ = "GPL-v2"
__version__ = "1.5"

PluginLanguageDomain = 'Apsattv'
PluginLanguagePath = 'Extensions/Apsattv/res/locale'
host22 = 'aHR0cDovL3d3dy5hcHNhdHR2LmNvbS9zdHJlYW1zLmh0bWw='


def paypal():
    conthelp = "If you like what I do you\n"
    conthelp += "can contribute with a coffee\n"
    conthelp += "scan the qr code and donate € 1.00"
    return conthelp


def localeInit():
    gettext.bindtextdomain(
        PluginLanguageDomain,
        resolveFilename(
            SCOPE_PLUGINS,
            PluginLanguagePath))


def _(txt):
    translated = gettext.dgettext(PluginLanguageDomain, txt)
    if translated:
        return translated
    else:
        print(("[%s] fallback to default translation for %s" %
              (PluginLanguageDomain, txt)))
        return gettext.gettext(txt)


localeInit()
language.addCallback(localeInit)
