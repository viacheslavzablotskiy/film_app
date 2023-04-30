from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # def ready(self):
    #     from django.db.models.signals import post_save
    #     from accounts.signals_app.create_profile import create_profile_
    #     from accounts.models import User
    #     post_save.connect(create_profile_, sender=User)
