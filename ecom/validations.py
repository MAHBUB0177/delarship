from .models import *
from django.db import connection, transaction
from django.db.models import Count, Sum, Avg
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from appauth.utils import fn_get_query_result


def fn_val_check_ecom_category_exist(p_categories_name):
    try:

        categories_name = p_categories_name.upper()
        sql = ''' select count(*) from ecom_product_categories where upper(categories_name) = ''' + \
            "'"+categories_name+"'"
        result = fn_get_query_result(sql)
        if result[0]['count'] == 1:
            return True
        else:
            return False
    except Exception as e:
        return False

def fn_val_check_ecom_subcategory_exist(p_subcategories_name):
    try:

        subcategories_name = p_subcategories_name.upper()
        sql = ''' select count(*) from ecom_product_sub_categories where upper(subcategories_name) = ''' + \
            "'"+subcategories_name+"'"
        result = fn_get_query_result(sql)
        if result[0]['count'] == 1:
            return True
        else:
            return False
    except Exception as e:
        return False
