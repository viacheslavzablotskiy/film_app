from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .scripts_model.page_acounts import validate_size_image
from .scripts_model.path_file import get_path_upload_avatar
from .scripts_model.UserManger import UserAccountManager
import uuid


class User(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserAccountManager()
    username = models.CharField(
        db_index=True,
        max_length=255,
        unique=True,
        blank=False
    )
    email = models.EmailField('email', unique=True, blank=False, null=False)
    full_name = models.CharField('full name', blank=True, null=True, max_length=400)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    is_verified = models.BooleanField('verified', default=False)  # Add the `is_verified` flag
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)

    def get_full_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    def get_tokens(self):
        self.refresh_token = self._generate_refresh_token()

        return {
            'access_token': self._generate_access_token(),
            'refresh_token': self._generate_refresh_token()
        }

    def _generate_access_token(self):
        dt = datetime.now() + timedelta(days=1)
        token = jwt.encode({
            'id': self.pk,
            "type": "access",
            'exp': dt.utcfromtimestamp(dt.timestamp())  # CHANGE HERE
        }, settings.SECRET_KEY, algorithm='HS256')
        # token = generate_token(
        #     id=self.pk,
        #     type="access",
        #     exp=dt.strftime('%S')
        # )
        return token

    def _generate_refresh_token(self):
        dt = datetime.now() + timedelta(days=5)
        token = jwt.encode({
            'id': self.pk,
            "type": "refresh",
            'exp': dt.utcfromtimestamp(dt.timestamp())  # CHANGE HERE
        }, settings.SECRET_KEY, algorithm='HS256')
        # token = generate_token(
        #     id=self.pk,
        #     type="refresh",
        #     exp=dt.strftime('%S')
        # )

        self.refresh_token = token
        self.save()

        return token


class AuthUser(models.Model):
    """ Модель пользователя на платформе(profile)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user_profile", related_query_name="user_profile")
    email = models.EmailField(max_length=150)
    join_date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=2000, blank=True, null=True)
    display_name = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=get_path_upload_avatar,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_size_image]
    )

    @property
    def is_authenticated(self):
        """ Всегда возвращает True. Это способ узнать, был ли пользователь аутентифицированы
        """
        return True

    def __str__(self):
        return f"{self.user}"

    @transaction.atomic
    @receiver(post_save, sender=User)
    def create_profile_(sender, instance, created, signal, *args, **kwargs):
        if created:
            AuthUser.objects.create(user=instance)


class Follower(models.Model):
    """ Модель подписчиков
    """
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='owner')
    subscriber = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='subscribers')

    def __str__(self):
        return f'{self.subscriber} подписан на {self.user}'


class SocialLink(models.Model):
    """ Модель ссылок на соц. сети пользователя
    """
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='social_links')
    link = models.URLField(max_length=100)

    def __str__(self):
        return f'{self.user}'
