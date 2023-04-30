from rest_framework.serializers import BaseSerializer

from .models import Movie, Review, Rating, Actor, MovieShots
from rest_framework import serializers

from .services.delte_file import delete_old_file


# class AlbumSerializer(BaseSerializer):
#     class Meta:
#         model = models.Album
#         fields = ('id', 'name', 'description', 'cover', 'private')
#
#     def update(self, instance, validated_data):
#         delete_old_file(instance.cover.path)
#         return super().update(instance, validated_data)


class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ActorListSerializer(serializers.ModelSerializer):
    """Вывод списка актеров и режиссеров"""

    class Meta:
        model = Actor
        fields = ("id", "name", "image")


class ActorDetailSerializer(serializers.ModelSerializer):
    """Вывод полного описани актера или режиссера"""

    class Meta:
        model = Actor
        fields = "__all__"


class MovieListSerializer(serializers.ModelSerializer):
    """Список фильмов"""

    class Meta:
        model = Movie
        fields = ("id", "title", "tagline", "category", "poster")


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзыва"""

    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзыво"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("id", "name", "text", "children",)


class MovieDetailSerializer(serializers.ModelSerializer):
    """Полный фильм"""
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = ActorListSerializer(read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    reviews = ReviewSerializer(many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)

    class Meta:
        model = Movie
        exclude = ("draft",)


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователем"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Rating
        fields = ("rating", "movie", "user",)

    def create(self, validated_data):
        "_ - Чтобы не получить исключение при  получении tuple"

        rating, _ = Rating.objects.update_or_create(
            user=validated_data.get("user"),
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get("star")}
        )
        return rating


class ImageMoment(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    count_views = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = MovieShots
        fields = ('id', 'movie', 'cover', 'description', 'title', 'user', 'count_views',)

    # def update(self, instance, validated_data):
    #     delete_old_file(instance.cover.path)
    #     return super().update(instance, validated_data)


class ImageMomentDetail(serializers.ModelSerializer):
    """Вывод полного описани актера или режиссера"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MovieShots
        fields = "__all__"



    # def update(self, instance, validated_data):
    #     delete_old_file(instance.cover.path)
    #     return super().update(instance, validated_data)
