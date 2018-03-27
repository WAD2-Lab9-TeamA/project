from django import template
from django.utils.safestring import mark_safe
from urllib.parse import urlencode
from django.contrib.staticfiles.templatetags.staticfiles import static

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

@register.simple_tag(takes_context=True)
def query_string(context, reset=False, **params):
    """
    Tag to build query strings, use argument reset to make a fresh query string
    """
    if 'query_string' in context and not reset:
        query = context['query_string'].copy()
    else:
        query = {}

    for arg in params:
        if params[arg].strip():
            query[arg] = params[arg].strip()
        elif arg in query:
            del query[arg]

    string = urlencode(query)

    if string:
        return '?%s' % string
    else:
        return ''

@register.simple_tag(takes_context=True)
def category_picture(context):
    """
    Tag to retrieve the category's picture
    """
    if 'category' in context:
        return mark_safe("""
        <img src="%s" alt="Picture" class="category-picture img-fluid">
        """ % static('categories/%s.svg' % context['category'].slug))
    else:
        return ''

@register.filter
def get_type(var):
    """
    Get variable type
    """
    return type(var)

@register.filter
def get(dictionary, key):
    """
    Fetch value from dictionary
    """
    return dictionary[key]

@register.filter
def firstentry(dictionary):
    """
    Get first entry of a dictionary
    """
    return dictionary[list(dictionary.keys())[0]]
