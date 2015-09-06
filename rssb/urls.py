from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(   
	'',
    # Examples:
    # url(r'^$', 'rssb.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^sots-api/', include('sots.urls')),
)

    