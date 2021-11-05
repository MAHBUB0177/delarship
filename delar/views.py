from sales.models import *
from sales.forms import InvoiceSearch
from sales.utils import fn_get_product_id, fn_get_product_barcode, get_product_offer, add_free_product_to_list, fn_get_product_price
from appauth.utils import fn_get_query_result
from finance.utils import fn_get_account_ledger
from appauth.globalparam import fn_is_user_permition_exist
from finance.utils import fn_get_accountinfo_bytran, fn_get_cash_gl_code, fn_cash_tran_posting, fn_transfer_tran_posting, fn_cancel_tran_batch
from finance.validations import fn_val_account_number
from finance.utils import fn_open_account_transaction_screen, fn_get_transaction_account_type, fn_get_account_info_byactype, fn_create_account, fn_get_accountinfo_byacnumber, fn_get_transaction_gl
from appauth.views import get_global_data, fn_get_employee_by_app_user_id
from .forms import *
from .models import *
from .validations import *
from .utils import *
import math
from django.utils import timezone
import time
from datetime import date, datetime, timedelta
from decimal import Decimal
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import FieldDoesNotExist
from django.core import serializers
from random import randint

from sales.models import products
from appauth.models import Employees
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


def delar_choice_centerlist(request):
    branch_code = request.GET.get('branch_code')
    list_data = Center.objects.filter(center_closure_date__isnull=True).values(
        'center_code', 'center_name', 'branch_center_code').order_by('center_name')
    if branch_code:
        list_data = list_data.filter(branch_code=branch_code)
    return render(request, 'delar/delar-choice-centerlist.html', {'list_data': list_data})


class delar_center_view(TemplateView):
    template_name = 'delar/delar-center-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = Center_Model_Form(initial={'center_open_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def delar_center_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Center_Model_Form(request.POST)
                if form.is_valid():
                    branch_code = form.cleaned_data["branch_code"]
                    center_code = fn_get_center_id(branch_code)
                    branch_center_code = fn_get_branch_center_id(branch_code)
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.center_code = center_code
                    post.branch_center_code = branch_center_code
                    post.center_status = 'A'
                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = 'Region Opened Successfully.'
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        return JsonResponse(data)


def delar_center_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Center, center_code=id)
    branch_code = instance_data.branch_code
    center_code = instance_data.center_code
    template_name = 'delar/delar-center-edit.html'
    context = {}
    data = dict()

    if request.method == 'POST':
        form = Center_Model_Form(
            request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():

            obj = form.save(commit=False)
            obj.branch_code = branch_code
            obj.center_code = center_code
            obj.save()
            context = get_global_data(request)
            context['success_message'] = ''
            context['error_message'] = ''
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = Center_Model_Form(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


class delar_clientcenter_transfer(TemplateView):
    template_name = 'delar/delar-clientcenter-transfer.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = ClientCenterTransfer()
        args = {'form': form}
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def delar_clientcenter_transfer_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''
    if request.method == 'POST':
        form = ClientCenterTransfer(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    client_id = form.cleaned_data['client_id']
                    new_center_code = form.cleaned_data['new_center_code']
                    if not client_id or not new_center_code:
                        data['form_is_valid'] = False
                        data['error_message'] = 'Invalid Transfer Data!'
                        return JsonResponse(data)
                    cursor = connection.cursor()
                    cursor.callproc("fn_delar_client_center_transfer", [
                                    client_id, new_center_code])
                    row = cursor.fetchone()

                    if row[0] != 'S':
                        data['error_message'] = row[1]
                        logger.error("Database Error in fn_delar_client_center_transfer {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
                        raise Exception(row[1])

                    data['form_is_valid'] = True
                    data['success_message'] = 'Client Transfer Successfully Completed!'

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


class delar_sales_create_view(TemplateView):
    template_name = 'delar/delar-sales-create.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        total_quantity, total_discount, total_price = get_product_cart_summary(
            app_user_id=request.session["app_user_id"])
        print(total_quantity)
        cbd = get_business_date(branch_code, app_user_id)

        sales_master = SalesMasterModelForm(initial={'invoice_date': cbd, 'total_quantity': total_quantity, 'total_discount_amount': total_discount,
                                                     'bill_amount': total_price-total_discount, 'total_bill_amount': total_price, 'invoice_discount': ''})
        sales_details = SalesDetailsModelForm()

        context = get_global_data(request)
        context['sales_master'] = sales_master
        context['sales_details'] = sales_details
        return render(request, self.template_name, context)


@transaction.atomic
def delar_details_entry(request):
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
                    client_id = ''

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

                    if product_id is None or len(product_id) == 0:
                        data['error_message'] = 'Invalid Product!'
                        return JsonResponse(data)

                    if product_name:
                        pass
                    else:
                        data['error_message'] = 'Invalid Product!'
                        return JsonResponse(data)

                    if Srstage_Details_Temp.objects.filter(product_id=product_id, app_user_id=app_user_id).exists():
                        prod_temp = Srstage_Details_Temp.objects.get(
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


def delar_details_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Srstage_Details_Temp, id=id)
    template_name = 'delar/delar-sales-edit.html'
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


def delar_details_delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    Srstage_Details_Temp.objects.filter(id=id).delete()

    total_quantity, total_discount, total_price = get_product_cart_summary(
        app_user_id=request.session["app_user_id"])

    data['total_quantity'] = total_quantity
    data['total_discount'] = total_discount
    data['total_price'] = total_price

    data['form_is_valid'] = True
    return JsonResponse(data)


def delar_details_clear(request):
    if not request.user.is_authenticated:
        return render(request, 'sales/appauth-appauth.html')
    Srstage_Details_Temp.objects.filter(
        app_user_id=request.session["app_user_id"]).delete()
    data = {}
    data['success_message'] = "Save Successfully"
    return JsonResponse(data)


@transaction.atomic
def delar_post_sales(request):
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
                employee_id = form.cleaned_data["employee_id"]
                branch_code = form.cleaned_data["branch_code"]
                app_user_id = request.session["app_user_id"]

                if invoice_date is None:
                    data['error_message'] = 'Please Enter Invoice Date!'
                    return JsonResponse(data)

                if employee_id is None or not employee_id:
                    data['error_message'] = 'Please Select Sales Representative!'
                    return JsonResponse(data)

                if branch_code is None or not branch_code:
                    data['error_message'] = 'Please Select Branch!'
                    return JsonResponse(data)

            except Exception as e:
                data['error_message'] = str(e)
                data['form_is_valid'] = False
                return JsonResponse(data)
            try:
                with transaction.atomic():
                    #invoice_number = fn_generate_srsales_number(branch_code)
                    cursor = connection.cursor()
                    cursor.callproc("fn_delar_srstage_post", [
                                    branch_code, invoice_date, employee_id, app_user_id])
                    row = cursor.fetchone()

                    if row[0] != 'S':
                        data['error_message'] = row[1]
                        raise Exception(row[1])

                    message = "Product Assignment Successfully!"

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


def delar_product_price(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    try:
        app_user_id = request.session["app_user_id"]
        product_code = request.GET.get('product_id')
        account_number = request.GET.get('account_number')
        branch_code = request.GET.get('branch_code')
        tran_type_code = request.GET.get('tran_type_code')

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


class delar_invoice_list(TemplateView):
    template_name = 'delar/delar-invoice-list.html'

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


def delar_invoice_details(request, id=0):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    batch_number = request.GET.get('batch_number')
    transaction_date = request.GET.get('transaction_date')
    branch_code = request.GET.get('branch_code')
    rows = Srstage_Master.objects.raw('''SELECT p.product_id,
       s.id,
       d.id,
       p.product_name || ' (' || p.product_model || ' )' product_name,
       d.quantity,
       d.return_quantity,
       d.product_price,
       d.total_price,
       d.discount_amount,
       (d.total_price - d.discount_amount) price_after_discount
  FROM delar_srstage_master s, delar_srstage_details d, sales_products p
 WHERE     s.invoice_number = d.invoice_number
       AND p.product_id = d.product_id
       AND s.id ='''+"'"+str(id)+"'")

    context = get_global_data(request)
    context['data'] = rows
    return render(request, 'delar/delar-invoice-details.html', context)


@transaction.atomic
def delar_invoice_cancel(request, id):
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


################ sales return packet ############
class delar_sales_return_packet_view(TemplateView):
    template_name = 'delar/delar-sales-return-packet.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = Sales_Return_PacketForm(initial={'return_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def delar_sales_return_packet_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = Sales_Return_PacketForm(request.POST)
                if form.is_valid():
                    branch_code = form.cleaned_data["branch_code"]
                    return_invoice = fn_get_return_invoice(branch_code)
                    post = form.save(commit=False)
                    post.app_user_id = request.session["app_user_id"]
                    post.return_invoice = return_invoice

                    post.save()
                    data['form_is_valid'] = True
                    data['success_message'] = ' packet return Successfully.'
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['form_is_valid'] = False
        data['error_message'] = str(e)
        return JsonResponse(data)


def delar_sales_packet_return_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Sales_Return_Packet, id=id)
    branch_code = instance_data.branch_code
    return_invoice = instance_data.return_invoice
    template_name = 'delar/delar-sales-return-packet-edit.html'
    context = {}
    data = dict()

    if request.method == 'POST':
        form = Sales_Return_PacketForm(
            request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():

            obj = form.save(commit=False)
            obj.branch_code = branch_code
            obj.return_invoice = return_invoice
            quantity = obj.receive_quantity
            row = products.objects.get(product_id=obj.product_id)
            product_price = row.product_purces_price
            total_price = product_price*quantity
            instance_data.receive_value = total_price
            instance_data.save()
            # obj.receive_value = total_price
            # # obj.save()

            obj.save()
            context = get_global_data(request)
            context['success_message'] = 'UPDATE SUCCESSFULLY'
            context['error_message'] = ''
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = Sales_Return_PacketForm(instance=instance_data)
        clients = Clients.objects.all()
        product = products.objects.all()
        employee = Employees.objects.all()
        print(instance_data.client_id)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['employee'] = employee
        context['data'] = instance_data
        context['clients'] = clients
        context['product'] = product
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)


####### invoice###########
class delar_packet_return_invoice_list(TemplateView):
    template_name = 'delar/delar-return-invoice-list.html'

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


def delar_invoice_return_details(request, id=0):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    batch_number = request.GET.get('batch_number')
    transaction_date = request.GET.get('transaction_date')
    branch_code = request.GET.get('branch_code')
    rows = Sales_Return_Packet.objects.raw('''SELECT p.product_id,
       d.id,
       p.product_name || ' (' || p.product_model || ' )' product_name,
       d.receive_quantity,
       d.receive_value
  FROM  delar_sales_return_packet d, sales_products p
 WHERE  p.product_id = d.product_id and d.id = '''+str(id)+'''
 ''')
    print(rows)

    context = get_global_data(request)
    context['data'] = rows
    return render(request, 'delar/delar-invoice-return-details.html', context)


@transaction.atomic
def delar_invoice_return_cancel(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    data['form_is_valid'] = False
    data['error_message'] = ''
    sales = Sales_Return_Packet.objects.get(pk=id)
    invoice_number = sales.return_invoice

    branch_code = sales.branch_code
    app_user_id = request.session["app_user_id"]

    try:
        with transaction.atomic():
            cursor = connection.cursor()
            cursor.callproc("fn_sales_sales_cancel", [
                            branch_code, app_user_id, invoice_number, 'Cancel Invoice'])
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



###################### sr target #################

class delar_sales_sr(TemplateView):
    template_name = 'delar/delar-sales-sr.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')

        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        form = SR_Target_Details_Form()
        form1 = SR_Target_master_Form(
            initial={'target_from_date': cbd, 'target_to_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        context['form1'] = form1

        return render(request, self.template_name, context)



def sales_sr_purchase_details_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = {}
    data['form_is_valid'] = False
    try:
        with transaction.atomic():
            if request.method == 'POST':
                product_id = request.POST.get('product_id')
                               
                unit_id = request.POST.get('unit_id')
                total_quantity = request.POST.get('total_quantity')
                unit_price = request.POST.get('unit_price')
                total_price = request.POST.get('total_price')
                is_deleted = request.POST.get('is_deleted')
                branch_code = request.POST.get('branch_code')
                app_user_id = request.session["app_user_id"]
                transaction_id=fn_get_transaction_id(branch_code)


                if not branch_code or branch_code is None:
                    branch_code = request.session["branch_code"]

                if not product_id:
                    data['error_message'] = 'Please Select Valid Product!'
                    return JsonResponse(data)
                if not unit_id:
                    data['error_message']= " unit_id required "
                    return JsonResponse (data)

                if not fn_valid_product_code(p_branch_code=branch_code, p_product_id=product_id):
                    data['error_message'] = 'Invalid Product!'
                    return JsonResponse(data)

                if int(total_quantity) <= 0:
                    data['error_message'] = 'Quantity can not be Negative or Zero!'
                    return JsonResponse(data)
                branch_instance = get_object_or_404(
                    Branch, branch_code=branch_code)
                product_instance = get_object_or_404(
                    products, product_id=product_id)

                if SR_Target_Details_Temp.objects.filter(product_id=product_id, branch_code=branch_code, app_user_id=app_user_id).exists():
                    prod_temp_update = StockDetailsTemp.objects.get(
                        product_id=product_id, branch_code=branch_code, app_user_id=app_user_id)
                    prod_temp_update.quantity = prod_temp_update.total_quantity + \
                        int(total_quantity)
                    prod_temp_update.total_price = prod_temp_update.total_price + \
                        Decimal(total_price)
                    prod_temp_update.unit_price = prod_temp_update.unit_price + \
                        Decimal(unit_price)
                    
                    prod_temp_update.save()
                else:
                    temp_stock_submit = SR_Target_Details_Temp(product_id=product_id,  unit_id=unit_id,is_deleted=is_deleted,transaction_id=transaction_id,
                                                         total_quantity=total_quantity,  branch_code=branch_code, total_price=total_price,
                                                         unit_price=unit_price,  app_user_id=app_user_id)
                    temp_stock_submit.save()

                
                # try:
                #      with transaction.atomic():

                #             cursor = connection.cursor()
                #             cursor.callproc("fn_sales_target_submit", [
                #                              branch_code, app_user_id])
                #             row = cursor.fetchone()

                #             if row[0] != 'S':
                #                 data['error_message'] = row[1]
                #                 raise Exception(row[1])

                #             message = "Save Successfully : Stock ID : " + \
                #                 row[2]

                #             data['message'] = message
                #             data['form_is_valid'] = True

                #             return JsonResponse(data)
                # except Exception as e:
                #         data['form_is_valid'] = False
                #         if len(data['error_message']) == 0:
                #             data['error_message'] = str(e)
                #         logger.error("Error on line {} \nType: {} \nError:{}".format(
                #             sys.exc_info()[-1], type(e).__name__, str(e)))
                #         return JsonResponse(data)


                # details_row_list = []

                # dtl_data = SR_Target_Details_Temp.objects.filter(
                #         app_user_id=app_user_id)


                # for dtl_row in dtl_data:
                #         row = SR_Target_Details(branch_code=branch_code, transaction_id=dtl_row.transaction_id,
                #                            product_id=dtl_row.product_id, unit_id=dtl_row.unit_id,
                #                            total_quantity=dtl_row.total_quantity, unit_price=dtl_row.unit_price, 
                #                            total_price=dtl_row.total_price, is_deleted=dtl_row.is_deleted, app_user_id=app_user_id, app_data_time=timezone.now())
              
                #         row.save()


                # SR_Target_Details_Temp.objects.filter(
                #                 app_user_id=app_user_id).delete()

               
                data['form_is_valid'] = True
                
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)

def delar_delete_temp_stock_data(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    SR_Target_Details_Temp.objects.filter(id=id).delete()
    return JsonResponse(data)


@transaction.atomic
def delar_sr_target_post(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = SR_Target_master_Form(request.POST)
                if form.is_valid():
                    employee_id = form.cleaned_data["employee_id"]
                    target_from_date = form.cleaned_data["target_from_date"]
                    
                    comments = form.cleaned_data["comments"]
                    target_to_date = form.cleaned_data["target_to_date"]
                    branch_code = form.cleaned_data["branch_code"]
                    target_amount = form.cleaned_data["target_amount"]
                    target_type = form.cleaned_data["target_type"]
                    app_user_id = request.session["app_user_id"]
                    transaction_id=fn_get_transaction_id1(branch_code)
                    

                    if not branch_code or branch_code is None:
                        data['error_message'] = 'Please select Branch Name!'
                        return JsonResponse(data)


                    stock_summary = SR_Target_Details_Temp.objects.filter(
                        app_user_id=app_user_id).aggregate(Count('product_id'), Sum('total_quantity'), Sum('unit_price'),
                                                           Sum('total_price'))
                    total_product = stock_summary['product_id__count']
                    total_quantity = stock_summary['total_quantity__sum']
                    unit_price = stock_summary['unit_price__sum']
                    total_price = stock_summary['total_price__sum']
                    
                    

                    dtl_data = SR_Target_Details_Temp.objects.filter(
                        app_user_id=app_user_id)


                    for dtl_row in dtl_data:
                        row = SR_Target_Details(branch_code=branch_code, transaction_id=dtl_row.transaction_id,
                                           product_id=dtl_row.product_id, unit_id=dtl_row.unit_id,
                                           total_quantity=total_quantity, unit_price=unit_price, 
                                           total_price=total_price, is_deleted=dtl_row.is_deleted, app_user_id=app_user_id, app_data_time=timezone.now())
                   
                        row.save()
                    

                    
                    stock_auth = SR_Target(branch_code=branch_code, app_user_id=app_user_id,
                                                  employee_id=employee_id, target_from_date=target_from_date, target_to_date=target_to_date, transaction_id=transaction_id, 
                                                  comments=comments, target_amount=target_amount, target_type=target_type, )
                    stock_auth.save()

                    try:
                        with transaction.atomic():
                            message = "Save Successfully with Transaction ID : " + transaction_id

                            data['message'] = message
                            data['form_is_valid'] = True

                            SR_Target_Details_Temp.objects.filter(
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