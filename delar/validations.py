from .models import *
from django.db import connection, transaction
from django.db.models import Count, Sum, Avg, F, Value
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.functions import Length, Upper
from appauth.utils import fn_get_query_result


def fn_val_check_product_price_list_exist(p_product_id, p_client_type):
    if Product_Price_List.objects.filter(product_id=p_product_id, client_type_code=p_client_type).exists():
        return True
    else:
        return False


def fn_val_check_product_price_list_count(p_product_id, p_client_type):
    product_count = Product_Price_List.objects.filter(
        product_id=p_product_id, client_type_code=p_client_type).aggregate(Count('product_id'))
    return product_count['product_id_count']


def fn_val_check_product_offer_list_exist(p_product_id, p_client_type, p_offer_type):
    if Product_Offer_List.objects.filter(product_id=p_product_id, client_type_code=p_client_type, sales_offer_type=p_offer_type).exists():
        return True
    else:
        return False


def fn_validate_chart_phone_mismatch(p_sales_account_number, p_app_user):
    total_row = Sales_Details_Temp.objects.filter(
        ~Q(sales_account_number=p_sales_account_number), app_user_id=p_app_user).aggregate(Count('sales_account_number'))
    total_record = total_row['sales_account_number__count']
    if total_record > 0:
        return False
    else:
        return True


def fn_valid_product_code(p_branch_code, p_product_id):
    if products.objects.filter(product_id=p_product_id.upper()).exists():
        return True
    else:
        return False


def fn_valid_product_barcode(p_product_bar_code):
    if products.objects.filter(product_bar_code=p_product_bar_code).exists():
        return True
    else:
        return False


def fn_val_client_exist(p_client_id):
    if Clients.objects.filter(client_id=p_client_id).exists():
        return True
    else:
        return False


def fn_val_invoice_canceled(p_invoice_nmber):
    if Sales_Master.objects.filter(invoice_number=p_invoice_nmber, status='C').exists():
        return True
    else:
        return False


def fn_val_emisetup_exist(p_emi_reference_no):
    if Emi_Setup.objects.filter(emi_reference_no=p_emi_reference_no, emi_cancel_by__isnull=True).exists():
        return True
    else:
        return False


def fn_val_check_product_group_exist(p_group_name):
    try:

        group_name = p_group_name.upper()
        sql = ''' select count(*) from sales_products_group where upper(group_name) = ''' + \
            "'"+group_name+"'"
        result = fn_get_query_result(sql)
        if result[0]['count'] == 1:
            return True
        else:
            return False
    except Exception as e:
        return False


def fn_val_check_product_brand_exist(p_brand_name):
    try:

        brand_name = p_brand_name.upper()
        sql = ''' select count(*) from sales_products_brand where upper(brand_name) = ''' + \
            "'"+brand_name+"'"
        result = fn_get_query_result(sql)
        if result[0]['count'] == 1:
            return True
        else:
            return False
    except Exception as e:
        return False
