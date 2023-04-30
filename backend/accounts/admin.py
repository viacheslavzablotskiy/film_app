from django.contrib import admin
from .models import AuthUser, User, SocialLink, Follower
# Register your models here.
admin.site.register(User),
admin.site.register(AuthUser)
admin.site.register(SocialLink)
admin.site.register(Follower)