from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pegapega.views.home', name='home'),
    # url(r'^pegapega/', include('pegapega.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # url(r'^$', direct_to_template, {'template': 'login.html'}),
    url(r'^$', direct_to_template, {'template': 'home/index.html', 'extra_context' : {'domain_url': settings.DOMAIN_URL}}, name='home'),
    url(r'^partidas/', include('partidas.urls')),
    url(r'^accounts/', include('accounts.urls')),
)
