from django import template
from studeals.models import Category, Offer
register=template.Library()


@register.filter(name="filt")
def in_category(offers, category):
    return offers.filter(category=category)