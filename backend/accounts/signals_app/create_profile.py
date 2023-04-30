from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User, AuthUser


# @transaction.atomic
# @receiver(post_save, sender=User)
# def create_profile_(sender, instance, created, signal, *args, **kwargs):
#     if created:
#         AuthUser.objects.create(user=instance)