from django import template
register = template.Library()
from django.contrib.auth import get_user_model

USER = get_user_model()

@register.filter(name="isOdd")
def isOdd(value: int): return False if value%2 == 0 else True


@register.filter
def getList(arr):
    
    return [x for x in arr]



@register.filter
def hasPerm(user: USER, perm)->bool:

    return user.has_perm(perm)