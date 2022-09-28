from numbers import Rational
from django.contrib.contenttypes.fields import GenericRelation
from pyexpat import model
from django.db import models
from django.db.models import Avg,Max,Min

# Create your models here.

from django.utils import timezone
from django.db.models.signals import pre_save
from django.db import models
from django.utils.text import slugify

from djngoflix.db.models import PublishStateOptions
from djngoflix.db.receivers import publish_state_pre_save,slugify_pre_save

from videos.models import Video
from ratings.models import Rating
from tags.models import TaggedItem
from categosies.models import Category


class PlaylistQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state = PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now
        )

class PlaylistManager(models.Manager):
    def get_queryset(self):
       return PlaylistQuerySet(self.model,using= self._db)

    def published(self):
        return self.get_queryset().published()
    
    def featured_playlist(self):
        return self.get_queryset().filter(
            type=Playlist.PlaylistTypeChoices.PLAYLIST

        )

    def get_short_display(self):
        return ""


class Playlist(models.Model):
    class PlaylistTypeChoices(models.TextChoices):
        MOVIE = "MOV","Movie"
        SHOW = "TVS","TV Show"
        SEASON = "SEA","Season"
        PLAYLIST = "PLY","Playlist"

    parent = models.ForeignKey("self",blank=True,null=True,on_delete=models.SET_NULL)
    category= models.ForeignKey(Category,related_name='playlists',blank=True,null=True,on_delete=models.SET_NULL)
    order= models.IntegerField(default=1)
    title = models.CharField(max_length=220,verbose_name="Kino nomi")
    type = models.CharField(max_length=3,choices=PlaylistTypeChoices.choices,default=PlaylistTypeChoices.PLAYLIST)
    description = models.TextField(blank=True,null=True)
    slug = models.SlugField(blank=True,null=True)
    video = models.ForeignKey(Video,related_name='playlist_featured',blank=True,on_delete=models.SET_NULL,null=True)
    videos= models.ManyToManyField(Video,through='PlaylistItem',blank=True,related_name='playlist_item')
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated =   models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2,choices=PublishStateOptions.choices,
                            default=PublishStateOptions.DRAFT)
    publish_timestamp=models.DateTimeField(auto_now_add=False,auto_now=False,blank=True,null=True)
    tags = GenericRelation(TaggedItem,related_query_name='playlist')
    ratings = GenericRelation(Rating,related_query_name='playlist')

    
    objects = PlaylistManager()   

    def get_rating_avg(self):
        return Playlist.objects.filter(id=self.id).aggregate(
            Avg("ratings__value")
            )

    def get_rating_spread(self):
        return Playlist.objects.filter(id=self.id).aggregate(
            max=Max("ratings__value"),min=Min("ratings__value")
            )

    def get_short_display(self):
        return ""


    @property
    def is_published(self):
        return self.active
    
    def __str__(self):
        return self.title
  




  

class MovieProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(
            type=Playlist.PlaylistTypeChoices.MOVIE
        )


class MovieProxy(Playlist):

    objects = MovieProxyManager()
    
    class Meta:
        verbose_name = "Movies"
        verbose_name_plural = "Movies"
        proxy = True
    
    def save(self,*args,**kwargs):
        self.type = Playlist.PlaylistTypeChoices.MOVIE
        super().save(*args,**kwargs)



class TVShowProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=True,
            type=Playlist.PlaylistTypeChoices.SHOW
        )

class TVShowSeasonProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=False,
            type=Playlist.PlaylistTypeChoices.SEASON
        )

class TVShowProxy(Playlist):

    objects = TVShowProxyManager()
    
    class Meta:
        verbose_name = "TV Show"
        verbose_name_plural = "TV Shows"
        proxy = True
    
    def save(self,*args,**kwargs):
        self.type = Playlist.PlaylistTypeChoices.SHOW
        super().save(*args,**kwargs)

    
    
    @property   
    def seasons(self):
        return self.playlist_set.published()



    def get_short_display(self):
        return f"{self.seasons.count()} Seasons"
    

    

class TVShowSeasonProxy(Playlist):

    objects = TVShowSeasonProxyManager()
    class Meta:
        verbose_name = "Season"
        verbose_name_plural = "Seasons"
        proxy = True

    def save(self,*args,**kwargs):
        self.type = Playlist.PlaylistTypeChoices.SEASON
        super().save(*args,**kwargs)
    
    



class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist,on_delete=models.CASCADE)
    video =models.ForeignKey(Video,on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order','-timestamp']


pre_save.connect(publish_state_pre_save,sender=Playlist)
pre_save.connect(slugify_pre_save,sender=Playlist)  

pre_save.connect(publish_state_pre_save,sender=TVShowProxy)
pre_save.connect(slugify_pre_save,sender=TVShowProxy)  

pre_save.connect(publish_state_pre_save,sender=MovieProxy)
pre_save.connect(slugify_pre_save,sender=MovieProxy)

pre_save.connect(publish_state_pre_save,sender=TVShowSeasonProxy)
pre_save.connect(slugify_pre_save,sender=TVShowSeasonProxy)  