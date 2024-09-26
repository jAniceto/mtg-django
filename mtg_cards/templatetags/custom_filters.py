from django import template
from django.template.defaultfilters import stringfilter
from mtg_utils.mtg import color_families, symbols_html


register = template.Library()

@register.filter
def absandformat(value):
    """Formats a float value and makes it absolute"""
    value = abs(round(value))
    return f'{value:.0f}'


@register.filter
@stringfilter
def manasymbols(value):
    """Returns the list of color symbols from the family name"""
    colors_dict = color_families()
    try:
        colors = colors_dict[value.lower()]
    except KeyError as e:
        colors = []
    return colors


@register.filter
@stringfilter
def parse_mana_symbols(value):
    """Returns the list of color symbols from the family name"""
    mana_dict = symbols_html()
    for k, v in mana_dict.items():
        value = value.replace(k, v)
    return value
