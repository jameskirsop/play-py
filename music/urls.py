from django.conf.urls import url
from django.urls import path

from music import views

app_name = 'music'
urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^artwork/current$', views.artwork, name='artwork'),
	url(r'^artwork/album/(?P<albumName>.+)$', views.artwork_find, name='artwork_find'),
	url(r'^artwork/(?P<artistName>.+)/album/(?P<albumName>.+)$', views.artwork_find, name='artwork_find'),
	url(r'^screen$', views.bigscreen, name='bigscreen'),
	url(r'^filter/artist/(?P<artistName>.+)/album/(?P<albumName>.+)$', views.get_album, name='get_album'),
	url(r'^search/(?P<queryString>.+)$', views.search, name='search'),
	url(r'^list/(?P<queryString>.+)/(?P<start>\d+)/(?P<end>\d+)$', views.list, name='list'),
	url(r'^filter/(?P<sType>(artist|album){1})/(?P<queryString>.+)$', views.filter, name='search'),
	url(r'^add/$', views.add, name='add')
]