#!/bin/bash
##setup command=wget https://raw.githubusercontent.com/fairbird/Athantimes/main/installer.sh -O - | /bin/sh

version=3.8
echo ""
#########################
PLUGIN_PATH="/usr/lib/enigma2/python/Plugins/Extensions/AthanTimes"
PrayerTimes="$PLUGIN_PATH/PrayerTimes.xml"
Prayer="$PLUGIN_PATH/Prayer.txt"
city="$PLUGIN_PATH/city.txt"
ChoiceTime="$PLUGIN_PATH/PrayerTimes/ChoiceTime.txt"
### Tmp
TMP_PrayerTimes="/tmp/PrayerTimes.xml"
TMP_Prayer="/tmp/Prayer.txt"
TMP_city="/tmp/city.txt"
TMP_ChoiceTime="/tmp/ChoiceTime.txt"

# check depends packges
if [ -f /var/lib/dpkg/status ]; then
   STATUS=/var/lib/dpkg/status
   OSTYPE=DreamOs
else
   STATUS=/var/lib/opkg/status
   OSTYPE=Opensource
fi

if [ -f /usr/bin/python3 ] ; then
	echo "You have Python3 image"
	PYTHON=PY3
	CRYPT='python3-crypt'
	REQUESTS='python3-requests'
else
	echo "You have Python2 image"
	PYTHON=PY2
	CRYPT='python-crypt'
	REQUESTS='python-requests'
fi

# install depend packges if need it
if grep -qs "Package: $CRYPT" "$STATUS" && \
	grep -qs "Package: $REQUESTS" "$STATUS"; then
	echo ""
	echo "All depend packages Installed"
else
	opkg update >/dev/null 2>&1
	if grep -qs "Package: $CRYPT" cat $STATUS ; then
		echo ""
	else
		echo "Need to install $CRYPT"
		opkg install $CRYPT update >/dev/null 2>&1
	fi
	if grep -qs "Package: $REQUESTS" cat $STATUS ; then
		echo ""
	else
		echo "Need to install $REQUESTS"
		opkg install $REQUESTS update >/dev/null 2>&1
	fi
fi
# Download and install plugin
cd /tmp
echo "BackUp saved files"
cp -f $PrayerTimes $TMP_PrayerTimes
cp -f $Prayer $TMP_Prayer
cp -f $city $TMP_city
cp -f $ChoiceTime $TMP_ChoiceTime
echo ""
set -e
rm -rf *Athantimes* > /dev/null 2>&1
rm -rf *main* > /dev/null 2>&1
wget https://github.com/fairbird/Athantimes/archive/refs/heads/main.tar.gz
tar -xzf main.tar.gz
cp -r Athantimes-main/usr /
echo "Restore backup files"
cp -f  $TMP_PrayerTimes $PrayerTimes
cp -f  $TMP_Prayer $Prayer
cp -f  $TMP_city $city
cp -f  $TMP_ChoiceTime $ChoiceTime
echo ""
rm -rf *Athantimes* > /dev/null 2>&1
rm -rf *main* > /dev/null 2>&1
#
set +e
cd ..
sync

echo "#########################################################"
echo "#           Athantimes INSTALLED SUCCESSFULLY           #"
echo "#               AbouYacine  &  RAED                     #"              
echo "#                     support                           #"
echo "#   https://www.tunisia-sat.com/forums/threads/3739939/ #"
echo "#########################################################"
echo "#           Your STB Will RESTARTING Now                #"
echo "#########################################################"
sleep 3
killall enigma2
exit 0
