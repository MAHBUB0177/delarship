from sales.models import Supplier_Information
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
from django.db.models import Count, Sum, Avg, Subquery, Q, F
import logging
import sys
logger = logging.getLogger(__name__)
from decimal import Decimal
from datetime import date, datetime, timedelta
import time
from django.utils import timezone

from .utils import *
from .validations import *
from .myException import *
from .models import *
from .forms import *
from appauth.views import get_global_data, get_business_date
from appauth.manage_session import fn_is_user_permition_exist
from delar.utils import fn_get_center_employee

class finance_ledger_view(TemplateView):
    template_name = 'finance/finance-create-ledger.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = GeneralLedgerForm()
        context = get_global_data(request)
        context['success_message'] = ''
        context['error_message'] = ''
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def finance_ledger_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = GeneralLedgerForm(request.POST)
                if form.is_valid():
                    parent_code = form.cleaned_data["parent_code"]
                    gl_code = form.cleaned_data["gl_code"]
                    reporting_gl_code = form.cleaned_data["reporting_gl_code"]

                    if fn_is_ledger_exist(gl_code):
                        data['error_message'] = 'Ledger Code Already Exist!'
                        return JsonResponse(data)

                    if fn_is_reporting_ledger_exist(reporting_gl_code):
                        data['error_message'] = 'Reporting Ledger Code Already Exist!'
                        return JsonResponse(data)

                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Ledger Created Successfully.'
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def finance_ledger_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        with transaction.atomic():
            gl_code = id
            instance_data = get_object_or_404(General_Ledger, gl_code=gl_code)
            template_name = 'finance/finance-ledger-edit.html'
            context = {}
            data = dict()

            if request.method == 'POST':
                form = GeneralLedgerForm(
                    request.POST, instance=instance_data)
                if form.is_valid():
                    parent_code = form.cleaned_data["parent_code"]
                    obj = form.save(commit=False)
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
                form = GeneralLedgerForm(instance=instance_data)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


class finance_trantype_view(TemplateView):
    template_name = 'finance/finance-trantype-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Transaction_Type_Form()
        context = get_global_data(request)
        context['success_message'] = ''
        context['error_message'] = ''
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def finance_trantype_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Transaction_Type_Form(request.POST)
                if form.is_valid():
                    tran_type_id = fn_get_transaction_type_id()
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.tran_type_id = tran_type_id
                    post.app_data_time = timezone.now()
                    post.is_active = True
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Record Added Successfully.'
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def finance_trantype_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(
                Transaction_Type, tran_type_id=id)
            template_name = 'finance/finance-trantype-edit.html'
            context = {}
            data = dict()

            if request.method == 'POST':
                form = Transaction_Type_Form(
                    request.POST, instance=instance_data)
                if form.is_valid():
                    obj = form.save(commit=False)
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
                form = Transaction_Type_Form(instance=instance_data)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


class finance_trantypeledger_view(TemplateView):
    template_name = 'finance/finance-trantypeledger-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Ledger_Transaction_Type_Form()
        context = get_global_data(request)
        context['success_message'] = ''
        context['error_message'] = ''
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def finance_trantypeledger_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Ledger_Transaction_Type_Form(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.is_active = True
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Record Added Successfully.'
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def finance_trantypeledger_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(
                Ledger_Transaction_Type, id=id)
            template_name = 'finance/finance-trantypeledger-edit.html'
            context = {}
            data = dict()

            if request.method == 'POST':
                form = Ledger_Transaction_Type_Form(
                    request.POST, instance=instance_data)
                if form.is_valid():
                    obj = form.save(commit=False)
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
                form = Ledger_Transaction_Type_Form(instance=instance_data)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


class finance_cashnbankledger_view(TemplateView):
    template_name = 'finance/finance-cashnbankledger-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Cash_And_Bank_Ledger_Form()
        context = get_global_data(request)
        context['success_message'] = ''
        context['error_message'] = ''
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def finance_cashnbankledger_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Cash_And_Bank_Ledger_Form(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.is_active = True
                    post.is_deleted = False
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Record Added Successfully.'
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def finance_cashnbankledger_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(
                Cash_And_Bank_Ledger, id=id)
            template_name = 'finance/finance-cashnbankledger-edit.html'
            context = {}
            data = dict()

            if request.method == 'POST':
                form = Cash_And_Bank_Ledger_Form(
                    request.POST, instance=instance_data)
                if form.is_valid():
                    obj = form.save(commit=False)
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
                form = Cash_And_Bank_Ledger_Form(instance=instance_data)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


class finance_accounttype_view(TemplateView):
    template_name = 'finance/finance-accounttype-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Account_Type_Form()
        context = get_global_data(request)
        context['success_message'] = ''
        context['error_message'] = ''
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def finance_accounttype_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Account_Type_Form(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Record Added Successfully.'
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def finance_accounttype_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(
                Account_Type, account_type_code=id)
            template_name = 'finance/finance-accounttype-edit.html'
            context = {}
            data = dict()

            if request.method == 'POST':
                form = Account_Type_Form(
                    request.POST, instance=instance_data)
                if form.is_valid():
                    obj = form.save(commit=False)
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
                form = Account_Type_Form(instance=instance_data)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


class finance_clienttype_view(TemplateView):
    template_name = 'finance/finance-clienttype-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Client_Type_Form()
        context = get_global_data(request)
        context['success_message'] = ''
        context['error_message'] = ''
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def finance_clienttype_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Client_Type_Form(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Record Added Successfully.'
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def finance_clienttype_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(
                Client_Type, client_type_code=id)
            template_name = 'finance/finance-clienttype-edit.html'
            context = {}
            data = dict()

            if request.method == 'POST':
                form = Client_Type_Form(
                    request.POST, instance=instance_data)
                if form.is_valid():
                    obj = form.save(commit=False)
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
                form = Client_Type_Form(instance=instance_data)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


class finance_clientacmap_view(TemplateView):
    template_name = 'finance/finance-clientacmap-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Client_Account_Mapping_Form()
        context = get_global_data(request)
        context['success_message'] = ''
        context['error_message'] = ''
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def finance_clientacmap_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Client_Account_Mapping_Form(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Record Added Successfully.'
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def finance_clientacmap_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(
                Client_Account_Mapping, id=id)
            template_name = 'finance/finance-clientacmap-edit.html'
            context = {}
            data = dict()

            if request.method == 'POST':
                form = Client_Account_Mapping_Form(
                    request.POST, instance=instance_data)
                if form.is_valid():
                    obj = form.save(commit=False)
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
                form = Client_Account_Mapping_Form(instance=instance_data)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


def finance_transaction_typelist(request):
    transaction_screen = request.GET.get('transaction_screen')
    list_data = Transaction_Type.objects.filter(transaction_screen=transaction_screen, is_active=True, is_deleted=False).values(
        'tran_type_id', 'tran_type_code', 'tran_type_name').order_by('tran_type_name')
    return render(request, 'finance/finance-choice-trantype.html', {'list_data': list_data})


def finance_client_typelist(request):
    transaction_screen = request.GET.get('transaction_screen')
    list_data = Client_Type.objects.filter(transaction_screen=transaction_screen, is_active=True, is_deleted=False).values(
        'client_type_code', 'client_type_name').order_by('client_type_name')
    return render(request, 'finance/finance-choice-clienttype.html', {'list_data': list_data})


def finance_transaction_ledgerlist(request):
    tran_type_id = request.GET.get('tran_type_id')
    tran_led_list = Ledger_Transaction_Type.objects.filter(
        tran_type_id=tran_type_id).values('gl_code')
    list_data = General_Ledger.objects.filter(is_deleted=False, is_leaf_node=True, maintain_by_system=False, closer_date__isnull=True,
                                              gl_code__in=(Subquery(tran_led_list.values('gl_code')))).values(
        'gl_code', 'gl_name').order_by('gl_name')
    return render(request, 'finance/finance-choice-ledger.html', {'list_data': list_data})


def finance_all_ledgerlist(request):
    list_data = General_Ledger.objects.filter(is_deleted=False, is_leaf_node=True, maintain_by_system=False, closer_date__isnull=True).values(
        'gl_code', 'gl_name').order_by('gl_name')
    return render(request, 'finance/finance-choice-ledger.html', {'list_data': list_data})


def finance_choice_branchlist(request):
    branch_code = request.GET.get('branch_code')
    list_data = Branch.objects.filter().values(
        'branch_code', 'branch_name').order_by('branch_name')
    return render(request, 'finance/finance-choice-branchlist.html', {'list_data': list_data})


def finance_choice_accountslist(request):
    account_type = request.GET.get('account_type')
    tran_screen = request.GET.get('tran_screen')
    transaction_type = request.GET.get('transaction_type')
    branch_code = request.GET.get('branch_code')

    if transaction_type and tran_screen:
        account_type, client_type = fn_get_transaction_account_type_screen(
            tran_screen, transaction_type)

    if not transaction_type and not account_type and tran_screen:
        account_type, client_type = fn_get_transaction_account_type(
            tran_screen)

    list_data = Accounts_Balance.objects.filter(account_type=account_type, account_closing_date__isnull=True).values(
        'account_number', 'account_title', 'phone_number', 'account_address').order_by('account_title')
    if branch_code:
        list_data.filter(branch_code=branch_code)
    return render(request, 'finance/finance-choice-accountslist.html', {'list_data': list_data})


def finance_account_typelist(request):
    list_data = Account_Type.objects.filter(is_active=True, is_deleted=False).values(
        'account_type_code', 'account_type_name').order_by('account_type_name')
    return render(request, 'finance/finance-choice-accounttype.html', {'list_data': list_data})


def finance_choice_cashnbank_list(request):
    branch_code = request.GET.get('branch_code')
    tran_led_list = Cash_And_Bank_Ledger.objects.filter(
        is_active=True, is_deleted=False).values('gl_code')

    if branch_code or branch_code != 'readonly':
        tran_led_list.filter(branch_code=branch_code)

    list_data = General_Ledger.objects.filter(is_deleted=False, is_leaf_node=True, maintain_by_system=False, closer_date__isnull=True,
                                              gl_code__in=(Subquery(tran_led_list.values('gl_code')))).values(
        'gl_code', 'gl_name').order_by('gl_name')
    # print(list_data.query)
    return render(request, 'finance/finance-choice-ledger.html', {'list_data': list_data})


class finance_ledger_transaction(TemplateView):
    template_name = 'finance/finance-ledger-transaction.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        branch_code = request.session['branch_code']
        app_user_id = request.session["app_user_id"]
        transaction_date = get_business_date(branch_code, app_user_id)
        Transaction_Table.objects.filter(app_user_id=app_user_id).delete()

        tran_table = TransactionTableForm(
            initial={'transaction_date': transaction_date, 'account_number': '0', 'tran_gl_code': '', 'tran_document_number': '',
                     'tran_screen': 'LEDCASH_TRAN'})
        context = get_global_data(request)
        context['forms'] = tran_table
        return render(request, self.template_name, context)


class finance_account_transaction(TemplateView):
    template_name = 'finance/finance-account-transaction.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        branch_code = request.session["branch_code"]
        app_user_id = request.session["app_user_id"]
        #document_number = fn_generate_document_number(branch_code)
        transaction_date = get_business_date(branch_code, app_user_id)
        Transaction_Table.objects.filter(app_user_id=app_user_id).delete()

        tran_table = TransactionTableForm(
            initial={'transaction_date': transaction_date, 'account_number': 0, 'phone_number': '',
                     'tran_gl_code': '', 'tran_document_number': ''})
        context = get_global_data(request)
        context['forms'] = tran_table
        return render(request, self.template_name, context)


@transaction.atomic
def finance_transaction_post(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        data['form_is_valid'] = False
        if request.method == 'POST':
            form = TransactionTableForm(request.POST)
            if form.is_valid():

                table_summary = Transaction_Table.objects.filter(
                    app_user_id=request.session["app_user_id"]).aggregate(Count('app_user_id'), Sum('tran_amount'))
                row_count = table_summary['app_user_id__count']

                try:
                    with transaction.atomic():

                        branch_code = form.cleaned_data["branch_code"]
                        app_user_id = request.session["app_user_id"]
                        transaction_date = form.cleaned_data["transaction_date"]
                        transaction_narration = form.cleaned_data["transaction_narration"]
                        account_number = form.cleaned_data["account_number"]
                        tran_gl_code = form.cleaned_data["tran_gl_code"]
                        tran_amount = form.cleaned_data["tran_amount"]
                        tran_type = form.cleaned_data["tran_type"]
                        tran_document_number = form.cleaned_data["tran_document_number"]
                        tran_screen = form.cleaned_data["tran_screen"]
                        center_code = '0'

                        if tran_screen == 'LEDCASH_TRAN':
                            account_number = '0'
                            center_code = '0'
                            if not tran_gl_code:
                                data['error_message'] = 'Please Enter Ledger Code!'
                                data['form_is_valid'] = False
                                return JsonResponse(data)

                        if tran_screen == 'CASH_TRANSACTION':
                            tran_gl_code = '0'
                            receipt_payment_ledger = form.cleaned_data["receipt_payment_ledger"]
                            _, _, center_code, _, _, _, _, _, _, _ = fn_get_accountinfo_byacnumber(
                                account_number)

                        if len(str(tran_amount)) > 22:
                            data['error_message'] = 'Length of transaction amount exceed!'
                            data['form_is_valid'] = False
                            return JsonResponse(data)

                        if tran_type is None:
                            data['error_message'] = 'Please select Transaction Type!'
                            data['form_is_valid'] = False
                            return JsonResponse(data)

                        if (account_number == '0' and tran_gl_code == '0'):
                            data['error_message'] = 'Both ledger code and phone number can not be Zero!'
                            data['form_is_valid'] = False
                            return JsonResponse(data)

                        if (account_number != '0' and tran_gl_code != '0'):
                            data['error_message'] = 'Please enter only ledger code or phone number!'
                            data['form_is_valid'] = False
                            return JsonResponse(data)

                        if (account_number != '0'and not fn_val_account_number(account_number)):
                            data['error_message'] = 'Invalid Account Number!'
                            data['form_is_valid'] = False
                            return JsonResponse(data)

                        if (tran_gl_code != '0'and not fn_val_ledger_code(tran_gl_code)):
                            data['error_message'] = 'Invalid Ledger Code!'
                            data['form_is_valid'] = False
                            return JsonResponse(data)

                        try:
                            transaction_type = Transaction_Type.objects.get(
                                tran_type_id=tran_type, transaction_screen=tran_screen)
                            tran_debit_credit = transaction_type.default_debit_credit

                            if tran_debit_credit == 'C':
                                contra_gl_code = transaction_type.debit_gl_code.gl_code
                            else:
                                contra_gl_code = transaction_type.credit_gl_code.gl_code

                            if tran_screen == 'LEDCASH_TRAN':
                                if tran_debit_credit == 'C':
                                    receipt_payment_ledger = transaction_type.credit_gl_code.gl_code
                                else:
                                    receipt_payment_ledger = transaction_type.debit_gl_code.gl_code

                        except Transaction_Type.DoesNotExist:
                            data['error_message'] = 'Transaction Debit/Credit is Not Define!'
                            data['form_is_valid'] = False
                            return JsonResponse(data)

                        if receipt_payment_ledger is None or not receipt_payment_ledger:
                            data['error_message'] = 'Invalid Transaction Ledger!'
                            data['form_is_valid'] = False
                            return JsonResponse(data)

                        if transaction_narration is None or not transaction_narration:
                            transaction_narration = transaction_type.tran_type_name

                        post = form.save(commit=False)
                        post.app_user_id = app_user_id
                        post.branch_code = branch_code
                        post.center_code = center_code
                        post.tran_debit_credit = tran_debit_credit
                        post.transaction_narration = transaction_narration
                        post.contra_gl_code = contra_gl_code
                        post.batch_serial = row_count+1
                        post.save()

                        if tran_debit_credit == 'C' and tran_type is None:
                            ct_tran_type = 'CP'
                        else:
                            ct_tran_type = 'CR'

                        cursor = connection.cursor()
                        cursor.callproc("fn_finance_post_cash_tran", [
                                        branch_code, center_code, app_user_id, 'CS', receipt_payment_ledger, transaction_date, transaction_narration, ct_tran_type, 'CASH'])
                        row = cursor.fetchone()

                        if row[0] != 'S':
                            data['error_message'] = row[1]
                            data['form_is_valid'] = False
                            raise Exception(row[1])

                        message = "Post Successfully :Batch Number : " + row[2]

                        data['form_is_valid'] = True
                        data['success_message'] = message

                        return JsonResponse(data)
                except Exception as e:
                    data['error_message'] = str(e)
                    data['form_is_valid'] = False
                    logger.error("Error on line {} \nType: {} \nError:{}".format(
                        sys.exc_info()[-1], type(e).__name__, str(e)))
                    return JsonResponse(data)
            else:
                data['error_message'] = form.errors.as_json()
                data['form_is_valid'] = False
                return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        return JsonResponse(data)


class finance_transaction_list(TemplateView):
    template_name = 'finance/finance-transaction-list.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        forms = TransactionSearch(
            initial={'tran_date': cbd, 'tran_from_date': cbd, 'tran_upto_date': cbd})
        context = get_global_data(request)
        context['forms'] = forms
        return render(request, self.template_name, context)


def finance_transaction_details_list(request, id=0):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    batch_number = request.GET.get('batch_number')
    transaction_date = request.GET.get('transaction_date')
    branch_code = request.GET.get('branch_code')
    rows = Transaction_Details.objects.raw('''SELECT t.id, l.gl_code, t.batch_number,t.batch_serial, t.account_number, 
    t.tran_gl_code ||' - '||gl_name gl_name,t.tran_debit_credit, t.tran_amount, t.cancel_amount, 
    t.tran_document_number, t.tran_person_phone, t.transaction_narration, t.app_user_id, t.auth_by, 
    t.cancel_by, t.cancel_on FROM finance_transaction_details t, finance_general_ledger l where t.tran_gl_code=gl_code 
    and t.branch_code='''+"'"+str(branch_code)+"'"+" and t.transaction_date= '"+str(transaction_date)+"'"+"and t.batch_number='"+str(batch_number)+"'"+" order by t.batch_serial ")
    context = get_global_data(request)
    context['data'] = rows
    return render(request, 'finance/finance-transaction-details-list.html', context)


@transaction.atomic
def finance_tranbatch_cancel(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    try:
        data = dict()
        data['form_is_valid'] = False
        data = dict()
        tran_row = Transaction_Master.objects.get(pk=id)
        branch_code = tran_row.branch_code
        app_user_id = request.session["app_user_id"]
        transaction_date = tran_row.transaction_date
        batch_number = tran_row.batch_number

        if tran_row.system_posted_tran:
            data['error_message'] = 'You can not cancel the system posted transaction.\nPlease try to cancel related stock/sales transaction.'
            return JsonResponse(data)

        cancel_comments = 'Cancel by '+app_user_id

        cursor = connection.cursor()
        cursor.callproc("fn_post_tran_cancel", [
                        branch_code, app_user_id, transaction_date, batch_number, cancel_comments])
        row = cursor.fetchone()
        if row[0] != 'S':
            data['error_message'] = row[1]
            data['form_is_valid'] = False
            raise Exception(row[1])

        data['message'] = "Batch Cancel Successfully"
        data['form_is_valid'] = True
        return JsonResponse(data)

    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        return JsonResponse(data)


class finance_transaction_query(TemplateView):
    template_name = 'finance/finance-transaction-query.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        branch_code = request.session["branch_code"]
        app_user_id = request.session["app_user_id"]
        transaction_date = get_business_date(branch_code, app_user_id)
        forms = TransactionSearch(
            initial={'tran_from_date': transaction_date, 'tran_upto_date': transaction_date, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms
        return render(request, self.template_name, context)


@transaction.atomic
def finance_transaction_query_cancel(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    try:
        with transaction.atomic():

            batch_row = Query_Table.objects.get(id=id)

            tran_row = Transaction_Master.objects.get(
                branch_code=batch_row.int_column1, transaction_date=batch_row.dat_column1, batch_number=batch_row.int_column2)
            branch_code = tran_row.branch_code
            app_user_id = request.session["app_user_id"]
            transaction_date = tran_row.transaction_date
            batch_number = tran_row.batch_number

            if tran_row.tran_source_table == 'SALES_RETURN':
                data['error_message'] = 'Please Cancel Sales Return!'
                return JsonResponse(data)
            if tran_row.tran_source_table == 'SALES':
                data['error_message'] = 'Please Cancel Invoice!'
                return JsonResponse(data)
            if tran_row.tran_source_table == 'STOCK':
                data['error_message'] = 'Please Cancel Stock Entry!'
                return JsonResponse(data)
            if tran_row.tran_source_table == 'STOCK_RETURN':
                data['error_message'] = 'Please Cancel Stock Return!'
                return JsonResponse(data)

            if tran_row.system_posted_tran:
                data['error_message'] = 'You can not cancel the system posted transaction.\nPlease try to cancel related stock/sales transaction.'
                return JsonResponse(data)

            cancel_comments = 'Cancel by '+app_user_id

            cursor = connection.cursor()
            cursor.callproc("fn_finance_post_tran_cancel", [
                            branch_code, app_user_id, transaction_date, batch_number, cancel_comments])
            row = cursor.fetchone()

            if row[0] != 'S':
                logger.error("Error in fn_finance_post_tran_cancel on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
                data['error_message'] = row[1]
                raise Exception(row[1])

            data['success_message'] = "Batch Cancel Successfully"
            data['form_is_valid'] = True
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        logger.error("Error on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)


def finance_transaction_details_query_submit(request):
    app_user_id = request.session["app_user_id"]
    data = dict()
    data['form_is_valid'] = True

    tran_from_date = request.GET.get('tran_from_date')
    tran_upto_date = request.GET.get('tran_upto_date')
    branch_code = request.GET.get('branch_code', None)
    account_number = request.GET.get('account_number')
    tran_ledger_code = request.GET.get('tran_ledger_code')

    if branch_code == 'readonly':
        branch_code = request.session["branch_code"]

    try:

        cursor = connection.cursor()
        cursor.callproc("fn_finance_query_daily_transaction", [
                        branch_code, tran_from_date, tran_upto_date, account_number, tran_ledger_code, app_user_id])
        row = cursor.fetchone()

        if row[0] != 'S':
            logger.error("Error in fn_finance_query_daily_transaction on line {} \nType: {} \nError:{}".format(
                sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
            data['error_message'] = row[1]
            raise Exception(row[1])

        data['form_is_valid'] = True
        return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        logger.error("Error in fn_finance_query_daily_transaction on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)


class finance_deposit_receive_view(TemplateView):
    template_name = 'finance/finance-depositreceive-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = Deposit_Receive_Model_Form(initial={'deposit_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def finance_deposit_receive_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''

    if request.method == 'POST':
        form = Deposit_Receive_Model_Form(request.POST)  # forms name
        if form.is_valid():
            try:
                with transaction.atomic():
                    app_user_id = request.session["app_user_id"]
                    #branch_code = form.cleaned_data["branch_code"]
                    tran_document_number = form.cleaned_data["deposit_doc_num"]
                    tran_amount = form.cleaned_data["deposit_amount"]
                    deposit_date = form.cleaned_data["deposit_date"]
                    client_id = form.cleaned_data["client_id"]
                    narration = form.cleaned_data["narration"]
                    account_number = form.cleaned_data["account_number"]

                    narration = "Deposit Receive "+narration

                    _, branch_code, center_code, _, client_id, _, _, _, _, _ = fn_get_accountinfo_byacnumber(
                        account_number)

                    if len(str(tran_amount)) > 22:
                        data['error_message'] = 'Length of transaction amount exceed!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    if tran_amount < 0:
                        data['error_message'] = 'Negative amount is not allowed!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    param = Application_Settings.objects.get()

                    if fn_doc_number_validation(branch_code, tran_document_number, 'DEP') and param.transaction_doc_required:
                        data['error_message'] = 'Memo Number Already Used!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    cash_gl_code = fn_get_cash_gl_code()
                    transaction_details = {}
                    transaction_details["tran_date"] = deposit_date
                    transaction_details["branch_code"] = branch_code
                    transaction_details["center_code"] = center_code
                    transaction_details["tran_type"] = 'CR'
                    transaction_details["transaction_screen"] = 'DEP_RECEIVE'
                    transaction_details["account_number"] = account_number
                    transaction_details["account_phone"] = ''
                    transaction_details["tran_gl_code"] = '0'
                    transaction_details["contra_gl_code"] = cash_gl_code
                    transaction_details["tran_debit_credit"] = 'C'
                    transaction_details["tran_amount"] = tran_amount
                    transaction_details["tran_document_number"] = tran_document_number
                    transaction_details["app_user_id"] = app_user_id
                    transaction_details["transaction_narration"] = narration

                    status, message, batch_number = fn_cash_tran_posting(
                        transaction_details)

                    if not status:
                        data['error_message'] = message
                        logger.error("Error in finance_deposit_receive_insert {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(message).__name__, str(message)))
                        raise MyDatabaseError()

                    post = form.save(commit=False)
                    post.app_user_id = app_user_id
                    post.branch_code = branch_code
                    post.center_code = center_code
                    post.client_id = client_id
                    post.tran_batch_number = batch_number
                    post.narration = narration
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Deposit Receive With Batch Number :'+batch_number
            except Exception as e:
                data['form_is_valid'] = False
                if len(str(data['error_message'])) > 0:
                    return JsonResponse(data)
                data['error_message'] = str(e)
                logger.error("Error on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                return JsonResponse(data)
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def finance_deposit_receive_cancel(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    app_user_id = request.session["app_user_id"]
    data['error_message'] = ''
    data['form_is_valid'] = False

    if not fn_is_user_permition_exist(request.session["app_user_id"], 'F10000005', 'Finance'):
        data['error_message'] = "You are not allowed to cancel this transaction!"
        data['form_is_valid'] = False
        return JsonResponse(data)

    try:
        with transaction.atomic():

            status, error_message = fn_deposit_receive_cancel(
                id, app_user_id)
            if not status:
                data['error_message'] = error_message
                data['form_is_valid'] = False
                raise Exception(error_message)

            data['form_is_valid'] = True
            data['success_message'] = 'Cancel Successfully!'
            return JsonResponse(data)

    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        logger.error("Error on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)


class finance_deposit_payment_view(TemplateView):
    template_name = 'finance/finance-depositpayment-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = Deposit_Payment_Model_Form(initial={'payment_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def finance_deposit_payment_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''

    if request.method == 'POST':
        form = Deposit_Payment_Model_Form(request.POST)  # forms name
        if form.is_valid():
            try:
                with transaction.atomic():
                    app_user_id = request.session["app_user_id"]
                    tran_document_number = form.cleaned_data["payment_doc_num"]
                    tran_amount = form.cleaned_data["payment_amount"]
                    payment_date = form.cleaned_data["payment_date"]
                    client_id = form.cleaned_data["client_id"]
                    narration = form.cleaned_data["narration"]
                    account_number = form.cleaned_data["account_number"]

                    narration = "Deposit Payment "+narration

                    _, branch_code, center_code, _, client_id, _, _, _, _, _ = fn_get_accountinfo_byacnumber(
                        account_number)

                    if len(str(tran_amount)) > 22:
                        data['error_message'] = 'Length of transaction amount exceed!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    if tran_amount < 0:
                        data['error_message'] = 'Negative amount is not allowed!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    param = Application_Settings.objects.get()

                    if fn_doc_number_validation(branch_code, tran_document_number, 'DEP') and param.transaction_doc_required:
                        data['error_message'] = 'Memo Number Already Used!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    cash_gl_code = fn_get_cash_gl_code()
                    transaction_details = {}
                    transaction_details["tran_date"] = payment_date
                    transaction_details["branch_code"] = branch_code
                    transaction_details["center_code"] = center_code
                    transaction_details["tran_type"] = 'CP'
                    transaction_details["transaction_screen"] = 'DEP_PAYMENT'
                    transaction_details["account_number"] = account_number
                    transaction_details["account_phone"] = ''
                    transaction_details["tran_gl_code"] = '0'
                    transaction_details["contra_gl_code"] = cash_gl_code
                    transaction_details["tran_debit_credit"] = 'D'
                    transaction_details["tran_amount"] = tran_amount
                    transaction_details["tran_document_number"] = tran_document_number
                    transaction_details["app_user_id"] = app_user_id
                    transaction_details["transaction_narration"] = narration

                    status, message, batch_number = fn_cash_tran_posting(
                        transaction_details)

                    if not status:
                        data['error_message'] = message
                        logger.error("Error in finance_deposit_payment_insert {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(message).__name__, str(message)))
                        raise MyDatabaseError()

                    post = form.save(commit=False)
                    post.app_user_id = app_user_id
                    post.branch_code = branch_code
                    post.center_code = center_code
                    post.client_id = client_id
                    post.tran_batch_number = batch_number
                    post.narration = narration
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Deposit Payment With Batch Number :'+batch_number
            except Exception as e:
                data['form_is_valid'] = False
                if len(str(data['error_message'])) > 0:
                    return JsonResponse(data)
                data['error_message'] = str(e)
                logger.error("Error on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                return JsonResponse(data)
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def finance_deposit_payment_cancel(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    app_user_id = request.session["app_user_id"]
    data['error_message'] = ''
    data['form_is_valid'] = False

    if not fn_is_user_permition_exist(request.session["app_user_id"], 'F10000006', 'Finance'):
        data['error_message'] = "You are not allowed to cancel this transaction!"
        data['form_is_valid'] = False
        return JsonResponse(data)

    try:
        with transaction.atomic():

            status, error_message = fn_deposit_payment_cancel(id, app_user_id)
            if not status:
                data['error_message'] = error_message
                data['form_is_valid'] = False
                raise Exception(error_message)

            data['form_is_valid'] = True
            data['success_message'] = 'Cancel Successfully!'
            return JsonResponse(data)

    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        logger.error("Error on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)


class finance_deposit_transfer_view(TemplateView):
    template_name = 'finance/finance-deposittransfer-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = Deposit_Transfer_Model_Form(initial={'transaction_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def finance_deposit_transfer_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''

    if request.method == 'POST':
        form = Deposit_Transfer_Model_Form(request.POST)  # forms name
        if form.is_valid():
            try:
                with transaction.atomic():
                    app_user_id = request.session["app_user_id"]
                    tran_document_number = form.cleaned_data["transaction_doc_num"]
                    tran_amount = form.cleaned_data["transaction_amount"]
                    transaction_date = form.cleaned_data["transaction_date"]
                    from_client_id = form.cleaned_data["from_client_id"]
                    to_client_id = form.cleaned_data["to_client_id"]
                    narration = form.cleaned_data["narration"]
                    from_account_number = form.cleaned_data["from_account_number"]
                    to_account_number = form.cleaned_data["to_account_number"]

                    if from_account_number == to_account_number:
                        data['error_message'] = 'Same Customer Transfer Not Allowed!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    _, from_branch_code, from_center_code, _, from_client_id, _, _, _, _, _ = fn_get_accountinfo_byacnumber(
                        from_account_number)
                    _, to_branch_code, to_center_code, _, to_client_id, _, _, _, _, _ = fn_get_accountinfo_byacnumber(
                        to_account_number)

                    narration = "Deposit Transfer from " + \
                        from_client_id+" to "+to_client_id+" "+narration

                    if len(str(tran_amount)) > 22:
                        data['error_message'] = 'Length of transaction amount exceed!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    if tran_amount < 0:
                        data['error_message'] = 'Negative amount is not allowed!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    param = Application_Settings.objects.get()

                    if fn_doc_number_validation(from_branch_code, tran_document_number, 'DEP') and param.transaction_doc_required:
                        data['error_message'] = 'Memo Number Already Used!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    transaction_master = {}
                    transaction_details = {}
                    tran_details = []
                    transfer_data = {}
                    transaction_master["tran_date"] = transaction_date
                    transaction_master["branch_code"] = from_branch_code
                    transaction_master["center_code"] = from_center_code
                    transaction_master["tran_type"] = 'DEP_TRANSFER'
                    transaction_master["transaction_screen"] = 'DEP_TRANSFER'
                    transaction_master["app_user_id"] = app_user_id
                    transaction_master["master_narration"] = narration

                    transaction_details = {}
                    transaction_details["account_number"] = from_account_number
                    transaction_details["account_phone"] = ''
                    transaction_details["tran_gl_code"] = '0'
                    transaction_details["contra_gl_code"] = fn_get_account_ledger(
                        to_account_number)
                    transaction_details["tran_debit_credit"] = 'D'
                    transaction_details["tran_amount"] = tran_amount
                    transaction_details["tran_document_number"] = tran_document_number
                    transaction_details["transaction_narration"] = "Deposit Transfer to " + \
                        to_client_id

                    tran_details.append(transaction_details)
                    transaction_details = {}
                    transaction_details["account_number"] = to_account_number
                    transaction_details["account_phone"] = ''
                    transaction_details["tran_gl_code"] = '0'
                    transaction_details["contra_gl_code"] = fn_get_account_ledger(
                        from_account_number)
                    transaction_details["tran_debit_credit"] = 'C'
                    transaction_details["tran_amount"] = tran_amount
                    transaction_details["tran_document_number"] = tran_document_number
                    transaction_details["transaction_narration"] = "Deposit Transfer from " + \
                        from_client_id

                    tran_details.append(transaction_details)

                    status, message, batch_number = fn_transfer_tran_posting(
                        transaction_master, tran_details)

                    if not status:
                        data['error_message'] = 'Error in Deposit Transfer!\n'+message
                        logger.error("Error in finance_deposit_transfer_insert {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(message).__name__, str(message)))
                        raise Exception('Error in Deposit Transfer! '+message)

                    transfer_data["from_branch_code"] = from_branch_code
                    transfer_data["from_center_code"] = from_center_code
                    transfer_data["from_client_id"] = from_client_id
                    transfer_data["from_account_number"] = from_account_number
                    transfer_data["transaction_date"] = transaction_date
                    transfer_data["transaction_amount"] = tran_amount
                    transfer_data["tran_batch_number"] = batch_number
                    transfer_data["tran_document_number"] = tran_document_number
                    transfer_data["narration"] = narration
                    transfer_data["app_user_id"] = app_user_id
                    transfer_data["to_branch_code"] = to_branch_code
                    transfer_data["to_center_code"] = to_center_code
                    transfer_data["to_client_id"] = to_client_id
                    transfer_data["to_account_number"] = to_account_number

                    status, message = fn_deposit_transfer(transfer_data)

                    post = form.save(commit=False)
                    post.app_user_id = app_user_id
                    post.branch_code = from_branch_code
                    post.center_code = from_center_code
                    post.from_client_id = from_client_id
                    post.to_client_id = to_client_id
                    post.tran_batch_number = batch_number
                    post.narration = narration
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Deposit Transfer With Batch Number :'+batch_number
            except Exception as e:
                data['form_is_valid'] = False
                if len(str(data['error_message'])) > 0:
                    return JsonResponse(data)
                data['error_message'] = str(e)
                logger.error("Error on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                return JsonResponse(data)
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def finance_deposit_transfer_cancel(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    app_user_id = request.session["app_user_id"]
    data['error_message'] = ''
    data['form_is_valid'] = False

    if not fn_is_user_permition_exist(request.session["app_user_id"], 'F10000006', 'Finance'):
        data['error_message'] = "You are not allowed to cancel this transaction!"
        data['form_is_valid'] = False
        return JsonResponse(data)

    try:
        with transaction.atomic():

            status, error_message = fn_deposit_payment_cancel(id, app_user_id)
            if not status:
                data['error_message'] = error_message
                data['form_is_valid'] = False
                raise Exception(error_message)

            data['form_is_valid'] = True
            data['success_message'] = 'Cancel Successfully!'
            return JsonResponse(data)

    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        logger.error("Error on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)


class finance_deposit_closing_view(TemplateView):
    template_name = 'finance/finance-depositclosing-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = Deposit_Closing_Model_Form(initial={'closing_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def finance_deposit_closing_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''

    if request.method == 'POST':
        form = Deposit_Closing_Model_Form(request.POST)  # forms name
        if form.is_valid():
            try:
                with transaction.atomic():
                    app_user_id = request.session["app_user_id"]
                    tran_document_number = form.cleaned_data["closing_doc_num"]
                    tran_amount = form.cleaned_data["closing_balance"]
                    closing_date = form.cleaned_data["closing_date"]
                    client_id = form.cleaned_data["client_id"]
                    narration = form.cleaned_data["narration"]
                    account_number = form.cleaned_data["account_number"]

                    narration = "Account Closing "+narration

                    _, branch_code, center_code, _, client_id, _, _, _, _, _ = fn_get_accountinfo_byacnumber(
                        account_number)

                    if len(str(tran_amount)) > 22:
                        data['error_message'] = 'Length of transaction amount exceed!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    if tran_amount < 0:
                        data['error_message'] = 'Negative amount is not allowed!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    param = Application_Settings.objects.get()

                    if fn_doc_number_validation(branch_code, tran_document_number, 'DEP') and param.transaction_doc_required:
                        data['error_message'] = 'Memo Number Already Used!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    cash_gl_code = fn_get_cash_gl_code()
                    transaction_details = {}
                    transaction_details["tran_date"] = closing_date
                    transaction_details["branch_code"] = branch_code
                    transaction_details["center_code"] = center_code
                    transaction_details["tran_type"] = 'CP'
                    transaction_details["transaction_screen"] = 'DEP_PAYMENT'
                    transaction_details["account_number"] = account_number
                    transaction_details["account_phone"] = ''
                    transaction_details["tran_gl_code"] = '0'
                    transaction_details["contra_gl_code"] = cash_gl_code
                    transaction_details["tran_debit_credit"] = 'D'
                    transaction_details["tran_amount"] = tran_amount
                    transaction_details["tran_document_number"] = tran_document_number
                    transaction_details["app_user_id"] = app_user_id
                    transaction_details["transaction_narration"] = narration

                    status, message, batch_number = fn_cash_tran_posting(
                        transaction_details)

                    if not status:
                        data['error_message'] = message
                        logger.error("Error in finance_deposit_closing_insert {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(message).__name__, str(message)))
                        raise Exception(message)

                    status, message = fn_update_account_closing(
                        account_number, closing_date)

                    if not status:
                        data['error_message'] = message
                        logger.error("Error in finance_deposit_closing_insert {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(message).__name__, str(message)))
                        raise Exception(message)

                    post = form.save(commit=False)
                    post.app_user_id = app_user_id
                    post.branch_code = branch_code
                    post.center_code = center_code
                    post.client_id = client_id
                    post.tran_batch_number = batch_number
                    post.narration = narration
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Closing Batch Number :'+batch_number
            except Exception as e:
                data['form_is_valid'] = False
                if len(str(data['error_message'])) > 0:
                    return JsonResponse(data)
                data['error_message'] = str(e)
                logger.error("Error on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                return JsonResponse(data)
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def finance_deposit_closing_cancel(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    app_user_id = request.session["app_user_id"]
    data['error_message'] = ''
    data['form_is_valid'] = False

    if not fn_is_user_permition_exist(request.session["app_user_id"], 'F10000006', 'Finance'):
        data['error_message'] = "You are not allowed to cancel this transaction!"
        data['form_is_valid'] = False
        return JsonResponse(data)

    try:
        with transaction.atomic():

            status, error_message = fn_deposit_closing_cancel(id, app_user_id)
            if not status:
                data['error_message'] = error_message
                data['form_is_valid'] = False
                raise Exception(error_message)

            data['form_is_valid'] = True
            data['success_message'] = 'Cancel Successfully!'
            return JsonResponse(data)

    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        logger.error("Error on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)


def finance_get_account_infobyacnumber(request, account_number):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    try:
        account_title = ''
        account_balance = 0
        credit_limit = 0
        account_address = ''
        try:
            account_number, branch_code, center_code, phone_number, client_id, account_type, account_title, account_address, account_balance, credit_limit = fn_get_accountinfo_byacnumber(
                account_number)
            employee_id = fn_get_center_employee(center_code)
        except Exception as e:
            account_title = ''
            account_balance = 0
            credit_limit = 0
            account_number = '0'
            account_type = ''
            phone_number = ''
            client_id = ''
            branch_code = ''
            center_code = ''
            employee_id = ''

        data['account_title'] = account_title
        data['account_number'] = account_number
        data['account_balance'] = account_balance
        data['phone_number'] = phone_number
        data['credit_limit'] = credit_limit
        data['account_type'] = account_type
        data['client_id'] = client_id
        data['account_address'] = account_address
        data['branch_code'] = branch_code
        data['center_code'] = center_code
        data['employee_id'] = employee_id
        data['form_is_valid'] = True
    except Exception as e:
        data["error_message"] = str(e)
    return JsonResponse(data)


def finance_get_client_account_balance(request, client_id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    try:
        message = ''
        try:
            message = fn_get_client_accounts_info(client_id)
        except Exception as e:
            message = ''
        data['message'] = message
        data['form_is_valid'] = True
    except Exception as e:
        data["error_message"] = str(e)
    return JsonResponse(data)


class finance_account_balance_query(TemplateView):
    template_name = 'finance/finance-accounts-balance.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]

        forms = AccountBalance(initial={'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class finance_actran_details(TemplateView):
    template_name = 'finance/finance-actran-details.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]

        cbd = get_business_date(branch_code)
        forms = AccountStatementDetails(
            initial={'from_date': cbd, 'upto_date': cbd})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


def finance_account_statement(request, account_number, tran_from_date, tran_upto_date):
    branch_code = request.session["branch_code"]
    app_user_id = request.session["app_user_id"]
    data = dict()
    data['form_is_valid'] = True

    try:

        cursor = connection.cursor()
        cursor.callproc("fn_finance_query_account_statement", [
                        account_number, tran_from_date, tran_upto_date, app_user_id])
        row = cursor.fetchone()

        if row[0] != 'S':
            logger.error("Error in fn_finance_query_account_statement on line {} \nType: {} \nError:{}".format(
                sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
            data['error_message'] = row[1]
            raise Exception(row[1])

        data['form_is_valid'] = True
        return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        logger.error("Error in fn_finance_query_account_statement on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        data['error_message'] = str(e)
        return JsonResponse(data)


class finance_telbaltrf_view(TemplateView):
    template_name = 'finance/finance-telbaltrf-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Tran_Telbal_Details_Form()
        context = get_global_data(request)
        context['success_message'] = ''
        context['error_message'] = ''
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def finance_telbaltrf_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Tran_Telbal_Details_Form(request.POST)
                if form.is_valid():
                    branch_code = form.cleaned_data["branch_code"]
                    res_teller_id = form.cleaned_data["res_teller_id"]
                    try:
                        row = Transaction_Telbal.objects.get(
                            branch_code=branch_code, teller_id=res_teller_id)
                        cash_balance = row.cash_balance
                    except Transaction_Telbal.DoesNotExist:
                        cash_balance = 0
                        row = Transaction_Telbal(
                            branch_code=branch_code, teller_id=res_teller_id, cash_od_allowed=False)
                        row.save()
                    post = form.save(commit=False)
                    post.org_teller_id = request.session["app_user_id"]
                    post.app_user_id = request.session["app_user_id"]
                    post.transaction_date = get_business_date(
                        branch_code, res_teller_id)
                    post.available_balance = cash_balance
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Request Send Successfully.'
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


class finance_telbaltrf_authlist(TemplateView):
    template_name = 'finance/finance-telbaltrf-authlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        forms = Tran_Telbal_Details_Query_Form(
            initial={'transaction_date': cbd, 'from_date': cbd, 'upto_date': cbd})
        context = get_global_data(request)
        context['forms'] = forms
        return render(request, self.template_name, context)


@transaction.atomic
def finance_telbaltrf_reject(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    try:
        with transaction.atomic():
            row = Tran_Telbal_Details.objects.get(pk=id)

            if row.auth_by:
                data['error_message'] = 'Transaction Already Accepted!'
                return JsonResponse(data)

            if row.cancel_by:
                data['error_message'] = 'Transaction Already Rejected!'
                return JsonResponse(data)

            row.cancel_amount = row.tran_amount
            row.cancel_by = request.session["app_user_id"]
            row.cancel_on = timezone.now()
            row.save()
            data['form_is_valid'] = True
            data['success_message'] = "Save Successfully"
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def finance_telbaltrf_accept(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    try:
        with transaction.atomic():
            row = Tran_Telbal_Details.objects.get(pk=id)

            if row.auth_by:
                data['error_message'] = 'Transaction Already Accepted!'
                return JsonResponse(data)

            if row.cancel_by:
                data['error_message'] = 'Transaction Already Rejected!'
                return JsonResponse(data)

            if row.res_teller_id != request.session["app_user_id"]:
                data['error_message'] = 'This Transaction Should Accept By ' + \
                    row.res_teller_id
                return JsonResponse(data)

            branch_code = row.branch_code

            row.auth_by = request.session["app_user_id"]
            row.auth_on = timezone.now()
            row.save()

            try:
                tel = Transaction_Telbal.objects.get(
                    teller_id=row.org_teller_id)
            except Transaction_Telbal.DoesNotExist:
                cash_balance = 0
                tel = Transaction_Telbal(
                    branch_code=branch_code, teller_id=row.org_teller_id, cash_od_allowed=False)
                tel.save()

            if row.tran_debit_credit == 'D':
                tran_debit_credit = 'C'
            else:
                tran_debit_credit = 'D'

            responding_tran = Tran_Telbal_Details(branch_code=branch_code, org_teller_id=request.session["app_user_id"],
                                                  res_teller_id=request.session[
                                                      "app_user_id"], tran_debit_credit=tran_debit_credit, transaction_date=row.transaction_date,
                                                  tran_amount=row.tran_amount, cancel_amount=row.cancel_amount, available_balance=row.available_balance,
                                                  auth_by=request.session["app_user_id"], auth_on=timezone.now(), app_user_id=request.session["app_user_id"],
                                                  app_data_time=timezone.now())
            responding_tran.save()

            res_bal = Transaction_Telbal.objects.get(
                teller_id=request.session["app_user_id"])
            if tran_debit_credit == 'D':
                res_bal.total_debit_amount = res_bal.total_debit_amount+row.tran_amount
                res_bal.cash_balance = res_bal.cash_balance-row.tran_amount
                res_bal.save()
            else:
                res_bal.total_credit_amount = res_bal.total_credit_amount+row.tran_amount
                res_bal.cash_balance = res_bal.cash_balance+row.tran_amount
                res_bal.save()

            org_bal = Transaction_Telbal.objects.get(
                teller_id=row.org_teller_id)
            if row.tran_debit_credit == 'D':
                org_bal.total_debit_amount = org_bal.total_debit_amount+row.tran_amount
                org_bal.cash_balance = org_bal.cash_balance-row.tran_amount
                org_bal.save()
            else:
                org_bal.total_credit_amount = org_bal.total_credit_amount+row.tran_amount
                org_bal.cash_balance = org_bal.cash_balance+row.tran_amount
                org_bal.save()

            data['form_is_valid'] = True
            data['success_message'] = "Accept Successfully"
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


class finance_charges_view(TemplateView):
    template_name = 'finance/finance-charges-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = ChargesModelForm(initial={'effective_from_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def finance_charges_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = ChargesModelForm(request.POST)
        if form.is_valid():

            charges_code = form.cleaned_data["charges_code"]
            app_user_id = request.session["app_user_id"]

            post = form.save(commit=False)
            charges_id = fn_generate_charges_id(100)
            post.app_user_id = app_user_id
            post.charges_id = charges_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Charge Parameter Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()

    return JsonResponse(data)


def finance_charges_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Charges, charges_code=id)
    old_charges_id = instance_data.charges_code
    template_name = 'finance/finance-charges-edit.html'
    context = {}
    data = dict()

    if request.method == 'POST':
        form = ChargesModelForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            charges_id = form.cleaned_data["charges_id"]

            if charges_id != old_charges_id:
                data['error_message'] = 'Charge Code Modification is Not Allowed!'
                data['form_is_valid'] = False
                return JsonResponse(data)

            obj = form.save(commit=False)
            obj.charges_id = old_charges_id
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
        form = ChargesModelForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)
