from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class TokenGenerator(PasswordResetTokenGenerator):
    """
    Source: https://medium.com/@frfahim/django-registration-with-confirmation-email-bb5da011e4ef
    """
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(user.is_active) +
            six.text_type(timestamp)
        )

activation = TokenGenerator()
