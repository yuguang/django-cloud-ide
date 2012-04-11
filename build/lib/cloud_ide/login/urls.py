from django.conf.urls.defaults import patterns, url, include

from views import login, logout, done

urlpatterns = patterns('',
    url(r'^login/$', login, name='login'),
    url(r'^done/$', done, name='done'),
    url(r'^logout/$', logout, name='logout'),
    url(r'', include('social_auth.urls')),
)
