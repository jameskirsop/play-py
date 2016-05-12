from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
import mutagen
from mpd import MPDClient
from music.models import Artist,Song
from pprint import pprint
import os
from contextlib import contextmanager
import json

import pusher
pusher_client = pusher.Pusher(
  app_id='190359',
  key='***REMOVED***',
  secret='e9a5ea2bc88d8ffedf76',
  cluster='ap1',
  ssl=True
)

@contextmanager
def mpdConnection():
	client = MPDClient()
	try:
		client.connect("localhost",6600)
		yield client
	finally:
		client.close()
		client.disconnect()

def index(request):
	with mpdConnection() as client:
		cursong = Song()
		cursong.now_playing()
		playlist = client.playlistinfo()
		artistList = client.list('Artist')
	return render(request,'music/index.html',{
			'artist': cursong.artist if hasattr(cursong,'artist') else '',
			'title': cursong.title if hasattr(cursong,'title') else '',
			'album': cursong.album if hasattr(cursong,'album') else '',
			'lUpcoming': playlist[1:11],
			'iTotalTracks': len(playlist) - 1,
			'artistList':artistList
		})

def search(request, queryString):
	if request.method == 'GET':
		with mpdConnection() as client:
			print queryString
			print client.search('any',queryString)
			return HttpResponse(
				json.dumps(client.search('any',queryString)[1:11]),
	            content_type="application/json"
	        )
	else:
		return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def add(request):
	# if request.is_ajax() and request.method == "POST":
	if request.method == "POST":
		with mpdConnection() as client:
			if json.loads(request.body)['uri']:
				client.add(json.loads(request.body)['uri'])
				playlist = client.playlistinfo()
				pusher_client.trigger('play-py', 'upcoming-track-list', {
					'tracks': playlist[1:11],
					'iTotalTracks': len(playlist) - 1
					})
				client.play()
				return HttpResponse(
					json.dumps({"result": "success"}),
					content_type="application/json"
				)
			return HttpResponseBadRequest(
				json.dumps({"result": "failure"}),
				content_type="application/json"
			)
	else:
		return HttpResponseBadRequest(
			json.dumps({"result": "failure"}),
			content_type="application/json"
		)


'''
NOTE: iTunes doesn't embed album artwork (that's seen in the application) in the files in it's library.
To do this, you can use the following script: http://dougscripts.com/itunes/scripts/ss.php?sp=reembedartwork
'''
def artwork(request):
	client = MPDClient()
	client.connect("localhost",6600)
	current = Song()
	current.now_playing()
	if current.file:
		file = mutagen.File(os.environ['HOME']+"/Music/"+current.file)
		if type(file) is mutagen.mp4.MP4:
			print file.tags
			if file.tags.has_key('covr'):
				return HttpResponse(file.tags['covr'][0],content_type="image/jpeg")

		if type(file) is mutagen.mp3.MP3:
			print file.tags.keys()
			if file.tags.has_key('APIC:'):
				return HttpResponse(file.tags['APIC:'].data,content_type=file.tags['APIC:'].mime)

	with open(os.path.join(settings.BASE_DIR, "static/no-artwork.png"), "rb") as f:
		return HttpResponse(f.read(), content_type="image/jpeg")

def bigscreen(request):
	with mpdConnection():
		cursong = Song()
		cursong.now_playing()
	return render(request, 'music/bigscreen.html',{
			'artist': cursong.artist if hasattr(cursong,'artist') else '',
			'title': cursong.title if hasattr(cursong,'title') else '',
			'album': cursong.album if hasattr(cursong,'album') else ''
		})