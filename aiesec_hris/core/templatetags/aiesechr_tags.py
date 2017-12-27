from django import template
from django.core.exceptions import FieldDoesNotExist

from bs4 import BeautifulSoup

register = template.Library()


@register.filter(name='bootstrap_form_input')
def bootstrap_form_input(value, arg):
    """
    1. Adds the `form-control` class to the input field
    2. Sets placeholder
    3. Strips html tags from placeholder
    """
    # incase args has html tags, strip them
    soup = BeautifulSoup(arg, 'html.parser')
    arg = soup.get_text()
    return value.as_widget(attrs={'placeholder': arg, 'class': 'form-control'})


@register.filter('fieldtype')
def fieldtype(field):
    return field.field.widget.__class__.__name__


@register.filter('get_attr')
def get_attr(obj, attr):
    result = '-'
    try:
        result = ", ".join([val.__str__() for val in getattr(obj, attr).all()])
    except AttributeError:
        try:
            func = 'get_%s_display' % attr
            result = getattr(obj, func)()
        except AttributeError:
            result = getattr(obj, attr)

    return result


@register.filter('get_help_text')
def get_help_text(obj, attr):
    return obj.__class__._meta.get_field(attr).help_text


@register.filter('get_verbose')
def get_verbose(obj, attr):
    try:
        return obj.__class__._meta.get_field(attr).verbose_name
    except FieldDoesNotExist:
        return attr.replace('_', ' ')


@register.filter('parse_int')
def parse_int(obj):
    return int(obj)

@register.filter('is_parent_of')
def is_parent_of(p1, p2):
    return p1.is_parent_of(p2)
