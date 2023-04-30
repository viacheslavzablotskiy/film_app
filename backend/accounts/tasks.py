from __future__ import absolute_import, unicode_literals
from celery import shared_task, Celery
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
import ssl
import logging

from backend.celery import app
from django.core.mail import send_mail

@app.task
def send_mail_task(*args):

    send_mail(*args)




# @app.task
# def send_verification_email(user_id):
#     UserModel = get_user_model()
#     try:
#         user = UserModel.objects.get(pk=user_id)
#         token = user.verification_uuid
#         send_mail(
#             'Verify your QuickPublisher account',
#             'Follow this link to verify your account: '
#             'http://localhost:8000%s' % reverse('message', kwargs={'token': str(token)}),
#             'zlava.mag@gmail.com',
#             [user.email],
#             fail_silently=False,
#         )
#     except UserModel.DoesNotExist:
#         logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
