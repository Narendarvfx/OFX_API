"""
Custom Django Template Tags for OFX App
"""

#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import random
from django import template
from django.contrib.auth.models import Group


register = template.Library()


@register.filter(name='percentage')
def percentage(a, b):
    try:
        return "%.2f%%" % ((float(a) / float(b)) * 100)
    except (ValueError, ZeroDivisionError):
        return ''


@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)


@register.filter
def shuffle(arg):
    tmp = list(arg)[:]
    random.shuffle(tmp)
    return tmp


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False