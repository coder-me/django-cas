from functools import wraps
from django.core.exceptions import SuspiciousOperation

from django.utils.decorators import (
    available_attrs
)


def require_AJAX(view_func):
    """
    Decorator that allow ajax request only and
    raise SuspiciousOperation exception if request
    is not an ajax.
    """
    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.is_ajax():
            raise SuspiciousOperation
        response = view_func(request, *args, **kwargs)
        return response
    return _wrapped_view_func
