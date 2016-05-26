from django.core.management.base import BaseCommand, CommandError
from mpd import MPDClient
from music.models import Artist,Song

import pusher
pusher_client = pusher.Pusher(
  app_id='190359',
  key='***REMOVED***',
  secret='***REMOVED***',
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
		pusher_client.trigger('play-py', 'upcoming-track-list', {
			'tracks': playlist[1:11],
			'iTotalTracks': len(playlist) - 1
			})