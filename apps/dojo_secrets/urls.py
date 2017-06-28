from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^create$', views.create),
    url(r'^secret$', views.secret, name='secret'),
    url(r'^create_secret$', views.create_secret, name='create_secret'),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^create_like/(?P<id>\d+)$', views.create_like, name='create_like'),
    url(r'^popular$', views.popular, name='popular')
]
