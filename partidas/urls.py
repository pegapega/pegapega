from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'partidas/list.html'}),
    url(r'^partida/new$', direct_to_template, {'template': 'partidas/nova_partida.html'}),
    url(r'^test/$', 'partidas.views.test', name='test'),
)
