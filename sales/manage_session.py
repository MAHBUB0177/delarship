from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import timezone

def delete_all_unexpired_sessions_for_user(user):
    try:
        user_sessions = []
        user_info = User.objects.get(username=user)
        all_sessions = Session.objects.filter(
            expire_date__gte=timezone.now())
        for session in all_sessions:
            session_data = session.get_decoded()
            if user_info.pk == int(session_data.get('_auth_user_id')):
                user_sessions.append(session.pk)
        Session.objects.filter(pk__in=user_sessions).delete()
        return Session.objects.filter(pk__in=user_sessions)
    except Exception as e:
        pass

def fn_is_user_permition_exist(p_app_user_name, p_program_id):
    try:
        user_info = User.objects.get(username=p_app_user_name)
        if user_info.has_perm('SalesERP.'+p_program_id):
            return True
        else:
            return False
    except Exception as e:
        return False
