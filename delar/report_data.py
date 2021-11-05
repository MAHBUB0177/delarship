from django.db.models.fields import IntegerField
from sales.models import *
from django.db import connection, transaction
from django.db.models import Count, Sum, Avg, Max, Min
import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from decimal import Decimal
from .validations import *
import logging
import sys
from django.utils import timezone
import datetime
logger = logging.getLogger(__name__)
from django.db.models.functions import Cast
from django.db.models import FloatField, F, Func, Value, CharField, DateField
from appauth.models import Report_Table_Tabular, Report_Parameter, Query_Table
from appauth.utils import fn_get_employee_phone, fn_get_query_result, fn_get_reports_parameter



# def  fn_get_packet_return_rpt(p_app_user_id):
#             #print ('A')
#     try:
#         rep_param = fn_get_reports_parameter(p_app_user_id)
#         sql = ''' select   
#   c.client_id  ,client_name,
#  product_name  ,
#   return_invoice  ,
#   return_date,  
#   receive_quantity  ,
#   receive_value 
#   from delar_sales_return_packet r,sales_clients c,sales_products p
#   where r.product_id=p.product_id
#   and r.client_id=c.client_id
#   order by return_date asc'''

#         if rep_param["p_branch_code"]:
#                     sql=sql+' and  branch_code='+rep_param["p_branch_code"] 
#         if rep_param["p_client_id"]:
#             sql=sql+' and c.client_id ='+"'" +rep_param["p_client_id"]+"'"

#         if   rep_param["p_product_id"]:
#            sql=sql+' and p.product_id='+"'" +rep_param["p_product_id"]+"'"
#         print(sql)

      
#         #print(sql)
#         results = fn_get_query_result(sql)
#         return results
#     except Exception as e:
#         print(str(e)) 

    

# def fn_get_packet_return_rpt_sum(p_app_user_id):
#     #print ('A')
#     try:
#         rep_param = fn_get_reports_parameter(p_app_user_id)
#         sql = ''' select  
#     sum(  netpay)  total_netpay
#     from hrm_department_info,hrm_salary_sheet
#     where dept_id=department_id '''

#         if rep_param["p_branch_code"]:
#             sql=sql+' and  branch_code='+rep_param["p_branch_code"] 
#         if rep_param["p_dept_id"]:
#             sql=sql+' and department_id ='+"'" +rep_param["p_dept_id"]+"'"

#         if   rep_param["p_month_year"]:
#            sql=sql+' and  month_year='+"'" +rep_param["p_month_year"]+"'"
#         #print(sql)
#         results = fn_get_query_result(sql)
#         return results
#     except Exception as e:
#         print(str(e)) 