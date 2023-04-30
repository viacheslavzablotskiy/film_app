from __future__ import absolute_import, unicode_literals
from celery import shared_task, Celery
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
import ssl
from film import models
from backend.celery import app


@shared_task
def update_middle_star():
    movies = list(models.Movie.objects.all())
    movies_count = len(list(models.Movie.objects.all()))
    if movies:
        if movies_count == 1:
            movies = movies[0]
            stars = list(models.Rating.objects.filter(movie_id=movies.id))
            stars_count = len(list(models.Rating.objects.filter(movie_id=movies.id)))
            if stars_count == 1:
                stars = stars[0]
                movies.middle_stars = stars.rating
                movies.save()
            else:
                count = 0
                for star in stars:
                    count += star.rating
                    result = count / stars_count
                    movies.middle_stars = result
                    movies.save()
        else:
            for movie in movies:
                stars = list(models.Rating.objects.filter(movie_id=movie.id))
                stars_count = len(list(models.Rating.objects.filter(movie_id=movie.id)))
                if stars:
                    if stars_count != 1:
                        stars_count = len(list(models.Rating.objects.filter(movie_id=movie.id)))
                        count = 0
                        for star in stars:
                            count += star.rating
                            result = count / stars_count
                            movie.middle_stars = result
                            movie.save()
                    else:
                        stars = stars[0]
                        movie.middle_stars = stars.rating
                        movie.save()







