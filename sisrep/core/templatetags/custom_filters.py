from django import template

register = template.Library()

@register.filter
def get_value_from_dict(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key, '')
    else:
        return ''
    

@register.filter
def get_value_from_dict(data, key):
    if isinstance(data, dict):
        return data.get(key, 0)
    return 0


@register.filter(name='get_value_from_dict_custom')
def get_value_from_dict_custom(dictionary, key):
    return dictionary.get(key, None)


register = template.Library()

@register.filter
def index(sequence, position):
    try:
        return sequence[position]
    except IndexError:
        return ''