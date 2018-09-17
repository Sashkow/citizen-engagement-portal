from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)




@register.filter
def divide(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None

@register.filter
def multiply(value, arg):
    return value*arg

@register.filter()
def to_int(value):
    return int(value)

def to_float(value):
    return float(value)

def minus(value, arg):
    return value - arg