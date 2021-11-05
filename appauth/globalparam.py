from django.contrib.auth.models import User


class Globaldata:
    def __init__(self, user_full_name, application_title, app_user_id, user_designation, branch_code, head_office_user):
        self.user_full_name = user_full_name
        self.application_title = application_title
        self.app_user_id = app_user_id
        self.user_designation = user_designation
        self.branch_code = branch_code
        self.head_office_user = head_office_user

        self.menu_permition = {'user_full_name': self.user_full_name,
                               'application_title': self.application_title,
                               'app_user_id': self.app_user_id,
                               'global_branch_code': self.branch_code,
                               'is_head_office_user': head_office_user,
                               'user_designation': self.user_designation}
        user_info = User.objects.get(username=self.app_user_id)
        all_permissions = user_info.get_all_permissions()

        for permition in all_permissions:
            self.menu_permition[permition.split('.')[1]] = True

    def get_global_data(self):

        return self.menu_permition

def fn_is_user_permition_exist(p_app_user_name, p_program_id, p_app_name):
    try:
        user_info = User.objects.get(username=p_app_user_name)
        if user_info.has_perm(p_app_name+'.'+p_program_id):
            return True
        else:
            return False
    except Exception as e:
        return False
