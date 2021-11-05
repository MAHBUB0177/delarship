from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import timezone
import logging
import sys
logger = logging.getLogger(__name__)

def delete_all_unexpired_sessions_for_user(user):
    try:
        user_sessions = []
        user_info = User.objects.get(username=user)
        #all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        all_sessions = Session.objects.filter()
        for session in all_sessions:
            session_data = session.get_decoded()
            if user_info.pk == int(session_data.get('_auth_user_id')):
                user_sessions.append(session.pk)
        Session.objects.filter(pk__in=user_sessions).delete()
        return Session.objects.filter(pk__in=user_sessions)
    except Exception as e:
        logger.error("Error in delete_all_unexpired_sessions_for_user on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        pass

def fn_is_user_permition_exist(p_app_user_name, p_program_id, p_app_name):
    try:
        user_info = User.objects.get(username=p_app_user_name)
        if user_info.has_perm(p_app_name+'.'+p_program_id):
            return True
        else:
            return False
    except Exception as e:
        return False
