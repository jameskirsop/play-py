#!/bin/sh
#
# Manages the music daemon powering Play.

case $1 in
	start)
		/usr/local/bin/mpd config/mpd.conf
		exit $?
		;;
	stop)
		/usr/local/bin/mpd config/mpd.conf --kill
		exit $?
		;;
esac