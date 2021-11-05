
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
from decimal import Decimal
from datetime import date, datetime, timedelta
import time

from .report_data import *
from sales.forms import CommonReportForm, Emi_History_Query
from appauth.views import get_global_data
from appauth.utils import fn_get_reports_parameter, get_business_date

from sales.models import Application_Settings
def get_global_report_data(request):

    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    try:
        user_full_name = request.session['user_full_name']
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        company = Application_Settings.objects.get()
        application_title = request.session["application_title"]
        company_name = company.company_name
        company_address = company.company_address
        company_mobile = company.company_mobile
        company_email = company.company_email
        invoice_line1 = company.invoice_line1
        invoice_line2 = company.invoice_line2
        invoice_line3 = company.invoice_line3
        company_logo = company.company_logo
        if invoice_line1 is None:
            invoice_line1 = ''
        if invoice_line2 is None:
            invoice_line2 = ''
        if invoice_line3 is None:
            invoice_line3 = ''
    except Exception as e:
        return render(request, 'appauth/appauth-login.html')
    data = {
        'user': request.user,
        'user_full_name': user_full_name,
        'app_user_id': app_user_id,
        'branch_code': branch_code,
        'company_name': company_name,
        'company_address': company_address,
        'company_mobile': company_mobile,
        'company_email': company_email,
        'invoice_line1': invoice_line1,
        'invoice_line2': invoice_line2,
        'invoice_line3': invoice_line3,
        'application_title': application_title,
        'company_logo': company_logo
    }

    return data

# class sales_report_packet_return(TemplateView):
#     template_name = 'delar_report/delar-report-packet-return.html'

#     def get(self, request):
#         if not request.user.is_authenticated:
#             return render(request, 'appauth/appauth-login.html')
#         app_user_id = request.session["app_user_id"]
#         branch_code = request.session["branch_code"]
#         cbd = get_business_date(branch_code, app_user_id)

#         forms = CommonReportForm(
#             initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
#         context = get_global_data(request)
#         context['forms'] = forms

#         return render(request, self.template_name, context)

# class sales_report_packet_return_print_view(TemplateView):
#     template_name = 'delar_report/delar-report-packet-return-print-view.html'

#     def get(self, request):
#         if not request.user.is_authenticated:
#             return render(request, 'appauth/appauth-login.html')
#         try:
#             app_user_id = request.session["app_user_id"]
#             data = get_global_report_data(request)
#             dtl_data = fn_get_packet_return_rpt(app_user_id)
#             sum_data = fn_get_sales_summary(app_user_id)
#             rep_param = fn_get_reports_parameter(app_user_id)
#             data['dtl_data'] = dtl_data
#             data = { **data,**sum_data, **rep_param}
#             return render(request, self.template_name, data)
#         except Exception as e:
#             return render(request, self.template_name)






# class sales_report_packet_return(TemplateView):
#     template_name = 'delar_report/delar-report-packet-return.html'

#     def get(self, request):
#         if not request.user.is_authenticated:
#             return render(request, 'appauth/appauth-login.html')
#         app_user_id = request.session["app_user_id"]
#         branch_code = request.session["branch_code"]
#         cbd = get_business_date(branch_code, app_user_id)

#         forms = CommonReportForm(
#             initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
#         context = get_global_data(request)
#         context['forms'] = forms

#         return render(request, self.template_name, context)



# class sales_report_packet_return_print_view(TemplateView):
#     template_name = 'delar_report/delar-report-packet-return-print-view.html'

#     def get(self, request):
#         if not request.user.is_authenticated:
#             return render(request, 'appauth/appauth-login.html')
#         try:
#             app_user_id = request.session["app_user_id"]
#             data = get_global_report_data(request)
#             dtl_data = fn_get_packet_return_rpt(app_user_id)
#             # sum_data = fn_get_sales_summary(app_user_id)
#             rep_param = fn_get_reports_parameter(app_user_id)
#             data['dtl_data'] = dtl_data
#             data = { **data, **rep_param}
#             return render(request, self.template_name, data)
#         except Exception as e:
#             return render(request, self.template_name)   