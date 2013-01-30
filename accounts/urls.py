from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^login/$', 'accounts.views.login', name='facebook_login'),
    url(r'^authentication_callback/$', 'accounts.views.callback', name='facebook_callback'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
)
