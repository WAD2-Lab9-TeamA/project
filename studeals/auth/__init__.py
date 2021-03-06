from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from app import settings
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

def authenticate(username=None, password=None):
    try:
        user = User.objects.get(username=username)

        if user.check_password(password):
            return user
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=username)

            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

def send_password_reset_email(request, user):
    mail_subject = 'Your password reset link'
    content = render_to_string('studeals/emails/reset_password.html', {
        'user': user,
        'absolute_url': request.build_absolute_uri('/').strip('/'),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)
    })

    #email = EmailMessage(mail_subject, strip_tags(content), to=[user.email])
    email = EmailMultiAlternatives(mail_subject, strip_tags(content), to=[user.email])
    email.attach_alternative(content, "text/html")
    email.send()

def recaptcha_check(recaptcha_response):
    data = urlencode({
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    })
    req = Request('https://www.google.com/recaptcha/api/siteverify', data.encode())

    try:
        response = json.load(urlopen(req))

        if response['success']:
            return True
    except:
        pass

    return False
