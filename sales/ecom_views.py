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

from .utils import *
from .validations import *
from .myException import *
from .ecom_models import *
from .forms import *
from appauth.views import get_global_data, fn_get_employee_by_app_user_id
from finance.utils import fn_open_account_transaction_screen, fn_get_transaction_account_type, fn_get_account_info_byactype, fn_create_account, fn_get_accountinfo_byacnumber, fn_get_transaction_gl
from finance.validations import fn_val_account_number

class ecom_orderlist_view(TemplateView):
    template_name = 'sales/ecom-order-list.html'

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


def ecom_order_details(request, order_number):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    order = Ecom_Order_Master.objects.get(order_number=order_number)
    rows = Order_Details.objects.raw('''select o.id,p.id, o.order_number, p.product_name, p.product_id, o.order_quantity,
    o.product_price, o.total_price, o.discount_rate, o.discount_amount, (o.total_price-o.discount_amount) as sales_amount 
    from ecom_order_details o INNER JOIN ecom_products p 
    on o.product_id=p.product_id and order_number='''+"'"+order_number+"'")
    context = get_global_data(request)
    context['data'] = rows
    context['order'] = order
    return render(request, 'sales/ecom-order-details.html', context)


@transaction.atomic
def ecom_order_accept(request, order_number):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():

            order = Ecom_Order_Master.objects.get(order_number=order_number)
            branch_code = request.session["branch_code"]
            order_number = order.order_number
            account_number = order.account_number
            discount_amount=order.discount_amount
            bill_amount = order.bill_amount+Decimal(order.delivery_charge)-Decimal(order.discount_amount)
            app_user_id = request.session["app_user_id"]
            cbd = get_business_date(branch_code, app_user_id)
            employee_id = fn_get_employee_by_app_user_id(app_user_id)
      
            app_param = Application_Settings.objects.get()
            tran_type_code = app_param.quick_payment_type
            tran_screen = 'SALES_ENTRY'

            credit_gl_code, debit_gl_code = fn_get_transaction_gl(
                p_transaction_screen=tran_screen, p_tran_type_code=tran_type_code)

            if credit_gl_code is None and debit_gl_code is None:
                data['error_message'] = 'Sales Configuration Ledger Not Exist!\nPlease Contact with your Admin.'
                return JsonResponse(data)

            invoice_number = fn_generate_invoice_number(branch_code)
            _, _, client_id, _, _, _, _, _ = fn_get_accountinfo_byacnumber(
                account_number)
            cursor = connection.cursor()
            cursor.callproc("fn_sales_online_order_accept", [branch_code, app_user_id, order_number, invoice_number, cbd, employee_id,
                                                      bill_amount, discount_amount,  tran_type_code, credit_gl_code, debit_gl_code,order_number])
            
            row = cursor.fetchone()

            if row[0] != 'S':
                data['error_message'] = row[1]
                raise Exception(row[1])

            message = "Order Accepted Successfully with Invoice Number : " + invoice_number

            data['success_message'] = message
            data['form_is_valid'] = True

            data['form_is_valid'] = True
            data['success_message'] = message
    except Exception as e:
        data['error_message'] = str(e)
    return JsonResponse(data)

def sales_order_details_update(request):
    try:
        data = dict()
        data_string = request.POST.getlist('data_string')
        data_dict = json.loads(data_string[0])
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
                try:
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
                data['error_message'] = 'Error for Updating Product ' + \
                    str(product_id)+' ' + str(e)
                data['form_is_valid'] = False
                return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        return JsonResponse(data)

    data['form_is_valid'] = True
    data['success_message'] = 'Save Successfully!'
    return JsonResponse(data)
