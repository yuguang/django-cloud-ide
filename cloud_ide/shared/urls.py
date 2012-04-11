from django.conf.urls.defaults import patterns, include, url
from cloud_ide.fiddle.sitemap import sitemaps
from django.contrib import admin
admin.autodiscover()
from django.template import add_to_builtins
add_to_builtins('mediasync.templatetags.media')

urlpatterns = patterns('',
    url(r'', include('cloud_ide.login.urls')),
    url(r'', include('mediasync.urls')),
)

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)

urlpatterns += patterns('',
    url(r'^fiddles/', include('cloud_ide.snippet.urls')),
)

urlpatterns += patterns('cloud_ide.snippet.views',
    url(r'^dashboard/', 'dashboard'),
    url(r'^users/(?P<username>[-\w\._]+)/$', 'author_snippets', name='author_snippets'),
)