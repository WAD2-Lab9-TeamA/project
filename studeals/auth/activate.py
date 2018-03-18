from django.template.loader import render_to_string
from django.core.mail import EmailMessage#, EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.html import strip_tags
from . import tokens

def is_activated(user):
    if user is not None and user.last_login is not None:
        return True
    return False

def send_email(request, user):
    activation_url = request.build_absolute_uri(
        reverse('activate_user', args=(
            urlsafe_base64_encode(force_bytes(user.pk)),
        tokens.activation.make_token(user)
        ))
    )
    mail_subject = 'Activate your Studeals account!'
    content = render_to_string('studeals/emails/activate_user.html', {
        'user': user,
        'activation_url': activation_url,
    })

    email = EmailMessage(mail_subject, strip_tags(content), to=[user.email])
    #email = EmailMultiAlternatives(mail_subject, strip_tags(content), to=[user.email])
    #email.attach_alternative(content, "text/html")
    email.send()
