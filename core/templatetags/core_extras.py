from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_dict_item_list(dict_list, key):
    """Given a list of dicts [{key: key, val: ...}, ...] return the val for the given key, or None."""
    for entry in dict_list:
        if entry.get('key') == key:
            return entry.get('val')
    return None

@register.filter
def dict_key(d, key):
    return d.get(key)
