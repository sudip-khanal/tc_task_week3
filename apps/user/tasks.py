import logging

from django.contrib.auth import get_user_model

from celery import shared_task
from time import sleep
from apps.user.utils import send_verification_email, send_reset_email

User = get_user_model()
logger = logging.getLogger(__name__)

@shared_task(name='send_verification_email')
def send_verification_email_task(user_id):
    """
    Task to send verification email
    """
    user = User.objects.filter(id=user_id).first()  
    if user:
        send_verification_email(user)
    else:
        logger.error("User not found")


# @shared_task(name='send_reset_email')
# def send_reset_email_task(user_id):
#     """
#     Task to send password reset email
#     """
#     user = User.objects.filter(id=user_id)
#     if user:
#         send_reset_email(user)
#     else:
#         logger.error("Failed to send the email, user not found")


