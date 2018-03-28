from django import template
from django.utils.safestring import mark_safe
from urllib.parse import urlencode
from django.contrib.staticfiles.templatetags.staticfiles import static
from app import settings

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

@register.simple_tag(takes_context=True)
def generate_map(context,zoom=14,size="300x250"):

    if 'position' in context:
        position = '%s,%s' % (
            context['position']['results'][0]['geometry']['location']['lat'],
            context['position']['results'][0]['geometry']['location']['lng']
        )
    else:
        position = '%s,%s' % (
            context['offer'].place_latitude,
            context['offer'].place_longitude
        )

    if 'radius' in context:
        radius = context['radius']
        if radius == 0.2:
            zoom = 15
        elif radius == 0.5:
            zoom = 14
        elif radius == 1.0:
            zoom = 13
        elif radius == 2.0:
            zoom = 12

    query_str = urlencode({
        'zoom': zoom,
        'center': position,
        'key': settings.GMAPS_CLIENTSIDE_API_KEY,
        'size': size
    })

    index = 1

    if 'offer' in context:
        query_str += "&" + urlencode({
            "markers": str(context['offer'].place_latitude) + "," + str(context['offer'].place_longitude)
        })

    if 'offers' in context:
        print(context['offers'])
        for offer in context['offers']:
            query_str += "&" + urlencode({
                "markers": "label:" + str(index) + "|" + str(offer.place_latitude) + "," + str(offer.place_longitude)
            })
            index += 1

    return mark_safe("""<img
    class="img-fluid"
    alt="Map"
    src="https://maps.googleapis.com/maps/api/staticmap?%s"
    >""" % query_str)
