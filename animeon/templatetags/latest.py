import animeon.models
from django import template

register = template.Library()

def do_latest_episodes(parser,token):
    return GetLatestEpisodesNode()

class GetLatestEpisodesNode(template.Node):
    def render(self,context):
        context["latest_episodes"] = animeon.models.Episode.objects.order_by('-pub_date')[:10]
        return ''

register.tag('get_latest_episodes', do_latest_episodes)

def do_all_animes(parser,token):
    return GetAllAnimesNode()

class GetAllAnimesNode(template.Node):
    def render(self,context):
        context["all_animes"] = animeon.models.Anime.objects.all()
        return ''

register.tag('get_all_animes', do_all_animes)

def do_top_animes(parser,token):
    return GetTopAnimesNode()

class GetTopAnimesNode(template.Node):
    def render(self,context):
        context["top_animes"] = animeon.models.Anime.objects.order_by('-average_score')[:10]
        return ''

register.tag('get_top_animes', do_top_animes)