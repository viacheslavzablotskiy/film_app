from django.core.mail import send_mail
from accounts.signals import user_created

from django.contrib.auth.base_user import BaseUserManager
from rest_framework.reverse import reverse

from accounts.autorization.generate_token import generate_token, get_domain


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _send_confirm_link_on_mail(self, user):
        token = generate_token(pk=user.pk)
        link = get_domain() + reverse('activate-detail', args=[token])

        message = "Dear, {}. In order to activate your account folow" \
                  "this link: {}".format(user, link)

        send_mail(
            'Confirmation email',
            message,
            "zlava.mag@gmail.com",
            [user.email],
            fail_silently=False,

        )

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("Username is required!")
        if not email:
            raise ValueError("Email is required!")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()

        user_created.send(
            sender=user.__class__,
            instance=user
        )

        self._send_confirm_link_on_mail(user)

        return user

    # def _create_user(self, email, password, **extra_fields):
    #     if not email:
    #         raise ValueError('Email address must be provided')
    #
    #     if not password:
    #         raise ValueError('Password must be provided')
    #
    #     email = self.normalize_email(email)
    #     user = self.model(email=email, **extra_fields)
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    def create_user(self, email=None, password=None, username=None,  **extra_fields):
        return self._create_user(username, email, password,  **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self._create_user(email, password, **extra_fields)