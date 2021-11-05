from appauth.models import *
from django.db import connection, transaction
from django.db.models import Count, Sum, Avg, Max, Min
import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from decimal import Decimal
import logging
import sys
from django.utils import timezone
from appauth.validations import *
logger = logging.getLogger(__name__)

from appauth.models import *
from appauth.utils import get_inv_number

def get_business_date(p_branch_code, p_app_user=None):
    cbd = datetime.date.today()
    #glob_param = Global_Parameters.objects.get()
    #cbd = glob_param.current_business_day
    return cbd


def fn_get_departmnet_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Department ID Generate', 6)
    return inventory_number[0]

def fn_get_designation_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Department ID Generate', 6)
    return inventory_number[0]

def fn_get_company_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Department ID Generate', 6)
    return inventory_number[0]
   
def fn_get_office_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Department ID Generate', 6)
    return inventory_number[0]


def fn_get_shift_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Department ID Generate', 6)
    return inventory_number[0]

def fn_get_degree_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Department ID Generate', 6)
    return inventory_number[0]


def fn_get_employee_type_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Department ID Generate', 6)
    return inventory_number[0]




def fn_get_salscale_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Department ID Generate', 6)
    return inventory_number[0]




def fn_get_salsdtlcale_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'salary scale detail ID Generate', 6)
    return inventory_number[0]



def fn_get_salsbonus_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'salary scale detail ID Generate', 6)
    return inventory_number[0]

    

def fn_get_alownce_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Department ID Generate', 6)
    return inventory_number[0]


def fn_get_bank_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Department ID Generate', 6)
    return inventory_number[0]

def fn_get_employee_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Department ID Generate', 6)
    return inventory_number[0]



def fn_get_document_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Department ID Generate', 6)
    return inventory_number[0]

 

def fn_get_leave_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Department ID Generate', 6)
    return inventory_number[0]


def fn_get_bill_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Department ID Generate', 6)
    return inventory_number[0]


def fn_get_holiday_type_id():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Holiday ID Generate', 6)
    return inventory_number[0]

def fn_get_holiday_sl_no():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', 'Holiday ID Generate', 6)
    return inventory_number[0]

def fn_get_holiday_sl_no1():
    branch_code = 1
    inventory_number = get_inv_number(
        100, branch_code, '', ' Employee Holiday ID Generate', 8)
    return inventory_number[0]

##################
# def fn_hrm_salary_process(p_branch_code , p_dept_id , p_month_year , p_app_user_id ):
#     error_message = None
#     status = False
#     cursor = connection.cursor()
#     cursor.callproc("fn_hrm_salary_processing", [
#     p_branch_code   ,
#      p_dept_id       ,
#      p_month_year    ,
#      p_app_user_id   ])
#     row = cursor.fetchone()
#     if row[0] != 'S':
#         error_message = row[1]
#         status = False
#         return status, error_message
#     status = True
#     return status, error_message