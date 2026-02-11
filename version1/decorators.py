"""
Session-based access control.
- login_required: redirect guests to Login, preserve ?next= for post-login redirect.
- organizer_required: redirect non-organizers to index (or login if not logged in).
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings


def login_required(view_func):
    """Redirect to login if session has no user_id. Store next= for post-login redirect."""

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.session.get("user_id"):
            messages.warning(request, "Please log in to access this page.")
            login_url = getattr(settings, "LOGIN_URL", "/login/")
            next_path = request.path
            if next_path != login_url.rstrip("/") and next_path != "/login":
                return redirect(f"{login_url}?next={next_path}")
            return redirect(login_url)
        return view_func(request, *args, **kwargs)

    return _wrapped


def organizer_required(view_func):
    """Require logged-in user with role organizer. Else redirect to index or login."""

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.session.get("user_id"):
            messages.warning(request, "Please log in to access this page.")
            login_url = getattr(settings, "LOGIN_URL", "/login/")
            next_path = request.path
            if next_path != login_url.rstrip("/") and next_path != "/login":
                return redirect(f"{login_url}?next={next_path}")
            return redirect(login_url)
        if request.session.get("user_role") != "organizer":
            messages.error(request, "This area is for organizers only.")
            return redirect("index")
        return view_func(request, *args, **kwargs)

    return _wrapped
