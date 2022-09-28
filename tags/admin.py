from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin

from .models import TaggedItem





class TagedItemInline(GenericTabularInline):
    model = TaggedItem
    extra = 0


class TaggenItemAdmin(admin.ModelAdmin):
    field = ['tag','content_type','object_id','content_object']
    readonly_fields = ['content_object']
    class Meta:
        model = TaggedItem
       
admin.site.register(TaggedItem,TaggenItemAdmin)
