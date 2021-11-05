from appauth.models import *
from django.db import connection, transaction
from django.db.models import Count, Sum, Avg, Max, Min
import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from decimal import Decimal
import logging
import sys
from django.utils import timezone
import datetime
from appauth.validations import *
logger = logging.getLogger(__name__)

from appauth.models import *

def fn_get_reports_parameter(p_app_user_id):
    data = dict()
    parm_list = Report_Parameter.objects.filter(app_user_id=p_app_user_id)
    for param in parm_list:
        try:
            if param.parameter_name in ('p_from_date','p_upto_date','p_ason_date'):
                date_object = datetime.datetime.strptime(param.parameter_values, '%Y-%m-%d')
                parameter_values = date_object.strftime("%d-%m-%Y")
            else:
                parameter_values = param.parameter_values
        except Exception as e:
            parameter_values = param.parameter_values
        data[param.parameter_name]=parameter_values
    return data

def fn_get_query_result(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
    return results

def get_inv_number(p_inv_code, p_branch_code, p_inv_prefix, p_inv_naration, p_length):
    cursor = connection.cursor()
    cursor.callproc("fn_get_inventory_number", [
                    p_inv_code, p_branch_code, p_inv_prefix, p_inv_naration, p_length])
    inv_number = cursor.fetchone()
    return inv_number

def fn_get_country_id():
    branch_code = 100
    inventory_number = get_inv_number(
        10000, branch_code, '', 'Country ID Generate', 6)
    return inventory_number[0]

def fn_get_employee_id():
    branch_code = 100
    inventory_number = get_inv_number(
        10001, branch_code, '', 'Employee ID Generate', 6)
    return inventory_number[0]

def fn_get_employee_name(p_employee_id):
    employee_name = None
    try:
        emp_info = Employees.objects.get(employee_id=p_employee_id)
        employee_name = emp_info.employee_name
        return employee_name
    except Exception as e:
        return employee_name

def fn_get_employee_phone(p_employee_id):
    mobile_num = None
    try:
        emp_info = Employees.objects.get(employee_id=p_employee_id)
        mobile_num = emp_info.mobile_num
        return mobile_num
    except Exception as e:
        return mobile_num


def get_business_date(p_branch_code, p_app_user=None):
    cbd = datetime.date.today()
    #glob_param = Global_Parameters.objects.get()
    #cbd = glob_param.current_business_day
    return cbd

def fn_is_head_office_user(p_app_user_id):
    ret_bool = False
    try:
        row = User_Settings.objects.get(app_user_id=p_app_user_id)
        if row.head_office_admin:
            ret_bool = True
        else:
            ret_bool = False
        return ret_bool
    except User_Settings.DoesNotExist:
        ret_bool = False
        return ret_bool

def fn_get_branch_instance(p_branch_code):
    branch_code = None
    try:
        row = Branch.objects.get(branch_code=p_branch_code)
        branch_code = row.branch_code
        return branch_code
    except Exception as e:
        return None

def fn_get_employee_by_app_user_id(p_app_user_id):
    employee_id = None
    try:
        row = User_Settings.objects.get(app_user_id=p_app_user_id)
        employee_id = row.employee_id.employee_id
        return employee_id
    except Exception as e:
        return None
