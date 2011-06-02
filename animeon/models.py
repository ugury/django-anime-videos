from django.db import models
import datetime

AGE_RATING_CHOICES = (
    ('All Ages','All Ages'),
    ('Children','Children'),
    ('Teens 13 or older','Teens 13 or older'),
    ('Violence & Profanity','Violence & Profanity'),
    ('Mild Nudity','Mild Nudity'),
)

LANG_CHOICES = (
    ('English Sub','English Sub'),
    ('English Dub','English Dub'),
    ('Japanese Sub','Japanese Sub'),
)

STATUS_CHOICES = (
    ('Ongoing','Ongoing'),
    ('Completed','Completed')
)


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return "/genre/%s" % self.slug

class Producer(models.Model):
    name = models.CharField(max_length=120)

    def __unicode__(self):
        return self.name


class Anime(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    summary = models.TextField()
    num_of_episodes = models.IntegerField()
    age_rating = models.CharField(choices=AGE_RATING_CHOICES,max_length=25)
    genres = models.ManyToManyField(Genre)
    producers = models.ManyToManyField(Producer)
    status = models.CharField(max_length=40,choices=STATUS_CHOICES)
    total_votes = models.IntegerField()
    total_score = models.IntegerField()
    average_score = models.FloatField()
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return "/anime/%s/%s" % (self.pk,self.slug)
    
    def get_genres(self):
        genres = Genre.objects.filter(anime=self)
        return genres
    
    def get_producers(self):
        producers = Producer.objects.filter(anime=self)
        return producers
    
    def get_episode_list(self):
        eps = Episode.objects.filter(anime=self)
        return eps


class Episode(models.Model):
    episode_num = models.IntegerField()
    anime = models.ForeignKey(Anime)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    
    def __unicode__(self):
        return "%s - Episode %s" % (self.anime,self.episode_num)
    
    def get_absolute_url(self):
        return "/%s/episode/%s" % (self.anime.slug,self.episode_num)
    
    def get_next(self):
        num = self.episode_num+1
        try:
            ep = Episode.objects.get(episode_num=num,anime=self.anime)
        except Episode.DoesNotExist:
            ep = None
        return ep
        
    def get_prev(self):
        num = self.episode_num-1
        try:
            ep = Episode.objects.get(episode_num=num,anime=self.anime)
        except Episode.DoesNotExist:
            ep = None
        return ep


class Link(models.Model):
    url = models.TextField()
    type = models.CharField(choices=LANG_CHOICES,max_length=20)
    episode = models.ForeignKey(Episode)
    mirror = models.CharField(max_length=50)
    pub_date = models.DateField(default=datetime.datetime.now)
    
    def __unicode__(self):
        return "%s" % (self.episode)