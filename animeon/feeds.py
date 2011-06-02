from django.contrib.syndication.views import Feed
from animeon.models import Episode

class LatestEpisodesFeed(Feed):
    title = "Shinpaku | Latest Anime Episodes"
    link = "/"
    description = "Latest added anime episodes"

    def items(self):
        return Episode.objects.order_by('-pub_date')[:10]

    def item_title(self, item):
        title = item.anime.title + ' - Episode ' + str(item.episode_num)
        return title

    def item_description(self, item):
        return item.anime.summary[:100]