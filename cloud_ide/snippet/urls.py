from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^$',
        snippet_list,
        name='fiddle_snippet_list'),
    url(r'^tags/$',
        top_tags,
        name='fiddle_top_tags'),
    url(r'^tags/(?P<slug>[-\w]+)/$',
        matches_tag,
        name='fiddle_snippet_matches_tag'),
)
