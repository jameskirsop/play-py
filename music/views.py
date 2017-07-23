# coding: utf-8
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, HttpResponseBadRequest
import mutagen
from mpd import MPDClient
from music.models import Artist,Song
from pprint import pprint
import os
from contextlib import contextmanager
import json
import string
import urllib2
import HTMLParser
import pusher
from pprint import pprint

pusher_client = pusher.Pusher(
  app_id=settings.PUSHER_CONFIG['app_id'],
  key=settings.PUSHER_CONFIG['key'],
  secret=settings.PUSHER_CONFIG['secret'],
  cluster=settings.PUSHER_CONFIG['cluster'],
  ssl=settings.PUSHER_CONFIG['ssl']
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

def list(request, queryString,start,end):
	if request.method == 'GET':
		lReturn = []
		with mpdConnection() as client:
			if queryString == 'albums':
				for artist in client.list('artist')[int(start):int(end)]:
					for album in client.list('album','artist',artist):
						# print album
						# print '=='+artist
						lReturn.append({'artist':artist,'album':album})
					# pass
			return HttpResponse(
				json.dumps(lReturn),
				content_type="application/json"
				)	

def search(request, queryString):
	if request.method == 'GET':
		with mpdConnection() as client:
			results = client.search('any',queryString)
			if len(results) == 0:
				query = []
				for sString in string.split(queryString):
					query.append('any')
					query.append(sString)
				results = client.search(*query)
			if len(results) > 10:
				return HttpResponse(
					json.dumps(results[1:11]),
		            content_type="application/json"
		        )
			return HttpResponse(
				json.dumps(results),
	            content_type="application/json"
	        )
	else:
		return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def filter(request, sType, queryString):
	html_parser = HTMLParser.HTMLParser()
	# print html_parser.unescape(urllib2.unquote(queryString))
	dResult = dict()
	with mpdConnection() as client:
		results = client.list('album',sType,html_parser.unescape(urllib2.unquote(queryString)))
		for result in results:
			# print client.search('album',result)
			dResult[result] = client.search('album',result)
	return HttpResponse(
		json.dumps(dResult),
		content_type="application/json"
	)


def get_album(request, artistName, albumName):
	html_parser = HTMLParser.HTMLParser()
	dResult = []
	with mpdConnection() as client:
		results = client.find('artist',html_parser.unescape(urllib2.unquote(artistName)))
		for result in results:
			print result
			if 'album' in result and result['album'] == albumName:
				dResult.append(result)
		pprint(results)
	return HttpResponse(
		json.dumps(dResult),
		content_type="application/json"
	)

def add(request):
	# if request.is_ajax() and request.method == "POST":
	if request.method == "POST":
		with mpdConnection() as client:
			if json.loads(request.body)['uri']:
				try:
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
				except Exception, e:
					return HttpResponseBadRequest(
						json.dumps({"result": "failure"}),
						content_type="application/json"
					)
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
			if file.tags.has_key('covr'):
				return HttpResponse(file.tags['covr'][0],content_type="image/jpeg")

		if type(file) is mutagen.mp3.MP3:
			if file.tags.has_key('APIC:'):
				return HttpResponse(file.tags['APIC:'].data,content_type=file.tags['APIC:'].mime)

	with open(os.path.join(settings.BASE_DIR, "static/no-artwork.png"), "rb") as f:
		return HttpResponse(f.read(), content_type="image/jpeg")

def artwork_find(request,albumName):
	if request.method == "GET":
		with mpdConnection() as client:
			html_parser = HTMLParser.HTMLParser()
			result = client.search('album',albumName)
			file = mutagen.File(os.environ['HOME']+"/Music/"+result[0]['file'])
			if type(file) is mutagen.mp4.MP4:
				if file.tags.has_key('covr'):
					return HttpResponse(file.tags['covr'][0],content_type="image/jpeg")

			if type(file) is mutagen.mp3.MP3:
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