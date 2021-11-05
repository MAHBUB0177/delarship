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
        'company_logo':company_logo
    }

    return data