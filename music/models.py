from __future__ import unicode_literals

from django.db import models

from mpd import MPDClient, ConnectionError
from contextlib import contextmanager
client = MPDClient()

@contextmanager
def mpdConnection():
	client = MPDClient()
	try:
		client.connect("localhost",6600)
		yield client
	finally:
		client.close()
		client.disconnect()

class ArtistManager(models.Manager):
	def get_queryset(self):
		result_list = []
		with mpdConnection:
			for artist in client.list('Artist'):
				a = self.model(name=artist)
				result_list.append(a)
			return result_list
		

class Artist(models.Model):
	name = models.CharField(max_length=200)
	objects = ArtistManager()


class SongManager(models.Manager):
	def get_queryset(self):
		result_list = []
		with mpdConnection():
			for song in client.list('Title'):
				a = self.model(title=song)
				result_list.append(a)
			return result_list

class Song(models.Model):
	title = models.CharField(max_length=200)
	# artist = 
	album = models.CharField(max_length=200)
	artist = models.CharField(max_length=200)
	date = models.IntegerField()
	# 'disc': '1/2',
	file = models.CharField(max_length=250)
	genre = models.CharField(max_length=100)
	# 'time': '179',
	# 'track': '3/21'}]
	objects = SongManager()

	def now_playing(self):
		with mpdConnection() as client:
			if client.status()['state'] == 'stop':
				return None
			self.__dict__ = client.currentsong()

