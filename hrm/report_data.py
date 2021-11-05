from django.db.models.fields import IntegerField
from django.db import connection, transaction
from django.db.models import Count, Sum, Avg, Max, Min
import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from decimal import Decimal
import logging
import sys
from django.utils import timezone
logger = logging.getLogger(__name__)
from django.db.models.functions import Cast
from django.db.models import FloatField, F, Func, Value, CharField, DateField
from appauth.models import Report_Table_Tabular, Report_Parameter, Query_Table
from appauth.utils import fn_get_employee_phone, fn_get_query_result,fn_get_reports_parameter
from finance.utils import fn_get_accountinfo_byacnumber 


def  fn_get_salary_sheet_rpt(p_app_user_id):
    #print ('A')
    try:
        rep_param = fn_get_reports_parameter(p_app_user_id)
        sql = ''' select branch_code ,
dept_id ,
department_name,
desig_name ,
EMPLOYEE_ID,
employee_name ,
total_atten ,
salary_gross ,
house_rent ,
travel_allowance ,
pf_cutting ,
welfare_cutting,
SALES_COMISSION,
total_advance ,
others_allowance ,
others_deduction ,
stamp_ded_amount ,
total_salary ,
netpay ,
month_year
  from hrm_department_info,hrm_salary_sheet
  where dept_id=department_id '''

        if rep_param["p_branch_code"]:
            sql=sql+' and  branch_code='+rep_param["p_branch_code"] 
        if rep_param["p_dept_id"]:
            sql=sql+' and department_id ='+"'" +rep_param["p_dept_id"]+"'"

        if   rep_param["p_month_year"]:
           sql=sql+' and  month_year='+"'" +rep_param["p_month_year"]+"'"

      
        #print(sql)
        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e)) 
    

def fn_get_salary_sheet_rpt_sum(p_app_user_id):
    print ('A')
    try:
        rep_param = fn_get_reports_parameter(p_app_user_id)

        sql = ''' select  sum(salary_gross) sum_salary_gross ,
sum(house_rent ) sum_house_rent,
sum(travel_allowance ) sum_travel_allow,
sum(pf_cutting) sum_pf_cutting ,
sum(welfare_cutting) sum_welfare_cutt,
sum(SALES_COMISSION)sum_sales_cum,
sum(total_advance ) sum_total_adv,
sum(others_allowance ) sum_others_allow,
sum(others_deduction ) sum_others_dedu,
sum(stamp_ded_amount) sum_stamp_ded ,
sum(total_salary ) sum_total_salary,

    sum(  netpay)  sum_total_netpay
    from hrm_department_info,hrm_salary_sheet
    where dept_id=department_id '''
        if rep_param["p_branch_code"]:
                        sql=sql+' and  branch_code='+rep_param["p_branch_code"] 
        if rep_param["p_dept_id"]:
                        sql=sql+' and department_id ='+"'" +rep_param["p_dept_id"]+"'"

        if   rep_param["p_month_year"]:
                    sql=sql+' and  month_year='+"'" +rep_param["p_month_year"]+"'"
        #print(sql)
        results = fn_get_query_result(sql)
        print(results)
        return results
        
    except Exception as e:
        print(str(e)) 
        

def fn_get_employee_sheet_rpt(p_app_user_id):
    try:
        rep_param = fn_get_reports_parameter(p_app_user_id)
        sql=''' SELECT employee_id,
       employee_name, 
       attendance_date,(select desig_name from hrm_employee_designation where desig_id=designation_id)
       design_name,
       (select bunit_name from hrm_business_unit where business_unit_id=bunit_id)bunit_name,
       shift_name,
       in_time,
       out_time,
       CASE
          WHEN in_time_sec > work_start_time_sec
          THEN
             in_time_sec - work_start_time_sec
          ELSE
             00
       END late_in,
         (CASE
             WHEN out_time_sec < work_end_time_sec
             THEN
                work_end_time_sec - out_time_sec
             ELSE
                00
          END)
       / 3600 early_exit,
       round (
            (CASE WHEN total_ot <= duty_gap_time THEN 0 ELSE total_ot END)
          / 3600) total_ot,STATUS
  FROM (SELECT E.employee_id,
               employee_name,
               attendance_date,
               shift_name,
               to_char (in_time, 'hh:mi:ss') in_time,
               to_char (out_time, 'hh:mi:ss') out_time,
               (  EXTRACT (EPOCH FROM (out_time - in_time))
                - s.work_start_time_sec) total_ot,
               (duty_gap_time * 60) duty_gap_time,
               to_seconds (to_char (in_time, 'hh:mi:ss')) in_time_sec,
               s.work_start_time_sec,
               to_seconds (to_char (out_time, 'hh:mi:ss')) out_time_sec,
               s.work_end_time_sec,
               CASE
                  WHEN 1 = (SELECT 1
                              FROM hrm_attendance_log a
                             WHERE E.employee_id = a.employee_id )
                  THEN
                     'PRESENT'
                  WHEN 1 =
                       (SELECT 1
                         FROM hrm_holyday_info
                        WHERE ATTENDANCE_DATE BETWEEN HOLIDAY_FROM_DATE
                                                  AND HOLIDAY_END_DATE)
                  THEN
                     'HOLIDAY'
                  ELSE
                     'ABSENT'
               END STATUS,designation_id,business_unit_id
          FROM HRM_EMPLOYEE_DETAILS e, hrm_attendance_log a, hrm_shift_info s
         WHERE E.employee_id = a.employee_id AND a.shift_id = current_shift)
        where employee_id = and ATTENDANCE_DATE between :p_from_date and :p_to_date '''


        #  if rep_param["p_branch_code"]:
        #     sql=sql+' and  branch_code='+rep_param["p_branch_code"] 
        # if rep_param["p_dept_id"]:
        #     sql=sql+' and department_id ='+"'" +rep_param["p_dept_id"]+"'"

        # if   rep_param["p_month_year"]:
        #    sql=sql+' and  month_year='+"'" +rep_param["p_month_year"]+"'"
        #print(sql)
        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e)) 




