from multiprocessing import context
from time import time
from django.views.generic import ListView,DetailView
from django.shortcuts import render
from django.http import Http404
from django.utils import timezone
from djngoflix.db.models import PublishStateOptions

from .models import (
    MovieProxy,
    TVShowProxy,
    Playlist,
    TVShowSeasonProxy,
)


class PlaylistMixin():
    template_name = 'playlist_list.html'
    title = None
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        if self.title is not None:
            context['title'] = self.title
        print(context)
        return context
    
    def get_queryset(self):
        return super().get_queryset().published()


class MovieListView(PlaylistMixin,ListView):
    queryset = MovieProxy.objects.all()
    title = "Movies"

class TVShowListView(PlaylistMixin,ListView):
    queryset = MovieProxy.objects.all()
    title = "TV Shows"


class MovieDetailView(PlaylistMixin,DetailView):
    template_name = 'playlists/movie_detail.html'
    queryset = MovieProxy.objects.all()


class PlaylistDetailView(PlaylistMixin,DetailView):
    template_name = 'playlists/playlist_detail.html'
    queryset = Playlist.objects.all()
    




class TVShowProxyListView(PlaylistMixin,ListView):
    queryset = TVShowProxy.objects.all()
    title = "TV Shows"



class TVShowDetailView(PlaylistMixin,DetailView):
    template_name = 'playlists/tvshow_detail.html'
    queryset = TVShowProxy.objects.all()




class TVShowSeasonsDetailView(PlaylistMixin,DetailView):
    template_name = 'playlists/season_detail.html'
    queryset = TVShowSeasonProxy.objects.all()

    def get_object(self):
        kwargs = self.kwargs
        show_slug = kwargs.get("showSlug")
        season_slug = kwargs.get("seasonSlug")
        now = timezone.now()
        try:
            obj = TVShowSeasonProxy.objects.get(
                state=PublishStateOptions.PUBLISH,
                publish_timestamp__lte=now,
                parent__slug__iexact=show_slug,
                slug__iexact=season_slug
            )
        except TVShowSeasonProxy.MultipleObjectsReturned:
            obj = None
        except:
            # obj = None
            raise Http404
        return obj
        # qs = self.get_queryset().filter(
        #     parent__slug__iexact=show_slug,
        #     slug__iexact=season_slug
        #     )
        # if not qs.count() == 1:
        #     raise Http404("Not found")
        # return qs.first()

class FeaturedPlaylistProxyListView(PlaylistMixin,ListView):
    queryset = Playlist.objects.featured_playlist()
    title = "Featured"