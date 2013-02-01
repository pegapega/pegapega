
from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from .views import PartidasListView

urlpatterns = patterns('',
    url(r'^$', login_required(PartidasListView.as_view()), name='partida_list'),
    url(r'^criar/$', 'partidas.views.partida_create', name='partida_create'),
    url(r'^(?P<partida_id>\d+)/alvo/$', 'partidas.views.alvo', name='alvo'),
)
