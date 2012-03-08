'''
Created on 2012-11-20
@author: Perchouli
@contact: jp.chenyang@gmail.com
@version: 0.1.0
'''
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def substring(value, arg):
    try:
        length = int(arg)
    except ValueError:
        return value
    
    if len(value) < length:
        return value
    else:
        return value[0:length] + '...'
substring.is_safe = True
substring = stringfilter(substring)

@register.filter
def divstring(value, arg):
    try:
        length = int(arg)
    except ValueError:
        return value
    v = ''
    values = value.split('\n')
    for vv in values:
        for k in range(len(vv)):
            if k%length == 0 :
                v = v + '\n'
            v = v + vv[k]
    return v        
divstring.is_safe = True
divstring = stringfilter(divstring)