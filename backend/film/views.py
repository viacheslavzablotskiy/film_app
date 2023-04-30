import os
from rest_framework.permissions import IsAuthenticated
from film.pagination.pagination_movie import PaginationMovies
from .models import Movie, Actor, Review, Rating
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer, ImageMoment, ImageMomentDetail,
)
from django.http import FileResponse, Http404, StreamingHttpResponse
from film.video_image.service import open_file
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, parsers, views, mixins
from film import models
from film.permissions.permissions import AdminOrReadOnly, IsAutoregistrationOrReadOnly
from film.services.delte_file import delete_old_file
from film.services.ip_user import get_client_ip

""" Просмотр видео без переметоки """


class StreamingFileView(views.APIView):
    def set_play(self, track):
        track.count_review += 1
        track.save()

    def get(self, request, pk):
        track = get_object_or_404(models.Movie, id=pk)
        if os.path.exists(track.cover.path):
            self.set_play(track)
            return FileResponse(open(track.cover.path, "rb"), filename=track.cover.name)
        else:
            return Http404


"""С перемоткой"""


def set_play_film(self, _video):
    _video.count_review += 1
    _video.save()


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range, _video = open_file(request, pk)
    set_play_film(_video)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка фильмов"""

    pagination_class = PaginationMovies
    permission_classes = [IsAuthenticated, IsAutoregistrationOrReadOnly]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False)
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == "retrieve":
            return MovieDetailSerializer

    def __delete__(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated, IsAutoregistrationOrReadOnly]


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Добавление рейтинга фильму"""
    serializer_class = CreateRatingSerializer
    permission_classes = [IsAuthenticated, IsAutoregistrationOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод актеров или режиссеров"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == "retrieve":
            return ActorDetailSerializer


class MovieMoment(viewsets.ModelViewSet):
    """ CRUD альбомов автора
    """
    # parser_classes = (parsers.MultiPartParser,)
    serializer_class = ImageMoment
    permission_classes = [IsAuthenticated, IsAutoregistrationOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class MovieMomentDetail(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = models.MovieShots.objects.all()
    serializer_class = ImageMomentDetail
    permission_classes = (IsAuthenticated,
                          )

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.count_views = obj.count_views + 1
        obj.save(update_fields=("count_views",))
        return super().retrieve(request, *args, **kwargs)

        # def get_serializer_class(self):
        #     if self.action == 'list':
        #         return ActorListSerializer
        #     elif self.action == "retrieve":
        #         return ActorDetailSerializer

    # def perform_destroy(self, instance):
    #     delete_old_file(instance.cover.path)
    #     instance.delete()
