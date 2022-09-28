from django.contrib import admin

from .models import VideoAllProxy,VidePublishedProxy
# Register your models here.

class VideoAllAdmin(admin.ModelAdmin):
    list_display = ['title','id','state','video_id','is_published','get_playlist_ids']
    search_fields = ['title']
    list_filter = ['state','active']
    readonly_fields = ['id','is_published','publish_timestamp']
    class Meta:
        model = VideoAllProxy

    # def published(self,obj,*args,**kwargs):
    #     return obj.active

admin.site.register(VideoAllProxy,VideoAllAdmin)

class VideoPublishProxyAdmin(admin.ModelAdmin):
    list_display = ['title','video_id']
    search_fields = ['title']
    class Meta:
        model = VidePublishedProxy

    def get_queryset(self,request):
        return VidePublishedProxy.objects.filter(active=True)
    
admin.site.register(VidePublishedProxy,VideoPublishProxyAdmin)