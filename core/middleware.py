"""
RBAC Middleware and Decorators
"""
from functools import wraps
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.models import User
from core.models import UserProfile, UserRole

logger = __import__('logging').getLogger(__name__)


class RolePermissionMiddleware:
    """Attach request.user_profile and request.role_permissions to every request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                profile = UserProfile.objects.select_related('role').get(user=user)
                request.user_profile = profile
                request.role_permissions = profile.role
            except UserProfile.DoesNotExist:
                request.user_profile = None
                request.role_permissions = None
        else:
            request.user_profile = None
            request.role_permissions = None
        return self.get_response(request)


def role_required(*allowed_codes):
    """Decorator: restrict view to users with one of the given UserRole.codes."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                from django.shortcuts import redirect
                return redirect(settings.LOGIN_URL)
            try:
                profile = UserProfile.objects.select_related('role').get(user=user)
                role = profile.role
            except UserProfile.DoesNotExist:
                from django.contrib import messages
                messages.error(request, "Access denied — no role assigned.")
                return redirect('/dashboard/')
            if role.code not in allowed_codes:
                from django.contrib import messages
                messages.error(request, "Access denied — insufficient role.")
                return redirect('/dashboard/')
            request.role_permissions = role
            request.user_profile = profile
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def has_permission(request, perm_field):
    """Check whether the logged-in user has a given permission field on their role."""
    rp = getattr(request, 'role_permissions', None)
    if rp is None:
        return False
    return bool(getattr(rp, perm_field, False))
