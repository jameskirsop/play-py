# PlayPy

After the author (@holman) declared that [Play](https://github.com/play/play) wasn't under active development, I took it upon myself to rewrite the project (to some extent) in Python, on top of Django. PlayPy is the result.

## What it does

PlayPy allows multiple computers/devices connected to the same network to listen to and create a music playlist based off a common library. We use it at my day job at [Daraco](https://www.daraco.com.au) to play music in the office for for staff to contribute to the vibes in the office.

## How it works

PlayPy is written off the back of [mpd](https://github.com/MusicPlayerDaemon/) and mpc. It sits on top of the Django framework and uses Pusher.js to provide playlist and now-playing updates to clients listening to the stream.

There's also a full screen web view to show a Now Playing display on a TV or other monitor. This is available at http://yourweburl:port/screen. We have PlayPy running on a 27" iMac in the office and this view is what is on the screen, so staff know what song is playing.

## Requirements and Setup

You'll need a Pusher.js account (a basic account is free), and an API key for the service. You'll need to place your key into the appropriate location in static/js/pusher.js

Inside your virtualenv you'll want to use pip to install the packages in requirements.txt