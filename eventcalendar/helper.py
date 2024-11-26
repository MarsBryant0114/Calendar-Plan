from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth.models import User


def get_current_user():
    try:
        # Retrieve all active sessions
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        user_id_list = []

        for session in active_sessions:
            data = session.get_decoded()
            user_id = data.get("_auth_user_id", None)
            if user_id is not None:
                user_id_list.append(user_id)

        if not user_id_list:
            return None  # No active authenticated users

        # Retrieve the first user (example use case)
        user = User.objects.get(id=user_id_list[0])
        return user
    except (IndexError, User.DoesNotExist) as e:
        # Handle case where no valid users are found
        print(f"Error: {e}")
        return None
