from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import FieldDoesNotExist
from django.core import serializers
from random import randint
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import date, datetime, timedelta
from django.db import connection, transaction
from django.template.loader import render_to_string
from django.db.models import Count, Sum, Avg
import logging
import sys
logger = logging.getLogger(__name__)
from decimal import Decimal
from django.utils import timezone
import time

all_permissions = {}
from hrm.models import Department_Info,Employee_Designation
from .models import *
from .forms import *
from .utils import *
from .validations import *
from .myException import *
from .globalparam import *
from finance.utils import fn_open_account_transaction_screen, fn_get_transaction_account_type, fn_get_account_info_byactype
from appauth.manage_session import *

# Create your views here.

global_parameters = {}


# def get_global_data(request):

#     if not request.user.is_authenticated:
#         return render(request, 'appauth/appauth-login.html')

#     return global_parameters

def get_global_data(request):

    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    try:
        user_full_name = request.session['user_full_name']
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        application_title = request.session["application_title"]
        is_head_office_user = request.session["is_head_office_user"]

        if is_head_office_user == 'Y':
            is_head_office_user_bool = True
        else:
            is_head_office_user_bool = False

    except Exception as e:
        return render(request, 'appauth/appauth-login.html')
    user_info = User.objects.get(username=request.user)
    all_permissions = user_info.get_all_permissions()
    context = {
        'user': request.user,
        'user_full_name': user_full_name,
        'app_user_id': app_user_id,
        'all_permissions': all_permissions,
        'branch_code': branch_code,
        'global_branch_code': branch_code,
        'is_head_office_user': is_head_office_user_bool,
        'is_head_office_user_bool': is_head_office_user_bool,
        'application_title': application_title,
    }

    for programs in all_permissions:
        context[programs.split('.')[1]] = True

    return context


class HomeView(TemplateView):
    template_name = 'appauth/appauth-login.html'


def appauth_home(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    context = get_global_data(request)
    return render(request, "appauth/appauth-home.html", context)


def login_view(request):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    global global_parameters

    delete_all_unexpired_sessions_for_user(username)

    try:

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            user_info = User.objects.get(username=username)

            request.session['user_full_name'] = user_info.first_name + \
                " "+user_info.last_name
            request.session['app_user_id'] = username
            app_setting = Global_Parameters.objects.get()
            user_setting = User_Settings.objects.get(
                app_user_id=username, is_active=True, is_deleted=False)
            reset_user_password = user_setting.reset_user_password
            request.session['application_title'] = app_setting.application_title
            request.session['branch_code'] = user_setting.branch_code

            if reset_user_password:
                return render(request, "appauth/appauth-reset-password.html", {"message": "Reset Your Password!"})

            if not user_setting.is_active:
                return render(request, "appauth/appauth-login.html", {"message": "You Are Not Permitted Now."})

            if user_setting.head_office_admin:
                is_head_office_user = 'Y'
            else:
                is_head_office_user = 'N'
            request.session["is_head_office_user"] = is_head_office_user

            global_param = Globaldata(request.session['user_full_name'], request.session['application_title'],
                                      request.session["app_user_id"], '.....', user_setting.branch_code, is_head_office_user)
            global_parameters = global_param.get_global_data()
            return HttpResponseRedirect(reverse("appauth-home"))
        else:
            return render(request, "appauth/appauth-login.html", {"message": "Invalid Credentials."})

    except Exception as e:
        return render(request, "appauth/appauth-login.html", {"message": str(e)})


def logout_view(request):
    logout(request)
    return render(request, "appauth/appauth-login.html", {"message": "Logged out."})


class reset_password(TemplateView):
    template_name = 'appauth/appauth-reset-password.html'


def reset_user_password(request):

    new_password = request.POST.get('new_password', False)
    old_password = request.POST.get('password', False)
    user_name = request.POST.get('username', False)
    confirm_password = request.POST.get('new_password_confirm', False)

    if new_password != confirm_password:
        return render(request, "appauth/appauth-reset-password.html", {"message": "New password and confirm password does not match!"})

    user = authenticate(request, username=user_name, password=old_password)

    if user is not None:
        try:
            user = User.objects.get(username=user_name)
            user_info = User_Settings.objects.get(app_user_id=user_name)
            user_info.reset_user_password = False
            user.set_password(new_password)
            user.save()
            user_info.save()
            return render(request, "appauth/appauth-login.html", {"message": "Password Reset Successfully"})
        except Exception as e:
            message = str(e)
        return render(request, "appauth/appauth-reset-password.html", {"message": message})
    else:
        return render(request, "appauth/appauth-reset-password.html", {"message": "Invalid Credentials!"})


def DashboardView(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    context = get_global_data(request)
    data = dict()
    try:
        app_user_id = request.session["app_user_id"]
        #cbd = get_business_date(branch_code)
        #cursor = connection.cursor()
        #cursor.callproc("fn_fin_dashboard_data",[branch_code, somity_code, app_user_id, cbd])
        #row = cursor.fetchone()
    except Exception as e:
        data['form_is_valid'] = False
        logger.error("Error in finance_ledger_balance on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))


class CreateUser(TemplateView):
    template_name = 'appauth/appauth-app-user.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = AppUserModelForm()
        context = get_global_data(request)
        context['success_message'] = ''
        context['error_message'] = ''
        context['form'] = form
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        context = get_global_data(request)
        form = AppUserModelForm(request.POST)
        print(form)
        error_message = "Please check the error"
        success_message = ""
        if form.is_valid():
            try:
                with transaction.atomic():
                    user_setting = Global_Parameters.objects.get()
                    app_user_id = form.cleaned_data["app_user_id"]
                    employee_id = form.cleaned_data["employee_id"].employee_id
                    branch_code = form.cleaned_data["branch_code"]
                    employee_name = fn_get_employee_name(employee_id)
                    user_password = str(randint(111111, 999999))
                    user = User.objects.create_user(
                        app_user_id, '', user_password)
                    user.last_name = employee_name
                    user.save()
                    user_info = User.objects.get(username=app_user_id)
                    post = form.save(commit=False)
                    post.django_user_id = user_info.id
                    post.reset_user_password = True
                    post.cash_gl_code = user_setting.cash_gl_code
                    post.employee_name = employee_name
                    post.save()
                    success_message = "User Created Successfully! \nTemporary password for the User : "+user_password
                    error_message = ""
                    form = AppUserModelForm()
            except Exception as e:
                logger.error("Error in Creating User {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                context['form'] = form
                context['success_message'] = success_message
                context['error_message'] = 'Error '+str(e)+' in Creating User!'
                return render(request, self.template_name, context)
        else:
            error_message = form.errors.as_json()

        context['form'] = form
        context['success_message'] = success_message
        context['error_message'] = error_message
        return render(request, self.template_name, context)


class ApplicationUserList(TemplateView):
    template_name = 'appauth/appauth-application-users.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        forms = AppUserModelForm()
        context = get_global_data(request)
        context['forms'] = forms
        return render(request, self.template_name, context)


@transaction.atomic
def reset_appuser_password(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    data['success_message'] = ''
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            app_user_id = request.POST.get('app_user_id')
            user_info = User_Settings.objects.get(app_user_id=app_user_id)
            user = User.objects.get(username=user_info.app_user_id)
            user_info.reset_user_password = True
            new_password = str(randint(111111, 999999))
            user.set_password(new_password)
            user.save()
            user_info.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Password Reset Successfully\nNew temporary password for this user : '+new_password
    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        logger.error("Error on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)
    return JsonResponse(data)


def appauth_appuser_update(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    try:
        #django_user_id = request.GET.get('django_user_id')
        instance_data = get_object_or_404(
            User_Settings, django_user_id=id)
        employee_name = instance_data.employee_name
        template_name = 'appauth/appauth-appuser-update.html'
        context = {}
        data = dict()

        if request.method == 'POST':
            form = AppUserEditForm(request.POST, instance=instance_data)
            data['form_error'] = form.errors.as_json()
            if form.is_valid():
                obj = form.save(commit=False)
                obj.employee_name = employee_name
                obj.save()
                context = get_global_data(request)
                context['success_message'] = ''
                context['error_message'] = ''
                data['form_is_valid'] = True
            else:
                data['form_is_valid'] = False
                data['error_message'] = form.errors.as_json()
                return JsonResponse(data)
        else:
            form = AppUserEditForm(instance=instance_data)
            context = get_global_data(request)
            context['form'] = form
            context['id'] = id
            data['html_form'] = render_to_string(
                template_name, context, request=request)
        return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        return JsonResponse(data)


class appauth_branch_view(TemplateView):
    template_name = 'appauth/appauth-branch-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = BranchModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def appauth_branch_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = BranchModelForm(request.POST)
                if form.is_valid():
                    branch_code = form.cleaned_data["branch_code"]
                    if fn_val_check_branch_exist(branch_code):
                        data['error_message'] = 'Branch Code Already Exist!'
                        return JsonResponse(data)

                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Branch Opened Successfully!'
                else:
                    data['form_is_valid'] = False
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def appauth_branch_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(Branch, branch_code=id)
            old_branch_code = instance_data.branch_code
            template_name = 'appauth/appauth-branch-edit.html'

            if request.method == 'POST':
                form = BranchModelForm(request.POST, instance=instance_data)
                data['form_error'] = form.errors.as_json()
                if form.is_valid():
                    branch_code = form.cleaned_data["branch_code"]

                    if branch_code != old_branch_code:
                        data['error_message'] = 'Branch Code Modification is Not Allowed!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    obj = form.save(commit=False)
                    obj.save()
                    data['success_message'] = 'Updated Successfully!'
                    data['error_message'] = ''
                    data['form_is_valid'] = True
                    return JsonResponse(data)
                else:
                    data['form_is_valid'] = False
                    data['error_message'] = form.errors.as_json()
                    return JsonResponse(data)
            else:
                form = BranchModelForm(instance=instance_data)
                context = get_global_data(request)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


class appauth_country_view(TemplateView):
    template_name = 'appauth/appauth-country-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Country_Model_Form()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def appauth_country_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Country_Model_Form(request.POST)
                if form.is_valid():
                    country_id = fn_get_country_id()
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.country_id = country_id
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Country Added Successfully!'
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def appauth_country_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(Loc_Country, branch_code=id)
            template_name = 'appauth/appauth-country-edit.html'

            if request.method == 'POST':
                form = Country_Model_Form(request.POST, instance=instance_data)
                data['form_error'] = form.errors.as_json()
                if form.is_valid():

                    obj = form.save(commit=False)
                    obj.save()
                    data['success_message'] = 'Updated Successfully!'
                    data['error_message'] = ''
                    data['form_is_valid'] = True
                    return JsonResponse(data)
                else:
                    data['form_is_valid'] = False
                    data['error_message'] = form.errors.as_json()
                    return JsonResponse(data)
            else:
                form = Country_Model_Form(instance=instance_data)
                context = get_global_data(request)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


class appauth_employee_view(TemplateView):
    template_name = 'appauth/appauth-employee-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Employees_Model_Form()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def appauth_employee_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Employees_Model_Form(request.POST)
                if form.is_valid():
                    app_user_id=request.session['app_user_id']
                    branch_code = form.cleaned_data["branch_code"].branch_code
                    employee_name = form.cleaned_data["employee_name"]
                    present_address = form.cleaned_data["present_address"]
                    phone_number = form.cleaned_data["mobile_num"]
                    employee_id = fn_get_employee_id()
                    cbd = get_business_date(branch_code, app_user_id)

                    status, error_message = fn_open_account_transaction_screen(p_transaction_screen='EMP_ENTRY', p_branch_code=branch_code, p_center_code='0',
                                                                               p_app_user_id=request.session[
                                                                                   "app_user_id"], p_client_id=employee_id, p_client_name=employee_name,
                                                                               p_client_address=present_address, p_phone_number=phone_number,p_cbd=cbd, p_limit_amount=0.00)
                    if not status:
                        data['error_message'] = error_message
                        raise Exception(error_message)
                        

                    account_type, client_type = fn_get_transaction_account_type(
                        p_transaction_screen='EMP_ENTRY')

                    account_number, _, _, _ = fn_get_account_info_byactype(
                        p_client_id=employee_id, p_account_type=account_type)

                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.employee_id = employee_id
                    post.account_number = account_number
                    post.save()

                    data['form_is_valid'] = True
                    data['success_message'] = 'Employee Added Successfully.'
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        if len(data['error_message']) > 0:
            return JsonResponse(data)
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def appauth_employee_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(Employees, employee_id=id)
            old_employee_id = instance_data.employee_id
            template_name = 'appauth/appauth-employee-edit.html'

            if request.method == 'POST':
                form = Employees_Model_Form(
                    request.POST, instance=instance_data)
                data['form_error'] = form.errors.as_json()
                if form.is_valid():
                    employee_id = form.cleaned_data["employee_id"]

                    if employee_id != old_employee_id:
                        data['error_message'] = 'Employee Code Modification is Not Allowed!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    obj = form.save(commit=False)
                    obj.save()
                    data['success_message'] = 'Updated Successfully!'
                    data['error_message'] = ''
                    data['form_is_valid'] = True
                    return JsonResponse(data)
                else:
                    data['form_is_valid'] = False
                    data['error_message'] = form.errors.as_json()
                    return JsonResponse(data)
            else:
                form = Employees_Model_Form(instance=instance_data)
                context = get_global_data(request)
                designation=Employee_Designation.objects.all()
                department=Department_Info.objects.all()
                context['designation']=designation
                context['department']=department
                context['data'] = instance_data
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


def appauth_choice_employeelist(request):
    branch_code = request.GET.get('branch_code')

    list_data = Employees.objects.filter().values(
        'employee_id', 'employee_name').order_by('employee_name')
    if branch_code:
        list_data.filter(branch_code=branch_code)
    return render(request, 'appauth/appauth-choice-employeelist.html', {'list_data': list_data})


def appauth_choice_branchlist(request):
    branch_code = request.GET.get('branch_code')
    list_data = Branch.objects.filter().values(
        'branch_code', 'branch_name').order_by('branch_name')
    return render(request, 'appauth/appauth-choice-branchlist.html', {'list_data': list_data})


def appauth_choice_appuserlist(request):
    branch_code = request.GET.get('branch_code')
    list_data = User_Settings.objects.filter(branch_code=branch_code).values(
        'employee_name', 'app_user_id').order_by('employee_name')
    return render(request, 'appauth/appauth-choice-appuserlist.html', {'list_data': list_data})


def appauth_report_submit(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    if request.method == 'GET':
        report_name = request.GET["report_name"]
        app_user_id = request.session["app_user_id"]
        report_config = Report_Configuration.objects.get()
        report_urls = report_config.report_url + \
            'report_name='+report_name+'&user_id='+app_user_id
        data['form_is_valid'] = True
        data['report_urls'] = report_urls
        return JsonResponse(data)

    report_data = request.POST.getlist('report_data')
    data_dict = json.loads(report_data[0])
    report_name = request.POST["report_name"]
    app_user_id = request.session["app_user_id"]
    branch_code = request.session["branch_code"]
    try:
        parameter_list = []
        for param in data_dict:
            parameter_name = param
            parameter_name_value = data_dict[parameter_name]
            row = Report_Parameter(app_user_id=app_user_id, report_name=report_name,
                                   parameter_name=parameter_name, parameter_values=parameter_name_value)
            parameter_list.append(row)

        Report_Parameter.objects.filter(app_user_id=app_user_id).delete()
        Report_Parameter.objects.bulk_create(parameter_list)

        cursor = connection.cursor()
        cursor.callproc("fn_run_report", [app_user_id, report_name])
        row = cursor.fetchone()

        if row[0] != 'S':
            logger.error("Error in fn_run_report on line {} \nType: {} \nError:{}".format(
                sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
            raise Exception(row[1])

        report_config = Report_Configuration.objects.get()
        report_urls = report_config.report_url
        data['form_is_valid'] = True
        data['report_urls'] = report_urls
        return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        logger.error("Error in appauth_report_submit on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        data['error_message'] = 'Report Error : '+str(e)
        return JsonResponse(data)
