from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^login/$', 'pegapega.apps.accounts.views.login', name='facebook_login'),
    url(r'^authentication_callback/$', 'pegapega.apps.accounts.views.callback', name='facebook_callback'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
)
