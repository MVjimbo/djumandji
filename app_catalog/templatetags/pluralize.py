from django import template


register = template.Library()


@register.filter
def rupluralize(val, arg):
    args = arg.split(',')
    num = int(val)
    cat_of_units = num % 10
    cat_of_tens = (num % 100) // 10

    if cat_of_units == 1 and cat_of_tens != 1:
        return args[0]
    elif 2 <= cat_of_units <= 4 and cat_of_tens != 1:
        return args[1]
    else:
        return args[2]
