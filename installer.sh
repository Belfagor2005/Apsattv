#!/bin/bash
## setup command=wget -q --no-check-certificate https://raw.githubusercontent.com/Belfagor2005/Apsattv/main/installer.sh -O - | /bin/sh

version='1.3'
changelog='\nAdd ChannelUp / ChannelDown in Player\nFix major'
TMPPATH=/tmp/Apsattv-main
FILEPATH=/tmp/main.tar.gz

if [ ! -d /usr/lib64 ]; then
    PLUGINPATH=/usr/lib/enigma2/python/Plugins/Extensions/Apsattv
else
    PLUGINPATH=/usr/lib64/enigma2/python/Plugins/Extensions/Apsattv
fi

if [ -f /var/lib/dpkg/status ]; then
    STATUS=/var/lib/dpkg/status
    OSTYPE=DreamOs
else
    STATUS=/var/lib/opkg/status
    OSTYPE=Dream
fi
echo ""

if ! command -v wget >/dev/null 2>&1; then
    echo "Installing wget..."
    if [ "$OSTYPE" = "DreamOs" ]; then
        apt-get update && apt-get install -y wget
    else
        opkg update && opkg install wget
    fi || { echo "Failed to install wget"; exit 1; }
fi

if python --version 2>&1 | grep -q '^Python 3\.'; then
    PYTHON=PY3
    Packagesix=python3-six
    Packagerequests=python3-requests
else
    PYTHON=PY2
    Packagerequests=python-requests
fi

if [ "$PYTHON" = "PY3" ] && ! grep -qs "Package: $Packagesix" "$STATUS"; then
    opkg update && opkg install "$Packagesix"
fi

if ! grep -qs "Package: $Packagerequests" "$STATUS"; then
    echo "Installing $Packagerequests..."
    if [ "$OSTYPE" = "DreamOs" ]; then
        apt-get update && apt-get install -y "$Packagerequests"
    else
        opkg update && opkg install "$Packagerequests"
    fi || { echo "Failed to install $Packagerequests"; exit 1; }
fi

echo ""
mkdir -p "$TMPPATH"
cd "$TMPPATH" || exit 1

if [ -f /var/lib/dpkg/status ]; then
    echo "# Your image is OE2.5/2.6 #"
else
    echo "# Your image is OE2.0 #"
fi
echo ""

if [ "$OSTYPE" != "DreamOs" ]; then
    opkg update && opkg install ffmpeg gstplayer exteplayer3 enigma2-plugin-systemplugins-serviceapp
fi

sleep 2

wget --no-check-certificate 'https://github.com/Belfagor2005/Apsattv/archive/refs/heads/main.tar.gz' -O "$FILEPATH" || { echo "Download failed"; exit 1; }
tar -xzf "$FILEPATH" -C /tmp/ || { echo "Extraction failed"; exit 1; }
cp -r /tmp/Apsattv-main/usr/ / || { echo "Copy failed"; exit 1; }
set +e
cd
sleep 2

if [ ! -d "$PLUGINPATH" ]; then
    echo "Something went wrong... Plugin not installed"
    rm -rf "$TMPPATH" "$FILEPATH"
    exit 1
fi

rm -rf "$TMPPATH" "$FILEPATH"
sync

FILE="/etc/image-version"
box_type=$(head -n 1 /etc/hostname 2>/dev/null || echo "Unknown")
distro_value=$(grep '^distro=' "$FILE" 2>/dev/null | awk -F '=' '{print $2}')
distro_version=$(grep '^version=' "$FILE" 2>/dev/null | awk -F '=' '{print $2}')
python_vers=$(python --version 2>&1)

echo "#########################################################
#          	    INSTALLED SUCCESSFULLY                  #
#                developed by LULULLA                   #
#               https://corvoboys.org                   #
#########################################################
#           your Device will RESTART Now                #
#########################################################
^^^^^^^^^^Debug information:
BOX MODEL: $box_type
OO SYSTEM: $OSTYPE
PYTHON: $python_vers
IMAGE NAME: ${distro_value:-Unknown}
IMAGE VERSION: ${distro_version:-Unknown}
"

sleep 5
killall -9 enigma2
exit 0
