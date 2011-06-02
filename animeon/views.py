from models import Genre,Anime,Producer,Episode,Link
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,Http404

def get_anime(request,id,slug,template="my.html"):
    try:
        a = Anime.objects.get(pk=id,slug=slug)
    except Anime.DoesNotExist:
        a = None
    return render_to_response(template,{'anime':a},context_instance=RequestContext(request))


def get_episode(request,anime_slug,num,template="episode.html"):
    try:
        a = Anime.objects.get(slug=anime_slug)
    except Anime.DoesNotExist:
        a = None
    
    try:
        ep = Episode.objects.get(anime=a,episode_num=num)
    except Episode.DoesNotExist:
        ep = None
    
    if ep is not None:
        links = Link.objects.filter(episode=ep)
    
    if links:
        return render_to_response(template,{'links':links,'anime':a,'episode':ep},context_instance=RequestContext(request))

def index(request,template="base.html"):
    return render_to_response(template,context_instance=RequestContext(request))


def search(request,template="search.html"):
    if 'query' in request.POST:
        query = request.POST['query']
    else:
        query = None
    
    if query:
        result = Anime.objects.filter(title__icontains=query)
    else:
        result = None
    
    return render_to_response(template,{'result':result},context_instance=RequestContext(request))


def get_anime_list(request,template="anime_list.html"):
    if 'orderby' in request.POST:
        q = request.POST['orderby']
        animes = Anime.objects.order_by(q)
    else:
        animes = Anime.objects.order_by('title')
    
    return render_to_response(template,{'animes':animes},context_instance=RequestContext(request))


def get_popular_animes(request,template="popular_animes.html"):
    animes = Anime.objects.order_by('total_score')[:20]
    return render_to_response(template,{'animes':animes},context_instance=RequestContext(request))


def cast_vote(request):
    if 'score' in request.POST:
        s = request.POST['score']
    else:
        s = None
    
    if 'anime' in request.POST:
        a = request.POST['anime']
    
    try:
        anime = Anime.objects.get(title=a)
    except Anime.DoesNotExist:
        raise Http404
    
    anime.total_votes = anime.total_votes + 1
    anime.total_score = anime.total_score + int(s)
    t = float(anime.total_score) / float(anime.total_votes)
    t1 = str(t)[:3]
    anime.average_score = float(t1)
    anime.save()
    
    return HttpResponseRedirect(anime.get_absolute_url())