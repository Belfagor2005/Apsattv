#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 17.04.2026
# a common tips used from Lululla

from Components.config import config
from enigma import getDesktop
from os.path import isdir, exists, realpath, dirname, join, isfile
from os import system, stat, statvfs, listdir, remove, chmod, popen
from random import choice
import base64
import datetime
import re
import requests
import ssl
import sys
import html.entities
from urllib.parse import quote
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)

screenwidth = getDesktop(0).size()

ssl_context = ssl.create_default_context()
# Disable SSLv2, SSLv3, TLS1.0 and TLS1.1 explicitly
ssl_context.options |= ssl.OP_NO_SSLv2
ssl_context.options |= ssl.OP_NO_SSLv3
ssl_context.options |= ssl.OP_NO_TLSv1
ssl_context.options |= ssl.OP_NO_TLSv1_1

try:
    from Components.AVSwitch import AVSwitch
except ImportError:
    from Components.AVSwitch import eAVControl as AVSwitch


text_type = str
binary_type = bytes
MAXSIZE = sys.maxsize

_UNICODE_MAP = {
    k: chr(v) for k, v in html.entities.name2codepoint.items()
}
_ESCAPE_RE = re.compile(r"[&<>\"']")
_UNESCAPE_RE = re.compile(r"&\s*(#?)(\w+?)\s*;")
_ESCAPE_DICT = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&apos;",
}


def unicodify(s, encoding='utf-8', norm=None):
    if not isinstance(s, str):
        s = str(s, encoding)
    if norm:
        from unicodedata import normalize
        s = normalize(norm, s)
    return s


def installed(plugin_name):
    """Check if an Enigma2 plugin is installed in the Extensions directory."""
    from Tools.Directories import resolveFilename, SCOPE_PLUGINS
    path = resolveFilename(SCOPE_PLUGINS, "Extensions/" + plugin_name)
    return exists(path)


def checktoken(token):
    import base64
    import zlib
    result = base64.b64decode(token)
    result = zlib.decompress(base64.b64decode(result))
    result = base64.b64decode(result).decode()
    return result


def getEncodedString(value):
    returnValue = ""
    try:
        returnValue = value.encode("utf-8", 'ignore')
    except UnicodeDecodeError:
        try:
            returnValue = value.encode("iso8859-1", 'ignore')
        except UnicodeDecodeError:
            try:
                returnValue = value.decode("cp1252").encode("utf-8")
            except UnicodeDecodeError:
                returnValue = "n/a"
    return returnValue


def ensure_str(s, encoding="utf-8", errors="strict"):
    if isinstance(s, str):
        return s
    if isinstance(s, binary_type):
        return s.decode(encoding, errors)
    raise TypeError(f"not expecting type '{type(s).__name__}'")


def html_escape(value):
    """Escape HTML special characters"""
    return _ESCAPE_RE.sub(lambda m: _ESCAPE_DICT[m.group(0)], value.strip())


def html_unescape(value):
    """Unescape HTML entities"""
    return _UNESCAPE_RE.sub(_convert_entity, ensure_str(value).strip())


def _convert_entity(m):
    """Helper for HTML entity conversion"""
    if m.group(1) == "#":
        try:
            if m.group(2)[:1].lower() == "x":
                return chr(int(m.group(2)[1:], 16))
            else:
                return chr(int(m.group(2)))
        except ValueError:
            return f"&#{m.group(2)};"
    return _UNICODE_MAP.get(m.group(2), f"&{m.group(2)};")


def checkGZIP(url):
    from io import BytesIO
    import gzip
    hdr = {"User-Agent": "Enigma2 - Plugin"}
    request = Request(url, headers=hdr)

    try:
        response = urlopen(request, timeout=10)

        if response.info().get('Content-Encoding') == 'gzip':
            buffer = BytesIO(response.read())
            deflatedContent = gzip.GzipFile(fileobj=buffer)
            return deflatedContent.read().decode('utf-8')
        else:
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        return None


sslverify = False
try:
    from twisted.internet import ssl
    from twisted.internet._sslverify import ClientTLSOptions
    sslverify = True
except ImportError:
    pass

if sslverify:
    class SNIFactory(ssl.ClientContextFactory):
        def __init__(self, hostname=None):
            self.hostname = hostname

        def getContext(self):
            ctx = self._contextFactory(self.method)
            if self.hostname:
                ClientTLSOptions(self.hostname, ctx)
            return ctx


def ssl_urlopen(url):
    return urlopen(url, context=ssl_context)


class AspectManager:
    """Manages aspect ratio settings for the plugin"""

    def __init__(self):
        self.init_aspect = self.get_current_aspect()
        print("[INFO] Initial aspect ratio:", self.init_aspect)

    def get_current_aspect(self):
        """Get current aspect ratio setting"""
        try:
            return int(AVSwitch().getAspectRatioSetting())
        except Exception as e:
            print("[ERROR] Failed to get aspect ratio:", str(e))
            return 0

    def restore_aspect(self):
        """Restore original aspect ratio"""
        try:
            print("[INFO] Restoring aspect ratio to:", self.init_aspect)
            AVSwitch().setAspectRatio(self.init_aspect)
        except Exception as e:
            print("[ERROR] Failed to restore aspect ratio:", str(e))


aspect_manager = AspectManager()


def getDesktopSize():
    from enigma import getDesktop
    s = getDesktop(0).size()
    return (s.width(), s.height())


def isUHD():
    return screenwidth.width() == 2560


def isFHD():
    return screenwidth.width() == 1920


def isHD():
    return screenwidth.width() == 1280


def DreamOS():
    return exists('/var/lib/dpkg/status')


def mountipkpth():
    try:
        from Tools.Directories import fileExists
        myusb = myusb1 = myhdd = myhdd2 = mysdcard = mysd = myuniverse = myba = mydata = ''
        mdevices = []
        myusb = None
        myusb1 = None
        myhdd = None
        myhdd2 = None
        mysdcard = None
        mysd = None
        myuniverse = None
        myba = None
        mydata = None
        if fileExists('/proc/mounts'):
            with open('/proc/mounts', 'r') as f:
                for line in f.readlines():
                    if line.find('/media/usb') != -1:
                        myusb = '/media/usb/picon'
                        if not exists('/media/usb/picon'):
                            system('mkdir -p /media/usb/picon')
                    elif line.find('/media/usb1') != -1:
                        myusb1 = '/media/usb1/picon'
                        if not exists('/media/usb1/picon'):
                            system('mkdir -p /media/usb1/picon')
                    elif line.find('/media/hdd') != -1:
                        myhdd = '/media/hdd/picon'
                        if not exists('/media/hdd/picon'):
                            system('mkdir -p /media/hdd/picon')
                    elif line.find('/media/hdd2') != -1:
                        myhdd2 = '/media/hdd2/picon'
                        if not exists('/media/hdd2/picon'):
                            system('mkdir -p /media/hdd2/picon')
                    elif line.find('/media/sdcard') != -1:
                        mysdcard = '/media/sdcard/picon'
                        if not exists('/media/sdcard/picon'):
                            system('mkdir -p /media/sdcard/picon')
                    elif line.find('/media/sd') != -1:
                        mysd = '/media/sd/picon'
                        if not exists('/media/sd/picon'):
                            system('mkdir -p /media/sd/picon')
                    elif line.find('/universe') != -1:
                        myuniverse = '/universe/picon'
                        if not exists('/universe/picon'):
                            system('mkdir -p /universe/picon')
                    elif line.find('/media/ba') != -1:
                        myba = '/media/ba/picon'
                        if not exists('/media/ba/picon'):
                            system('mkdir -p /media/ba/picon')
                    elif line.find('/data') != -1:
                        mydata = '/data/picon'
                        if not exists('/data/picon'):
                            system('mkdir -p /data/picon')
        if myusb:
            mdevices.append(myusb)
        if myusb1:
            mdevices.append(myusb1)
        if myhdd:
            mdevices.append(myhdd)
        if myhdd2:
            mdevices.append(myhdd2)
        if mysdcard:
            mdevices.append(mysdcard)
        if mysd:
            mdevices.append(mysd)
        if myuniverse:
            mdevices.append(myuniverse)
        if myba:
            mdevices.append(myba)
        if mydata:
            mdevices.append(mydata)
    except Exception as e:
        print(e)
    mdevices.append('/picon')
    mdevices.append('/usr/share/enigma2/picon')
    return mdevices


def getEnigmaVersionString():
    try:
        from enigma import getEnigmaVersionString
        return getEnigmaVersionString()
    except BaseException:
        return "N/A"


def getImageVersionString():
    try:
        from Tools.Directories import resolveFilename, SCOPE_SYSETC
        with open(resolveFilename(SCOPE_SYSETC, 'image-version'), 'r') as file:
            lines = file.readlines()
            for x in lines:
                splitted = x.split('=')
                if splitted[0] == "version":
                    version = splitted[1]
                    image_type = version[0]  # 0 = release, 1 = experimental
                    major = version[1]
                    minor = version[2]
                    revision = version[3]
                    year = version[4:8]
                    month = version[8:10]
                    day = version[10:12]
                    date = '-'.join((year, month, day))
                    if image_type == '0':
                        image_type = "Release"
                    else:
                        image_type = "Experimental"
                    version = '.'.join((major, minor, revision))
                    if version != '0.0.0':
                        return ' '.join((image_type, version, date))
                    else:
                        return ' '.join((image_type, date))
    except IOError:
        pass

    return "unavailable"


def mySkin():
    from Components.config import config
    currentSkin = config.skin.primary_skin.value.replace('/skin.xml', '')
    return currentSkin


def getFreeMemory():
    mem_free = None
    mem_total = None
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f.readlines():
                if line.find('MemFree') != -1:
                    parts = line.strip().split()
                    mem_free = float(parts[1])
                elif line.find('MemTotal') != -1:
                    parts = line.strip().split()
                    mem_total = float(parts[1])
    except BaseException:
        pass
    return (mem_free, mem_total)


def sizeToString(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    size = "0 B"
    if nbytes > 0:
        i = 0
        while nbytes >= 1024 and i < len(suffixes) - 1:
            nbytes /= 1024.
            i += 1
        f = ('%.2f' % nbytes).rstrip('0').rstrip('.').replace(".", ",")
        size = '%s %s' % (f, suffixes[i])
    return size


def convert_size(size_bytes):
    import math
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes // p, 2)
    return "%s %s" % (s, size_name[i])


def getMountPoint(path):
    pathname = realpath(path)
    parent_device = stat(pathname).st_dev
    path_device = stat(pathname).st_dev
    mount_point = ""
    while parent_device == path_device:
        mount_point = pathname
        pathname = dirname(pathname)
        if pathname == mount_point:
            break
        parent_device = stat(pathname).st_dev
    return mount_point


def getMointedDevice(pathname):
    md = None
    try:
        with open("/proc/mounts", "r") as f:
            for line in f:
                fields = line.rstrip('\n').split()
                if fields[1] == pathname:
                    md = fields[0]
                    break
    except BaseException:
        pass
    return md


def getFreeSpace(path):
    try:
        moin_point = getMountPoint(path)
        device = getMointedDevice(moin_point)
        print(moin_point + "|" + device)
        stat = statvfs(device)  # @UndefinedVariable
        print(stat)
        return sizeToString(stat.f_bfree * stat.f_bsize)
    except BaseException:
        return "N/A"


def listDir(what):
    f = None
    try:
        f = listdir(what)
    except BaseException:
        pass
    return f


def purge(directory, pattern):
    """Delete files matching pattern in directory"""
    from re import search
    for f in listdir(directory):
        file_path = join(directory, f)
        if isfile(file_path) and search(pattern, f):
            remove(file_path)


def getLanguage():
    try:
        from Components.config import config
        language = config.osd.language.value
        language = language[:-3]
    except BaseException:
        language = 'en'
    return language


def downloadFile(url, target):
    import socket
    try:
        response = urlopen(url, None, 15)
        with open(target, 'wb') as output:
            output.write(response.read())
        response.close()
        return True
    except HTTPError:
        print('Http error')
        return False
    except URLError:
        print('Url error')
        return False
    except socket.timeout:
        print('socket error')
        return False


def downloadFilest(url, target):
    try:
        req = Request(url)
        req.add_header(
            'User-Agent',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = ssl_urlopen(req)
        with open(target, 'wb') as output:
            output.write(response.read())
        return True
    except HTTPError as e:
        print('HTTP Error code: ', e.code)
    except URLError as e:
        print('URL Error: ', e.reason)


def defaultMoviePath():
    result = config.usage.default_path.value
    if not isdir(result):
        from Tools import Directories
        return Directories.defaultRecordingLocation(
            config.usage.default_path.value)
    return result


if not isdir(config.movielist.last_videodir.value):
    try:
        config.movielist.last_videodir.value = defaultMoviePath()
        config.movielist.last_videodir.save()
    except BaseException:
        pass
downloadm3u = config.movielist.last_videodir.value


def getserviceinfo(service_ref):
    """Get service name and URL from service reference"""
    try:
        from ServiceReference import ServiceReference
        ref = ServiceReference(service_ref)
        return ref.getServiceName(), ref.getPath()
    except Exception:
        return None, None


def sortedDictKeys(adict):
    keys = list(adict.keys())
    keys.sort()
    return keys


def daterange(start_date, end_date):
    for n in range((end_date - start_date).days + 1):
        yield end_date - datetime.timedelta(n)


global CountConnOk
CountConnOk = 0


def zCheckInternet(opt=1, server=None, port=None):
    global CountConnOk
    sock = False
    checklist = [("8.8.44.4", 53), ("8.8.88.8", 53), ("www.lululla.altervista.org/",
                                                      80), ("www.linuxsat-support.com", 443), ("www.google.com", 443)]
    if opt < 5:
        srv = checklist[opt]
    else:
        srv = (server, port)
    try:
        import socket
        socket.setdefaulttimeout(0.5)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(srv)
        sock = True
        CountConnOk = 0
        print('Status Internet: %s:%s -> OK' % (srv[0], srv[1]))
    except BaseException:
        sock = False
        print('Status Internet: %s:%s -> KO' % (srv[0], srv[1]))
        if CountConnOk == 0 and opt != 2 and opt != 3:
            CountConnOk = 1
            print('Restart Check 1 Internet.')
            return zCheckInternet(0)
        elif CountConnOk == 1 and opt != 2 and opt != 3:
            CountConnOk = 2
            print('Restart Check 2 Internet.')
            return zCheckInternet(4)
    return sock


def checkInternet():
    try:
        import socket
        socket.setdefaulttimeout(0.5)
        socket.socket(
            socket.AF_INET, socket.SOCK_STREAM).connect(
            ('8.8.8.8', 53))
        return True
    except BaseException:
        return False


def check(url):
    import socket
    try:
        response = urlopen(url, None, 15)
        response.close()
        return True
    except HTTPError:
        return False
    except URLError:
        return False
    except socket.timeout:
        return False


def testWebConnection(host='www.google.com', port=80, timeout=3):
    import socket
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as e:
        print('error: ', e)
        return False


def checkStr(text, encoding='utf8'):
    if isinstance(text, bytes):
        text = text.decode('utf-8')
    return text


def str_encode(text, encoding="utf8"):
    return str(text)


def checkRedirect(url):
    import requests
    from requests.adapters import HTTPAdapter
    hdr = {"User-Agent": "Enigma2 - Enigma2 Plugin"}
    x = ""
    adapter = HTTPAdapter()
    http = requests.Session()
    http.mount("http://", adapter)
    http.mount("https://", adapter)
    try:
        x = http.get(url, headers=hdr, timeout=15, verify=False, stream=True)
        return str(x.url)
    except Exception as e:
        print(e)
        return str(url)


def freespace():
    try:
        diskSpace = statvfs('/')
        capacity = float(diskSpace.f_bsize * diskSpace.f_blocks)
        available = float(diskSpace.f_bsize * diskSpace.f_bavail)
        fspace = round(float(available / 1048576.0), 2)
        tspace = round(float(capacity / 1048576.0), 1)
        spacestr = 'Free space(' + str(fspace) + \
            'MB) Total space(' + str(tspace) + 'MB)'
        return spacestr
    except BaseException:
        return ''


def b64encoder(source):
    if isinstance(source, str):
        source = source.encode('utf-8')
    content = base64.b64encode(source).decode('utf-8')
    return content


def b64decoder(data):
    """Robust base64 decoding with padding correction"""
    data = data.strip()
    pad = len(data) % 4
    if pad == 1:  # Invalid base64 length
        return ""
    if pad:
        data += "=" * (4 - pad)
    try:
        decoded = base64.b64decode(data)
        return decoded.decode('utf-8')
    except Exception as e:
        print("Base64 decoding error: %s" % e)
        return ""


is_tmdb = False
is_TMDB = False
is_imdb = False
tmdb = None
TMDB = None
imdb = None

try:
    from Plugins.Extensions.tmdb import tmdb
    is_tmdb = True
except ImportError:
    pass

try:
    from Plugins.Extensions.IMDb.plugin import main as imdb
    is_imdb = True
except Exception as e:
    print("error:", e)

try:
    from Plugins.Extensions.TMDB import TMDB
    is_TMDB = True
except Exception as e:
    print("error:", e)


print("is_tmdb =", is_tmdb)
print("is_TMDB =", is_TMDB)
print("is_imdb =", is_imdb)


def substr(data, start, end):
    i1 = data.find(start)
    i2 = data.find(end, i1)
    return data[i1:i2]


def uniq(inlist):
    uniques = []
    for item in inlist:
        if item not in uniques:
            uniques.append(item)
    return uniques


def ReloadBouquets():
    """Reload Enigma2 bouquets and service lists"""
    from enigma import eDVBDB
    db = eDVBDB.getInstance()
    db.reloadServicelist()
    db.reloadBouquets()


def deletetmp():
    system('rm -rf /tmp/unzipped;rm -f /tmp/*.ipk;rm -f /tmp/*.tar;rm -f /tmp/*.zip;rm -f /tmp/*.tar.gz;rm -f /tmp/*.tar.bz2;rm -f /tmp/*.tar.tbz2;rm -f /tmp/*.tar.tbz;rm -f /tmp/*.m3u')


def del_jpg():
    import glob
    for i in glob.glob(join('/tmp', '*.jpg')):
        try:
            chmod(i, 0o777)
            remove(i)
        except OSError:
            pass


def OnclearMem():
    try:
        system('sync')
        system('echo 1 > /proc/sys/vm/drop_caches')
        system('echo 2 > /proc/sys/vm/drop_caches')
        system('echo 3 > /proc/sys/vm/drop_caches')
    except BaseException:
        pass


def MemClean():
    """Clear system memory cache"""
    try:
        system('sync')
        for i in range(1, 4):
            system("echo " + str(i) + " > /proc/sys/vm/drop_caches")
    except Exception:
        pass


def findSoftCamKey():
    paths = ['/usr/keys',
             '/etc/tuxbox/config/oscam-emu',
             '/etc/tuxbox/config/oscam-trunk',
             '/etc/tuxbox/config/oscam',
             '/etc/tuxbox/config/ncam',
             '/etc/tuxbox/config/gcam',
             '/etc/tuxbox/config',
             '/etc',
             '/var/keys']
    from os import path as os_path
    if os_path.exists('/tmp/.oscam/oscam.version'):
        with open('/tmp/.oscam/oscam.version', 'r') as f:
            data = f.readlines()
    elif os_path.exists('/tmp/.ncam/ncam.version'):
        with open('/tmp/.ncam/ncam.version', 'r') as f:
            data = f.readlines()
    elif os_path.exists('/tmp/.gcam/gcam.version'):
        with open('/tmp/.gcam/gcam.version', 'r') as f:
            data = f.readlines()
            for line in data:
                if 'configdir:' in line.lower():
                    paths.insert(0, line.split(':')[1].strip())
    for path in paths:
        softcamkey = os_path.join(path, 'SoftCam.Key')
        print('[key] the %s exists %d' %
              (softcamkey, os_path.exists(softcamkey)))
        if os_path.exists(softcamkey):
            return softcamkey
        else:
            return '/usr/keys/SoftCam.Key'
    return '/usr/keys/SoftCam.Key'


def web_info(message):
    try:
        from urllib.parse import quote_plus
        message = quote_plus(message)
        cmd = "wget -qO - 'http://127.0.0.1/web/message?type=2&timeout=10&text=%s' > /dev/null 2>&1 &" % message
        popen(cmd)
    except Exception as e:
        print('error: ', e)
        print('web_info ERROR')


def trace_error():
    import traceback
    try:
        traceback.print_exc(file=sys.stdout)
        traceback.print_exc(file=open('/tmp/Error.log', 'a'))
    except Exception as e:
        print('error: ', e)
        pass


def log(label, data):
    data = str(data)
    open('/tmp/my__debug.log', 'a').write('\n' + label + ':>' + data)


def ConverDate(data):
    year = data[:2]
    month = data[-4:][:2]
    day = data[-2:]
    return day + '-' + month + '-20' + year


def ConverDateBack(data):
    year = data[-2:]
    month = data[-7:][:2]
    day = data[:2]
    return year + month + day


def isPythonFolder():
    path = '/usr/lib/'
    for name in listdir(path):
        fullname = path + name
        if not isfile(fullname) and 'python' in fullname:
            print(fullname)
            import sys
            print("sys.version_info =", sys.version_info)
            pythonvr = fullname
            print('pythonvr is ', pythonvr)
            x = ('%s/site-packages/streamlink' % pythonvr)
            print(x)
    return x


def isStreamlinkAvailable():
    pythonvr = isPythonFolder()
    return pythonvr


def isExtEplayer3Available():
    from enigma import eEnv
    return isfile(eEnv.resolve('$bindir/exteplayer3'))


def AdultUrl(url):
    req = Request(url)
    req.add_header(
        'User-Agent',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    r = urlopen(req, None, 15)
    link = r.read()
    r.close()
    tlink = link
    if isinstance(tlink, bytes):
        try:
            tlink = tlink.decode("utf-8")
        except Exception as e:
            print('error: ', e)
    return tlink


std_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Accept-Charset': 'utf-8, ISO-8859-1;q=0.7, *;q=0.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}

ListAgent = [
    # Chrome / Edge (Windows)
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    # Firefox (Windows)
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    # macOS
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    # Linux
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
    # Android
    'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36',
    # iOS
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
]


def RequestAgent():
    RandomAgent = choice(ListAgent)
    return RandomAgent


def make_request(url):
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            return requests.get(
                url,
                headers={'User-Agent': RequestAgent()},
                timeout=15,
                verify=False,
                stream=True).text
    except ImportError:
        req = Request(url)
        req.add_header('User-Agent', 'E2 Plugin')
        response = urlopen(req, None, 10)
        link = response.read().decode('utf-8')
        response.close()
        return link
    return None


def ReadUrl2(url, referer):
    TIMEOUT_URL = 30
    print('ReadUrl1:\n  url = %s' % url)
    try:
        req = Request(url)
        req.add_header('User-Agent', RequestAgent())
        req.add_header('Referer', referer)
        try:
            r = urlopen(req, None, TIMEOUT_URL, context=ssl_context)
        except Exception as e:
            r = urlopen(req, None, TIMEOUT_URL)
            print('CreateLog Codifica ReadUrl: %s.' % e)
        link = r.read()
        r.close()

        dec = 'Null'
        dcod = 0
        tlink = link
        if isinstance(link, bytes):
            try:
                tlink = link.decode('utf-8')
                dec = 'utf-8'
            except Exception as e:
                dcod = 1
                print('ReadUrl2 - Error: ', e)
            if dcod == 1:
                dcod = 0
                try:
                    tlink = link.decode('cp437')
                    dec = 'cp437'
                except Exception as e:
                    dcod = 1
                    print('ReadUrl3 - Error:', e)
            if dcod == 1:
                dcod = 0
                try:
                    tlink = link.decode('iso-8859-1')
                    dec = 'iso-8859-1'
                except Exception as e:
                    dcod = 1
                    print('CreateLog Codific ReadUrl: ', e)
            link = tlink
        else:
            dec = 'str'

        print('CreateLog Codifica ReadUrl: %s.' % dec)
    except Exception as e:
        print('ReadUrl5 - Error: ', e)
        link = None
    return link


def ReadUrl(url):
    TIMEOUT_URL = 30
    print('ReadUrl1:\n  url = %s' % url)
    try:
        req = Request(url)
        req.add_header('User-Agent', RequestAgent())
        try:
            r = urlopen(req, None, TIMEOUT_URL, context=ssl_context)
        except Exception as e:
            r = urlopen(req, None, TIMEOUT_URL)
            print('CreateLog Codifica ReadUrl: %s.' % e)
        link = r.read()
        r.close()

        dec = 'Null'
        dcod = 0
        tlink = link
        if isinstance(link, bytes):
            try:
                tlink = link.decode('utf-8')
                dec = 'utf-8'
            except Exception as e:
                dcod = 1
                print('ReadUrl2 - Error: ', e)
            if dcod == 1:
                dcod = 0
                try:
                    tlink = link.decode('cp437')
                    dec = 'cp437'
                except Exception as e:
                    dcod = 1
                    print('ReadUrl3 - Error:', e)
            if dcod == 1:
                dcod = 0
                try:
                    tlink = link.decode('iso-8859-1')
                    dec = 'iso-8859-1'
                except Exception as e:
                    dcod = 1
                    print('CreateLog Codific ReadUrl: ', e)
            link = tlink
        else:
            dec = 'str'

        print('CreateLog Codifica ReadUrl: %s.' % dec)
    except Exception as e:
        print('ReadUrl5 - Error: ', e)
        link = None
    return link


def getUrl(url):
    req = Request(url)
    req.add_header('User-Agent', RequestAgent())
    try:
        response = urlopen(req, timeout=10, context=ssl_context)
        link = response.read().decode(errors='ignore')
        response.close()
        return link
    except Exception as e:
        print(e)
        return ""


def getUrl2(url, referer):
    req = Request(url)
    req.add_header('User-Agent', RequestAgent())
    req.add_header('Referer', referer)
    try:
        response = urlopen(req, timeout=10, context=ssl_context)
        link = response.read().decode()
        response.close()
        return link
    except BaseException:
        response = urlopen(req, timeout=10, context=ssl_context)
        link = response.read().decode()
        response.close()
        return link


def getUrlresp(url):
    req = Request(url)
    req.add_header('User-Agent', RequestAgent())
    try:
        response = urlopen(req, timeout=10, context=ssl_context)
    except BaseException:
        response = urlopen(req, timeout=10, context=ssl_context)
    return response


def decodeUrl(text):
    text = text.replace('%20', ' ')
    text = text.replace('%21', '!')
    text = text.replace('%22', '"')
    text = text.replace('%23', '&')
    text = text.replace('%24', '$')
    text = text.replace('%25', '%')
    text = text.replace('%26', '&')
    text = text.replace('%2B', '+')
    text = text.replace('%2F', '/')
    text = text.replace('%3A', ':')
    text = text.replace('%3B', ';')
    text = text.replace('%3D', '=')
    text = text.replace('&#x3D;', '=')
    text = text.replace('%3F', '?')
    text = text.replace('%40', '@')
    return text


def normalize(title):
    try:
        import unicodedata
        try:
            return title.decode('ascii').encode("utf-8")
        except BaseException:
            pass

        return str(
            ''.join(
                c for c in unicodedata.normalize(
                    'NFKD', title) if unicodedata.category(c) != 'Mn'))
    except BaseException:
        return title


def get_safe_filename(filename, fallback=''):
    '''Convert filename to safe filename'''
    import unicodedata
    import re
    name = filename.replace(' ', '_').replace('/', '_')
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore')
    name = re.sub(b'[^a-z0-9-_]', b'', name.lower())
    if not name:
        name = fallback
    return name.decode()


def decodeHtml(text):
    import html
    text = html.unescape(text)

    replacements = {
        '&amp;': '&', '&apos;': "'", '&lt;': '<', '&gt;': '>', '&ndash;': '-',
        '&quot;': '"', '&ntilde;': '~', '&rsquo;': "'", '&nbsp;': ' ',
        '&equals;': '=', '&quest;': '?', '&comma;': ',', '&period;': '.',
        '&colon;': ':', '&lpar;': '(', '&rpar;': ')', '&excl;': '!',
        '&dollar;': '$', '&num;': '#', '&ast;': '*', '&lowbar;': '_',
        '&lsqb;': '[', '&rsqb;': ']', '&half;': '1/2', '&DiacriticalTilde;': '~',
        '&OpenCurlyDoubleQuote;': '"', '&CloseCurlyDoubleQuote;': '"'
    }
    for entity, char in replacements.items():
        text = text.replace(entity, char)

    return text.strip()


# Cyrillic to Latin conversion (simplified)
conversion = {
    'а': 'a', 'А': 'A', 'б': 'b', 'Б': 'B', 'в': 'v', 'В': 'V',
    'г': 'g', 'Г': 'G', 'д': 'd', 'Д': 'D', 'е': 'e', 'Е': 'E',
    'ё': 'jo', 'Ё': 'jo', 'ж': 'zh', 'Ж': 'ZH', 'з': 'z', 'З': 'Z',
    'и': 'i', 'И': 'I', 'й': 'j', 'Й': 'J', 'к': 'k', 'К': 'K',
    'л': 'l', 'Л': 'L', 'м': 'm', 'М': 'M', 'н': 'n', 'Н': 'N',
    'о': 'o', 'О': 'O', 'п': 'p', 'П': 'P', 'р': 'r', 'Р': 'R',
    'с': 's', 'С': 'S', 'т': 't', 'Т': 'T', 'у': 'u', 'У': 'U',
    'ф': 'f', 'Ф': 'F', 'х': 'h', 'Х': 'H', 'ц': 'c', 'Ц': 'C',
    'ч': 'ch', 'Ч': 'CH', 'ш': 'sh', 'Ш': 'SH', 'щ': 'sh', 'Щ': 'SH',
    'ъ': '', 'Ъ': '', 'ы': 'y', 'Ы': 'Y', 'ь': 'j', 'Ь': 'J',
    'э': 'je', 'Э': 'JE', 'ю': 'ju', 'Ю': 'JU', 'я': 'ja', 'Я': 'JA'
}


def cyr2lat(text):
    text = str(text).strip(' \t\n\r')
    retval = ''
    for ch in text:
        retval += conversion.get(ch, ch)
    return retval


def charRemove(text):
    char = [
        '1080p', 'PF1', 'PF2', 'PF3', 'PF4', 'PF5', 'PF6', 'PF7', 'PF8', 'PF9',
        'PF10', 'PF11', 'PF12', 'PF13', 'PF14', 'PF15', 'PF16', 'PF17', 'PF18', 'PF19',
        'PF20', 'PF21', 'PF22', 'PF23', 'PF24', 'PF25', 'PF26', 'PF27', 'PF28', 'PF29',
        'PF30', '480p', '4K', '720p', 'ANIMAZIONE', 'BIOGRAFICO', 'BDRip', 'BluRay',
        'CINEMA', 'DOCUMENTARIO', 'DRAMMATICO', 'FANTASCIENZA', 'FANTASY', 'HDCAM',
        'HDTC', 'HDTS', 'LD', 'MAFIA', 'MARVEL', 'MD', 'NEW_AUDIO', 'POLIZIE', 'R3', 'R6',
        'SD', 'SENTIMENTALE', 'TC', 'TEEN', 'TELECINE', 'TELESYNC', 'THRILLER', 'Uncensored',
        'V2', 'WEBDL', 'WEBRip', 'WEB', 'WESTERN', '-', '_', '.', '+', '[', ']',
    ]
    myreplace = text
    for ch in char:
        myreplace = myreplace.replace(
            ch,
            '').replace(
            '  ',
            ' ').replace(
            '   ',
            ' ').strip()
    return myreplace


def clean_html(html):
    '''Clean an HTML snippet into a readable string'''
    import xml.sax.saxutils as saxutils
    # Ensure string
    if isinstance(html, bytes):
        html = html.decode('utf-8', 'ignore')
    # Newline vs <br />
    html = html.replace('\n', ' ')
    html = re.sub(r'\s*<\s*br\s*/?\s*>\s*', '\n', html)
    html = re.sub(r'<\s*/\s*p\s*>\s*<\s*p[^>]*>', '\n', html)
    # Strip html tags
    html = re.sub('<.*?>', '', html)
    # Replace html entities
    html = saxutils.unescape(html)
    return html.strip()


def cachedel(folder):
    system(f"rm {folder}/*")


def cleanName(name):
    non_allowed_characters = "/.\\:*?<>|\""
    name = name.replace('\xc2\x86', '').replace('\xc2\x87', '')
    name = name.replace(' ', '-').replace("'", '').replace('&', 'e')
    name = name.replace('(', '').replace(')', '')
    name = name.strip()
    name = ''.join(
        ['_' if c in non_allowed_characters or ord(c) < 32 else c for c in name])
    return name


def cleantitle(title):
    cleanName = re.sub(r'[\'\<\>\:\"\/\\\|\?\*\(\)\[\]]', "", str(title))
    cleanName = re.sub(r"   ", " ", cleanName)
    cleanName = re.sub(r"  ", " ", cleanName)
    cleanName = re.sub(r" ", "-", cleanName)
    cleanName = re.sub(r"---", "-", cleanName)
    cleanName = cleanName.strip()
    return cleanName


def cleanTitle(x):
    x = x.replace('~', '')
    x = x.replace('#', '')
    x = x.replace('%', '')
    x = x.replace('&', '')
    x = x.replace('*', '')
    x = x.replace('{', '')
    x = x.replace('}', '')
    x = x.replace(':', '')
    x = x.replace('<', '')
    x = x.replace('>', '')
    x = x.replace('?', '')
    x = x.replace('/', '')
    x = x.replace('+', '')
    x = x.replace('|', '')
    x = x.replace('"', '')
    x = x.replace('\\', '')
    x = x.replace('--', '-')
    return x


def remove_line(filename, pattern):
    """Remove lines containing pattern from file"""
    if not isfile(filename):
        return
    with open(filename, 'r') as f:
        lines = [line for line in f if pattern not in line]
    with open(filename, 'w') as f:
        f.writelines(lines)


def badcar(name):
    bad_chars = [
        "sd", "hd", "fhd", "uhd", "4k", "1080p", "720p", "blueray", "x264", "aac",
        "ozlem", "hindi", "hdrip", "(cache)", "(kids)", "[3d-en]", "[iran-dubbed]",
        "imdb", "top250", "multi-audio", "multi-subs", "multi-sub", "[audio-pt]",
        "[nordic-subbed]", "[nordic-subbeb]",
        "SD", "HD", "FHD", "UHD", "4K", "1080P", "720P", "BLUERAY", "X264", "AAC",
        "OZLEM", "HINDI", "HDRIP", "(CACHE)", "(KIDS)", "[3D-EN]", "[IRAN-DUBBED]",
        "IMDB", "TOP250", "MULTI-AUDIO", "MULTI-SUBS", "MULTI-SUB", "[AUDIO-PT]",
        "[NORDIC-SUBBED]", "[NORDIC-SUBBEB]",
        "-ae-", "-al-", "-ar-", "-at-", "-ba-", "-be-", "-bg-", "-br-", "-cg-",
        "-ch-", "-cz-", "-da-", "-de-", "-dk-", "-ee-", "-en-", "-es-", "-ex-yu-",
        "-fi-", "-fr-", "-gr-", "-hr-", "-hu-", "-in-", "-ir-", "-it-", "-lt-",
        "-mk-", "-mx-", "-nl-", "-no-", "-pl-", "-pt-", "-ro-", "-rs-", "-ru-",
        "-se-", "-si-", "-sk-", "-tr-", "-uk-", "-us-", "-yu-",
        "-AE-", "-AL-", "-AR-", "-AT-", "-BA-", "-BE-", "-BG-", "-BR-", "-CG-",
        "-CH-", "-CZ-", "-DA-", "-DE-", "-DK-", "-EE-", "-EN-", "-ES-", "-EX-YU-",
        "-FI-", "-FR-", "-GR-", "-HR-", "-HU-", "-IN-", "-IR-", "-IT-", "-LT-",
        "-MK-", "-MX-", "-NL-", "-NO-", "-PL-", "-PT-", "-RO-", "-RS-", "-RU-",
        "-SE-", "-SI-", "-SK-", "-TR-", "-UK-", "-US-", "-YU-",
        "|ae|", "|al|", "|ar|", "|at|", "|ba|", "|be|", "|bg|", "|br|", "|cg|",
        "|ch|", "|cz|", "|da|", "|de|", "|dk|", "|ee|", "|en|", "|es|", "|ex-yu|",
        "|fi|", "|fr|", "|gr|", "|hr|", "|hu|", "|in|", "|ir|", "|it|", "|lt|",
        "|mk|", "|mx|", "|nl|", "|no|", "|pl|", "|pt|", "|ro|", "|rs|", "|ru|",
        "|se|", "|si|", "|sk|", "|tr|", "|uk|", "|us|", "|yu|",
        "|AE|", "|AL|", "|AR|", "|AT|", "|BA|", "|BE|", "|BG|", "|BR|", "|CG|",
        "|CH|", "|CZ|", "|DA|", "|DE|", "|DK|", "|EE|", "|EN|", "|ES|", "|EX-YU|",
        "|FI|", "|FR|", "|GR|", "|HR|", "|HU|", "|IN|", "|IR|", "|IT|", "|LT|",
        "|MK|", "|MX|", "|NL|", "|NO|", "|PL|", "|PT|", "|RO|", "|RS|", "|RU|",
        "|SE|", "|SI|", "|SK|", "|TR|", "|UK|", "|US|", "|YU|",
        "|Ae|", "|Al|", "|Ar|", "|At|", "|Ba|", "|Be|", "|Bg|", "|Br|", "|Cg|",
        "|Ch|", "|Cz|", "|Da|", "|De|", "|Dk|", "|Ee|", "|En|", "|Es|", "|Ex-Yu|",
        "|Fi|", "|Fr|", "|Gr|", "|Hr|", "|Hu|", "|In|", "|Ir|", "|It|", "|Lt|",
        "|Mk|", "|Mx|", "|Nl|", "|No|", "|Pl|", "|Pt|", "|Ro|", "|Rs|", "|Ru|",
        "|Se|", "|Si|", "|Sk|", "|Tr|", "|Uk|", "|Us|", "|Yu|",
        "(", ")", "[", "]", "u-", "3d", "'", "#", "/", "-", "_", ".", "+",
        "PF1", "PF2", "PF3", "PF4", "PF5", "PF6", "PF7", "PF8", "PF9", "PF10",
        "PF11", "PF12", "PF13", "PF14", "PF15", "PF16", "PF17", "PF18", "PF19", "PF20",
        "PF21", "PF22", "PF23", "PF24", "PF25", "PF26", "PF27", "PF28", "PF29", "PF30",
        "480p", "ANIMAZIONE", "AVVENTURA", "BIOGRAFICO", "BDRip", "BluRay", "CINEMA",
        "COMMEDIA", "DOCUMENTARIO", "DRAMMATICO", "FANTASCIENZA", "FANTASY", "HDCAM",
        "HDTC", "HDTS", "LD", "MARVEL", "MD", "NEW_AUDIO", "R3", "R6", "SENTIMENTALE",
        "TC", "TELECINE", "TELESYNC", "THRILLER", "Uncensored", "V2", "WEBDL", "WEBRip",
        "WEB", "WESTERN"
    ]
    for j in range(1900, 2025):
        bad_chars.append(str(j))
    for i in bad_chars:
        name = name.replace(i, '')
    return name


def get_title(title):
    if title is None:
        return
    title = re.sub(r'&#(\d+);', '', title)
    title = re.sub(r'(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub(
        r'\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|–|"|,|\'|\_|\.|\?)|\s',
        '',
        title).lower()
    return title


def clean_filename(s):
    if not s:
        return ''
    badchars = '\\/:*?\"<>|\''
    for c in badchars:
        s = s.replace(c, '')
    return s.strip()


def cleantext(text):
    import html
    text = html.unescape(text)
    text = text.replace('&amp;', '&')
    text = text.replace('&apos;', "'")
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&ndash;', '-')
    text = text.replace('&quot;', '"')
    text = text.replace('&ntilde;', '~')
    text = text.replace('&rsquo;', '\'')
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&equals;', '=')
    text = text.replace('&quest;', '?')
    text = text.replace('&comma;', ',')
    text = text.replace('&period;', '.')
    text = text.replace('&colon;', ':')
    text = text.replace('&lpar;', '(')
    text = text.replace('&rpar;', ')')
    text = text.replace('&excl;', '!')
    text = text.replace('&dollar;', '$')
    text = text.replace('&num;', '#')
    text = text.replace('&ast;', '*')
    text = text.replace('&lowbar;', '_')
    text = text.replace('&lsqb;', '[')
    text = text.replace('&rsqb;', ']')
    text = text.replace('&half;', '1/2')
    text = text.replace('&DiacriticalTilde;', '~')
    text = text.replace('&OpenCurlyDoubleQuote;', '"')
    text = text.replace('&CloseCurlyDoubleQuote;', '"')
    return text.strip()


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def addstreamboq(bouquetname=None):
    boqfile = '/etc/enigma2/bouquets.tv'
    if not exists(boqfile):
        return
    with open(boqfile, 'r') as fp:
        lines = fp.readlines()
    add = True
    for line in lines:
        if f'userbouquet.{bouquetname}.tv' in line:
            add = False
            break
    if add:
        with open(boqfile, 'a') as fp:
            fp.write(
                f'#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.{bouquetname}.tv" ORDER BY bouquet\n')


def stream2bouquet(url=None, name=None, bouquetname=None):
    error = 'none'
    bouquetname = 'MyFavoriteBouquet'
    fileName = f'/etc/enigma2/userbouquet.{bouquetname}.tv'
    out = f'#SERVICE 4097:0:0:0:0:0:0:0:0:0:{quote(url)}:{quote(name)}\r\n'

    try:
        addstreamboq(bouquetname)
        if not exists(fileName):
            with open(fileName, 'w') as fp:
                fp.write(f'#NAME {bouquetname}\n')
            with open(fileName, 'a') as fp:
                fp.write(out)
        else:
            with open(fileName, 'r') as fp:
                lines = fp.readlines()
            for line in lines:
                if out in line:
                    error = 'Stream already added to bouquet'
                    return error
            with open(fileName, 'a') as fp:
                fp.write(out)
    except BaseException:
        error = 'Adding to bouquet failed'
    return error
