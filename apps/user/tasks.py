from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.models import User

from celery.utils.log import get_task_logger
from celery import shared_task

from time import sleep
logger = get_task_logger(__name__)


@shared_task(name='send_verification_email')
def send_verification_email(user_id):
    try:
        user = User.objects.get(id=user_id)  # Fetch the user object from the database
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = f"{settings.SITE_URL}/user/verify_email/{uid}/{token}/"
        subject = 'Verify your email'
        message = f'Hi {user.username}, please verify your email by clicking the link: {verification_url}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} does not exist.")


@shared_task(name='send_reset_email')
def send_reset_email(user_id):
    try:
        user = User.objects.get(id=user_id)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_password_url = f"{settings.SITE_URL}/user/reset_password/{uid}/{token}/"
        subject = "Password Reset"
        message = f"Hi {user.username}, please click the link to reset your password:\n{reset_password_url}"
        sleep(30)  #  delay for testing purposes
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} does not exist.")
    except Exception as e:
        logger.error(f"Failed to send reset password email to user ID {user_id}: {str(e)}")
