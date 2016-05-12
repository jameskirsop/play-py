from django.conf import settings
import os

def run():
	os.system(os.path.join(settings.BASE_DIR,'script/music.sh') + ' start')
	os.system('mpc play')