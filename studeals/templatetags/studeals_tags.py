from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="filt")
def in_category(offers, category):
    return offers.filter(category=category)

@register.simple_tag(takes_context=True)
def profile_picture(context):
    """
    Tag to retrieve Bootstrap 4 compatible profile picture HTML tag
    """
    if 'user' in context:
        user = context['user']
        if user.userprofile.picture:
            style_class = ''
            src = user.userprofile.picture.url
        else:
            style_class = ' profile_picture'
            src = '#'

        return mark_safe("""
        <img id="profile-picture" src="%s" class="img-fluid img-thumbnail%s" alt="%s\'s profile picture">
        """ % (
            src,
            style_class,
            user.username
        ))
    return ""