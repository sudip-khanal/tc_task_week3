import unittest

from unittest.mock import patch
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

from apps.user.models import User
from apps.user.utils import send_verification_email


class TestSendVerificationEmail(unittest.TestCase):
    
    @patch('apps.user.tasks.User.objects.get')
    @patch('apps.user.tasks.send_mail')
    @patch('apps.user.tasks.default_token_generator.make_token')
    def test_send_verification_email(self, mock_make_token, mock_send_mail, mock_get_user):
        # Arrange
        user_id = 2
        mock_user = User(id=user_id, username='testuser', email='testuser@example.com')
        mock_get_user.return_value = mock_user
        mock_make_token.return_value = 'test-token'
        
        # Act
        send_verification_email(user_id)
        
        # Assert
        mock_get_user.assert_called_once_with(id=user_id)
        mock_make_token.assert_called_once_with(mock_user)
        
        uid = urlsafe_base64_encode(force_bytes(mock_user.pk))
        verification_url = f"{settings.SITE_URL}/user/verify_email/{uid}/test-token/"
        subject = 'Verify your email'
        message = f'Hi {mock_user.username}, please verify your email by clicking the link: {verification_url}'
        
        mock_send_mail.assert_called_once_with(subject, message, settings.EMAIL_HOST_USER, [mock_user.email])
        call_args = mock_send_mail.call_args[0]
        sent_subject = call_args[0]
        sent_message = call_args[1]
        sent_from = call_args[2]
        sent_to = call_args[3][0]
        
        self.assertEqual(sent_subject, subject)
        self.assertEqual(sent_message, message)
        self.assertEqual(sent_from, settings.EMAIL_HOST_USER)
        self.assertEqual(sent_to, mock_user.email)



