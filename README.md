# PlayPy

After the author (@holman) declared that [Play](https://github.com/play/play) wasn't under active development, I took it upon myself to rewrite the project (to some extent) in Python, on top of Django. PlayPy is the result.

<img src="https://user-images.githubusercontent.com/1734219/92557192-ff51be80-f2ae-11ea-8100-c68d4107d42b.png" width=50% height=50%>

## What it does

PlayPy allows multiple computers/devices connected to the same network to listen to and create a music playlist based off a common library. We use it at my day job at [Daraco](https://www.daraco.com.au) to play music in the office for for staff to contribute to the vibes in the office.

## How it works

PlayPy is written off the back of [mpd](https://github.com/MusicPlayerDaemon/) and mpc. It sits on top of the Django framework and uses Pusher.js to provide playlist and now-playing updates to clients listening to the stream.

There's also a full screen web view to show a Now Playing display on a TV or other monitor. This is available at http://yourweburl:port/screen. We have PlayPy running on a 27" iMac in our office and this view is what is on the screen, so staff know what song is playing.

## Requirements and Setup
First create a virtualenv and copy/clone this project into it.

Inside your virtualenv you'll want to use pip to install the packages in requirements.txt

Install [mpd](https://github.com/MusicPlayerDaemon/MPD/) and nginx or Apache on your system. On a computer running macOS using `brew install mpd` and `brew install nginx` is the recommended method. You will need to setup your web server to serve the uwsgi process.

Inside the `script` directory, there are two plist files for you to use to control the `monitor` and `queue` management command processes and a third to spin up the wsgi process. You can place these in the [appropriate directories of your choosing](https://medium.com/swlh/how-to-use-launchd-to-run-services-in-macos-b972ed1e352). On a homebrew installation, we have found that you are best off placing these in your `~/Library/LaunchAgents` folder as that is where Homebrew places the nginx startup files.

Once you've placed the launchctl scripts in your directory, you will need to adjust the paths to your virtualenv in each of the `.plist` files. We assume that you're running this project on a macOS system and you've installed mpd via homebrew, but if that's not the case you will want to adjust the path to `mpd` in `script/music.sh` and `mpc` in `music/startup.py`.

You will also need a Pusher.js account (a basic account is free), and an API key for the service. You'll need to place your key into the appropriate location in static/js/pusher.js

## Help required!
I'd like to try and automate or extract some of the above confguration steps so that the files can be generated using a setup script or similar - leaving the source files able to be easily updated using `git pull`. If you would like to help with that, please get in touch.