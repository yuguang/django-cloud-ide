from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap, Sitemap
from models import Snippet, Language
from datetime import datetime

info_dict = {
    'queryset': Snippet.objects.all(),
    'date_field': 'last_modified',
}

class MainSitemap(Sitemap):
    def items(self):
      return [self]

    location = "/"
    changefreq = "monthly"
    priority = "1"
    date_str = "2011-12-14 10:30:00"
    lastmod = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    
sitemaps = {
    'flatpages': FlatPageSitemap,
    'fiddles': GenericSitemap(info_dict, priority=0.6),
    'mainpage': MainSitemap,
}

languages = Language.objects.all()
if len(languages) > 1:
    sitemaps['languages'] = GenericSitemap({'queryset': languages}, priority=0.8)
