from django.contrib.sitemaps import Sitemap
from animeon.models import Anime,Episode

class EpisodeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    
    def items(self):
        return Episode.objects.all()
    
    def lastmod(self, obj):
        return obj.pub_date


class AnimeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    
    def items(self):
        return Anime.objects.all()