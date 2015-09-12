from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^get-a-song/$', views.get_a_song, name='get_a_song'),
	url(r"^get-specific-song/(?P<artist>.+)/(?P<title>.+)/$", views.get_specific_song, name='get_specific_song'),
	url(r'^get-all-songs/$', views.get_all_songs, name='get_all_songs'),
    url(r'^build-model/$', views.build_model, name='build_model'),
]
