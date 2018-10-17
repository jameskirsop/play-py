from django.core.management.base import BaseCommand, CommandError
from mpd import MPDClient
from music.models import Artist,Song
import random

client = MPDClient()
client.connect("localhost",6600)

while True:
	client.idle()
	if len(client.playlistinfo()) <= 1:
		# add new song
		print('oh no!')
		print(client.stats())

		songChoice = random.choice(client.listallinfo())
		while not 'file' in songChoice:
			songChoice = random.choice(client.listallinfo())

		client.add(songChoice['file'])