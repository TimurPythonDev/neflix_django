from django.contrib import admin

from tags.admin import TagedItemInline
from.models import MovieProxy,Playlist,PlaylistItem,TVShowProxy,TVShowSeasonProxy


class MovieProxyAdmin(admin.ModelAdmin):
    fields = ['title','description','state','category','video','slug']
    list_display = ['title']
    class Meta:
        model = MovieProxy

    def get_queryset(self,request):
        return MovieProxy.objects.all()
  
admin.site.register(MovieProxy,MovieProxyAdmin)

class SesonEpisodeInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0


class TVShowSeasonProxyAdmin(admin.ModelAdmin):
    inlines = [SesonEpisodeInline]
    list_display = ['title','parent']
    class Meta:
        model = TVShowSeasonProxy
    
    def get_queryset(self,request):
        return TVShowSeasonProxy.objects.all()


admin.site.register(TVShowSeasonProxy,TVShowSeasonProxyAdmin)


class TVShowSeasonProxyInline(admin.TabularInline):
    model = TVShowSeasonProxy
    extra = 0
    fields = ['order','title','state']



class TVShowProxyAdmin(admin.ModelAdmin):
    inlines = [TagedItemInline,TVShowSeasonProxyInline]
    fields = ['title','description','state','category','video','slug']
    list_display = ['title']
    
    class Meta:
        model = TVShowProxy

    def get_queryset(self,request):
        return TVShowProxy.objects.all()


admin.site.register(TVShowProxy,TVShowProxyAdmin)

 



class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0


class PlaylistAdmin(admin.ModelAdmin):
    inlines = [PlaylistItemInline]
    class Meta:
        model = Playlist

    def get_queryser(self,request):
        return Playlist.objects.filter(type=Playlist.PlaylistTypeChoices.PLAYLIST)

admin.site.register(Playlist,PlaylistAdmin)

 