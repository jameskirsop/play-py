from django.core.management.base import BaseCommand, CommandError
from mpd import MPDClient
from music.models import Artist,Song
import time
from requests.exceptions import ConnectionError

import pusher
pusher_client = pusher.Pusher(
  app_id='190359',
  key='18e076434d0479a10e71',
  secret='e9a5ea2bc88d8ffedf76',
  cluster='ap1',
  ssl=True
)

print('Starting Monitor')

client = MPDClient()
client.connect("localhost",6600)

cursong = Song()
cursong.now_playing()
while True:
	client.idle()
	nextsong = Song()
	nextsong.now_playing()
	if cursong != nextsong:
		cursong = nextsong
		backoff = 2
		delay = 2
		while True:
			try:
				pusher_client.trigger('play-py', 'now-playing', {
					'artist': cursong.artist if hasattr(cursong,'artist') else '',
					'title': cursong.title if hasattr(cursong,'title') else '',
					'album': cursong.album if hasattr(cursong,'album') else '',
					'file': cursong.file if hasattr(cursong,'file') else ''
					})
				break
			except ConnectionError:
				time.sleep(delay)
				if delay < 90:
					delay *= backoff

		playlist = client.playlistinfo()
		backoff = 2
		delay = 2
		n = 0
		while True:
			try:
				pusher_client.trigger('play-py', 'upcoming-track-list', {
					'tracks': playlist[1:11],
					'iTotalTracks': len(playlist) - 1
					})
				break
			except Exception as e:
				time.sleep(delay)
				delay *= backoff
				if n < 20:
					continue
				delay = 2
				n = 0