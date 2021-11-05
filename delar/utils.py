from appauth.models import User_Settings
from sales.models import *
from django.db import connection, transaction
from django.db.models import Count, Sum, Avg, Max, Min
import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from decimal import Decimal
import logging
import sys
from django.utils import timezone
from sales.validations import *
logger = logging.getLogger(__name__)
from django.db.models import F

from appauth.utils import get_inv_number, get_business_date
from sales.validations import *
from finance.models import Application_Settings as Finance_Application_Settings, Client_Type
from finance.utils import fn_get_accountinfo_bytran, fn_get_cash_gl_code, fn_cash_tran_posting, fn_transfer_tran_posting, fn_cancel_tran_batch
from .models import *

def fn_get_transaction_id(p_branch_code):
    branch_code = p_branch_code
    client_inv = get_inv_number(
        40002, branch_code, '', 'Transaction ID', 5)
    return client_inv[0]

def fn_get_transaction_id1(p_branch_code):
    branch_code = p_branch_code
    client_inv = get_inv_number(
        40002, branch_code, '', 'Transaction ID1', 5)
    return client_inv[0]

def fn_generate_srsales_number(p_branch_code):
    branch_code = 100
    inventory_number = get_inv_number(
        40004, branch_code, 'SR', 'SR Invoice Number Generate', 6)
    return inventory_number[0]


def fn_get_center_id(p_branch_code):
    branch_code = 100
    client_inv = get_inv_number(40001, branch_code, '4', 'Center ID', 6)
    return client_inv[0]


def fn_get_branch_center_id(p_branch_code):
    branch_code = p_branch_code
    client_inv = get_inv_number(
        40002, branch_code, '', 'Branch Wise Center ID', 4)
    return client_inv[0]


def fn_get_centeradmin_id(p_branch_code):
    branch_code = 100
    client_inv = get_inv_number(40003, branch_code, '3', 'Center Admin ID', 6)
    return client_inv[0]

def fn_get_return_invoice(p_branch_code):
    branch_code = 100
    client_inv = get_inv_number(40001, branch_code, '4', 'return invoice', 6)
    return client_inv[0]


def fn_get_branch_center(p_center_code):
    try:
        row = Center.objects.get(center_code=p_center_code)
        branch_center_code = row.branch_center_code
        return branch_center_code
    except Exception as e:
        return None
        
def fn_get_center_employee(p_center_code):
    try:
        row = Center.objects.get(center_code=p_center_code)
        employee_id = row.center_employee_id.employee_id
        return employee_id
    except Exception as e:
        return None

def fn_get_center_code_by_branch(p_branch_code, p_center_code):
    try:
        row = Center.objects.get(branch_code=p_branch_code,branch_center_code=p_center_code)
        center_code = row.center_code
        return center_code
    except Exception as e:
        return None

def get_product_cart_summary(app_user_id):
    """
    This function are used for the purpose of return item summary information for making new sales invoice.
    """
    item_summary = Srstage_Details_Temp.objects.filter(app_user_id=app_user_id).aggregate(
        Sum('quantity'), Sum('discount_amount'), Sum('total_price'))
    total_quantity = item_summary['quantity__sum']
    total_discount = item_summary['discount_amount__sum']
    total_price = item_summary['total_price__sum']
    if total_discount is None:
        total_discount = 0
    if total_price is None:
        total_price = 0
    if total_quantity is None:
        total_quantity = 0
    return total_quantity, total_discount, total_price
##########
def fn_get_sr_available_stock(p_branch_code, p_product_id):
    item_summary = Srstage_Inventory_Status.objects.filter(product_id=p_product_id, branch_code=p_branch_code).aggregate(
        Sum('product_available_stock'))
    total_quantity = item_summary['product_available_stock__sum']
    if total_quantity is None:
        total_quantity = 0
    return total_quantity
###########
