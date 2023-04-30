from django.contrib import admin
from film.models import *
# Register your models here.

admin.site.register(Movie)
admin.site.register(MovieShots)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Actor)



