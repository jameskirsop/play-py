from django.conf import settings
import subprocess
import os

def run():
		# subprocess.Popen(os.path.join(settings.BASE_DIR,'script/music.sh') + ' start',shell=True).wait()
		retcode = subprocess.call(['/bin/sh',os.path.join(settings.BASE_DIR,'script/music.sh'),'start'],cwd=settings.BASE_DIR)
		if retcode > 0:
			raise RuntimeError('PlayPy couldn\'t start MPD, it may already be running')
		os.system('/usr/local/bin/mpc play')
