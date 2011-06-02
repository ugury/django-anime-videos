from django.conf.urls.defaults import patterns, include, url
from myproject import animeon,registration
from django.contrib import admin
from myproject.animeon.sitemap import EpisodeSitemap,AnimeSitemap
from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import *
from myproject.animeon.feeds import LatestEpisodesFeed

admin.autodiscover()

sitemaps = { "anime": AnimeSitemap , "episode" :EpisodeSitemap }

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^myproject/', include('myproject.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^$','animeon.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^anime/(\d+)/([-\w]+)/$','animeon.views.get_anime'),
    url(r'^([-\w]+)/episode/(\d+)/$','animeon.views.get_episode'),
    url(r'^popular-animes/$','animeon.views.get_popular_animes'),
    url(r'^anime-list/$','animeon.views.get_anime_list'),
    (r'^static/(.*)$','django.views.static.serve', {'document_root': '/home/luterien/webapps/shin_static/','show_indexes': True }),
    url(r'^register/','registration.views.register'),
    url(r'^login/','registration.views.mylogin'),
    url(r'^logout/','registration.views.logout_user'),
    url(r'^search/','animeon.views.search'),
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^robots.txt$', direct_to_template, {'template':'robots.txt', 'mimetype':'text/plain'}),
    url(r'^vote/$','animeon.views.cast_vote'),
    (r'^latest/feed/$', LatestEpisodesFeed()),
)
