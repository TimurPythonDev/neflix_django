from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.



class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey("content_type","object_id")


    # def get_reletated_object(self):
    #    Klass = self.content_type.mode_class()
    #    return Klass.objects.get(id=self.object_id)