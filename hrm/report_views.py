from hrm.validations import app_user_id
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
from django.db import connection, transaction
from django.template.loader import render_to_string
from django.db.models import Count, Sum, Avg
from django.db.models import Q, F
import logging
import sys
logger = logging.getLogger(__name__)
from decimal import Context, Decimal
from datetime import date, datetime, timedelta
import time
from .report_data import *
#from appauth.utils get_global_report_data
from appauth.views import get_global_data
from appauth.utils import fn_get_reports_parameter, get_business_date
from appauth.models import Branch, Global_Parameters
from hrm.forms import CommonReportForm

def get_global_report_data(request):
    
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    try:
        user_full_name = request.session['user_full_name']
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        company = Global_Parameters.objects.get()
        application_title = request.session["application_title"]
        company_name = company.company_name
        company_address = company.company_address
    except Exception as e:
        print(str(e))
        return render(request, 'appauth/appauth-login.html')
    data = {
        'user_full_name': user_full_name,
        'app_user_id': app_user_id,
        'branch_code': branch_code,
        'company_name': company_name,
        'company_address': company_address,
        'application_title': application_title,
    }

    return data
##################

class hrm_report_salary_sheet(TemplateView):
    template_name = 'hrm_report/hrm-report-salary-sheet.html'
   
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms
        return render(request, self.template_name, context)


class hrm_report_salary_sheet_print_view(TemplateView):
    template_name = 'hrm_report/hrm-report-salary-sheet-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_salary_sheet_rpt(app_user_id)
            sum_data=fn_get_salary_sheet_rpt_sum(app_user_id)
            rpt_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data, **rpt_param }
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name) 






########################


class hrm_report_employee_sheet(TemplateView):
    template_name = 'hrm_report/hrm-report-employee-sheet.html'
   
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, })
        context = get_global_data(request)
        context['forms'] = forms
        return render(request, self.template_name, context)


class hrm_report_employee_sheet_print_view(TemplateView):
    template_name = 'hrm_report/hrm-report-employee-sheet-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_employee_sheet_rpt(app_user_id)
            # sum_data=fn_get_employee_sheet_rpt(app_user_id)
            rpt_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            # data['sum_data'] = sum_data
            data = {**data, **rpt_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(str(e))
            return render(request, self.template_name) 