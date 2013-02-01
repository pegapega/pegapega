
from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from .views import PartidasListView

urlpatterns = patterns('',
    url(r'^$', PartidasListView.as_view()),
    url(r'^partida/new$', direct_to_template, {'template': 'partidas/nova_partida.html'}),
    url(r'^test/$', 'partidas.views.take_photo', name='take_photo'),
)
