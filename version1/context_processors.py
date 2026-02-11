"""
Session context for templates.
Exposes session.user (conceptual) and session.organizer so templates can
conditionally show/hide Login, Register, Create Workshop, Dashboard.
"""


def session_context(request):
    """
    Inject session user and organizer state into every template.
    Use in templates: {% if session_user %}, {% if is_organizer %}.
    """
    user_id = request.session.get("user_id")
    user_name = request.session.get("user_name")
    user_role = request.session.get("user_role")
    organizer_id = request.session.get("organizer_id")

    # session.user (conceptual): present when any user is logged in
    session_user = None
    if user_id and user_name is not None:
        session_user = {
            "id": user_id,
            "name": user_name,
            "role": user_role or "user",
        }

    # session.organizer: True when current user has organizer role (and we store organizer_id)
    is_organizer = (
        user_role == "organizer"
        and (organizer_id is not None or user_id is not None)
    )

    return {
        "session_user": session_user,
        "is_organizer": is_organizer,
    }
