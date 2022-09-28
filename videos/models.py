from django.utils import timezone
from django.db.models.signals import pre_save
from django.db import models
from django.utils.text import slugify

from djngoflix.db.models import PublishStateOptions
from djngoflix.db.receivers import publish_state_pre_save,slugify_pre_save



class VideoQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state = PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now
        )

class VideoManager(models.Manager):
    def get_queryset(self):
       return VideoQuerySet(self.model,using= self._db)

    def published(self):
        return self.get_queryset().published()
    



class Video(models.Model):
    

    title = models.CharField(max_length=220,verbose_name="Kino nomi")
    description = models.TextField(blank=True,null=True)
    slug = models.SlugField(blank=True,null=True)
    video_id = models.CharField(max_length=220,verbose_name="Video ID",unique=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated =   models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2,choices=PublishStateOptions.choices,
                            default=PublishStateOptions.DRAFT)
    publish_timestamp=models.DateTimeField(auto_now_add=False,auto_now=False,blank=True,null=True)

    objects = VideoManager()   

    @property
    def is_published(self):
        return self.active

    def get_playlist_ids(self):
        return list(self.playlist_featured.all().values_list('id',flat=True))

class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'All video'
        verbose_name_plural= 'All videos'
  
class VidePublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Publish video'
        verbose_name_plural= 'Publish videos'




pre_save.connect(publish_state_pre_save,sender=Video)
pre_save.connect(slugify_pre_save,sender=Video)    