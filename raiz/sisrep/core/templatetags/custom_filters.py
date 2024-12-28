from django import template

register = template.Library()

@register.filter(name='get_value_from_dict')
def get_value_from_dict(dictionary, key):
    """Obtiene un valor de un diccionario dado."""
    if isinstance(dictionary, dict):
        return dictionary.get(key, '')
    return ''

@register.filter(name='get_value_from_dict_custom')
def get_value_from_dict_custom(dictionary, key):
    """Filtro personalizado para obtener un valor de un diccionario."""
    if isinstance(dictionary, dict):
        return dictionary.get(key, None)
    return None

@register.filter
def index(sequence, position):
    """Obtiene un elemento en una posición específica de una secuencia."""
    try:
        return sequence[position]
    except (IndexError, TypeError):
        return ''

