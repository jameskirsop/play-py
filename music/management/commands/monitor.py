from django.core.management.base import BaseCommand, CommandError
from mpd import MPDClient
from music.models import Artist,Song
import time

import pusher
pusher_client = pusher.Pusher(
  app_id='190359',
  key='18e076434d0479a10e71',
  secret='e9a5ea2bc88d8ffedf76',
  cluster='ap1',
  ssl=True
)

print 'Starting Monitor'

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
		pusher_client.trigger('play-py', 'now-playing', {
			'artist': cursong.artist if hasattr(cursong,'artist') else '',
			'title': cursong.title if hasattr(cursong,'title') else '',
			'album': cursong.album if hasattr(cursong,'album') else '',
			'file': cursong.file if hasattr(cursong,'file') else ''
			})
		playlist = client.playlistinfo()
		backoff = 2
		delay = 2
		for n in range(5):
			try:
				pusher_client.trigger('play-py', 'upcoming-track-list', {
					'tracks': playlist[1:11],
					'iTotalTracks': len(playlist) - 1
					})
			except Exception as e:
				time.sleep(delay)
				delay *= backoff
				if n < 5:
					continue
				raise e		