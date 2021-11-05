from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import FieldDoesNotExist
from django.core import serializers
from django.core.files import File
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
import math

from .utils import *
from .validations import *
from .myException import *
from .models import *
from .forms import *
from appauth.views import get_global_data, fn_get_employee_by_app_user_id
from finance.utils import fn_open_account_transaction_screen, fn_get_transaction_account_type, fn_get_account_info_byactype, fn_create_account, fn_get_accountinfo_byacnumber, fn_get_transaction_gl
from finance.validations import fn_val_account_number
from finance.utils import fn_get_accountinfo_bytran, fn_get_cash_gl_code, fn_cash_tran_posting, fn_transfer_tran_posting, fn_cancel_tran_batch
from appauth.globalparam import fn_is_user_permition_exist
from finance.utils import fn_get_account_ledger, fn_get_client_accounts_balance, fn_get_client_accounts_debit_credit
from appauth.utils import fn_get_query_result
from delar.utils import fn_get_branch_center
from delar.models import Srstage_Inventory_Status
# barcode
import os
from io import BytesIO 
import barcode
from barcode.writer import ImageWriter
# import pdfkit
# import mimetypes

class sales_clients_view(TemplateView):
    template_name = 'sales/sales-clients-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        context = get_global_data(request)
        single_client, client_type = fn_get_default_client_type('CLIENT_ENTRY')
        initial_dict = {'client_joining_date': cbd}
        if single_client == 'Y':
            context['client_type'] = client_type
            context['single_client'] = single_client
            initial_dict['client_type'] = client_type
        form = clients_model_form(initial=initial_dict)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def sales_clients_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = clients_model_form(request.POST)
                if form.is_valid():
                    try:
                        with transaction.atomic():
                            app_user_id = request.session["app_user_id"]
                            client_type = form.cleaned_data["client_type"]
                            account_title = form.cleaned_data["client_name"]
                            client_phone = form.cleaned_data["client_phone"]
                            branch_code = form.cleaned_data["branch_code"]
                            center_code = form.cleaned_data["center_code"]
                            client_admit_fee = form.cleaned_data["client_admit_fee"]
                            client_present_address = form.cleaned_data["client_present_address"]
                            client_id = fn_generate_client_id(branch_code)
                            #branch_center_code = fn_get_branch_center(center_code)
                            #client_id = fn_generate_client_id(branch_code, branch_center_code)
                            #branch_client_id = fn_generate_branch_client_id(branch_code)
                            cbd = form.cleaned_data["client_joining_date"]
                            transaction_doc_number = form.cleaned_data["transaction_doc_number"]

                            if client_admit_fee is None or not client_admit_fee:
                                client_admit_fee = 0.00

                            single_client, default_client_type = fn_get_default_client_type(
                                'CLIENT_ENTRY')
                            if single_client == 'Y':
                                client_type = default_client_type

                            if not branch_code:
                                data['error_message'] = 'Invalid Branch Code!'
                                raise Exception('Invalid Branch Code!')

                            if not center_code:
                                data['error_message'] = 'Invalid Center Code!'
                                raise Exception('Invalid Center Code!')

                            post = form.save(commit=False)
                            post.app_user_id = app_user_id
                            post.client_id = client_id
                            #post.branch_client_id = branch_client_id
                            post.save()

                            status, error_message = fn_create_account(p_branch_code=branch_code, p_center_code=center_code, p_app_user_id=app_user_id,
                                                                      p_client_id=client_id, p_client_type=client_type, p_client_name=account_title,
                                                                      p_client_address=client_present_address, p_phone_number=client_phone,p_cbd=cbd, 
                                                                      p_limit_amount=0.00)
                            if not status:
                                data['error_message'] = error_message
                                raise Exception(error_message)

                            transaction_master = {}
                            transaction_details = {}
                            tran_details = []
                            batch_number = 0
                            transaction_master["tran_date"] = cbd
                            transaction_master["branch_code"] = branch_code
                            transaction_master["center_code"] = center_code
                            transaction_master["tran_type"] = 'ADF_FEE'
                            transaction_master["transaction_screen"] = 'ADF_FEE'
                            transaction_master["app_user_id"] = app_user_id
                            transaction_master["master_narration"] = "Admission fee for Client : " + (
                                client_id)
                            cash_gl_code = fn_get_cash_gl_code()

                            if float(client_admit_fee) > 0.00:
                                param = Application_Settings.objects.get()
                                tran_gl_code = param.client_admission_fee_ledger
                                if not tran_gl_code:
                                    data['error_message'] = 'Admission Fee Ledger is Not Define!'
                                    Exception(data['error_message'])
                                tran_amount = client_admit_fee
                                narration = "Admission fee for Client : " + \
                                    (client_id)

                                transaction_details = {}
                                transaction_details["account_number"] = '0'
                                transaction_details["account_phone"] = ''
                                transaction_details["tran_gl_code"] = tran_gl_code
                                transaction_details["contra_gl_code"] = cash_gl_code
                                transaction_details["tran_debit_credit"] = 'C'
                                transaction_details["tran_amount"] = tran_amount
                                transaction_details["tran_document_number"] = transaction_doc_number
                                transaction_details["transaction_narration"] = narration
                                tran_details.append(transaction_details)

                                transaction_details = {}
                                transaction_details["account_number"] = '0'
                                transaction_details["account_phone"] = ''
                                transaction_details["tran_gl_code"] = cash_gl_code
                                transaction_details["contra_gl_code"] = tran_gl_code
                                transaction_details["tran_debit_credit"] = 'D'
                                transaction_details["tran_amount"] = tran_amount
                                transaction_details["tran_document_number"] = transaction_doc_number
                                transaction_details["transaction_narration"] = narration
                                tran_details.append(transaction_details)

                                if len(tran_details) > 0:

                                    status, message, batch_number = fn_transfer_tran_posting(
                                        transaction_master, tran_details)

                                    if not status:
                                        data['error_message'] = 'Error in Fee Receive!\n'+message
                                        logger.error("Error in Fee Receive sales_clients_insert {} \nType: {} \nError:{}".format(
                                            sys.exc_info()[-1], type(message).__name__, str(message)))
                                        raise Exception(data['error_message'])

                                if float(client_admit_fee) > 0.00:
                                    if not fn_fees_history(p_client_id=client_id, p_branch_code=branch_code, p_center_code=center_code, p_app_user_id=app_user_id, p_fee_type='ADF',
                                                           p_fee_amount=client_admit_fee, p_tran_date=cbd, p_batch_number=batch_number, p_transaction_narration=narration,
                                                           p_fee_memo_number=''):
                                        data['error_message'] = 'Admission Fee Deduction Error!'
                                        Exception(data['error_message'])

                            data['form_is_valid'] = True
                            data['success_message'] = 'Your Client ID is : '+client_id
                    except Exception as e:
                        data['form_is_valid'] = False
                        data['error_message'] = str(e)
                        logger.error("Error on line {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(e).__name__, str(e)))
                        return JsonResponse(data)
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def sales_clients_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    context = {}
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(
                Clients, client_id=id)
            branch_code = instance_data.branch_code
            center_code = instance_data.center_code
            client_center_code = instance_data.center_code
            client_id = instance_data.client_id
            client_type = instance_data.client_type
            template_name = 'sales/sales-clients-edit.html'
            data['success_message'] = ''
            data['error_message'] = ''

            if request.method == 'POST':
                form = clients_model_form(
                    request.POST, instance=instance_data)
                data['form_error'] = form.errors.as_json()
                if form.is_valid():
                    try:
                        with transaction.atomic():
                            app_user_id = request.session["app_user_id"]
                            #client_type = form.cleaned_data["client_type"]
                            account_title = form.cleaned_data["client_name"]
                            client_phone = form.cleaned_data["client_phone"]
                            client_present_address = form.cleaned_data["client_present_address"]
                            cbd = form.cleaned_data["client_joining_date"]
                            obj = form.save(commit=False)
                            obj.branch_code = branch_code
                            obj.center_code = client_center_code
                            obj.client_type = client_type
                            obj.client_id = client_id
                            obj.save()

                            Accounts_Balance.objects.filter(client_id=client_id).update(account_title=account_title,
                                                                                        phone_number=client_phone, account_address=client_present_address)

                            status, error_message = fn_create_account(p_branch_code=branch_code, p_center_code=center_code, p_app_user_id=app_user_id,
                                                                      p_client_id=client_id, p_client_type=client_type, p_client_name=account_title,
                                                                      p_client_address=client_present_address, p_phone_number=client_phone,p_cbd=cbd, 
                                                                      p_limit_amount=0.00)
                            if not status:
                                data['error_message'] = error_message
                                raise Exception(error_message)

                            data['form_is_valid'] = True
                    except Exception as e:
                        data['form_is_valid'] = False
                        if len(str(data['error_message'])) > 0:
                            return JsonResponse(data)
                        data['error_message'] = str(e)
                        logger.error("Error on line {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(e).__name__, str(e)))
                        return JsonResponse(data)
                else:
                    data['form_is_valid'] = False
                    data['error_message'] = form.errors.as_json()
            else:
                form = clients_model_form(instance=instance_data)  # forms name
                context = get_global_data(request)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)

class sales_clientlist_view(TemplateView):
    template_name = 'sales/sales-clients-list.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        context = get_global_data(request)
        forms = ClientSearch()
        context['forms'] = forms
        return render(request, self.template_name, context)


class sales_image_upload(TemplateView):
    template_name = 'sales/sales-image-upload.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = ClientDocumentsModelForms()
        context = get_global_data(request)
        context['success_message'] = ''
        context['error_message'] = ''
        context['form'] = form
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = ClientDocumentsModelForms(request.POST, request.FILES)
        context = dict()
        try:
            if form.is_valid():
                context = get_global_data(request)
                branch_code = request.session["branch_code"]
                app_user_id = request.session["app_user_id"]
                client_id = form.cleaned_data["client_id"]
                document_type = form.cleaned_data["document_type"]

                try:
                    photo_exist = Client_Photo_Sign.objects.get(
                        client_id=client_id, document_type=document_type, status='A')

                    photo_exist.status = 'I'
                    photo_exist.save()
                except Client_Photo_Sign.DoesNotExist:
                    pass

                post = form.save(commit=False)
                post.app_user_id = app_user_id
                post.save()

            form = ClientDocumentsModelForms()
            context['success_message'] = 'Image Upload Successfully'
            context['error_message'] = ''
            context['form'] = form

            return render(request, self.template_name, context)
        except Exception as e:
            error_message = 'Error '+str(e)
            context = get_global_data(request)
            context['form'] = form
            context['error_message'] = error_message
            return render(request, self.template_name, context)


def sales_show_image(request, client_id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'sales/sales-show-image.html'
    context = {}
    data = dict()
    branch_code = request.session["branch_code"]

    try:
        sign_data = Client_Photo_Sign.objects.get(
            client_id=client_id, document_type='S', status='A')
        data['signature_card'] = sign_data.document_location.path
        logger.error("Image {} \nType: {} \nError:{}".format(sys.exc_info(
        )[-1], type(sign_data.document_location.path).__name__, str(sign_data.document_location.path)))
        sign_name = str(sign_data.document_location.path).split('/')[-1]
        data['signature_card'] = '/media/sign_image/'+sign_name
    except Client_Photo_Sign.DoesNotExist:
        data['signature_card'] = ''

    try:
        image_data = Client_Photo_Sign.objects.get(
            client_id=client_id, document_type='P', status='A')
        logger.error("Image {} \nType: {} \nError:{}".format(sys.exc_info(
        )[-1], type(image_data.document_location.path).__name__, str(image_data.document_location.path)))
        photo_name = str(image_data.document_location.path).split('/')[-1]
        data['client_photo'] = '/media/sign_image/'+photo_name
    except Client_Photo_Sign.DoesNotExist:
        data['client_photo'] = ''

    context = get_global_data(request)

    data['html_form'] = render_to_string(
        template_name, context, request=request)
    data['html_form'] = data['html_form'].replace(
        'client_photo', data['client_photo'])
    data['html_form'] = data['html_form'].replace(
        'client_signature', data['signature_card'])
    # return HttpResponse(data)
    return HttpResponse(json.dumps(data))


class sales_supplier_view(TemplateView):
    template_name = 'sales/sales-supplier-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = Supplier_Model_Form(initial={'joining_date': cbd})
        args = {'form': form}
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

@transaction.atomic
def sales_supplier_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Supplier_Model_Form(request.POST)
                if form.is_valid():
                    try:
                        with transaction.atomic():
                            app_user_id = request.session["app_user_id"]
                            branch_code = request.session["branch_code"]
                            supp_name = form.cleaned_data["supp_name"]
                            supp_mobile = form.cleaned_data["supp_mobile"]
                            supp_address = form.cleaned_data["supp_address"]
                            joining_date = form.cleaned_data["joining_date"]
                            supp_id = fn_generate_supplier_id(branch_code)

                            status, error_message = fn_open_account_transaction_screen(p_transaction_screen='SUPPLIER_ENTRY', p_branch_code=branch_code, p_center_code='0',
                                                                                       p_app_user_id=request.session[
                                                                                           "app_user_id"], p_client_id=supp_id, p_client_name=supp_name,
                                                                                       p_client_address=supp_address, p_phone_number=supp_mobile,p_cbd=joining_date, 
                                                                                       p_limit_amount=0.00)
                            if not status:
                                data['error_message'] = error_message
                                raise Exception(error_message)

                            account_type, client_type = fn_get_transaction_account_type(
                                p_transaction_screen='SUPPLIER_ENTRY')

                            account_number, _, _, _ = fn_get_account_info_byactype(
                                p_client_id=supp_id, p_account_type=account_type)

                            post = form.save(commit=False)
                            post.app_user_id = app_user_id
                            post.supp_id = supp_id
                            post.account_number = account_number
                            post.save()
                            data['success_message'] = 'Supplier Added Successfully! Supplier ID : ' + \
                                str(supp_id)
                            data['form_is_valid'] = True
                            return JsonResponse(data)
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
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


def sales_supplier_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    context = {}
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(
                Supplier_Information, supp_id=id)
            account_number = instance_data.account_number
            supp_id = instance_data.supp_id
            branch_code = instance_data.branch_code
            template_name = 'sales/sales-supplier-edit.html'
            context = {}
            data = dict()

            if request.method == 'POST':
                form = Supplier_Model_Form(
                    request.POST, instance=instance_data)  # forms name
                data['form_error'] = form.errors.as_json()
                if form.is_valid():
                    supp_name = form.cleaned_data["supp_name"]
                    # acc = Accounts_Balance.objects.get(account_number=account_number)
                    # acc.account_title = supp_name
                    # acc.save()
                    obj = form.save(commit=False)
                    obj.account_number = account_number
                    obj.supp_id = supp_id
                    obj.branch_code = branch_code
                    obj.save()
                    context = get_global_data(request)
                    context['success_message'] = ''
                    context['error_message'] = ''
                    data['form_is_valid'] = True
                else:
                    data['form_is_valid'] = False
            else:
                form = Supplier_Model_Form(
                    instance=instance_data)  # forms name
                context = get_global_data(request)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


class sales_productgroup_view(TemplateView):
    template_name = 'sales/sales-productgroup-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Products_Group_Form()
        args = {'form': form}
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def sales_productgroup_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Products_Group_Form(request.POST)
                if form.is_valid():
                    try:
                        with transaction.atomic():
                            app_user_id = request.session["app_user_id"]
                            branch_code = request.session["branch_code"]
                            group_name = form.cleaned_data['group_name']

                            if fn_val_check_product_group_exist(group_name):
                                data['error_message'] = 'This Group Name Already Exist!'
                                data['form_is_valid'] = False
                                return JsonResponse(data)

                            group_id = fn_generate_product_group_id(
                                branch_code)
                            post = form.save(commit=False)
                            post.app_user_id = app_user_id
                            post.group_id = group_id
                            post.is_active = True
                            post.is_deleted = False
                            post.save()
                            data['success_message'] = 'Group Added Successfully!'
                            data['form_is_valid'] = True
                            return JsonResponse(data)
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
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


def sales_productgroup_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    context = {}
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(
                Products_Group, group_id=id)
            group_id = instance_data.group_id
            template_name = 'sales/sales-productgroup-edit.html'
            context = {}
            data = dict()

            if request.method == 'POST':
                form = Products_Group_Form(
                    request.POST, instance=instance_data)  # forms name
                data['form_error'] = form.errors.as_json()
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.group_id = group_id
                    obj.save()
                    context = get_global_data(request)
                    context['success_message'] = ''
                    context['error_message'] = ''
                    data['form_is_valid'] = True
                else:
                    data['form_is_valid'] = False
            else:
                form = Products_Group_Form(
                    instance=instance_data)  # forms name
                context = get_global_data(request)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


class sales_productbrand_view(TemplateView):
    template_name = 'sales/sales-productbrand-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Products_Brand_Form()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def sales_productbrand_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Products_Brand_Form(request.POST)
                if form.is_valid():
                    try:
                        with transaction.atomic():
                            app_user_id = request.session["app_user_id"]
                            branch_code = request.session["branch_code"]
                            brand_name = form.cleaned_data['brand_name']

                            if fn_val_check_product_brand_exist(brand_name):
                                data['error_message'] = 'This Brand Name Already Exist!'
                                data['form_is_valid'] = False
                                return JsonResponse(data)

                            brand_id = fn_generate_product_brand_id(
                                branch_code)
                            post = form.save(commit=False)
                            post.app_user_id = app_user_id
                            post.brand_id = brand_id
                            post.is_active = True
                            post.is_deleted = False
                            post.save()
                            data['success_message'] = 'Brand Added Successfully!'
                            data['form_is_valid'] = True
                            return JsonResponse(data)
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
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


def sales_productbrand_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    context = {}
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(
                Products_Brand, brand_id=id)
            brand_id = instance_data.brand_id
            template_name = 'sales/sales-productbrand-edit.html'
            context = {}
            data = dict()

            if request.method == 'POST':
                form = Products_Brand_Form(
                    request.POST, instance=instance_data)  # forms name
                data['form_error'] = form.errors.as_json()
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.brand_id = brand_id
                    obj.save()
                    context = get_global_data(request)
                    context['success_message'] = ''
                    context['error_message'] = ''
                    data['form_is_valid'] = True
                else:
                    data['form_is_valid'] = False
            else:
                form = Products_Brand_Form(
                    instance=instance_data)  # forms name
                context = get_global_data(request)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


class sales_products_view(TemplateView):
    template_name = 'sales/sales-products-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = ProductsModelForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def sales_products_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = ProductsModelForm(request.POST)
                if form.is_valid():
                    try:
                        with transaction.atomic():
                            branch_code = request.session["branch_code"]
                            app_user_id = request.session["app_user_id"]
                            product_bar_code = form.cleaned_data['product_bar_code']

                            if product_bar_code is not None or product_bar_code:
                                if fn_valid_product_barcode(product_bar_code):
                                    data['error_message'] = 'Product Already Exist!'
                                    return JsonResponse(data)

                            product_id = fn_generate_product_id(branch_code)
                            if fn_valid_product_code(branch_code, product_id):
                                data['error_message'] = 'Product Code Already Exist!'
                                return JsonResponse(data)

                            product_name = form.cleaned_data['product_name']
                            product_model = form.cleaned_data['product_model']
                            if not product_model or product_model is None:
                                product_model = ''

                            product_stock_gl = fn_create_product_ledger(p_gl_for='stock', p_product_name=product_name,
                                                                        p_product_model=product_model+" Purchase", p_branch_code=branch_code, p_app_user_id=app_user_id)
                            product_sales_gl = fn_create_product_ledger(p_gl_for='sales', p_product_name=product_name,
                                                                        p_product_model=product_model+" Sales", p_branch_code=branch_code, p_app_user_id=app_user_id)
                            #product_order_gl = fn_create_product_ledger(p_gl_for='order', p_product_name=product_name, p_product_model=product_model+" Order", p_delar_id=delar_id, p_app_user_id=app_user_id)
                            #product_profit_gl = fn_create_product_ledger(p_gl_for='profit', p_product_name=product_name, p_product_model=product_model+" Profit", p_delar_id=delar_id, p_app_user_id=app_user_id)
                            #product_loss_gl = fn_create_product_ledger(p_gl_for='loss', p_product_name=product_name,p_product_model=product_model+" Loss", p_delar_id=delar_id, p_app_user_id=app_user_id)
                            product_stock_ret_gl = fn_create_product_ledger(p_gl_for='stock_ret', p_product_name=product_name,
                                                                            p_product_model=product_model+" Stock Return", p_branch_code=branch_code, p_app_user_id=app_user_id)
                            product_sales_ret_gl = fn_create_product_ledger(p_gl_for='sales_ret', p_product_name=product_name,
                                                                            p_product_model=product_model+" Sales Return", p_branch_code=branch_code, p_app_user_id=app_user_id)
                            product_damage_gl = fn_create_product_ledger(p_gl_for='damage', p_product_name=product_name,
                                                                         p_product_model=product_model+" Damage", p_branch_code=branch_code, p_app_user_id=app_user_id)
                            product_profit_gl = fn_create_product_ledger(p_gl_for='profit', p_product_name=product_name,
                                                                         p_product_model=product_model+" Profit", p_branch_code=branch_code, p_app_user_id=app_user_id)
                            product_loss_gl = fn_create_product_ledger(p_gl_for='loss', p_product_name=product_name,
                                                                       p_product_model=product_model+" Loos", p_branch_code=branch_code, p_app_user_id=app_user_id)

                            try:
                                if len(product_stock_gl) <= 0:
                                    data['error_message'] = 'Error in Creating Product Ledger!'
                                    return JsonResponse(data)
                            except Exception as e:
                                data['error_message'] = 'Error in Creating Product Ledger!'
                                return JsonResponse(data)

                            print(product_stock_gl)

                            product_search_text = product_name + \
                                " ( "+product_model+" )"
                            post = form.save(commit=False)
                            post.app_user_id = app_user_id
                            post.product_stock_gl = product_stock_gl
                            post.product_sales_gl = product_sales_gl
                            post.product_order_gl = product_stock_gl
                            post.product_profit_gl = product_profit_gl
                            post.product_loss_gl = product_loss_gl
                            post.product_stock_ret_gl = product_stock_ret_gl
                            post.product_sales_ret_gl = product_sales_ret_gl
                            post.product_damage_gl = product_damage_gl
                            post.product_id = product_id.upper()
                            post.is_active = True
                            post.product_search_text = product_search_text
                            post.save()

                            data['form_is_valid'] = True
                            data['success_message'] = "Save Successfully!"
                    except Exception as e:
                        data['form_is_valid'] = False
                        if len(str(data['error_message'])) > 0:
                            return JsonResponse(data)
                        data['error_message'] = str(e)
                        logger.error("Error in sales_product_create_insert {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(e).__name__, str(e)))
                        return JsonResponse(data)
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


def sales_products_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    context = {}
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(products, product_id=id)
            product_id = instance_data.product_id
            product_stock_gl = instance_data.product_stock_gl
            product_sales_gl = instance_data.product_sales_gl
            product_order_gl = instance_data.product_order_gl
            product_profit_gl = instance_data.product_profit_gl
            product_loss_gl = instance_data.product_loss_gl
            product_group = instance_data.product_group
            product_name = instance_data.product_name
            template_name = 'sales/sales-products-edit.html'
            context = {}
            data = dict()

            if request.method == 'POST':
                form = ProductsModelForm(request.POST, instance=instance_data)
                if form.is_valid():
                    product_name = form.cleaned_data['product_name']
                    product_model = form.cleaned_data['product_model']
                    if not product_model or product_model is None:
                        product_model = ''

                    product_search_text = product_name + \
                        " ( "+product_model+" )"
                    obj = form.save(commit=False)
                    obj.product_search_text = product_search_text
                    obj.product_stock_gl = product_stock_gl
                    obj.product_sales_gl = product_sales_gl
                    obj.product_order_gl = product_order_gl
                    obj.product_profit_gl = product_profit_gl
                    obj.product_loss_gl = product_loss_gl
                    obj.product_id = product_id
                    obj.save()
                    data['form_is_valid'] = True
                else:
                    data['form_is_valid'] = False
                    data['form_error'] = form.errors.as_json()
                    return JsonResponse(data)
            else:
                form = ProductsModelForm(instance=instance_data)
                context = get_global_data(request)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


class sales_product_balance(TemplateView):
    template_name = 'sales/sales-products-balance.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Products_Search_Forms()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


class sales_product_list(TemplateView):
    template_name = 'sales/sales-products-list.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Products_Search_Forms()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def get_product_info(request, product_code):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    product_name = ''
    product_purces_price = ''
    product_sales_price = ''
    sales_discount_percent = ''
    sales_discount_type = ''
    product_total_stock = ''
    product_stock_alert = ''
    sales_discount_maxamt = ''
    sales_discount_fromdt = ''
    sales_discount_uptodt = ''
    sales_discount_amount = ''
    product_model = ''
    product_bar_code = ''
    try:
        product_info = products.objects.get(product_id=product_code.upper())
        product_name = product_info.product_name
        product_model = product_info.product_model
        product_bar_code = product_info.product_bar_code
        product_purces_price = product_info.product_purces_price
        product_sales_price = product_info.product_sales_price
        sales_discount_percent = product_info.sales_discount_percent
        sales_discount_type = product_info.sales_discount_type
        product_total_stock = product_info.product_total_stock
        product_stock_alert = product_info.product_stock_alert
        sales_discount_maxamt = product_info.sales_discount_maxamt
        sales_discount_fromdt = product_info.sales_discount_fromdt
        sales_discount_uptodt = product_info.sales_discount_uptodt
        sales_discount_amount = int(
            (product_sales_price*sales_discount_percent)/100)

    except Exception as e:
        product_name = 'Invalid Product'

    data['product_name'] = product_name
    data['product_purces_price'] = product_purces_price
    data['product_sales_price'] = product_sales_price
    data['sales_discount_percent'] = sales_discount_percent
    data['product_total_stock'] = product_total_stock
    data['product_stock_alert'] = product_stock_alert
    data['sales_discount_amount'] = sales_discount_amount
    data['product_bar_code'] = product_bar_code
    data['product_model'] = product_model
    data['form_is_valid'] = True
    return JsonResponse(data)


class sales_purchase_view(TemplateView):
    template_name = 'sales/sales-purchase-master.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        context = get_global_data(request)

        try:
            app_settings = Application_Settings.objects.get()
        except Exception as e:
            print('Application Settings Not Define')

        barcode_enable = app_settings.barcode_enable
        total_quantity, total_price = fn_get_stock_temp_summary(
            p_branch_code=branch_code, app_user_id=app_user_id)
        stock_master = Sales_Purchase_Master_Form(
            initial={'stock_date': cbd, 'show_room': 1, 'total_quantity': total_quantity, 'total_price': total_price})
        stock_detail_temp = Sales_Purchase_Details_Form()

        context['stock_master'] = stock_master
        context['is_barcode_enable'] = barcode_enable
        context['stock_detail_temp'] = stock_detail_temp
        return render(request, self.template_name, context)


class sales_quickpurchase_view(TemplateView):
    template_name = 'sales/sales-quickpurchase-master.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        context = get_global_data(request)

        try:
            app_settings = Application_Settings.objects.get()
        except Exception as e:
            print('Application Settings Not Define')

        barcode_enable = app_settings.barcode_enable
        total_quantity, total_price = fn_get_stock_temp_summary(
            p_branch_code=branch_code, app_user_id=app_user_id)
        stock_master = Sales_Purchase_Master_Form(
            initial={'stock_date': cbd, 'show_room': 1, 'total_quantity': total_quantity, 'total_price': total_price})
        stock_detail_temp = Sales_Purchase_Details_Form()

        context['stock_master'] = stock_master
        context['is_barcode_enable'] = barcode_enable
        context['stock_detail_temp'] = stock_detail_temp
        return render(request, self.template_name, context)


def sales_purchase_details_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = {}
    data['form_is_valid'] = False
    try:
        with transaction.atomic():
            if request.method == 'POST':
                product_id = request.POST.get('product_id')
                product_name = request.POST.get('product_name')
                quantity = request.POST.get('quantity')
                purces_price = request.POST.get('purces_price')
                dtl_total_price = request.POST.get('dtl_total_price')
                product_model = request.POST.get('product_model')
                product_bar_code = request.POST.get('product_bar_code')
                discount_amount = request.POST.get('discount_amount')
                branch_code = request.POST.get('branch_code')
                app_user_id = request.session["app_user_id"]

                if not branch_code or branch_code is None:
                    branch_code = request.session["branch_code"]

                if not product_id:
                    data['error_message'] = 'Please Select Valid Product!'
                    return JsonResponse(data)

                if product_bar_code and not product_id:
                    product_id = fn_get_product_id(product_bar_code)

                if product_id and not product_bar_code:
                    product_bar_code = fn_get_product_barcode(product_id)

                if not fn_valid_product_code(p_branch_code=branch_code, p_product_id=product_id):
                    data['error_message'] = 'Invalid Product!'
                    return JsonResponse(data)

                if int(quantity) <= 0:
                    data['error_message'] = 'Quantity can not be Negative or Zero!'
                    return JsonResponse(data)

                _, product_name, product_model = fn_get_product_details(
                    product_id)

                branch_instance = get_object_or_404(
                    Branch, branch_code=branch_code)
                product_instance = get_object_or_404(
                    products, product_id=product_id)

                if StockDetailsTemp.objects.filter(product_id=product_id, branch_code=branch_code, app_user_id=app_user_id).exists():
                    prod_temp_update = StockDetailsTemp.objects.get(
                        product_id=product_id, branch_code=branch_code, app_user_id=app_user_id)
                    prod_temp_update.quantity = prod_temp_update.quantity + \
                        int(quantity)
                    prod_temp_update.total_price = prod_temp_update.total_price + \
                        Decimal(dtl_total_price)
                    prod_temp_update.purces_price = prod_temp_update.purces_price + \
                        Decimal(purces_price)
                    prod_temp_update.discount_amount = prod_temp_update.discount_amount + \
                        Decimal(discount_amount)
                    prod_temp_update.save()
                else:
                    temp_stock_submit = StockDetailsTemp(product_id=product_instance, product_name=product_name, product_model=product_model,
                                                         quantity=quantity, status='N', branch_code=branch_code, total_price=dtl_total_price,
                                                         purces_price=purces_price, discount_amount=discount_amount, app_user_id=app_user_id)
                    temp_stock_submit.save()

                total_quantity, total_price = fn_get_stock_temp_summary(
                    p_branch_code=branch_code, app_user_id=app_user_id)
                data['form_is_valid'] = True
                data['total_quantity'] = total_quantity
                data['total_price'] = total_price

            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


def sales_delete_temp_stock_data(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    StockDetailsTemp.objects.filter(id=id).delete()
    app_user_id = request.session["app_user_id"]
    branch_code = request.session["branch_code"]
    total_quantity, total_price = fn_get_stock_temp_summary(
        p_branch_code=branch_code, app_user_id=app_user_id)
    data['total_quantity'] = total_quantity
    data['total_price'] = total_price
    data['form_is_valid'] = True
    return JsonResponse(data)


@transaction.atomic
def sales_purchase_post(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Sales_Purchase_Master_Form(request.POST)
                if form.is_valid():
                    stock_date = form.cleaned_data["stock_date"]
                    show_room = 1
                    comments = form.cleaned_data["comments"]
                    voucher_number = form.cleaned_data["voucher_number"]
                    total_quantity = form.cleaned_data["total_quantity"]
                    branch_code = form.cleaned_data["branch_code"]
                    app_user_id = request.session["app_user_id"]
                    supplier_id = '0'

                    if not branch_code or branch_code is None:
                        data['error_message'] = 'Please select Branch Name!'
                        return JsonResponse(data)

                    if show_room:
                        pass
                    else:
                        data['error_message'] = 'Please select Showroom!'
                        return JsonResponse(data)

                    stock_summary = StockDetailsTemp.objects.filter(
                        app_user_id=app_user_id).aggregate(Count('product_id'))
                    total_product = stock_summary['product_id__count']
                    if total_product == 0:
                        data['error_message'] = 'Noting to Submit!'
                        return JsonResponse(data)

                    try:
                        with transaction.atomic():

                            cursor = connection.cursor()
                            cursor.callproc("fn_sales_stock_submit", [
                                            stock_date, branch_code, app_user_id, supplier_id, show_room, voucher_number, comments])
                            row = cursor.fetchone()

                            if row[0] != 'S':
                                data['error_message'] = row[1]
                                raise Exception(row[1])

                            message = "Save Successfully : Stock ID : " + \
                                row[2]

                            data['message'] = message
                            data['form_is_valid'] = True

                            return JsonResponse(data)
                    except Exception as e:
                        data['form_is_valid'] = False
                        if len(data['error_message']) == 0:
                            data['error_message'] = str(e)
                        logger.error("Error on line {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(e).__name__, str(e)))
                        return JsonResponse(data)
                else:
                    data['error_message'] = form.errors.as_json()
                    data['form_is_valid'] = False
                    return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def sales_quickpurchase_post(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Sales_Purchase_Master_Form(request.POST)
                if form.is_valid():
                    stock_date = form.cleaned_data["stock_date"]
                    receipt_payment_ledger = form.cleaned_data["receipt_payment_ledger"]
                    show_room = 1
                    comments = form.cleaned_data["comments"]
                    voucher_number = form.cleaned_data["voucher_number"]
                    branch_code = form.cleaned_data["branch_code"]
                    total_pay = form.cleaned_data["total_pay"]
                    account_number = form.cleaned_data["account_number"]
                    app_user_id = request.session["app_user_id"]
                    supplier_id = '0'

                    if not branch_code or branch_code is None:
                        data['error_message'] = 'Please select Branch Name!'
                        return JsonResponse(data)

                    if show_room:
                        pass
                    else:
                        data['error_message'] = 'Please select Showroom!'
                        return JsonResponse(data)

                    stock_summary = StockDetailsTemp.objects.filter(
                        app_user_id=app_user_id).aggregate(Count('product_id'), Sum('quantity'), Sum('purces_price'),
                                                           Sum('total_price'), Sum('discount_amount'))
                    total_product = stock_summary['product_id__count']
                    total_quantity = stock_summary['quantity__sum']
                    total_purces_price = stock_summary['purces_price__sum']
                    total_price = stock_summary['total_price__sum']
                    total_discount_amount = stock_summary['discount_amount__sum']
                    if total_product == 0:
                        data['error_message'] = 'Noting to Submit!'
                        return JsonResponse(data)

                    if not account_number:
                        account_number = get_general_account(app_user_id)

                    if not receipt_payment_ledger or receipt_payment_ledger is None:
                        data['error_message'] = 'Please Select Payment Method!'
                        return JsonResponse(data)

                    details_row_list = []

                    _, _, _, _, supplier_id, _, _, _, _, _ = fn_get_accountinfo_byacnumber(
                        account_number)

                    dtl_data = StockDetailsTemp.objects.filter(
                        app_user_id=app_user_id)

                    stock_id = fn_generate_stock_id(branch_code)
                    print(stock_id)

                    for dtl_row in dtl_data:
                        row = StockDetails(branch_code=branch_code, stock_id=stock_id,
                                           supplier_id=supplier_id, product_id=dtl_row.product_id.product_id, purces_price=dtl_row.purces_price,
                                           total_price=dtl_row.total_price, discount_amount=dtl_row.discount_amount, status="W",
                                           quantity=dtl_row.quantity, returned_quantity=0, app_user_id=app_user_id, app_data_time=timezone.now())
                        details_row_list.append(row)

                    StockDetails.objects.bulk_create(details_row_list)

                    total_price = total_price-total_discount_amount
                    due_amount = total_price-total_pay

                    stock_auth = StockMasterAuthQ(branch_code=branch_code, stock_id=stock_id, supplier_id=supplier_id,
                                                  stock_date=stock_date, voucher_number=voucher_number, show_room=show_room, status='W', tran_type_code='CS',
                                                  payment_comments=comments, total_quantity=total_quantity, returned_quantity=0, returned_amount=0, cancel_quantity=0,
                                                  cancel_amount=0, total_price=total_price, total_pay=total_pay, due_amount=due_amount,
                                                  discount_amount=total_discount_amount, comments=comments)
                    stock_auth.save()

                    try:
                        with transaction.atomic():

                            cursor = connection.cursor()
                            cursor.callproc("fn_sales_stock_authorization", [branch_code, app_user_id, supplier_id,
                                                                             account_number, total_price, total_pay, total_discount_amount, receipt_payment_ledger,
                                                                             'STOCK', stock_date, stock_id, 'A', voucher_number, comments])
                            row = cursor.fetchone()

                            if row[0] != 'S':
                                data['error_message'] = row[1]
                                raise Exception(row[1])

                            message = "Save Successfully with Stock ID : " + stock_id

                            data['message'] = message
                            data['form_is_valid'] = True

                            StockDetailsTemp.objects.filter(
                                app_user_id=app_user_id).delete()

                            return JsonResponse(data)
                    except Exception as e:
                        data['form_is_valid'] = False
                        if len(data['error_message']) == 0:
                            data['error_message'] = str(e)
                        logger.error("Error on line {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(e).__name__, str(e)))
                        return JsonResponse(data)
                else:
                    data['error_message'] = form.errors.as_json()
                    data['form_is_valid'] = False
                    return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)

class sales_purchase_approval(TemplateView):
    template_name = 'sales/sales-purchase-approval.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        context = get_global_data(request)
        return render(request, self.template_name, context)


@transaction.atomic
def sales_purchase_payment(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    product = get_object_or_404(StockMasterAuthQ, id=id)
    template_name = 'sales/sales-purchase-payment.html'
    context = {}
    data = dict()

    if request.method == 'POST':
        form = StockMasterAuthQForm(request.POST, instance=product)
        data = dict()
        data['form_is_valid'] = False
        data['message'] = ''
        if form.is_valid():

            stock_date = form.cleaned_data["stock_date"]
            voucher_number = form.cleaned_data["voucher_number"]
            account_number = form.cleaned_data["account_number"]
            tran_type_code = form.cleaned_data["tran_type_code"]
            payment_comments = form.cleaned_data["payment_comments"]
            total_pay = form.cleaned_data["total_pay"]
            stock_id = form.cleaned_data["stock_id"]
            branch_code = form.cleaned_data["branch_code"]
            due_amount = form.cleaned_data["due_amount"]
            discount_amount = form.cleaned_data["discount_amount"]
            total_price = form.cleaned_data["total_price"]
            total_price_after_disc = total_price-discount_amount
            app_user_id = request.session["app_user_id"]

            cbd = stock_date

            if not fn_val_account_number(account_number):
                data['error_message'] = 'Please Select Valid Supplier!'
                return JsonResponse(data)

            _, _, _, _, client_id, _, _, _, _, _ = fn_get_accountinfo_byacnumber(
                account_number)

            try:
                if cbd != stock_date:
                    payment_comments = payment_comments + \
                        " Stock Date : "+str(stock_date)
            except Exception as e:
                pass

            tran_screen = 'STOCK_PAYMENT'

            credit_gl_code, debit_gl_code = fn_get_transaction_gl(
                p_transaction_screen=tran_screen, p_tran_type_code=tran_type_code)

            if credit_gl_code is None and total_pay > 0:
                data['error_message'] = 'Ledger Configuration Not Exist.'
                return JsonResponse(data)

            if not account_number:
                account_number = get_general_account(app_user_id)

            try:
                with transaction.atomic():

                    cursor = connection.cursor()
                    cursor.callproc("fn_sales_stock_authorization", [branch_code, app_user_id, client_id, account_number, total_price_after_disc,
                                                                     total_pay, discount_amount, credit_gl_code, 'STOCK',
                                                                     cbd, stock_id, 'A', voucher_number, payment_comments])
                    row = cursor.fetchone()

                    if row[0] != 'S':
                        data['error_message'] = row[1]
                        logger.error("Database Error in fn_sales_stock_authorization {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
                        raise Exception(row[1])

                    data['form_is_valid'] = True
                    return JsonResponse(data)
            except Exception as e:
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                logger.error("Error on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                return JsonResponse(data)
        else:
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:

        rows = StockMasterAuthQ.objects.raw('''SELECT p.product_id,
        s.id, d.id, p.product_name || ' (' || p.product_model || ' )' product_name,
        p.product_id, d.quantity, d.purces_price, d.total_price, d.discount_amount, 
        (d.total_price-d.discount_amount) price_after_discount
        FROM sales_stockmasterauthq s, sales_stockdetails d, sales_products p
        WHERE s.stock_id = d.stock_id AND p.product_id = d.product_id and s.id='''+"'"+str(id)+"'")

        form = StockMasterAuthQForm(instance=product)
        context['form'] = form
        context['id'] = id
        context['dtl_data'] = rows
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


def sales_purchase_reject(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    stock = StockMasterAuthQ.objects.get(pk=id)
    stock_detail = StockDetails.objects.filter(
        stock_id=stock.stock_id).update(status='J')
    stock.status = 'J'
    stock.save()
    response_data = {}
    response_data['success_message'] = "Save Successfully"
    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


class sales_purchase_list(TemplateView):
    template_name = 'sales/sales-purchase-list.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        branch_code = request.session["branch_code"]
        app_user_id = request.session["app_user_id"]
        cbd = get_business_date(branch_code, app_user_id)

        form = Search_Purchase_List(
            initial={'from_date': cbd, 'upto_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def sales_purchase_return(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    data['form_is_valid'] = False
    data['error_message'] = ''
    stock = StockMaster.objects.get(pk=id)
    branch_code = stock.branch_code
    app_user_id = request.session["app_user_id"]
    cbd = get_business_date(branch_code, app_user_id)

    try:
        with transaction.atomic():
            cursor = connection.cursor()
            cursor.callproc("fn_sales_stock_return", [branch_code, app_user_id, stock.stock_id,
                                                      stock.stock_date, 'ALL', 0, 'Return All Product of '+stock.stock_id, cbd])
            row = cursor.fetchone()

            if row[0] != 'S':
                logger.error("Database Error in fn_sales_stock_return on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
                data['error_message'] = row[1]
                data['form_is_valid'] = False
                raise Exception(row[1])

            data['form_is_valid'] = True
            data['success_message'] = "Return Successfully"
            return JsonResponse(data)

    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        logger.error("Error on fn_sales_stock_return line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)


@transaction.atomic
def sales_purchase_cancel(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    data['form_is_valid'] = False
    data['error_message'] = ''
    stock = StockMaster.objects.get(pk=id)
    branch_code = stock.branch_code
    app_user_id = request.session["app_user_id"]

    try:
        with transaction.atomic():
            cursor = connection.cursor()
            cursor.callproc("fn_sales_stock_cancel", [
                            branch_code, app_user_id, stock.stock_id, 'Cancel Stock'])
            row = cursor.fetchone()

            if row[0] != 'S':
                logger.error("Database Error in fn_sales_stock_cancel on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
                data['error_message'] = row[1]
                data['form_is_valid'] = False
                raise MyDatabaseError()

            data['form_is_valid'] = True
            data['success_message'] = "Cancel Successfully"
            return JsonResponse(data)

    except Exception as e:
        if len(data['error_message']) == 0:
            data['error_message'] = str(e)
        data['form_is_valid'] = False
        logger.error("Error on fn_stock_cancel line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)


def sales_purchase_details(request, id=0):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    batch_number = request.GET.get('batch_number')
    transaction_date = request.GET.get('transaction_date')
    branch_code = request.GET.get('branch_code')
    rows = StockMasterAuthQ.objects.raw('''SELECT p.product_id,
    s.id, d.id, p.product_name || ' (' || p.product_model || ' )' product_name,
    p.product_id, d.quantity, d.purces_price, d.total_price, d.discount_amount, 
    (d.total_price-d.discount_amount) price_after_discount
    FROM sales_stockmaster s, sales_stockdetails d, sales_products p
    WHERE s.stock_id = d.stock_id AND p.product_id = d.product_id and s.id='''+"'"+str(id)+"'")

    context = get_global_data(request)
    context['data'] = rows
    return render(request, 'sales/sales-purchase-details.html', context)


class sales_purchase_returnproduct(TemplateView):
    template_name = 'sales/sales-purchase-returnproduct.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = PurchaseReturnModelForm(initial={'return_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def sales_purchase_returnproduct_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ""
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = PurchaseReturnModelForm(request.POST)
                if form.is_valid():

                    product_id = form.cleaned_data["product_id"]
                    return_date = form.cleaned_data["return_date"]
                    returned_quantity = form.cleaned_data["returned_quantity"]
                    branch_code = form.cleaned_data["branch_code"]
                    account_number = form.cleaned_data["supplier_account"]
                    return_reason = form.cleaned_data["return_reason"]
                    return_amount = form.cleaned_data["return_amount"]
                    app_user_id = request.session["app_user_id"]

                    if return_amount < 0:
                        data['error_message'] = 'Return Amount can not be Negative!'
                        return JsonResponse(data)

                    if returned_quantity < 0:
                        data['error_message'] = 'Negative Quantity is Not Allowed.'
                        return JsonResponse(data)

                    _, _, _, _, client_id, _, _, _, _, _ = fn_get_accountinfo_byacnumber(
                        account_number)

                    try:
                        with transaction.atomic():
                            cursor = connection.cursor()
                            cursor.callproc("fn_sales_stock_return_by_product", [
                                            branch_code, app_user_id, client_id, account_number, product_id, returned_quantity, return_amount, return_reason, return_date])
                            row = cursor.fetchone()

                            if row[0] != 'S':
                                data['error_message'] = row[1]
                                data['form_is_valid'] = False
                                raise Exception(row[1])

                            data['form_is_valid'] = True
                            data['success_message'] = "Purchase Return Successfully!"

                            return JsonResponse(data)

                    except Exception as e:
                        data['form_is_valid'] = False
                        data['error_message'] = str(e)
                        logger.error("Error on line {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(e).__name__, str(e)))
                        return JsonResponse(data)
                else:
                    data['error_message'] = form.errors.as_json()
                    data['form_is_valid'] = False
                    return JsonResponse(data)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        logger.error("Error on fn_sales_stock_return_by_product line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)


class sales_purchasereturn_list(TemplateView):
    template_name = 'sales/sales-purchasereturn-list.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        branch_code = request.session["branch_code"]
        app_user_id = request.session["app_user_id"]
        cbd = get_business_date(branch_code, app_user_id)

        form = Search_Damage_List(
            initial={'from_date': cbd, 'upto_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def sales_purchasereturn_entrydetails(request):
    data = dict()
    data['error_message'] = ""
    data['form_is_valid'] = False
    try:
        product_id = request.GET.get('product_id')
        branch_code = request.GET.get('branch_code')
        upto_date = request.GET.get('upto_date')
        from_date = request.GET.get('from_date')
        supplier_id = request.GET.get('supplier_id')
        if upto_date == from_date:
            return_date = upto_date
        else:
            return_date = ''
        sql = ''' SELECT p.product_id,
       d.id,
       d.branch_code,
       p.product_name || ' (' || p.product_model || ' )' product_name,
       d.return_date,
       d.stock_date,
       d.returned_quantity,
       d.return_amount, 
       s.supp_name,
       d.return_reason,
       d.cancel_by,
       d.cancel_on,
       d.app_user_id,
       d.app_data_time
  FROM sales_stock_return_details d,
       sales_products p,
       sales_supplier_information s
 WHERE p.product_id = d.product_id AND s.supp_id = d.supplier_id '''

        if product_id:
            sql = sql+" AND p.product_id ='"+product_id+"'"

        if supplier_id:
            sql = sql+" AND d.supplier_id ='"+supplier_id+"'"

        if branch_code:
            sql = sql+" AND d.branch_code ="+branch_code

        if return_date:
            sql = sql+" AND d.return_date ='"+return_date+"'"

        if upto_date:
            sql = sql+" AND d.return_date <='"+upto_date+"'"

        if from_date:
            sql = sql+" AND d.return_date >='"+from_date+"'"

        data['data'] = fn_get_query_result(sql)
        return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        return JsonResponse(data)


@transaction.atomic
def sales_purchasereturn_cancel(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            stock_return = Stock_Return_Details.objects.get(pk=id)
            branch_code = stock_return.branch_code
            return_date = stock_return.return_date
            tran_batch_number = stock_return.tran_batch_number
            product_id = stock_return.product_id
            returned_quantity = stock_return.returned_quantity
            return_amount = stock_return.return_amount
            app_user_id = request.session["app_user_id"]

            if stock_return.cancel_by:
                data['error_message'] = "This Transaction Already Canceled!"
                data['form_is_valid'] = False
                return JsonResponse(data)

            status, error_message = fn_cancel_tran_batch(
                branch_code, app_user_id, return_date, tran_batch_number, 'Cancel by '+app_user_id)

            if not status:
                raise Exception(error_message)

            inv = Products_Inventory_Status.objects.get(
                branch_code=branch_code, product_id=product_id)

            if inv.inv_balance_upto_date is None:
                w_last_balance_update = return_date
            else:
                if return_date < inv.inv_balance_upto_date:
                    w_last_balance_update = return_date
                else:
                    w_last_balance_update = inv.inv_balance_upto_date

            if inv.last_stock_return_date is None:
                w_last_transaction_date = return_date
            else:
                if return_date > inv.last_stock_return_date:
                    w_last_transaction_date = return_date
                else:
                    w_last_transaction_date = inv.last_stock_return_date

            if not w_last_transaction_date or w_last_transaction_date is None:
                w_last_transaction_date = return_date

            inv.product_available_stock = inv.product_available_stock + \
                stock_return.returned_quantity
            inv.total_purchase_amount = inv.total_purchase_amount+stock_return.return_amount
            inv.total_stock_return = inv.total_stock_return - stock_return.returned_quantity
            inv.stock_return_amount = inv.stock_return_amount - stock_return.return_amount
            inv.inv_balance_upto_date = w_last_balance_update
            inv.last_stock_return_date = w_last_transaction_date
            inv.save()

            stock_return.cancel_by = app_user_id
            stock_return.cancel_on = timezone.now()
            stock_return.save()

            data['form_is_valid'] = True
            data['success_message'] = "Cancel Successfully"
            return JsonResponse(data)

    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        logger.error("Error on sales_purchasereturn_cancel line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)


class sales_product_damage(TemplateView):
    template_name = 'sales/sales-damage-entry.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = Product_Damage_ModelForm(initial={'damage_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def sales_product_damage_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ""
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Product_Damage_ModelForm(request.POST)
                if form.is_valid():

                    product_id = form.cleaned_data["product_id"]
                    damage_date = form.cleaned_data["damage_date"]
                    damage_quantity = form.cleaned_data["damage_quantity"]
                    branch_code = form.cleaned_data["branch_code"]
                    account_number = form.cleaned_data["supplier_account"]
                    comments = form.cleaned_data["comments"]
                    receive_amount = form.cleaned_data["receive_amount"]
                    damage_amount = form.cleaned_data["damage_amount"]
                    app_user_id = request.session["app_user_id"]
                    tran_batch_number = 0

                    if receive_amount < 0:
                        data['error_message'] = 'Receive Amount can not be Negative!'
                        return JsonResponse(data)

                    if damage_quantity < 0:
                        data['error_message'] = 'Negative Quantity is Not Allowed.'
                        return JsonResponse(data)

                    _, _, _, _, client_id, _, _, _, _, _ = fn_get_accountinfo_byacnumber(
                        account_number)

                    inv = Products_Inventory_Status.objects.get(
                        branch_code=branch_code, product_id=product_id)

                    if inv.inv_balance_upto_date is None:
                        w_last_balance_update = damage_date
                    else:
                        if damage_date < inv.inv_balance_upto_date:
                            w_last_balance_update = damage_date
                        else:
                            w_last_balance_update = inv.inv_balance_upto_date

                    if inv.last_damage_date is None:
                        w_last_transaction_date = damage_date
                    else:
                        if damage_date > inv.last_damage_date:
                            w_last_transaction_date = damage_date
                        else:
                            w_last_transaction_date = inv.last_damage_date

                    if not w_last_transaction_date or w_last_transaction_date is None:
                        w_last_transaction_date = damage_date

                    inv.product_available_stock = inv.product_available_stock-damage_quantity
                    inv.total_damage_amount = inv.total_damage_amount+damage_amount
                    inv.damage_receive_amount = inv.damage_receive_amount + receive_amount
                    inv.inv_balance_upto_date = w_last_balance_update
                    inv.last_damage_date = w_last_transaction_date
                    inv.save()

                    try:
                        with transaction.atomic():

                            transaction_master = {}
                            transaction_details = {}
                            tran_details = []
                            batch_number = 0
                            cash_gl_code = fn_get_cash_gl_code()
                            product_damage_gl, product_stock_gl = fn_get_product_damage_gl(
                                product_id)
                            product_bar_code, product_name, product_model = fn_get_product_details(
                                product_id)
                            tran_narration = comments+" Damage Entry for "+product_name

                            transaction_master["tran_date"] = damage_date
                            transaction_master["branch_code"] = branch_code
                            transaction_master["center_code"] = '0'
                            transaction_master["tran_type"] = 'DAMAGE'
                            transaction_master["transaction_screen"] = 'DAMAGE'
                            transaction_master["app_user_id"] = app_user_id
                            transaction_master["master_narration"] = tran_narration

                            transaction_details = {}
                            transaction_details["account_number"] = '0'
                            transaction_details["account_phone"] = ''
                            transaction_details["tran_gl_code"] = product_stock_gl
                            transaction_details["contra_gl_code"] = product_damage_gl
                            transaction_details["tran_debit_credit"] = 'C'
                            transaction_details["tran_amount"] = damage_amount
                            transaction_details["tran_document_number"] = product_id
                            transaction_details["transaction_narration"] = tran_narration
                            tran_details.append(transaction_details)

                            if receive_amount > 0:
                                tran_amount = damage_amount-receive_amount

                                transaction_details = {}
                                transaction_details["account_number"] = '0'
                                transaction_details["account_phone"] = ''
                                transaction_details["tran_gl_code"] = product_damage_gl
                                transaction_details["contra_gl_code"] = product_stock_gl
                                transaction_details["tran_debit_credit"] = 'D'
                                transaction_details["tran_amount"] = tran_amount
                                transaction_details["tran_document_number"] = product_id
                                transaction_details["transaction_narration"] = tran_narration
                                tran_details.append(transaction_details)

                                transaction_details = {}
                                transaction_details["account_number"] = account_number
                                transaction_details["account_phone"] = ''
                                transaction_details["tran_gl_code"] = '0'
                                transaction_details["contra_gl_code"] = product_stock_gl
                                transaction_details["tran_debit_credit"] = 'D'
                                transaction_details["tran_amount"] = receive_amount
                                transaction_details["tran_document_number"] = product_id
                                transaction_details["transaction_narration"] = tran_narration
                                tran_details.append(transaction_details)
                            else:
                                tran_amount = damage_amount

                                transaction_details = {}
                                transaction_details["account_number"] = '0'
                                transaction_details["account_phone"] = ''
                                transaction_details["tran_gl_code"] = product_damage_gl
                                transaction_details["contra_gl_code"] = product_stock_gl
                                transaction_details["tran_debit_credit"] = 'D'
                                transaction_details["tran_amount"] = tran_amount
                                transaction_details["tran_document_number"] = product_id
                                transaction_details["transaction_narration"] = tran_narration
                                tran_details.append(transaction_details)

                            if len(tran_details) > 0:

                                status, message, tran_batch_number = fn_transfer_tran_posting(
                                    transaction_master, tran_details)

                                if not status:
                                    data['error_message'] = 'Error in Voucher Posting!\n'+message
                                    logger.error("Error in Profit sales_product_damage_insert {} \nType: {} \nError:{}".format(
                                        sys.exc_info()[-1], type(message).__name__, str(message)))
                                    raise Exception(data['error_message'])

                            post = form.save(commit=False)
                            post.app_user_id = app_user_id
                            post.supplier_id = client_id
                            post.tran_batch_number = tran_batch_number
                            post.save()

                            data['form_is_valid'] = True
                            data['success_message'] = "Damage Entry Successfully!"

                            return JsonResponse(data)

                    except Exception as e:
                        data['form_is_valid'] = False
                        data['error_message'] = str(e)
                        logger.error("Error on line {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(e).__name__, str(e)))
                        return JsonResponse(data)
                else:
                    data['error_message'] = form.errors.as_json()
                    data['form_is_valid'] = False
                    return JsonResponse(data)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        logger.error("Error on fn_sales_stock_return_by_product line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)


class sales_damage_list(TemplateView):
    template_name = 'sales/sales-damage-list.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        branch_code = request.session["branch_code"]
        app_user_id = request.session["app_user_id"]
        cbd = get_business_date(branch_code, app_user_id)

        form = Search_Damage_List(
            initial={'from_date': cbd, 'upto_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def sales_damage_entrydetails(request):
    data = dict()
    data['error_message'] = ""
    data['form_is_valid'] = False
    try:
        product_id = request.GET.get('product_id')
        branch_code = request.GET.get('branch_code')
        upto_date = request.GET.get('upto_date')
        from_date = request.GET.get('from_date')
        supplier_id = request.GET.get('supplier_id')
        if upto_date == from_date:
            damage_date = upto_date
        else:
            damage_date = ''
        sql = ''' SELECT p.product_id,
       d.id,
       d.branch_code,
       p.product_name || ' (' || p.product_model || ' )' product_name,
       d.damage_date,
       d.damage_quantity,
       d.damage_amount,
       d.receive_amount,
       s.supp_name,
       d.comments,
       d.cancel_by,
       d.cancel_on,
       d.app_user_id,
       d.app_data_time
  FROM sales_product_damage_details d,
       sales_products p,
       sales_supplier_information s
 WHERE p.product_id = d.product_id AND s.supp_id = d.supplier_id '''

        if product_id:
            sql = sql+" AND p.product_id ='"+product_id+"'"

        if supplier_id:
            sql = sql+" AND d.supplier_id ='"+supplier_id+"'"

        if branch_code:
            sql = sql+" AND d.branch_code ="+branch_code

        if damage_date:
            sql = sql+" AND d.damage_date ='"+damage_date+"'"

        if upto_date:
            sql = sql+" AND d.damage_date <='"+upto_date+"'"

        if from_date:
            sql = sql+" AND d.damage_date >='"+from_date+"'"

        data['data'] = fn_get_query_result(sql)
        return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        return JsonResponse(data)


@transaction.atomic
def sales_damage_cancel(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            damage = Product_Damage_Details.objects.get(pk=id)
            branch_code = damage.branch_code
            damage_date = damage.damage_date
            tran_batch_number = damage.tran_batch_number
            product_id = damage.product_id
            app_user_id = request.session["app_user_id"]

            if damage.cancel_by:
                data['error_message'] = "This Transaction Already Canceled!"
                data['form_is_valid'] = False
                return JsonResponse(data)

            inv = Products_Inventory_Status.objects.get(
                branch_code=branch_code, product_id=product_id)

            if inv.inv_balance_upto_date is None:
                w_last_balance_update = damage_date
            else:
                if damage_date < inv.inv_balance_upto_date:
                    w_last_balance_update = damage_date
                else:
                    w_last_balance_update = inv.inv_balance_upto_date

            if inv.last_damage_date is None:
                w_last_transaction_date = damage_date
            else:
                if damage_date > inv.last_damage_date:
                    w_last_transaction_date = damage_date
                else:
                    w_last_transaction_date = inv.last_damage_date

            if not w_last_transaction_date or w_last_transaction_date is None:
                w_last_transaction_date = damage_date

            inv.product_available_stock = inv.product_available_stock+damage.damage_quantity
            inv.total_damage_amount = inv.total_damage_amount-damage.damage_amount
            inv.damage_receive_amount = inv.damage_receive_amount - damage.receive_amount
            inv.inv_balance_upto_date = w_last_balance_update
            inv.last_damage_date = w_last_transaction_date
            inv.save()

            status, error_message = fn_cancel_tran_batch(
                branch_code, app_user_id, damage_date, tran_batch_number, 'Cancel by '+app_user_id)

            if not status:
                raise Exception(error_message)

            damage.cancel_by = app_user_id
            damage.cancel_on = timezone.now()
            damage.save()

            data['form_is_valid'] = True
            data['success_message'] = "Cancel Successfully"
            return JsonResponse(data)

    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        logger.error("Error on sales_damage_cancel line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)


class sales_sales_create_view(TemplateView):
    template_name = 'sales/sales-sales-create.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        total_quantity, total_discount, total_price = get_product_cart_summary(
            app_user_id=request.session["app_user_id"])
        cbd = get_business_date(branch_code, app_user_id)

        try:
            edit_param = Application_Settings.objects.get()
        except Exception as e:
            print('Application Settings Not Define')

        if not edit_param.sales_executive_phone_editable:
            employee_id = fn_get_employee_by_app_user_id(app_user_id)
        else:
            employee_id = fn_get_employee_by_app_user_id(app_user_id)

        sales_master = SalesMasterModelForm(initial={'invoice_date': cbd, 'total_quantity': total_quantity, 'employee_id': employee_id,
                                                     'total_discount_amount': total_discount, 'bill_amount': total_price-total_discount, 'total_bill_amount': total_price,
                                                     'invoice_discount': ''})
        sales_details = SalesDetailsModelForm()

        context = get_global_data(request)
        context['sales_master'] = sales_master
        context['sales_details'] = sales_details
        single_transaction, tran_type_code = fn_get_sales_transaction_type('SALES_ENTRY')
        if single_transaction == 'Y':
            context['tran_type_code'] = tran_type_code
            context['single_transaction'] = single_transaction
        context['tran_type_code'] = tran_type_code
        return render(request, self.template_name, context)

@transaction.atomic
def sales_details_entry(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    update_product = False
    data['error_message'] = 'Invalid Input Data!'

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = SalesDetailsModelForm(request.POST)
                if form.is_valid():
                    sales_account_number = form.cleaned_data['sales_account_number']
                    product_id = form.cleaned_data['product_id']
                    product_bar_code = form.cleaned_data['product_bar_code']
                    total_price = form.cleaned_data['total_price']
                    discount_amount = form.cleaned_data['discount_amount']
                    discount_rate = form.cleaned_data["discount_rate"]
                    quantity = form.cleaned_data['quantity']
                    app_user_id = request.session["app_user_id"]
                    branch_code = request.session["branch_code"]
                    product_name = form.cleaned_data['product_name']
                    stock_available = form.cleaned_data['stock_available']
                    total_product_price = total_price-discount_amount

                    if not product_id:
                        data['error_message'] = 'Please Select Valid Product!'
                        return JsonResponse(data)

                    if product_bar_code and not product_id:
                        product_id = fn_get_product_id(product_bar_code)

                    if product_id and not product_bar_code:
                        product_bar_code = fn_get_product_barcode(product_id)

                    if stock_available < quantity:
                        data['error_message'] = 'Product Stock Not Available!'
                        return JsonResponse(data)

                    if discount_amount < 0:
                        data['error_message'] = 'Discount Amount can not be Negative!'
                        return JsonResponse(data)

                    if quantity < 0:
                        data['error_message'] = 'Negative Quantity is Not Allowed.'
                        return JsonResponse(data)

                    if sales_account_number is None:
                        data['error_message'] = 'Please enter customer details!'
                        return JsonResponse(data)

                    if product_id is None or len(product_id) == 0:
                        data['error_message'] = 'Invalid Product!'
                        return JsonResponse(data)

                    if product_name:
                        pass
                    else:
                        data['error_message'] = 'Invalid Product!'
                        return JsonResponse(data)

                    _, _, _, _, client_id, _, _, _, _, _ = fn_get_accountinfo_byacnumber(
                        sales_account_number)

                    if Sales_Details_Temp.objects.filter(product_id=product_id, app_user_id=app_user_id).exists():
                        prod_temp = Sales_Details_Temp.objects.get(
                            product_id=product_id, app_user_id=app_user_id)
                        total_price = prod_temp.total_price+total_price
                        discount_amount = prod_temp.discount_amount+discount_amount
                        quantity = prod_temp.quantity+quantity
                        total_product_price = total_price-discount_amount
                        update_product = True

                    total_free_quantity, discount_offer, discount_percent = get_product_offer(p_branch_code=branch_code, p_app_user=app_user_id, p_client_id=client_id,
                                                                                              p_product_id=product_id, p_total_quantity=quantity, p_total_product_price=total_product_price)

                    add_free_product_to_list(p_branch_code=branch_code, p_app_user=app_user_id, p_client_id=client_id,
                                             p_product_id=product_id, p_total_quantity=quantity)

                    if update_product:
                        prod_temp.quantity = quantity+total_free_quantity
                        prod_temp.total_price = total_price
                        prod_temp.discount_rate = discount_percent+discount_rate
                        prod_temp.discount_amount = discount_amount+discount_offer
                        prod_temp.save()
                    else:
                        post = form.save(commit=False)
                        post.app_user_id = app_user_id
                        post.product_id = product_id
                        post.details_branch_code = branch_code
                        post.quantity = quantity+total_free_quantity
                        post.total_price = total_price
                        post.discount_rate = discount_percent+discount_rate
                        post.discount_amount = discount_amount+discount_offer
                        post.save()

                    data['form_is_valid'] = True
                    data['error_message'] = ''
                else:
                    error_message = form.errors.as_json()
                    data['error_message'] = error_message
                    return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        return JsonResponse(data)

    total_quantity, total_discount, total_price = get_product_cart_summary(
        app_user_id=request.session["app_user_id"])

    data['total_quantity'] = total_quantity
    data['total_discount'] = total_discount
    data['total_price'] = total_price
    return JsonResponse(data)


def sales_details_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Sales_Details_Temp, id=id)
    template_name = 'sales/sales-details-edit.html'
    context = {}
    data = dict()

    if request.method == 'POST':
        form = SalesDetailsModelFormEdit(request.POST, instance=instance_data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = SalesDetailsModelFormEdit(instance=instance_data)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


def sales_details_delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    Sales_Details_Temp.objects.filter(id=id).delete()

    total_quantity, total_discount, total_price = get_product_cart_summary(
        app_user_id=request.session["app_user_id"])

    data['total_quantity'] = total_quantity
    data['total_discount'] = total_discount
    data['total_price'] = total_price

    data['form_is_valid'] = True
    return JsonResponse(data)


def sales_details_clear(request):
    if not request.user.is_authenticated:
        return render(request, 'sales/appauth-appauth.html')
    Sales_Details_Temp.objects.filter(
        app_user_id=request.session["app_user_id"]).delete()
    data = {}
    data['success_message'] = "Save Successfully"
    return JsonResponse(data)


@transaction.atomic
def sales_post_sales(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''

    if request.method == 'POST':
        form = SalesMasterModelForm(request.POST)
        if form.is_valid():
            try:
                invoice_date = form.cleaned_data["invoice_date"]
                customer_id = form.cleaned_data["customer_id"]
                customer_name = form.cleaned_data["customer_name"]
                account_number = form.cleaned_data["input_account_number"]
                customer_phone = form.cleaned_data["customer_phone"]
                customer_phone_input = form.cleaned_data["customer_phone"]
                customer_address = form.cleaned_data["customer_address"]
                employee_id = form.cleaned_data["employee_id"]
                total_quantity = form.cleaned_data["total_quantity"]
                total_bill_amount = form.cleaned_data["total_bill_amount"]
                bill_amount = form.cleaned_data["bill_amount"]
                pay_amount = form.cleaned_data["pay_amount"]
                invoice_discount = form.cleaned_data["invoice_discount"]
                advance_pay = form.cleaned_data["advance_pay"]
                total_discount_rate = form.cleaned_data["total_discount_rate"]
                total_discount_amount = form.cleaned_data["total_discount_amount"]
                invoice_comments = form.cleaned_data["invoice_comments"]
                branch_code = form.cleaned_data["branch_code"]
                app_user_id = request.session["app_user_id"]
                latitude = form.cleaned_data["latitude"]
                longitude = form.cleaned_data["longitude"]
                tran_type_code = form.cleaned_data["tran_type_code"]
                type_code = form.cleaned_data["type_code"]
                payment_document = form.cleaned_data["payment_document"]
                center_code = form.cleaned_data["center_code"]

                if invoice_date is None:
                    data['error_message'] = 'Please Enter Invoice Date!'
                    return JsonResponse(data)

                if center_code is None:
                    data['error_message'] = 'Please Select Center!'
                    return JsonResponse(data)

                if account_number is None:
                    data['error_message'] = 'Please Enter Client Phone Number!'
                    return JsonResponse(data)

                if invoice_discount is None:
                    invoice_discount = 0

                if branch_code is None or not branch_code:
                    data['error_message'] = 'Please Select Branch!'
                    return JsonResponse(data)

                if pay_amount is None:
                    pay_amount = 0

                if pay_amount < 0:
                    data['error_message'] = 'Negative Amount Payment is Not Allowed!'
                    return JsonResponse(data)

                if invoice_discount < 0:
                    data['error_message'] = 'Negative Amount on Discount is Not Allowed!'
                    return JsonResponse(data)

                if not fn_validate_chart_phone_mismatch(p_sales_account_number=account_number, p_app_user=app_user_id):
                    data['error_message'] = 'You have changed the customer phone number which may impact on product price.\nPlease clear your item and try again.'
                    return JsonResponse(data)

                total_quantity, total_discount, total_price = get_product_cart_summary(
                    app_user_id=request.session["app_user_id"])

                total_discount_amount = total_discount
                bill_amount = total_price-(total_discount+invoice_discount)
                total_bill_amount = total_price
                # latitude=3.4
                # longitude=3.4
                due_amount = bill_amount-pay_amount

                if bill_amount == 0:
                    data['error_message'] = 'Bill Amount Should Not be Zero!'
                    return JsonResponse(data)

                if total_quantity == 0:
                    data['error_message'] = 'Noting to Submit.'
                    return JsonResponse(data)

                if account_number == get_general_account(app_user_id):
                    if ((bill_amount-pay_amount) < 0):
                        data['error_message'] = 'Please Register for Advance Payment!'
                        return JsonResponse(data)

                if account_number == get_general_account(app_user_id):
                    if bill_amount-pay_amount != 0:
                        data['error_message'] = 'Please Register Customer for Due Sales!'
                        return JsonResponse(data)

                tran_screen = 'SALES_ENTRY'

                credit_gl_code, debit_gl_code = fn_get_transaction_gl(
                    p_transaction_screen=tran_screen, p_tran_type_code=tran_type_code)

                if credit_gl_code is None and debit_gl_code is None:
                    data['error_message'] = 'Sales Configuration Ledger Not Exist!\nPlease Contact with your Admin.'
                    return JsonResponse(data)

            except Exception as e:
                data['error_message'] = str(e)
                data['form_is_valid'] = False
                return JsonResponse(data)
            try:
                with transaction.atomic():
                    invoice_number = fn_generate_invoice_number(branch_code)
                    _, _, center_code, _, client_id, _, _, _, _, _ = fn_get_accountinfo_byacnumber(
                        account_number)
                    cursor = connection.cursor()
                    cursor.callproc("fn_sales_sales_post", [branch_code, center_code, app_user_id, invoice_number, customer_phone, client_id, customer_name,
                                                            customer_address, account_number, employee_id, pay_amount, invoice_discount,
                                                            tran_type_code, credit_gl_code, debit_gl_code, payment_document,
                                                            total_discount_rate, total_discount_amount, invoice_date, latitude, longitude])
                    row = cursor.fetchone()

                    if row[0] != 'S':
                        data['error_message'] = row[1]
                        raise Exception(row[1])

                    message = "Invoice Post Successfully! Invoice Number : " + invoice_number

                    data['success_message'] = message
                    data['form_is_valid'] = True

                    return JsonResponse(data)
            except Exception as e:
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                logger.error("Error on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                return JsonResponse(data)
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)

def sales_product_price(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        app_user_id = request.session["app_user_id"]
        product_code = request.GET.get('product_id')
        account_number = request.GET.get('account_number')
        branch_code = request.GET.get('branch_code')
        tran_type_code = request.GET.get('tran_type_code')
        if not product_code:
            bar_code=request.GET.get('bar_code')
            product=products.objects.filter(product_bar_code=bar_code).first()
            product_code=product.product_id

        _, _, _, _, client_id, _, _, _, _, _ = fn_get_accountinfo_byacnumber(
            account_number)
        product_price, discount_amount, discount_percent, product_name, discount_type, stock_available, product_model = fn_get_product_price(
            p_branch_code=branch_code, p_app_user=app_user_id, p_client_id=client_id, p_product_id=product_code,
            p_tran_type_code=tran_type_code)

        data['product_name'] = product_name
        data['product_code'] = product_code
        data['product_model'] = product_model
        data['product_price'] = product_price
        data['discount_percent'] = discount_percent
        data['discount_amount'] = discount_amount
        data['discount_type'] = discount_type
        data['stock_available'] = stock_available
        data['form_is_valid'] = True
        return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        data["error_message"] = str(e)
        return JsonResponse(data)


def sales_product_purchase_rate(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        app_user_id = request.session["app_user_id"]
        product_code = request.GET.get('product_id')
        branch_code = request.GET.get('branch_code')

        product_current_rate = fn_get_product_purchase_rate(
            p_branch_code=branch_code, p_product_id=product_code)

        data['product_current_rate'] = product_current_rate
        data['form_is_valid'] = True
        return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        data["error_message"] = str(e)
        return JsonResponse(data)


def sales_emi_insurance_fee(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        app_user_id = request.session["app_user_id"]
        transaction_amount = request.GET.get('transaction_amount')

        charge_amount = fn_get_charge_amount(p_transaction_amount=transaction_amount)

        data['charge_amount'] = charge_amount
        data['form_is_valid'] = True
        return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        data["error_message"] = str(e)
        return JsonResponse(data)


class sales_invoice_list(TemplateView):
    template_name = 'sales/sales-invoice-list.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        branch_code = request.session["branch_code"]
        app_user_id = request.session["app_user_id"]
        cbd = get_business_date(branch_code, app_user_id)
        invoice_search = InvoiceSearch(
            initial={'invoice_from_date': cbd, 'invoice_upto_date': cbd})
        context = get_global_data(request)
        context['form'] = invoice_search
        return render(request, self.template_name, context)


def sales_invoice_details(request, id=0):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    batch_number = request.GET.get('batch_number')
    transaction_date = request.GET.get('transaction_date')
    branch_code = request.GET.get('branch_code')
    rows = Sales_Master.objects.raw('''SELECT p.product_id,
       s.id,
       d.id,
       p.product_name || ' (' || p.product_model || ' )' product_name,
       d.service_card_no,d.service_start_date,d.service_end_date,
       d.quantity,
       d.returned_quantity,
       d.product_price,
       d.total_price,
       d.discount_amount,
       (d.total_price - d.discount_amount) price_after_discount
  FROM sales_sales_master s, sales_sales_details d, sales_products p
 WHERE     s.invoice_number = d.invoice_number
       AND p.product_id = d.product_id
       AND s.id ='''+"'"+str(id)+"'")

    context = get_global_data(request)
    context['data'] = rows
    return render(request, 'sales/sales-invoice-details.html', context)


@transaction.atomic
def sales_invoice_return(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    data['form_is_valid'] = False
    sales = Sales_Master.objects.get(pk=id)
    branch_code = sales.branch_code
    app_user_id = request.session["app_user_id"]
    cbd = get_business_date(branch_code, app_user_id)

    try:
        with transaction.atomic():
            cursor = connection.cursor()
            cursor.callproc("fn_sales_sales_return", [
                            branch_code, app_user_id, sales.invoice_number, sales.invoice_date, 'ALL', 0, 0, 'Return Invoice', cbd])
            row = cursor.fetchone()
            if row[0] != 'S':
                data['error_message'] = row[1]
                data['form_is_valid'] = False
                raise Exception(row[1])

            data['form_is_valid'] = True
            data['success_message'] = "Invoice Return Successfully"

            return JsonResponse(data)

    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        logger.error("Error on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)


@transaction.atomic
def sales_invoice_cancel(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    data['form_is_valid'] = False
    data['error_message'] = ''
    sales = Sales_Master.objects.get(pk=id)
    branch_code = sales.branch_code
    app_user_id = request.session["app_user_id"]

    try:
        with transaction.atomic():
            cursor = connection.cursor()
            cursor.callproc("fn_sales_sales_cancel", [
                            branch_code, app_user_id, sales.invoice_number, 'Cancel Invoice'])
            row = cursor.fetchone()

            if row[0] != 'S':
                logger.error("Database Error in fn_sales_sales_cancel on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
                data['error_message'] = row[1]
                data['form_is_valid'] = False
                raise Exception(row[1])

            data['form_is_valid'] = True
            data['success_message'] = "Cancel Successfully"

            return JsonResponse(data)

    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        logger.error("Error on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)


class sales_invoicereturn_list(TemplateView):
    template_name = 'sales/sales-invoicereturn-list.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        branch_code = request.session["branch_code"]
        app_user_id = request.session["app_user_id"]
        cbd = get_business_date(branch_code, app_user_id)

        form = Search_Sales_Return_List(
            initial={'from_date': cbd, 'upto_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)



def sales_invoicereturn_entrydetails(request):
    data = dict()
    data['error_message'] = ""
    data['form_is_valid'] = False
    try:
        
        branch_code = request.GET.get('branch_code')
        from_date = request.GET.get('from_date')
        upto_date = request.GET.get('upto_date')
        client_id = request.GET.get('client_id')
        
            
        sql = '''SELECT p.product_id,
       d.id,
       d.branch_code,
       c.center_name,
       p.product_name || ' (' || p.product_model || ' )' product_name,
       d.return_date,
       d.sales_date,
       d.returned_quantity,
       d.return_amount,
       s.client_name,
       d.return_reason,
       d.cancel_by,
       d.cancel_on,
       d.app_user_id,
       d.app_data_time
  FROM sales_sales_return_details d,
       sales_products p,
       sales_clients s,
       delar_center c
 WHERE     p.product_id = d.product_id
       AND s.client_id = d.client_id
       AND c.center_code = d.center_code '''

        if client_id:
            sql = sql+" AND s.client_id ='"+client_id+"'"

        if branch_code:
            sql = sql+" AND s.branch_code ="+branch_code
    
        print('sql',sql)
        data['data'] = fn_get_query_result(sql)
        return JsonResponse(data)
    except Exception as e:
        print('exception',e)
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        return JsonResponse(data)

###############
@transaction.atomic
def sales_invoicereturn_cancel(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            sales_return = Sales_Return_Details.objects.get(pk=id)
            branch_code = sales_return.branch_code
            return_date = sales_return.return_date
            tran_batch_number = sales_return.tran_batch_number
            product_id = sales_return.product_id
            returned_quantity = sales_return.returned_quantity
            return_amount = sales_return.return_amount
            app_user_id = request.session["app_user_id"]

            if sales_return.cancel_by:
                data['error_message'] = "This Transaction Already Canceled!"
                data['form_is_valid'] = False
                return JsonResponse(data)

            status, error_message = fn_cancel_tran_batch(
                branch_code, app_user_id, return_date, tran_batch_number, 'Cancel by '+app_user_id)

            if not status:
                raise Exception(error_message)

            inv = Products_Inventory_Status.objects.get(
                branch_code=branch_code, product_id=product_id)

            if inv.inv_balance_upto_date is None:
                w_last_balance_update = return_date
            else:
                if return_date < inv.inv_balance_upto_date:
                    w_last_balance_update = return_date
                else:
                    w_last_balance_update = inv.inv_balance_upto_date

            if inv.last_damage_date is None:
                w_last_transaction_date = return_date
            else:
                if return_date > inv.last_damage_date:
                    w_last_transaction_date = return_date
                else:
                    w_last_transaction_date = inv.last_damage_date

            if not w_last_transaction_date or w_last_transaction_date is None:
                w_last_transaction_date = return_date

            inv.product_available_stock = inv.product_available_stock + \
                sales_return.returned_quantity
            inv.total_sales_amount = inv.total_sales_amount+sales_return.return_amount
            inv.product_total_sales = inv.product_total_sales+sales_return.returned_quantity
            inv.cost_of_good_sold = inv.cost_of_good_sold + sales_return.purchase_value
            inv.total_sales_return = inv.total_sales_return - sales_return.returned_quantity
            inv.sales_return_amount = inv.sales_return_amount - sales_return.return_amount
            inv.inv_balance_upto_date = w_last_balance_update
            inv.last_damage_date = w_last_transaction_date
            inv.save()

            sales_return.cancel_by = app_user_id
            sales_return.cancel_on = timezone.now()
            sales_return.status = 'C'
            sales_return.save()

            data['form_is_valid'] = True
            data['success_message'] = "Cancel Successfully"
            return JsonResponse(data)

    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        logger.error("Error on sales_invoicereturn_cancel line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)


class Sales_Return_View(TemplateView):
    template_name = 'sales/sales-sales-return.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = SalesReturnModelForm(initial={'return_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def sales_return_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''
    data['success_message'] = ''

    if request.method == 'POST':
        form = SalesReturnModelForm(request.POST)
        if form.is_valid():
            try:
                product_id = form.cleaned_data["product_id"]
                return_date = form.cleaned_data["return_date"]
                returned_quantity = form.cleaned_data["returned_quantity"]
                app_user_id = request.session["app_user_id"]
                sales_invoice = form.cleaned_data["sales_invoice"]
                sales_date = form.cleaned_data["sales_date"]
                return_reason = form.cleaned_data["return_reason"]
                return_amount = form.cleaned_data["return_amount"]
                total_quantity=form.cleaned_data["total_quantity"]
                # sum_quantity=total_quantity-return_amount
                # total_quantity=sum_quantity


                if total_quantity < returned_quantity:
                        data['error_message'] = 'Product Stock Not Available!'
                        return JsonResponse(data)

                try:
                    sales = Sales_Master.objects.get(
                        invoice_number=sales_invoice)
                    branch_code = sales.branch_code
                except Exception as e:
                    data['form_is_valid'] = False
                    data['error_message'] = "Invalid Invoice Number!"
                    return JsonResponse(data)

                try:
                    with transaction.atomic():
                        cursor = connection.cursor()
                        cursor.callproc("fn_sales_sales_return", [
                                        branch_code, app_user_id, sales_invoice, sales_date, product_id, returned_quantity, return_amount, return_reason, return_date])
                        row = cursor.fetchone()
                        print(row)
                        if row[0] != 'S':
                            data['error_message'] = row[1]
                            data['form_is_valid'] = False
                            raise MyDatabaseError()

                        data['form_is_valid'] = True
                        data['success_message'] = "Invoice Return Successfully"

                        return JsonResponse(data)

                except Exception as e:
                    data['form_is_valid'] = False
                    logger.error("Error on line {} \nType: {} \nError:{}".format(
                        sys.exc_info()[-1], type(e).__name__, str(e)))
                    return JsonResponse(data)
            except Exception as e:
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                logger.error("Error on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                return JsonResponse(data)
        else:
            print(form.errors.as_json())
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


class sales_quick_sales_view(TemplateView):
    template_name = 'sales/sales-quick-sales.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        total_quantity, total_discount, total_price = get_product_cart_summary(
            app_user_id=request.session["app_user_id"])
        cbd = get_business_date(branch_code, app_user_id)

        try:
            edit_param = Application_Settings.objects.get()
        except Exception as e:
            print('Application Settings Not Define')

        type_code = edit_param.quick_payment_type
        client_id = edit_param.quick_sales_client_id
        client_name = edit_param.quick_sales_client_name
        client_address = edit_param.quick_sales_client_address
        quick_sales_entry_customer = edit_param.quick_sales_entry_customer
        quick_sales_account_number = edit_param.quick_sales_account_number
        input_account_number = get_general_account(app_user_id)

        if not edit_param.sales_executive_phone_editable:
            employee_id = fn_get_employee_by_app_user_id(app_user_id)
        else:
            employee_id = fn_get_employee_by_app_user_id(app_user_id)

        sales_master = QuickSalesModelForm(initial={'invoice_date': cbd, 'total_quantity': total_quantity, 'employee_id': employee_id,
                                                    'total_discount_amount': total_discount, 'bill_amount': total_price-total_discount, 'total_bill_amount': total_price,
                                                    'invoice_discount': '', 'customer_id': client_id, 'type_code': type_code, 'customer_phone': client_id, 'customer_name': client_name,
                                                    'customer_address': client_address, 'tran_type_code': type_code,
                                                    'input_account_number': quick_sales_account_number, 'account_number': quick_sales_account_number,
                                                    'center_code': '0'})
        sales_details = SalesDetailsModelForm(
            initial={'sales_account_number': quick_sales_account_number})

        context = get_global_data(request)
        context['sales_master'] = sales_master
        context['sales_details'] = sales_details
        return render(request, self.template_name, context)


def get_invoice_details(request, product_code, invoice_number):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    sales_date, total_quantity, sales_price = fn_get_invoice_details(
        p_product_id=product_code, p_invoice_number=invoice_number)

    check=Sales_Return_Details.objects.values('sales_invoice').annotate(Qty=Sum('returned_quantity')).filter(product_id=product_code,sales_invoice=invoice_number)
    qty=0
    for q in check:
        qty=q['Qty']
    data['sales_date'] = sales_date
    data['total_quantity'] = total_quantity - qty
    data['sales_price'] = sales_price
    data['form_is_valid'] = True
    return JsonResponse(data)


########## EMI SETUP ########################
class sales_emisetup_view(TemplateView):
    template_name = 'sales/sales-emisetup-createlist.html'  # page name change

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        emi_fee, emi_ins_rate = fn_get_client_emi_fee()
        form = Emi_Setup_Model_Form(
            initial={'emi_fee_amount': emi_fee, 'emi_ins_rate': emi_ins_rate})  # form
        args = {'form': form}
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def sales_emisetup_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'sales/sales-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''

    if request.method == 'POST':
        form = Emi_Setup_Model_Form(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    app_user_id = request.session["app_user_id"]
                    emi_reference_no = form.cleaned_data["emi_reference_no"]
                    total_emi_amount = form.cleaned_data["total_emi_amount"]
                    number_of_installment = form.cleaned_data["number_of_installment"]
                    emi_inst_amount = form.cleaned_data["emi_inst_amount"]
                    emi_fee_amount = form.cleaned_data["emi_fee_amount"]
                    client_id = form.cleaned_data["client_id"]
                    emi_rate = form.cleaned_data["emi_rate"]
                    emi_profit_amount = form.cleaned_data["emi_profit_amount"]
                    emi_ins_fee_amount = form.cleaned_data["emi_ins_fee_amount"]
                    emi_down_amount = form.cleaned_data["emi_down_amount"]
                    emi_reference_date = form.cleaned_data["emi_reference_date"]
                    emi_doc_fee_amount = form.cleaned_data["emi_doc_fee_amount"]
                    emi_reference_no = emi_reference_no.upper()
                    cbd = emi_reference_date

                    branch_code, center_code = fn_get_invoice_branch_center(
                        emi_reference_no)

                    if emi_down_amount is None:
                        emi_down_amount = 0.00

                    if emi_fee_amount is None:
                        emi_fee_amount = 0.00

                    if emi_ins_fee_amount is None:
                        emi_ins_fee_amount = 0.00

                    if emi_profit_amount is None:
                        emi_profit_amount = 0.00

                    if total_emi_amount <= 0.00:
                        data['error_message'] = 'EMI Amount Should Be More Than Zero!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    if emi_rate < 0.00:
                        data['error_message'] = 'EMI Rate Should Be More Than Zero!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    if number_of_installment < 0:
                        data['error_message'] = 'Number of Installment Should Be More Than Zero!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    if emi_inst_amount < 0.00:
                        data['error_message'] = 'Installment Amount Should Be More Than Zero!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    if fn_val_emisetup_exist(emi_reference_no):
                        data['error_message'] = 'EMI Setup Already Exist for This Invoice!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    if fn_val_invoice_canceled(emi_reference_no):
                        data['error_message'] = 'You can not perform EMI setup for Canceled Invoice!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    account_number, account_title, account_balance, credit_limit = fn_get_accountinfo_bytran(
                        p_client_id=client_id, p_tran_screen='EMI_RECEIVE')

                    if not account_number:
                        data['error_message'] = 'Invalid Customer ID!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    transaction_master = {}
                    transaction_details = {}
                    tran_details = []
                    batch_number = 0
                    transaction_master["tran_date"] = cbd
                    transaction_master["branch_code"] = branch_code
                    transaction_master["center_code"] = center_code
                    transaction_master["tran_type"] = 'EMI_SETUP'
                    transaction_master["transaction_screen"] = 'EMI_SETUP'
                    transaction_master["app_user_id"] = app_user_id
                    transaction_master["master_narration"] = "EMI Setup For " + \
                        emi_reference_no
                    cash_gl_code = fn_get_cash_gl_code()

                    if float(emi_fee_amount) > 0.00:
                        param = EMI_Settings.objects.get()
                        tran_gl_code = param.emi_fee_ledger
                        if not tran_gl_code:
                            data['error_message'] = 'EMI Fee Ledger Not Define!'
                            Exception(data['error_message'])
                        tran_amount = emi_fee_amount
                        narration = "EMI fee for Client : " + \
                            str(client_id)+" Invoice : "+emi_reference_no

                        transaction_details = {}
                        transaction_details["account_number"] = '0'
                        transaction_details["account_phone"] = ''
                        transaction_details["tran_gl_code"] = tran_gl_code
                        transaction_details["contra_gl_code"] = cash_gl_code
                        transaction_details["tran_debit_credit"] = 'C'
                        transaction_details["tran_amount"] = tran_amount
                        transaction_details["tran_document_number"] = emi_reference_no
                        transaction_details["transaction_narration"] = narration
                        tran_details.append(transaction_details)

                        transaction_details = {}
                        transaction_details["account_number"] = '0'
                        transaction_details["account_phone"] = ''
                        transaction_details["tran_gl_code"] = cash_gl_code
                        transaction_details["contra_gl_code"] = tran_gl_code
                        transaction_details["tran_debit_credit"] = 'D'
                        transaction_details["tran_amount"] = tran_amount
                        transaction_details["tran_document_number"] = emi_reference_no
                        transaction_details["transaction_narration"] = narration
                        tran_details.append(transaction_details)

                    if float(emi_ins_fee_amount) > 0.00:
                        param = EMI_Settings.objects.get()
                        tran_gl_code = param.emi_insurance_ledger
                        if not tran_gl_code:
                            data['error_message'] = 'INS Fee Ledger Not Define!'
                            Exception(data['error_message'])
                        tran_amount = emi_ins_fee_amount
                        narration = "EMI Form fee for Client : " + \
                            str(client_id)+" Invoice : "+emi_reference_no

                        transaction_details = {}
                        transaction_details["account_number"] = '0'
                        transaction_details["account_phone"] = ''
                        transaction_details["tran_gl_code"] = tran_gl_code
                        transaction_details["contra_gl_code"] = cash_gl_code
                        transaction_details["tran_debit_credit"] = 'C'
                        transaction_details["tran_amount"] = tran_amount
                        transaction_details["tran_document_number"] = emi_reference_no
                        transaction_details["transaction_narration"] = narration
                        tran_details.append(transaction_details)

                        transaction_details = {}
                        transaction_details["account_number"] = '0'
                        transaction_details["account_phone"] = ''
                        transaction_details["tran_gl_code"] = cash_gl_code
                        transaction_details["contra_gl_code"] = tran_gl_code
                        transaction_details["tran_debit_credit"] = 'D'
                        transaction_details["tran_amount"] = tran_amount
                        transaction_details["tran_document_number"] = emi_reference_no
                        transaction_details["transaction_narration"] = narration
                        tran_details.append(transaction_details)

                    if float(emi_doc_fee_amount) > 0.00:
                        param = EMI_Settings.objects.get()
                        tran_gl_code = param.emi_doc_fee_ledger
                        if not tran_gl_code:
                            data['error_message'] = 'Document Fee Ledger Not Define!'
                            Exception(data['error_message'])
                        tran_amount = emi_doc_fee_amount
                        narration = "Document fee for Client : " + \
                            str(client_id)+" Invoice : "+emi_reference_no

                        transaction_details = {}
                        transaction_details["account_number"] = '0'
                        transaction_details["account_phone"] = ''
                        transaction_details["tran_gl_code"] = tran_gl_code
                        transaction_details["contra_gl_code"] = cash_gl_code
                        transaction_details["tran_debit_credit"] = 'C'
                        transaction_details["tran_amount"] = tran_amount
                        transaction_details["tran_document_number"] = emi_reference_no
                        transaction_details["transaction_narration"] = narration
                        tran_details.append(transaction_details)

                        transaction_details = {}
                        transaction_details["account_number"] = '0'
                        transaction_details["account_phone"] = ''
                        transaction_details["tran_gl_code"] = cash_gl_code
                        transaction_details["contra_gl_code"] = tran_gl_code
                        transaction_details["tran_debit_credit"] = 'D'
                        transaction_details["tran_amount"] = tran_amount
                        transaction_details["tran_document_number"] = emi_reference_no
                        transaction_details["transaction_narration"] = narration
                        tran_details.append(transaction_details)

                    if float(emi_profit_amount) > 0.00:
                        emi_receivable, emi_receive = fn_get_emi_gl_code()
                        emi_gl_code = emi_receivable

                        if emi_gl_code is None:
                            data['error_message'] = 'EMI Profit Receiveable parameter Not Define!'
                            raise Exception(data['error_message'])

                        tran_amount = emi_profit_amount
                        narration = 'EMI Profit Posting for Invoice : '+emi_reference_no

                        transaction_details = {}
                        transaction_details["account_number"] = account_number
                        transaction_details["account_phone"] = ''
                        transaction_details["tran_gl_code"] = '0'
                        transaction_details["contra_gl_code"] = emi_gl_code
                        transaction_details["tran_debit_credit"] = 'D'
                        transaction_details["tran_amount"] = tran_amount
                        transaction_details["tran_document_number"] = emi_reference_no
                        transaction_details["transaction_narration"] = narration
                        tran_details.append(transaction_details)
                        transaction_details = {}
                        transaction_details["account_number"] = '0'
                        transaction_details["account_phone"] = ''
                        transaction_details["tran_gl_code"] = emi_gl_code
                        transaction_details["contra_gl_code"] = cash_gl_code
                        transaction_details["tran_debit_credit"] = 'C'
                        transaction_details["tran_amount"] = tran_amount
                        transaction_details["tran_document_number"] = emi_reference_no
                        transaction_details["transaction_narration"] = narration
                        tran_details.append(transaction_details)

                    if float(emi_down_amount) > 0.00:
                        emi_receivable, emi_receive = fn_get_emi_gl_code()
                        tran_amount = emi_down_amount
                        profit_amount = round(tran_amount*(emi_rate/100))
                        investment_amount = tran_amount-(profit_amount)

                        narration = "Cash Receive For Invoice : "+emi_reference_no
                        account_ledger = fn_get_account_ledger(account_number)

                        transaction_details = {}
                        transaction_details["account_number"] = account_number
                        transaction_details["account_phone"] = ''
                        transaction_details["tran_gl_code"] = '0'
                        transaction_details["contra_gl_code"] = cash_gl_code
                        transaction_details["tran_debit_credit"] = 'C'
                        transaction_details["tran_amount"] = tran_amount
                        transaction_details["tran_document_number"] = emi_reference_no
                        transaction_details["transaction_narration"] = narration
                        tran_details.append(transaction_details)

                        transaction_details = {}
                        transaction_details["account_number"] = '0'
                        transaction_details["account_phone"] = ''
                        transaction_details["tran_gl_code"] = cash_gl_code
                        transaction_details["contra_gl_code"] = account_ledger
                        transaction_details["tran_debit_credit"] = 'D'
                        transaction_details["tran_amount"] = investment_amount
                        transaction_details["tran_document_number"] = emi_reference_no
                        transaction_details["transaction_narration"] = "EMI Investment Receive for " + emi_reference_no
                        tran_details.append(transaction_details)

                        transaction_details = {}
                        transaction_details["account_number"] = '0'
                        transaction_details["account_phone"] = ''
                        transaction_details["tran_gl_code"] = cash_gl_code
                        transaction_details["contra_gl_code"] = emi_receive
                        transaction_details["tran_debit_credit"] = 'D'
                        transaction_details["tran_amount"] = profit_amount
                        transaction_details["tran_document_number"] = emi_reference_no
                        transaction_details["transaction_narration"] = "EMI Profit Receive for " + \
                            emi_reference_no
                        tran_details.append(transaction_details)

                        if not fn_update_invoice(p_invoice_number=emi_reference_no, p_down_amount=emi_down_amount):
                            data['error_message'] = 'Error in Updating Invoice Receive Amount!'
                            raise Exception(data['error_message'])

                    if len(tran_details) > 0:

                        status, message, batch_number = fn_transfer_tran_posting(
                            transaction_master, tran_details)

                        if not status:
                            data['error_message'] = 'Error in EMI Receive!\n'+message
                            logger.error("Error in Profit sales_emisetup_model_insert {} \nType: {} \nError:{}".format(
                                sys.exc_info()[-1], type(message).__name__, str(message)))
                            raise Exception(data['error_message'])

                    if float(emi_fee_amount) > 0.00:
                        if not fn_fees_history(p_client_id=client_id, p_branch_code=branch_code, p_center_code=center_code, p_app_user_id=app_user_id, p_fee_type='EMI',
                                               p_fee_amount=emi_fee_amount, p_tran_date=cbd, p_batch_number=batch_number, p_transaction_narration=narration,
                                               p_fee_memo_number=''):
                            data['error_message'] = 'EMI Form Fee Deduction Error!'
                            Exception(data['error_message'])

                    if float(emi_ins_fee_amount) > 0.00:
                        if not fn_fees_history(p_client_id=client_id, p_branch_code=branch_code, p_center_code=center_code, p_app_user_id=app_user_id, p_fee_type='INS',
                                               p_fee_amount=emi_ins_fee_amount, p_tran_date=cbd, p_batch_number=batch_number, p_transaction_narration=narration,
                                               p_fee_memo_number=''):
                            data['error_message'] = 'EMI Fee Deduction Error!'
                            Exception(data['error_message'])

                    if float(emi_doc_fee_amount) > 0.00:
                        if not fn_fees_history(p_client_id=client_id, p_branch_code=branch_code, p_center_code=center_code, p_app_user_id=app_user_id, p_fee_type='DOC',
                                               p_fee_amount=emi_doc_fee_amount, p_tran_date=cbd, p_batch_number=batch_number, p_transaction_narration=narration,
                                               p_fee_memo_number=''):
                            data['error_message'] = 'DOC Fee Deduction Error!'
                            raise Exception(data['error_message'])

                    post = form.save(commit=False)
                    post.app_user_id = app_user_id
                    post.emi_reference_no = emi_reference_no
                    post.emi_setup_batch = batch_number
                    post.total_emi_due = total_emi_amount
                    post.branch_code = branch_code
                    post.center_code = center_code
                    post.account_number = account_number
                    post.emi_down_amount = emi_down_amount
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = "EMI Setup Completed!"
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
def sales_emisetup_cancel(request, id):
    if not request.user.is_authenticated:
        return render(request, 'sales/salse-login.html')
    data = dict()
    data['form_is_valid'] = False
    try:
        with transaction.atomic():
            emi_row = Emi_Setup.objects.get(pk=id)
            app_user_id = request.session["app_user_id"]
            emi_reference_date = emi_row.emi_reference_date
            emi_setup_batch = emi_row.emi_setup_batch
            emi_down_amount = emi_row.emi_down_amount
            emi_reference_no = emi_row.emi_reference_no
            branch_code = emi_row.branch_code

            if emi_row.emi_cancel_by:
                data['error_message'] = "This EMI Setup Already Canceled!"
                data['form_is_valid'] = False
                return JsonResponse(data)

            if emi_row.installment_tot_repay_amt > 0.00:
                data['error_message'] = "You can not cancel EMI setup which has Received Installment amount!"
                data['form_is_valid'] = False
                return JsonResponse(data)

            cancel_comments = 'EMI Cancel by '+app_user_id

            if emi_setup_batch > 0:
                status, error_message = fn_cancel_tran_batch(p_branch_code=branch_code, p_app_user_id=app_user_id,
                                                             p_transaction_date=emi_reference_date, p_batch_number=emi_setup_batch, p_cancel_comments=cancel_comments)
                if not status:
                    raise Exception(error_message)

                status, message = fn_fees_history_cancel(p_branch_code=branch_code, p_batch_number=emi_setup_batch,
                                                         p_fee_collection_date=emi_reference_date, p_app_user_id=app_user_id)

                if not status:
                    raise Exception(message)

            if not fn_cancel_invoice_update(p_invoice_number=emi_reference_no, p_down_amount=emi_down_amount):
                data['error_message'] = 'Error in Updating Invoice Amount!'
                data['form_is_valid'] = False
                return JsonResponse(data)

            emi_row.emi_cancel_by = app_user_id
            emi_row.emi_cancel_on = timezone.now()
            emi_row.save()

            data['success_message'] = "EMI Cancel Successfully!"
            data['form_is_valid'] = True
            return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        return JsonResponse(data)


def get_invoice_summary(request, invoice_number):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    app_user_id = request.session["app_user_id"]
    branch_code = request.session["branch_code"]

    sales_date = ''
    bill_amount = 0
    due_amount = 0
    total_quantity = 0
    invoice_number = invoice_number.upper()

    sales_date, bill_amount, due_amount, total_quantity, client_id = fn_get_invoice_summary(
        p_invoice_number=invoice_number)

    data['sales_date'] = sales_date
    data['bill_amount'] = bill_amount
    data['due_amount'] = due_amount
    data['total_quantity'] = total_quantity
    data['client_id'] = client_id
    data['form_is_valid'] = True
    return JsonResponse(data)


def sales_choice_emiinvoicelist(request):
    account_number = request.GET.get('account_number')
    list_data = Emi_Setup.objects.filter(account_number=account_number, total_emi_due__gt=0.00, emi_cancel_by__isnull=True).values(
        'emi_reference_no', 'emi_inst_amount', 'emi_inst_frequency', 'emi_reference_date').order_by('emi_reference_date')
    return render(request, 'sales/sales-choice-emiinvoicelist.html', {'list_data': list_data})


def sales_choice_emiinvoicelistall(request):
    client_id = request.GET.get('client_id')
    list_data = Emi_Setup.objects.filter(client_id=client_id, emi_cancel_by__isnull=True).values(
        'emi_reference_no', 'emi_inst_amount', 'emi_inst_frequency', 'emi_reference_date').order_by('emi_reference_date')
    return render(request, 'sales/sales-choice-emiinvoicelist.html', {'list_data': list_data})


def sales_emi_details(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    emi_reference_no = request.GET.get('emi_reference_no')
    account_number = request.GET.get('account_number')
    total_emi_amount, installment_amount, number_of_installment, paid_installment_number, total_emi_payment, total_emi_due = fn_get_emi_details(
        emi_reference_no, account_number)
    data['total_emi_amount'] = total_emi_amount
    data['installment_amount'] = installment_amount
    data['number_of_installment'] = number_of_installment
    data['paid_installment_number'] = math.floor(paid_installment_number)
    data['total_emi_payment'] = total_emi_payment
    data['total_emi_due'] = total_emi_due
    data['form_is_valid'] = True
    return JsonResponse(data)


def sales_emi_maturity_date(request, emi_freq, inst_number, from_date):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    maturity_date = get_emi_maturity_date(emi_freq, inst_number, from_date)
    first_inst_date = from_date
    data['maturity_date'] = maturity_date
    data['first_inst_date'] = first_inst_date
    data['form_is_valid'] = True
    return JsonResponse(data)


def sales_emi_maturity_date_fromcbd(request, emi_freq, inst_number):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    app_user_id = request.session["app_user_id"]
    branch_code = request.session["branch_code"]
    from_date = str(get_business_date(branch_code, app_user_id))
    maturity_date = get_emi_maturity_date(emi_freq, inst_number, from_date)
    first_inst_date = get_emi_maturity_date(emi_freq, '1', from_date)
    data['maturity_date'] = maturity_date
    data['first_inst_date'] = first_inst_date
    data['form_is_valid'] = True
    return JsonResponse(data)


########## EMI Receive ########################
class sales_emircv_view(TemplateView):
    template_name = 'sales/sales-emircv-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = Emi_Receive_Model_Form(initial={'receive_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def sales_emircv_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''

    if request.method == 'POST':
        form = Emi_Receive_Model_Form(request.POST)  # forms name
        if form.is_valid():
            try:
                with transaction.atomic():
                    app_user_id = request.session["app_user_id"]
                    tran_document_number = form.cleaned_data["receive_document_number"]
                    tran_amount = form.cleaned_data["receive_amount"]
                    receive_date = form.cleaned_data["receive_date"]
                    account_number = form.cleaned_data["account_number"]
                    emi_reference_no = form.cleaned_data["emi_reference_no"]
                    narration = 'EMI Receive for Invoice ' + emi_reference_no
                    #branch_code = request.session["branch_code"]
                    branch_code, center_code = fn_get_invoice_branch_center(
                        emi_reference_no)

                    if len(str(tran_amount)) > 22:
                        data['error_message'] = 'Length of transaction amount exceed!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    if tran_amount < 0:
                        data['error_message'] = 'Negative amount is not allowed!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    status, error_message = fn_validate_emi_amount(
                        p_account_number=account_number, p_invoice_number=emi_reference_no, p_emi_amount=tran_amount,
                        p_emi_receive_date=receive_date)
                    if not status:
                        data['error_message'] = error_message
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    cash_gl_code = fn_get_cash_gl_code()
                    account_ledger = fn_get_account_ledger(account_number)
                    emi_rate = fn_get_emi_rate(
                        emi_reference_no, account_number)
                    emi_receivable, emi_receive = fn_get_emi_gl_code()

                    emi_profit_amount = round(tran_amount*(emi_rate/100))
                    emi_invest_amount = tran_amount-(emi_profit_amount)

                    _, _, _, _, client_id, _, _, _, _, _ = fn_get_accountinfo_byacnumber(
                        account_number)

                    transaction_master = {}
                    transaction_details = {}
                    tran_details = []
                    transaction_master["tran_date"] = receive_date
                    transaction_master["branch_code"] = branch_code
                    transaction_master["center_code"] = center_code
                    transaction_master["tran_type"] = 'EMI_RECEIVE'
                    transaction_master["transaction_screen"] = 'EMI_RECEIVE'
                    transaction_master["app_user_id"] = app_user_id
                    transaction_master["master_narration"] = narration

                    transaction_details = {}
                    transaction_details["account_number"] = account_number
                    transaction_details["account_phone"] = ''
                    transaction_details["tran_gl_code"] = '0'
                    transaction_details["contra_gl_code"] = cash_gl_code
                    transaction_details["tran_debit_credit"] = 'C'
                    transaction_details["tran_amount"] = tran_amount
                    transaction_details["tran_document_number"] = tran_document_number
                    transaction_details["transaction_narration"] = "EMI Receive for " + \
                        emi_reference_no

                    tran_details.append(transaction_details)
                    transaction_details = {}
                    transaction_details["account_number"] = '0'
                    transaction_details["account_phone"] = ''
                    transaction_details["tran_gl_code"] = cash_gl_code
                    transaction_details["contra_gl_code"] = account_ledger
                    transaction_details["tran_debit_credit"] = 'D'
                    transaction_details["tran_amount"] = emi_invest_amount
                    transaction_details["tran_document_number"] = tran_document_number
                    transaction_details["transaction_narration"] = "EMI Investment Receive for " + emi_reference_no
                    tran_details.append(transaction_details)

                    transaction_details = {}
                    transaction_details["account_number"] = '0'
                    transaction_details["account_phone"] = ''
                    transaction_details["tran_gl_code"] = cash_gl_code
                    transaction_details["contra_gl_code"] = emi_receive
                    transaction_details["tran_debit_credit"] = 'D'
                    transaction_details["tran_amount"] = emi_profit_amount
                    transaction_details["tran_document_number"] = tran_document_number
                    transaction_details["transaction_narration"] = "EMI Profit Receive for " + \
                        emi_reference_no
                    tran_details.append(transaction_details)

                    transaction_details = {}
                    transaction_details["account_number"] = '0'
                    transaction_details["account_phone"] = ''
                    transaction_details["tran_gl_code"] = emi_receivable
                    transaction_details["contra_gl_code"] = emi_receive
                    transaction_details["tran_debit_credit"] = 'D'
                    transaction_details["tran_amount"] = emi_profit_amount
                    transaction_details["tran_document_number"] = tran_document_number
                    transaction_details["transaction_narration"] = "EMI Profit Adjustment for " + emi_reference_no
                    tran_details.append(transaction_details)

                    transaction_details = {}
                    transaction_details["account_number"] = '0'
                    transaction_details["account_phone"] = ''
                    transaction_details["tran_gl_code"] = emi_receive
                    transaction_details["contra_gl_code"] = emi_receivable
                    transaction_details["tran_debit_credit"] = 'C'
                    transaction_details["tran_amount"] = emi_profit_amount
                    transaction_details["tran_document_number"] = tran_document_number
                    transaction_details["transaction_narration"] = "EMI Profit Adjustment for " + emi_reference_no

                    tran_details.append(transaction_details)

                    status, message, batch_number = fn_transfer_tran_posting(
                        transaction_master, tran_details)

                    if not status:
                        data['error_message'] = 'Error in EMI Receive!\n'+message
                        logger.error("Error in emircv_model_insert {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(message).__name__, str(message)))
                        raise Exception('Error in EMI Receive! '+message)

                    status_emi, error_message_emi = fn_update_emi_receive(p_account_number=account_number,
                                                                          p_invoice_number=emi_reference_no, p_emi_amount=tran_amount, p_emi_receive_date=receive_date)
                    if status_emi:
                        pass
                    else:
                        data['error_message'] = error_message_emi
                        logger.error("Error in emircv_model_insert {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(message).__name__, str(message)))
                        raise Exception(error_message_emi)

                    post = form.save(commit=False)
                    post.app_user_id = app_user_id
                    post.branch_code = branch_code
                    post.center_code = center_code
                    post.tran_batch_number = batch_number
                    post.transaction_narration = narration
                    post.client_id = client_id
                    post.save()

                    status, message, = fn_update_emibal_hist(
                        account_number, emi_reference_no, receive_date)

                    if not status:
                        data['error_message'] = 'Error in fn_update_emibal_hist!\n'+message
                        logger.error("Error in fn_update_emibal_hist {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(message).__name__, str(message)))
                        raise Exception('Error in Updateing Balance! '+message)

                    data['form_is_valid'] = True
                    data['success_message'] = 'EMI Receive With Batch Number :'+batch_number
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


def sales_emircv_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Emi_Receive, id=id)  # Model name
    old_receive_amount = instance_data.receive_amount
    emi_reference_no = instance_data.emi_reference_no
    old_narration = instance_data.transaction_narration
    old_is_transfer = instance_data.is_transfer
    branch_code = instance_data.branch_code
    template_name = 'sales/sales-emircv-edit.html'  # page name change
    context = {}
    data = dict()
    data['error_message'] = ''

    if request.method == 'POST':
        form = Emi_Receive_Model_Form(
            request.POST, instance=instance_data)  # forms name
        if form.is_valid():
            try:
                with transaction.atomic():
                    app_user_id = request.session["app_user_id"]
                    tran_document_number = form.cleaned_data["receive_document_number"]
                    tran_amount = form.cleaned_data["receive_amount"]
                    receive_date = form.cleaned_data["receive_date"]
                    account_number = form.cleaned_data["account_number"]
                    emi_reference_no = form.cleaned_data["emi_reference_no"]
                    narration = 'Correction of previous amount ' + \
                        str(old_receive_amount)

                    if old_is_transfer:
                        data['error_message'] = 'You can not edit Transfer Transaction!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    if old_receive_amount == 0:
                        data['error_message'] = 'You can not edit cancel Transaction!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    if len(str(tran_amount)) > 22:
                        data['error_message'] = 'Length of transaction amount exceed!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    if tran_amount < 0:
                        data['error_message'] = 'Negative amount is not allowed!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    new_instrcv_instlmnt = tran_amount-old_receive_amount

                    if new_instrcv_instlmnt != 0:
                        if new_instrcv_instlmnt > 0:
                            tran_amount = new_instrcv_instlmnt
                            tran_debit_credit = 'C'
                            tran_type = 'CR'
                        else:
                            tran_amount = abs(new_instrcv_instlmnt)
                            tran_debit_credit = 'D'
                            tran_type = 'CP'

                        cash_gl_code = fn_get_cash_gl_code()
                        transaction_details = {}
                        transaction_details["tran_date"] = receive_date
                        transaction_details["branch_code"] = branch_code
                        transaction_details["tran_type"] = tran_type
                        transaction_details["transaction_screen"] = 'EMI_RECEIVE'
                        transaction_details["account_number"] = account_number
                        transaction_details["account_phone"] = ''
                        transaction_details["tran_gl_code"] = '0'
                        transaction_details["contra_gl_code"] = cash_gl_code
                        transaction_details["tran_debit_credit"] = tran_debit_credit
                        transaction_details["tran_amount"] = tran_amount
                        transaction_details["tran_document_number"] = emi_reference_no
                        transaction_details["app_user_id"] = app_user_id
                        transaction_details["transaction_narration"] = narration

                        status, message, batch_number = fn_cash_tran_posting(
                            transaction_details)

                        if not status:
                            data['error_message'] = 'Error in emircv_model_edit!\n'+message
                            logger.error("Error in emircv_model_edit {} \nType: {} \nError:{}".format(
                                sys.exc_info()[-1], type(message).__name__, str(message)))
                            raise MyDatabaseError()

                        if fn_update_emi_receive(p_account_number=account_number, p_invoice_number=emi_reference_no, p_emi_amount=new_instrcv_instlmnt,
                                                 p_emi_receive_date=receive_date):
                            pass
                        else:
                            data['error_message'] = 'Error in EMI Update!'
                            logger.error("Error in emircv_model_insert {} \nType: {} \nError:{}".format(
                                sys.exc_info()[-1], type(message).__name__, str(message)))
                            raise MyDatabaseError()

                    obj = form.save(commit=False)
                    obj.instrcv_inv_number = emi_reference_no
                    obj.branch_code = branch_code
                    obj.transaction_narration = old_narration + \
                        "Previous Amount " + str(old_receive_amount)
                    obj.save()
                    status, message, = fn_update_emibal_hist(
                        account_number, emi_reference_no, receive_date)
                    if not status:
                        data['error_message'] = 'Error in fn_update_emibal_hist!\n'+message
                        logger.error("Error in fn_update_emibal_hist {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(message).__name__, str(message)))
                        raise MyDatabaseError()
                    data['success_message'] = ''
                    data['error_message'] = ''
                    data['form_is_valid'] = True
            except Exception as e:
                data['form_is_valid'] = False
                if len(data['error_message']) > 0:
                    return JsonResponse(data)
                data['error_message'] = str(e)
                logger.error("Error in emircv_model_edit {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
    else:
        form = Emi_Receive_Model_Form(instance=instance_data)  # forms name
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


def sales_emircv_cancel(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    app_user_id = request.session["app_user_id"]
    data['error_message'] = ''
    data['form_is_valid'] = False

    if not fn_is_user_permition_exist(request.session["app_user_id"], 'S160092'):
        data['error_message'] = "You are not allowed to cancel this transaction!"
        data['form_is_valid'] = False
        return JsonResponse(data)

    try:
        with transaction.atomic():

            status, error_message = fn_cancel_emi_receive_transaction(
                id, app_user_id)
            if not status:
                data['error_message'] = error_message
                data['form_is_valid'] = False
                return JsonResponse(data)

            data['form_is_valid'] = True
            data['success_message'] = 'Cancel Successfully!'
            return JsonResponse(data)

    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        logger.error("Error on line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)


class sales_emihist_list(TemplateView):
    template_name = 'sales/sales-emihist-list.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = Emi_History_Query(initial={'from_date': cbd, 'upto_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


class sales_order_create_view(TemplateView):
    template_name = 'sales/sales-order-create.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        total_quantity, total_discount, total_price = get_product_cart_summary(
            app_user_id=request.session["app_user_id"])
        cbd = get_business_date(branch_code, app_user_id)
        try:
            edit_param = Application_Settings.objects.get()
        except Exception as e:
            print('Application Settings Not Define')
        type_code = edit_param.quick_payment_type

        if not edit_param.sales_executive_phone_editable:
            employee_id = fn_get_employee_by_app_user_id(app_user_id)
        else:
            employee_id = fn_get_employee_by_app_user_id(app_user_id)

        sales_master = OrderMasterModelForm(initial={'order_date': cbd, 'total_quantity': total_quantity, 'employee_id': employee_id,
                                                     'total_discount_amount': total_discount, 'bill_amount': total_price-total_discount,
                                                     'total_bill_amount': total_price, 'type_code': type_code, 'tran_type_code': type_code, })
        sales_details = SalesDetailsModelForm()

        context = get_global_data(request)
        context['sales_master'] = sales_master
        context['sales_details'] = sales_details
        return render(request, self.template_name, context)


def sales_clear_order_chart(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    Sales_Details_Temp.objects.filter(
        app_user_id=request.session["app_user_id"]).delete()
    data = {}
    data['success_message'] = "Save Successfully"
    return JsonResponse(data)


@transaction.atomic
def sales_post_order(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = OrderMasterModelForm(request.POST)
        if form.is_valid():
            try:

                order_date = form.cleaned_data["order_date"]
                customer_name = form.cleaned_data["customer_name"]
                customer_phone = form.cleaned_data["customer_phone"]
                customer_address = form.cleaned_data["customer_address"]
                employee_id = form.cleaned_data["employee_id"]
                total_quantity = form.cleaned_data["total_quantity"]
                total_bill_amount = form.cleaned_data["total_bill_amount"]
                bill_amount = form.cleaned_data["bill_amount"]
                pay_amount = form.cleaned_data["pay_amount"]
                #due_amount = form.cleaned_data["due_amount"]
                advance_pay = form.cleaned_data["advance_pay"]
                total_discount_rate = form.cleaned_data["total_discount_rate"]
                total_discount_amount = form.cleaned_data["total_discount_amount"]
                order_comments = form.cleaned_data["order_comments"]
                #delar_id = request.session["delar_id"]
                app_user_id = request.session["app_user_id"]
                latitude = form.cleaned_data["latitude"]
                longitude = form.cleaned_data["longitude"]
                account_number = form.cleaned_data["input_account_number"]
                branch_code = form.cleaned_data["branch_code"]
                center_code = form.cleaned_data["center_code"]
                delivary_date=form.cleaned_data["delivary_date"]

                if account_number is None:
                    data['error_message'] = 'Please Enter Client Phone Number!'
                    return JsonResponse(data)

                if order_date is None:
                    data['error_message'] = 'Please Enter Order Date!'
                    return JsonResponse(data)

                if delivary_date is None:
                    data['error_message'] = 'Please Enter Delivary Date!'
                    return JsonResponse(data)

                if pay_amount < 0:
                    data['error_message'] = 'Negative Amount Payment is Not Allowed!'
                    return JsonResponse(data)

                if account_number == get_general_account(app_user_id):
                    if ((bill_amount-pay_amount) < 0):
                        data['error_message'] = 'Please Register for Advance Payment!'
                        return JsonResponse(data)

                if account_number == get_general_account(app_user_id):
                    if bill_amount-pay_amount != 0:
                        data['error_message'] = 'Please Register Customer for Due Sales!'
                        return JsonResponse(data)

                if not fn_validate_chart_phone_mismatch(p_sales_account_number=account_number, p_app_user=app_user_id):
                    data['error_message'] = 'You have changed the customer phone number which may impact on product price.\nPlease clear your item and try again.'
                    return JsonResponse(data)

                total_quantity, total_discount, total_price = get_product_cart_summary(
                    app_user_id=request.session["app_user_id"])

                total_discount_amount = total_discount
                bill_amount = total_price-total_discount
                total_bill_amount = total_price
                # latitude=3.4
                # longitude=3.4
                due_amount = bill_amount-pay_amount

                if total_quantity == 0:
                    data['error_message'] = 'Noting to Submit.'
                    return JsonResponse(data)

                if account_number is None:
                    if ((bill_amount-pay_amount) < 0):
                        data['error_message'] = 'Please Register for Advance Payment!'
                        return JsonResponse(data)

            except Exception as e:
                data['error_message'] = str(e)
                data['form_is_valid'] = False
                return JsonResponse(data)
            try:
                with transaction.atomic():

                    order_number = fn_generate_order_number(branch_code)

                    _, _, _, _, customer_id, _, _, _, _, _ = fn_get_accountinfo_byacnumber(
                        account_number)

                    if account_number is None:
                        account_number = get_general_account(app_user_id)

                    cursor = connection.cursor()
                    cursor.callproc("fn_sales_order_post", [branch_code, center_code, app_user_id, order_number, customer_phone, customer_id, customer_name,
                                                            customer_address, account_number, employee_id, pay_amount, 'CS',
                                                            total_discount_rate, total_discount_amount, order_date,delivary_date, latitude, longitude])
                    row = cursor.fetchone()

                    if row[0] != 'S':
                        data['error_message'] = row[1]
                        raise Exception(row[1])

                    message = "Order Post Successfully with Order Number : " + order_number

                    data['success_message'] = message
                    data['form_is_valid'] = True

                    return JsonResponse(data)
            except Exception as e:
                data['error_message'] = str(e)
                data['form_is_valid'] = False
                logger.error("Error on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                return JsonResponse(data)
        else:
            data['error_message'] = form.errors.as_json()

        return JsonResponse(data)


class OrderListView(TemplateView):
    template_name = 'sales/sales-order-list.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = OrderSearchForm(initial={'from_date': cbd, 'upto_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def sales_order_details(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data=dict()
    order = Order_Master.objects.get(pk=id)
    branch_code = order.branch_code
    order_number = order.order_number
   
    rows = Order_Details.objects.raw('''select s.id, p.product_name, p.product_id, s.quantity,s.ordered_quantity,
    s.delivered_quantity, s.product_price, 
    s.total_price, s.ordered_total_price, s.delivered_total_price,
    s.discount_rate,s.ordered_discount_rate, s.delivered_discount_rate,
    s.discount_amount,s.ordered_discount_amount,s.delivered_discount_amount,
    (s.total_price-s.discount_amount) as sales_amount
    from sales_order_details s INNER JOIN sales_products p 
    on s.product_id=p.product_id and order_number='''+"'"+order_number+"'"+" and s.branch_code='"+str(branch_code)+"'")

    context = get_global_data(request)
    context['data'] = rows
    return render(request, 'sales/sales-order-details.html', context)


@transaction.atomic
def sales_order_accept(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            
                
            order = Order_Master.objects.get(pk=id)
            order.status = 'A'
            order.save()
          
            message = "Order Accepted Successfully"
            
            data['success_message'] = message
            data['form_is_valid'] = True

            # data['form_is_valid'] = True
            # data['success_message'] = message
    except Exception as e:
        data['error_message'] = str(e)
    return JsonResponse(data)


@transaction.atomic
def sales_order_cancel(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    data['form_is_valid'] = False
    data['error_message'] = ''
    # try:
    #             row=Order_Details.objects.get(product_id=product_id)
    #             ordered_quantity=row.ordered_quantity
    #             quantity=row.quantity

    #             if ordered_quantity<quantity:
    #                data['error_message'] = 'delivared quantity is not available'
    #                return JsonResponse(data)
                
    # except exception as e:
    #      print(str(e))
    try:
        with transaction.atomic():
            app_user_id = request.session["app_user_id"]
            order = Order_Master.objects.get(pk=id)
            branch_code = order.branch_code
            order_number = order.order_number
            order.status = 'C'
            order.cancel_by = app_user_id
            order.cancel_on = timezone.now()
            order.save()

            Order_Details.objects.filter(branch_code=branch_code, order_number=order_number ).update(status='C',
                                                                                                    cancel_by=app_user_id, cancel_on=timezone.now())

            message = "Order Cancel Successfully"

            data['success_message'] = message
            data['form_is_valid'] = True

            data['form_is_valid'] = True
            data['success_message'] = message
    except Exception as e:
        data['error_message'] = str(e)
    return JsonResponse(data)


@transaction.atomic
def sales_order_details_update(request):
    data = dict()
    try:
        with transaction.atomic():
            data_string = request.POST.getlist('data_string')
            payment_amount = Decimal(request.POST.get('payment_amount', None))
            order_number = request.POST.get('order_number', None)

            if not payment_amount or payment_amount is None:
                payment_amount = 0

            if payment_amount < 0:
                raise Exception(
                    'Negative Amount in Payment Receive is Not allowed!')

            data_dict = json.loads(data_string[0])
            order = Order_Master.objects.get(order_number=order_number)

            if order.status == 'I':
                raise Exception('This Order Already Accepted!')
            if order.status == 'C':
                raise Exception('This Order Already Canceled!')

            for row in data_dict:
                try:
                    product_id = row['product_id']
                    order_number = row['order_number']
                    quantity = row['quantity']
                    unit_price = row['unit_price']
                    total_price = row['total_price']
                    discount_rate = row['discount_rate']
                    discount_amount = row['discount_amount']
                    sales_amount = row['sales_amount']

                    if len(product_id) > 0:
                        try:
                            print(quantity)
                            update_row = Order_Details.objects.get(
                                product_id=product_id, order_number=order_number)
                            update_row.quantity = quantity
                            update_row.product_price = unit_price
                            update_row.total_price = total_price
                            update_row.discount_rate = discount_rate
                            update_row.discount_amount = discount_amount
                            update_row.save()
                        except Order_Details.DoesNotExist:
                            pass
                except Exception as e:
                    data['error_message'] = str(e)
                    data['form_is_valid'] = False
                    return JsonResponse(data)

            branch_code = order.branch_code
            order_number = order.order_number
            account_number = order.account_number
            bill_amount = order.bill_amount
            app_user_id = request.session["app_user_id"]
            cbd = get_business_date(branch_code, app_user_id)
            employee_id = fn_get_employee_by_app_user_id(app_user_id)
            
            try:
                app_param = Application_Settings.objects.get()
            except Exception as e:
                print('Application Settings Not Define')

            tran_type_code = app_param.quick_payment_type
            tran_screen = 'SALES_ENTRY'

            credit_gl_code, debit_gl_code = fn_get_transaction_gl(
                p_transaction_screen=tran_screen, p_tran_type_code=tran_type_code)

            if credit_gl_code is None and debit_gl_code is None:
                data['error_message'] = 'Sales Configuration Ledger Not Exist!\nPlease Contact with your Admin.'
                return JsonResponse(data)

            invoice_number = fn_generate_invoice_number(branch_code)
            _, _, _, _, client_id, _, _, _, _, _ = fn_get_accountinfo_byacnumber(
                account_number)
            cursor = connection.cursor()
            cursor.callproc("fn_sales_order_accept", [branch_code, app_user_id, order_number, invoice_number, cbd, employee_id,
                                                      payment_amount, 0.00,  tran_type_code, credit_gl_code, debit_gl_code, order_number])
            row = cursor.fetchone()

            if row[0] != 'S':
                data['error_message'] = row[1]
                raise Exception(row[1])

            message = "Order Deliver Successfully with Invoice Number : " + invoice_number

            data['success_message'] = message
            data['form_is_valid'] = True
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        return JsonResponse(data)


def sales_choice_clientsproductlist(request):
    client_id = request.GET.get('client_id')
    product_id = request.GET.get('product_id')
    list_data = Sales_Details.objects.filter(client_id=client_id, product_id=product_id).values(
        'invoice_number', 'product_price', 'quantity', 'app_data_time').order_by('app_data_time')
    return render(request, 'sales/sales-choice-clientsproductlist.html', {'list_data': list_data})


def sales_choice_supplierlist(request):
    branch_code = request.GET.get('branch_code')
    list_data = Supplier_Information.objects.filter(is_active=True, is_deleted=False).values(
        'supp_id', 'supp_name', 'proprietor_name').order_by('supp_name')
    return render(request, 'sales/sales-choice-supplierlist.html', {'list_data': list_data})

def sales_choice_productgrouplist(request):
    list_data = Products_Group.objects.filter(is_active=True, is_deleted=False).values(
        'group_id', 'group_name').order_by('group_name')
    return render(request, 'sales/sales-choice-productgrouplist.html', {'list_data': list_data})


def sales_choice_productbrandlist(request):
    list_data = Products_Brand.objects.filter(is_active=True, is_deleted=False).values(
        'brand_id', 'brand_name').order_by('brand_name')
    return render(request, 'sales/sales-choice-productbrandlist.html', {'list_data': list_data})

class sales_clientid_change(TemplateView):
    template_name = 'sales/sales-clientid-change.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Client_Id_Changes_Form()
        args = {'form': form}
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

@transaction.atomic
def sales_clientid_change_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''
    if request.method == 'POST':
        form = Client_Id_Changes_Form(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    client_id = form.cleaned_data['client_id']
                    new_client_id = form.cleaned_data['new_client_id']
                    if not client_id or not new_client_id:
                        data['form_is_valid'] = False
                        data['error_message'] = 'Invalid Transfer Data!'
                        return JsonResponse(data)
                    cursor = connection.cursor()
                    cursor.callproc("fn_sales_change_client_id", [
                                    client_id, new_client_id])
                    row = cursor.fetchone()

                    if row[0] != 'S':
                        data['error_message'] = row[1]
                        
                        logger.error("Database Error in fn_sales_change_client_id {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
                        raise MyDatabaseError()
                        
                    data['form_is_valid'] = True
                    data['success_message'] = 'Client ID Change Successfully Completed!'

                    return JsonResponse(data)
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
    return JsonResponse(data)


class sales_clientclosing_view(TemplateView):
    template_name = 'sales/sales-client-closing.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        initial_dict = {'closing_date': cbd}
        form = Client_Closing_ModelForm(initial=initial_dict)
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def sales_clientclosing_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''
    if request.method == 'POST':
        form = Client_Closing_ModelForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    client_id = form.cleaned_data['client_id']
                    branch_code = form.cleaned_data['branch_code']
                    closing_date = form.cleaned_data['closing_date']
                    status, total_balance = fn_get_client_accounts_balance(
                        client_id)

                    if total_balance > 0:
                        data['form_is_valid'] = False
                        data['error_message'] = 'You can not close customer which has account balance outstanding '+str(
                            total_balance)
                        return JsonResponse(data)

                    status, message = fn_client_closing(
                        branch_code, client_id, closing_date)

                    if not status:
                        data['error_message'] = message
                        raise Exception(message)

                    app_user_id = request.session["app_user_id"]
                    post = form.save(commit=False)
                    post.app_user_id = app_user_id
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Client Closing Successfully Completed!'

                    return JsonResponse(data)
            except Exception as e:
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                logger.error("Error on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                return JsonResponse(data)
        else:
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    return JsonResponse(data)


@transaction.atomic
def sales_clientclosing_remove(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''
    if request.method == 'POST':
        form = Client_Closing_ModelForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    client_id = form.cleaned_data['client_id']
                    branch_code = form.cleaned_data['branch_code']
                    closing_date = form.cleaned_data['closing_date']
                    status, message, total_debit_amount, total_credit_amount = fn_get_client_accounts_debit_credit(
                        client_id)

                    if not status:
                        data['form_is_valid'] = False
                        data['error_message'] = message
                        return JsonResponse(data)

                    if total_debit_amount > 0 or total_credit_amount > 0 or not status:
                        data['form_is_valid'] = False
                        data['error_message'] = 'You can not remove this Customer!'
                        return JsonResponse(data)

                    status, message = fn_client_remove(
                        branch_code, client_id, closing_date)

                    if not status:
                        data['error_message'] = message
                        raise Exception(message)

                    app_user_id = request.session["app_user_id"]
                    post = form.save(commit=False)
                    post.app_user_id = app_user_id
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Client Remove Successfully Completed!'

                    return JsonResponse(data)
            except Exception as e:
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                logger.error("Error on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                return JsonResponse(data)
        else:
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    return JsonResponse(data)


#################################

class sales_purchase_order_view(TemplateView):
    template_name = 'sales/sales-purchase-order-master.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        context = get_global_data(request)

        try:
            app_settings = Application_Settings.objects.get()
        except Exception as e:
            print('Application Settings Not Define')

        barcode_enable = app_settings.barcode_enable
        total_quantity, total_price = fn_get_purchase_order_temp_summary(
            p_branch_code=branch_code, app_user_id=app_user_id)
        purchase_order_master = Purchase_Order_MstForm(
            initial={'purchase_date': cbd,'show_room': 1, 'total_pur_qnty': total_quantity, 'g_total_price': total_price})
        purchase_detail_temp = Purchase_Order_Dtl_TempForm()

        context['purchase_order_master'] = purchase_order_master
        context['is_barcode_enable'] = barcode_enable
        context['purchase_detail_temp'] = purchase_detail_temp
        return render(request, self.template_name, context)


def sales_purchase_order_details_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = {}
    data['form_is_valid'] = False
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form=Purchase_Order_Dtl_TempForm(request.POST)
              
                product_id = request.POST.get('product_id')
                # product_name = request.POST.get('product_name')
                pur_qnty = request.POST.get('pur_qnty')
                unit_price = request.POST.get('unit_price')
                total_price = request.POST.get('total_price')
                # product_model = request.POST.get('product_model')
                product_bar_code = request.POST.get('product_bar_code')
                discount_amount = request.POST.get('discount_amount')
                branch_code = request.POST.get('branch_code')
                app_user_id = request.session["app_user_id"]
                purchase_ord_no=fn_generate_purchase_order_no(branch_code)
                

                post = form.save(commit=False)
                post.app_user_id = app_user_id
                post.purchase_ord_no=purchase_ord_no
                post.save()
                if not branch_code or branch_code is None:
                    branch_code = request.session["branch_code"]

                if not product_id:
                    data['error_message'] = 'Please Select Valid Product!'
                    return JsonResponse(data)

                if product_bar_code and not product_id:
                    product_id = fn_get_product_id(product_bar_code)

                if product_id and not product_bar_code:
                    product_bar_code = fn_get_product_barcode(product_id)

                if not fn_valid_product_code(p_branch_code=branch_code, p_product_id=product_id):
                    data['error_message'] = 'Invalid Product!'
                    return JsonResponse(data)
                

                if int(pur_qnty) <= 0:
                    data['error_message'] = 'Quantity can not be Negative or Zero!'
                    return JsonResponse(data)

                _, product_name, product_model = fn_get_product_details(
                    product_id)

                branch_instance = get_object_or_404(
                    Branch, branch_code=branch_code)
                product_instance = get_object_or_404(
                    products, product_id=product_id)
                
                 

                if Purchase_Order_Dtl_Temp.objects.filter(product_id=product_id, branch_code=branch_code, app_user_id=app_user_id).exists():
                    prod_temp_update = Purchase_Order_Dtl_Temp.objects.get(
                        product_id=product_id, branch_code=branch_code, app_user_id=app_user_id)
                    prod_temp_update.pur_qnty = prod_temp_update.pur_qnty + \
                        int(pur_qnty)
                    prod_temp_update.total_price = prod_temp_update.total_price + \
                        Decimal(total_price)
                    prod_temp_update.unit_price = prod_temp_update.unit_price + \
                        Decimal(unit_price)
                    prod_temp_update.discount_amount = prod_temp_update.discount_amount + \
                        Decimal(discount_amount)
                    prod_temp_update.save()
                else:
                    temp_stock_submit = Purchase_Order_Dtl_Temp(product_id=product_instance,  
                                                         pur_qnty=pur_qnty,  branch_code=branch_code, total_price=total_price,
                                                         unit_price=unit_price,  app_user_id=app_user_id,discount_amount=discount_amount)
                    temp_stock_submit.save()

                total_quantity, total_price = fn_get_purchase_order_temp_summary(
                    p_branch_code=branch_code, app_user_id=app_user_id)
                
                data['form_is_valid'] = True
                data['total_quantity'] = total_quantity
                data['total_price'] = total_price

            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


def sales_delete_temp_prorder_data(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    Purchase_Order_Dtl_Temp.objects.filter(id=id).delete()
    app_user_id = request.session["app_user_id"]
    branch_code = request.session["branch_code"]
    total_quantity, total_price = fn_get_purchase_order_temp_summary(
        p_branch_code=branch_code, app_user_id=app_user_id)
    data['total_quantity'] = total_quantity
    data['total_price'] = total_price
    data['form_is_valid'] = True
    return JsonResponse(data)



@transaction.atomic
def sales_purchase_order_post(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Purchase_Order_MstForm(request.POST)
                if form.is_valid():
                    purchase_date = form.cleaned_data["purchase_date"]
                    show_room = 1
                    comments = form.cleaned_data["comments"]
                    voucher_number = form.cleaned_data["voucher_number"]
                    total_quantity = form.cleaned_data["total_pur_qnty"]
                    branch_code = form.cleaned_data["branch_code"]
                    app_user_id = request.session["app_user_id"]
                    supplier_id = '0'
                    

                    if not branch_code or branch_code is None:
                        data['error_message'] = 'Please select Branch Name!'
                        return JsonResponse(data)

                    if show_room:
                        pass
                    else:
                        data['error_message'] = 'Please select Showroom!'
                        return JsonResponse(data)

                    order_summary = Purchase_Order_Dtl_Temp.objects.filter(
                        app_user_id=app_user_id).aggregate(Count('product_id'))
                    total_product = order_summary['product_id__count']
                    if total_product == 0:
                        data['error_message'] = 'Noting to Submit!'
                        return JsonResponse(data)

                    try:
                        with transaction.atomic():

                            cursor = connection.cursor()
                            cursor.callproc("fn_sales_purchase_submit", [
                                            purchase_date, branch_code, app_user_id, supplier_id, show_room, voucher_number, comments])
                            row = cursor.fetchone()

                            if row[0] != 'S':
                                data['error_message'] = row[1]
                                raise Exception(row[1])

                            message = "Save Successfully : purchase ID : " + \
                                row[2]

                            data['message'] = message
                            data['form_is_valid'] = True

                            return JsonResponse(data)
                    except Exception as e:
                        data['form_is_valid'] = False
                        if len(data['error_message']) == 0:
                            data['error_message'] = str(e)
                        logger.error("Error on line {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(e).__name__, str(e)))
                        return JsonResponse(data)
                else:
                    data['error_message'] = form.errors.as_json()
                    data['form_is_valid'] = False
                    return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


class sales_purchase_order_approval(TemplateView):
    template_name = 'sales/sales-purchase-order-approval.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        context = get_global_data(request)
        return render(request, self.template_name, context)


@transaction.atomic
def sales_purchase_order_payment(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    product = get_object_or_404(PurchaseMasterAuthQ, id=id)
    template_name = 'sales/sales-purchase-order-payment.html'
    context = {}
    data = dict()

    if request.method == 'POST':
        form = PurchaseMasterAuthQ(request.POST, instance=product)
        data = dict()
        data['form_is_valid'] = False
        data['message'] = ''
        if form.is_valid():

            purchase_date = form.cleaned_data["purchase_date"]
            voucher_number = form.cleaned_data["voucher_number"]
            account_number = form.cleaned_data["account_number"]
            purchase_type = form.cleaned_data["purchase_type"]
            payment_comments = form.cleaned_data["payment_comments"]
            total_pay = form.cleaned_data["total_pay"]
            purchase_ord_no = form.cleaned_data["purchase_ord_no"]
            branch_code = form.cleaned_data["branch_code"]
            due_amount = form.cleaned_data["due_amount"]
            discount_amount = form.cleaned_data["discount_amount"]
            g_total_price = form.cleaned_data["g_total_price"]
            total_price_after_disc = g_total_price-discount_amount
            app_user_id = request.session["app_user_id"]

            cbd = purchase_date

            if not fn_val_account_number(account_number):
                data['error_message'] = 'Please Select Valid Supplier!'
                return JsonResponse(data)

            _, _, _, _, client_id, _, _, _, _, _ = fn_get_accountinfo_byacnumber(
                account_number)

            try:
                if cbd != purchase_date:
                    payment_comments = payment_comments + \
                        " Purchase Date : "+str(purchase_date)
            except Exception as e:
                pass

            tran_screen = 'STOCK_PAYMENT'

            credit_gl_code, debit_gl_code = fn_get_transaction_gl(
                p_transaction_screen=tran_screen, p_tran_type_code=purchase_type)

            if credit_gl_code is None and total_pay > 0:
                data['error_message'] = 'Ledger Configuration Not Exist.'
                return JsonResponse(data)

            if not account_number:
                account_number = get_general_account(app_user_id)

            try:
                with transaction.atomic():

                    cursor = connection.cursor()
                    cursor.callproc("fn_sales_stock_authorization", [branch_code, app_user_id, client_id, account_number, total_price_after_disc,
                                                                     total_pay, discount_amount, credit_gl_code, 'STOCK',
                                                                     cbd, purchase_ord_no, 'A', voucher_number, payment_comments])
                    row = cursor.fetchone()

                    if row[0] != 'S':
                        data['error_message'] = row[1]
                        logger.error("Database Error in fn_sales_stock_authorization {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
                        raise Exception(row[1])

                    data['form_is_valid'] = True
                    return JsonResponse(data)
            except Exception as e:
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                logger.error("Error on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(e).__name__, str(e)))
                return JsonResponse(data)
        else:
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:

        rows = PurchaseMasterAuthQ.objects.raw('''SELECT p.product_id,
        s.id, d.id, p.product_name || ' (' || p.product_model || ' )' product_name,
        p.product_id, d.total_pur_qnty, d.unit_price, d.g_total_price, d.discount_amount, 
        (d.g_total_price-d.discount_amount) price_after_discount
        FROM sales_PurchaseMasterAuthQ s, sales_Purchase_Order_Dtl d, sales_products p
        WHERE s.purchase_ord_no = d.purchase_ord_no AND p.product_id = d.product_id and s.id='''+"'"+str(id)+"'")

        form = PurchaseMasterAuthQ(instance=product)
        context['form'] = form
        context['id'] = id
        context['dtl_data'] = rows
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


def sales_purchase_order_reject(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    stock = PurchaseMasterAuthQ.objects.get(pk=id)
    stock_detail = Purchase_Order_Dtl.objects.filter(
        purchase_ord_no=stock.purchase_ord_no).update(status='J')
    stock.status = 'J'
    stock.save()
    response_data = {}
    response_data['success_message'] = "Save Successfully"
    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


####################
class sales_branch_transfer_view(TemplateView):
    template_name = 'sales/sales-branch-transfer.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Stock_quantity_transferFrom()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

@transaction.atomic
def sales_branch_transfer_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method=='POST':
        form=Stock_quantity_transferFrom(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post=form.save(commit=False)
                    post.app_user_id=app_user_id
                    post.save()
                    data['form_is_valid']=True
                    data['success_message']=" successfull"
                    data['error_message']=''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

def sales_branch_transfer_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    

    instance_data = get_object_or_404(Stock_quantity_transfer,id=id)
    template_name = 'sales/sales-branch-transfer-edit.html'
    data = dict()

    if request.method == 'POST':
        form = Stock_quantity_transferFrom(request.POST, instance=instance_data)
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
        form = Stock_quantity_transferFrom (instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


##############

class sales_invoice_return_allocate_list(TemplateView):
    template_name = 'sales/sales-invoice-return-allocate-list.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        branch_code = request.session["branch_code"]
        app_user_id = request.session["app_user_id"]
        cbd = get_business_date(branch_code, app_user_id)
        invoice_search = InvoiceSearch(
            initial={'invoice_from_date': cbd, 'invoice_upto_date': cbd})
        context = get_global_data(request)
        context['form'] = invoice_search
        return render(request, self.template_name, context)


def sales_invoice_return_allocate_details(request):
    data = dict()
    data['error_message'] = ""
    data['form_is_valid'] = False
    try:
        product_id = request.GET.get('product_id')
        branch_code = request.GET.get('branch_code')
        invoice_from_date = request.GET.get('invoice_from_date')
        invoice_upto_date = request.GET.get('invoice_upto_date')
        employee_id = request.GET.get('employee_id')
        
            
        sql = '''SELECT e.employee_id,
            e.employee_name,
            s.product_id,
            product_name || '(' || product_model || ')' product_name,
            s.branch_code,
            s.product_total_stock,
            s.product_total_sales,
            s.total_stock_return,
            s.product_available_stock
        FROM delar_srstage_inventory_status s,
            sales_products p,
            appauth_employees e
        WHERE     p.product_id = s.product_id
            AND s.employee_id = e.employee_id
            AND s.product_available_stock <> 0 '''

        if product_id:
            sql = sql+" AND p.product_id ='"+product_id+"'"

        if employee_id:
            sql = sql+" AND e.employee_id ='"+employee_id+"'"

        if branch_code:
            sql = sql+" AND s.branch_code ="+branch_code
        

        # if invoice_from_date and invoice_upto_date:
        #            sql=sql+' and  s.last_stock_return_date between '+"'" +str(invoice_from_date)+"'"+" and "+"'" +str(invoice_upto_date)+"'"
       
        print('sql',sql)
        data['data'] = fn_get_query_result(sql)
        return JsonResponse(data)
    except Exception as e:
        print('exception',e)
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        return JsonResponse(data)

@transaction.atomic
def sales_invoice_allocate_details_return(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    data['form_is_valid'] = False
    data['error_message'] = ''
    

    branch_code = request.session["branch_code"]
    app_user_id = request.session["app_user_id"]
    product_id=request.POST.get('product_id')
    employee_id=request.POST.get('employee_id')
    product_total_stock=request.POST.get('product_total_stock')
    product_total_sales=request.POST.get('product_total_sales')
    total_stock_return=request.POST.get('total_stock_return')
    product_available_stock=request.POST.get('product_available_stock')
    cbd = get_business_date(branch_code, app_user_id)
    try:
        with transaction.atomic():
            cursor = connection.cursor()
            cursor.callproc('fn_delar_srproducts_return', [branch_code, app_user_id,cbd, product_id,product_available_stock,'0','SR Return',cbd,employee_id ])
            row = cursor.fetchone()

            if row[0] != 'S':
                logger.error("Database Error in fn_delar_srproducts_return on line {} \nType: {} \nError:{}".format(
                    sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
                data['error_message'] = row[1]
                data['form_is_valid'] = False
                raise Exception(row[1])

            data['form_is_valid'] = True
            data['success_message'] = "Return Successfully"
            return JsonResponse(data)

    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        logger.error("Error on fn_sales_stock_return line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return JsonResponse(data)

@transaction.atomic
def sales_product_barcode(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data=dict()
    app_user_id=request.session['app_user_id']
    if request.method=='POST':
        product_info=request.POST.getlist('product[]')
        try:
            with transaction.atomic():
                barcode_class=barcode.get_barcode_class('code128')
                Sales_barcode.objects.update(print_qty=0)
                for p in product_info:
                    pd=json.loads(p)
                    product=products.objects.filter(product_id=pd['product_id']).first()
                    if not product.product_bar_code:
                        product.product_bar_code = pd['product_id']
                        product.save()
                    bar_code=barcode_class(product.product_bar_code,writer=ImageWriter())
                    buffer=BytesIO()
                    bar_code.write(buffer)

                    check=Sales_barcode.objects.filter(product_id=product.product_id).first()
                    if check:
                        if os.path.exists(check.barcode_image.url[1:]):
                            os.remove(check.barcode_image.url[1:])
                        else:
                            print("The file does not exist")
                        check.barcode_image.save(product.product_id+".png",File(buffer),save=False)
                        check.print_qty=pd['qty']
                        check.save()
                    else:
                        code=Sales_barcode()
                        code.product_id=product
                        code.print_qty=pd['qty']
                        code.barcode_image.save(product.product_id+".png",File(buffer),save=False)
                        code.save()
                data['success_message']='Barcode Generated'
                return JsonResponse(data)

        except Exception as e:
            data['error_message']=str(e)
            return JsonResponse(data)
    else:
        template_name="sales/sales-product-barcode.html"
        form = Products_Search_Forms()
        Products=products.objects.filter(is_active=True)
        context = get_global_data(request)
        context['form'] = form
        context['Products'] = Products
        return render(request, template_name, context)

# def sales_product_barcode_html(request):
#     template_name="sales/sales-product-barcode-html.html"
#     data=dict()
#     barcode_list=Sales_barcode.objects.filter(print_qty__gte=0)
#     data['barcode_list']=barcode_list
#     return render(request, template_name, data)

def sales_product_barcode_pdf_gen(request):
    data=dict()
    barcode_list=list(Sales_barcode.objects.filter(~Q(print_qty=0),print_qty__gte=0).values())
    data['barcode_list']=barcode_list
    return JsonResponse(data)

# def sales_product_barcode_pdf(request):
#     if not request.user.is_authenticated:
#         return render(request,'appauth/appauth-login.html')
#     options = {
#             'page-size': 'A4',
#             'margin-top': '0.25in',
#             'margin-right': '0.25in',
#             'margin-bottom': '0.25in',
#             'margin-left': '0.25in',
#             'encoding': "UTF-8",
#         }
#     pdfkit.from_url(request.build_absolute_uri('/')+'sales-products-barcode-html', 'media/barcode/pdf/'+str(request.session["app_user_id"])+'_barcode.pdf',options=options)
#     file_name = str(timezone.now())+"_barcode.pdf" #get the filename
#     path_to_file ='media/barcode/pdf/'+str(request.session["app_user_id"])+'_barcode.pdf' #get the path of desired excel file
#     path = open(path_to_file, 'rb')
#     mime_type, _ = mimetypes.guess_type(path_to_file)
#     response = HttpResponse(path,content_type=mime_type)
#     response['Content-Disposition'] = 'attachment; filename=%s' % file_name
#     return response


##### product unit  #########
class sales_productunit_view(TemplateView):
    template_name = 'sales/sales-productunit-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Products_Unit_Form()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def sales_productunit_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Products_Unit_Form(request.POST)
                if form.is_valid():
                    try:
                        with transaction.atomic():
                            app_user_id = request.session["app_user_id"]
                            branch_code = request.session["branch_code"]
                            unit_name = form.cleaned_data['unit_name']

                            # if fn_val_check_product_unit_exist(unit_name):
                            #     data['error_message'] = 'This Unit Name Already Exist!'
                            #     data['form_is_valid'] = False
                            #     return JsonResponse(data)

                            unit_id = fn_generate_product_unit_id(
                                branch_code)
                            post = form.save(commit=False)
                            post.app_user_id = app_user_id
                            post.unit_id = unit_id
                            post.is_active = True
                            post.is_deleted = False
                            post.save()
                            data['success_message'] = 'Unit Added Successfully!'
                            data['form_is_valid'] = True
                            return JsonResponse(data)
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
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


def sales_productunit_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    context = {}
    try:
        with transaction.atomic():
            instance_data = get_object_or_404(
                Products_Unit, unit_id=id)
            unit_id = instance_data.unit_id
            template_name = 'sales/sales-productunit-edit.html'
            context = {}
            data = dict()

            if request.method == 'POST':
                form = Products_Unit_Form(
                    request.POST, instance=instance_data)  # forms name
                data['form_error'] = form.errors.as_json()
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.unit_id = unit_id
                    obj.save()
                    context = get_global_data(request)
                    context['success_message'] = ''
                    context['error_message'] = ''
                    data['form_is_valid'] = True
                else:
                    data['form_is_valid'] = False
            else:
                form = Products_Unit_Form(
                    instance=instance_data)  # forms name
                context = get_global_data(request)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)



############ quotion ##############
class sales_quation_master_view(TemplateView):
    template_name = 'sales/sales_quationmastre-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        context = get_global_data(request)
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        form_details = Quotation_Details_Form(initial={'quotation_date':cbd})
        form_master = Quotation_Master_Form(initial={'quotation_date': cbd, 'edd_date': cbd})
        context['form_master'] = form_master
        context['form_details'] = form_details
        return render(request, self.template_name, context)


@transaction.atomic
def sales_quation_master_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ""

    try:
        if request.method == 'POST':
            form = Quotation_Master_Form(request.POST)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        app_user_id = request.session["app_user_id"]
                        branch_code=request.session["branch_code"]
                        vat_condition = form.cleaned_data["vat_condition"]
                        supplier_id = form.cleaned_data["supplier_id"]
                        quotation_validity = form.cleaned_data["quotation_validity"]
                        edd_date = form.cleaned_data["edd_date"]
                        warranty=form.cleaned_data['warranty']
                        subject=form.cleaned_data['subject']
                        remarks=form.cleaned_data['remarks']
                        quotation_id=request.POST['quotation_id']
                        print(quotation_id)
                        product_id=request.POST['product_id']
                        print(product_id)
                       
                        post = form.save(commit=False)
                        post.vat_condition = vat_condition
                        post.quotation_id=quotation_id
                        post.product_id=product_id
                        post.branch_code = branch_code
                        post.quotation_validity = quotation_validity
                        post.remarks = remarks
                        post.supplier_id = supplier_id
                        post.app_user_id = app_user_id
                        post.subject=subject
                        post.warranty = warranty
                        post.save()
                        message = "quation Added Successfully!"
                        data['success_message'] = message
                        data['form_is_valid'] = True

                        return JsonResponse(data)
                except Exception as e:
                    data['form_is_valid'] = False
                    if len(data['error_message']) > 0:
                        return JsonResponse(data)
                    data['error_message'] = str(e)
                    logger.error("Error on line {} \nType: {} \nError:{}".format(
                        sys.exc_info()[-1], type(e).__name__, str(e)))
                    return JsonResponse(data)
            else:
                data['error_message'] = form.errors.as_json()
                return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def sales_quation_dtl_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Quotation_Details_Form(request.POST)
                if form.is_valid():
                    app_user_id = request.session["app_user_id"]
                    branch_code=request.session["branch_code"]
                    unit = form.cleaned_data["unit"]
                    quantity = form.cleaned_data["quantity"]
                    unit_price = form.cleaned_data["unit_price"]
                    total_price = form.cleaned_data["total_price"]
                    product_id = form.cleaned_data["product_id"]
                    quotation_id=fn_get_quation_id1(branch_code)
                    
                    post = form.save(commit=False)
                    post.app_user_id = app_user_id
                    post.unit = unit
                    post.quotation_id=quotation_id
                    post.unit_price = unit_price
                    post.save()
                    data['product_id'] = product_id
                    data['quotation_id'] = quotation_id
                    data['form_is_valid'] = True
                    data['success_message'] = 'Save Susscessfuly!'
                    return JsonResponse(data)
                else:
                    data['error_message'] = form.errors.as_json()
                    return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)
class sales_sales_pos_view(TemplateView):
    template_name = 'sales/sales-sales-pos.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        total_quantity, total_discount, total_price = get_product_cart_summary(
            app_user_id=request.session["app_user_id"])
        cbd = get_business_date(branch_code, app_user_id)

        try:
            edit_param = Application_Settings.objects.get()
        except Exception as e:
            print('Application Settings Not Define')

        if not edit_param.sales_executive_maintain:
            employee_id = fn_get_employee_by_app_user_id(app_user_id)
        else:
            employee_id = fn_get_employee_by_app_user_id(app_user_id)

        sales_master = SalesMasterModelForm(initial={'invoice_date': cbd, 'total_quantity': total_quantity, 'employee_id': employee_id,
                                                     'total_discount_amount': total_discount, 'bill_amount': total_price-total_discount, 'total_bill_amount': total_price,
                                                     'invoice_discount': ''})
        context = get_global_data(request)
        group_of_product = Products_Group.objects.values(
            "group_id", "group_name")
        print(group_of_product)
        context["group_of_product"] = group_of_product
        context['sales_master'] = sales_master

        return render(request, self.template_name, context)


def sales_pos_productslist_bygroup(request, id=0):
    context = {}
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    list_products = products.objects.values(
        "product_id", "product_name").filter(product_group=id)
    print(list_products)
    context["list_products"] = list(list_products)
    return JsonResponse(context)


def sales_pos_temp_update(request, id=0):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    update_product = False
    data['error_message'] = 'Invalid Input Data!'

    try:
        with transaction.atomic():
            quantity = request.GET.get("quantity")
            if(id == 0):
                sales_details = list(
                    Sales_Details_Temp.objects.filter().values())
                data["sales_details"] = sales_details
                data['form_is_valid'] = True
                data['error_message'] = ''
                return JsonResponse(data)
            else:
                product = products.objects.get(product_id=id)
                product_id = product.product_id
                product_bar_code = product.product_bar_code
                app_user_id = request.session["app_user_id"]
                branch_code = request.session["branch_code"]
                product_name = product.product_name
                product_price = product.product_sales_price
                product_model = product.product_model
                discount_rate = product.sales_discount_percent
                if Sales_Details_Temp.objects.filter(product_id=id).exists():
                    row = Sales_Details_Temp.objects.get(product_id=id)
                    if (quantity):
                        row.quantity = quantity
                    else:
                        row.quantity = row.quantity+1
                    row.save()
                else:
                    record = Sales_Details_Temp(product_id=product_id,
                                                product_bar_code=product_bar_code,
                                                app_user_id=app_user_id,
                                                details_branch_code=branch_code,
                                                product_name=product_name,
                                                product_price=product_price,
                                                product_model=product_model,
                                                discount_rate=discount_rate,
                                                quantity=1,
                                                total_price=float(
                                                    1*product_price)
                                                )
                    record.save()
                row2 = Sales_Details_Temp.objects.get(product_id=id)
                total_quantity = row2.quantity
                row2.total_price = float(total_quantity*product_price)
                row2.save()
                sales_details = list(
                    Sales_Details_Temp.objects.filter().values().order_by('id'))
                data["sales_details"] = sales_details
                data['form_is_valid'] = True
                data['error_message'] = ''
                return JsonResponse(data)

    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        return JsonResponse(data)

