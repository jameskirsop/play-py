from django.conf.urls import url

from music import views

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^artwork/current$', views.artwork, name='artwork'),
	url(r'^screen$', views.bigscreen, name='bigscreen'),
	url(r'^search/(?P<queryString>.+)$', views.search, name='search'),
	url(r'^filter/(?P<sType>(artist|album){1})/(?P<queryString>.+)$', views.filter, name='search'),
	url(r'^add/$', views.add, name='add')
]