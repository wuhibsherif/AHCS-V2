from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect
from login import urls


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied

        return wrapper_func

    return decorator
