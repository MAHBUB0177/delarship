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


def fn_get_invoice_details(p_app_user_id):
    try:
        row = Report_Table_Tabular.objects.filter(app_user_id=p_app_user_id).values(row_number=F("report_column1"),
                                                                                    product_name=F(
                                                                                        "report_column2"),
                                                                                    quantity=F("report_column4"), unit_price=F("report_column5"), total_price=F("report_column8"))
        return row
    except Exception as e:
        print(str(e))
        pass


def fn_get_invoice_master(p_app_user_id):
    data = dict()
    try:
        inv_row = Report_Parameter.objects.get(
            parameter_name="p_invoice_number", app_user_id=p_app_user_id)
        invoice_number = inv_row.parameter_values
        row = Sales_Master.objects.get(invoice_number=invoice_number)
        data["customer_name"] = row.customer_name
        data["customer_phone"] = row.customer_phone
        data["customer_address"] = row.customer_address
        data["executive_phone"] = fn_get_employee_phone(row.employee_id)
        data["total_bill_amount"] = "{:,}".format(row.total_bill_amount)
        data["bill_amount"] = "{:,}".format(row.bill_amount)
        data["pay_amount"] = "{:,}".format(row.pay_amount)
        data["due_amount"] = "{:,}".format(row.due_amount)
        data["advance_pay"] = "{:,}".format(row.advance_pay)
        data["total_discount_amount"] = "{:,}".format(
            row.total_discount_amount)
        data["invoice_number"] = row.invoice_number
        data["invoice_date"] = row.invoice_date
        data["app_user_id"] = row.app_user_id
        return data
    except Exception as e:
        print(str(e))
        return data


def fn_get_stock_details(p_app_user_id):
    try:
        row = Report_Table_Tabular.objects.filter(app_user_id=p_app_user_id).values(product_name=F("report_column3"),
                                                                                    product_model=F("report_column2"), stock_date=F("report_column4"), total_quantity=F("report_column6"),
                                                                                    unit_price=F("report_column5"), total_price=F("report_column7"), row_serial=F("report_column8"))
        return row
    except Exception as e:
        print(str(e))
        pass


def fn_get_stock_summary(p_app_user_id):
    data = dict()
    try:
        stock_summary = Report_Table_Tabular.objects.annotate(total_quantity=Cast('report_column6', output_field=FloatField()),
                                                              total_price=Cast('report_column7', output_field=FloatField())).filter(app_user_id=p_app_user_id).aggregate(
            Sum('total_quantity'), Sum('total_price'))
        data['total_quantity'] = stock_summary['total_quantity__sum']
        data['total_price'] = stock_summary['total_price__sum']
        from_date = Report_Parameter.objects.get(
            app_user_id=p_app_user_id, parameter_name='p_from_date', report_name='day_wise_stock_list')
        upto_date = Report_Parameter.objects.get(
            app_user_id=p_app_user_id, parameter_name='p_upto_date', report_name='day_wise_stock_list')
        data['p_from_date'] = from_date.parameter_values
        data['p_upto_date'] = upto_date.parameter_values
        return data
    except Exception as e:
        print(str(e))
        return data


def fn_get_stocknreturn_details(p_app_user_id):
    try:
        row = Report_Table_Tabular.objects.filter(app_user_id=p_app_user_id).values(supplier_id=F("report_column1"),
                                                                                    supplier_name=F("report_column2"), product_id=F("report_column3"), product_name=F("report_column4"),
                                                                                    transaction_date=F("report_column5"), purces_quantity=F("report_column6"), purces_rate=F("report_column7"),
                                                                                    purces_total_price=F("report_column8"), returned_quantity=F("report_column9"), return_rate=F("report_column10"),
                                                                                    return_total_price=F("report_column11")).order_by('report_column2', 'report_column5')
        return row
    except Exception as e:
        print(str(e))
        pass


def fn_get_stocknreturn_summary(p_app_user_id):
    data = dict()
    try:
        stock_summary = Report_Table_Tabular.objects.annotate(total_purces_quantity=Cast('report_column6', output_field=IntegerField()),
                                                              total_purces_price=Cast(
                                                                  'report_column8', output_field=FloatField()),
                                                              total_returned_quantity=Cast(
                                                                  'report_column9', output_field=IntegerField()),
                                                              total_return_price=Cast('report_column11', output_field=FloatField())).filter(app_user_id=p_app_user_id).aggregate(
            Sum('total_purces_quantity'), Sum('total_purces_price'), Sum('total_returned_quantity'), Sum('total_return_price'))
        data['total_purces_quantity'] = stock_summary['total_purces_quantity__sum']
        data['total_purces_price'] = stock_summary['total_purces_price__sum']
        data['total_returned_quantity'] = stock_summary['total_returned_quantity__sum']
        data['total_return_price'] = stock_summary['total_return_price__sum']
        from_date = Report_Parameter.objects.get(
            app_user_id=p_app_user_id, parameter_name='p_from_date', report_name='sales_stock_return_details')
        upto_date = Report_Parameter.objects.get(
            app_user_id=p_app_user_id, parameter_name='p_upto_date', report_name='sales_stock_return_details')
        data['p_from_date'] = from_date.parameter_values
        data['p_upto_date'] = upto_date.parameter_values
        return data
    except Exception as e:
        print(str(e))
        return data


def fn_get_stockinventory_details(p_app_user_id):
    try:
        rep_param = fn_get_reports_parameter(p_app_user_id)
        print(rep_param)
        sql = '''SELECT product_id,
       product_name,
       opening_available_stock opening_quantity,
       opening_purchase_rate opening_rate,
       product_opening_value opening_value,
       product_total_stock purchase_quantity,
       (CASE
           WHEN total_purchase_amount > 0
           THEN
              ROUND ((total_purchase_amount / product_total_stock), 2)
           ELSE
              0
        END) purchase_rate,
       total_purchase_amount purchase_value,
       product_total_sales sales_quantity,
       (CASE
           WHEN total_sales_amount > 0
           THEN
              ROUND ((total_sales_amount / product_total_sales), 2)
           ELSE
              0
        END) sales_rate,
       total_sales_amount sales_value,
       total_stock_return stock_return_quantity,
       (CASE
           WHEN stock_return_amount > 0
           THEN
              ROUND ((stock_return_amount / total_stock_return), 2)
           ELSE
              0
        END) stock_return_rate,
       stock_return_amount stock_return_value,
       total_sales_return sales_return_quantity,
       (CASE
           WHEN sales_return_amount > 0
           THEN
              ROUND ((sales_return_amount / total_sales_return), 2)
           ELSE
              0
        END) sales_return_rate,
       sales_return_amount sales_return_value,
       product_total_damage damage_quantity,
       (CASE
           WHEN total_return_damage > 0
           THEN
              ROUND ((total_return_damage / product_total_damage), 2)
           ELSE
              0
        END) damage_rate,
       total_return_damage damage_value,
       closing_available_stock closing_quantity,
       (CASE
           WHEN product_closing_value > 0
           THEN
              ROUND ((product_closing_value / closing_available_stock), 2)
           ELSE
              0
        END) closing_rate,
       product_closing_value closing_value,
       product_end_balance,
       stock_return_amount,
       closing_purchase_rate,
       closing_available_stock,
       total_order_quantity
  FROM (SELECT report_column1 product_id,
               report_column2 product_name,
               CASt (report_column3 AS NUMERIC) opening_purchase_rate,
               CASt (report_column4 AS INTEGER) opening_available_stock,
               CASt (report_column5 AS NUMERIC) product_opening_value,
               CASt (report_column6 AS INTEGER) product_total_stock,
               CASt (report_column7 AS INTEGER) total_order_quantity,
               CASt (report_column8 AS INTEGER) product_total_sales,
               CASt (report_column9 AS INTEGER) total_stock_return,
               CASt (report_column10 AS INTEGER) total_sales_return,
               CASt (report_column11 AS INTEGER) product_total_damage,
               CASt (report_column12 AS NUMERIC) product_end_balance,
               CASt (report_column13 AS NUMERIC) total_purchase_amount,
               CASt (report_column14 AS NUMERIC) total_sales_amount,
               CASt (report_column15 AS NUMERIC) stock_return_amount,
               CASt (report_column16 AS NUMERIC) sales_return_amount,
               CASt (report_column17 AS NUMERIC) total_return_damage,
               CASt (report_column18 AS NUMERIC) closing_purchase_rate,
               CASt (report_column19 AS INTEGER) closing_available_stock,
               CASt (report_column20 AS NUMERIC) product_closing_value
          FROM appauth_report_table_tabular WHERE app_user_id='''+"'"+p_app_user_id+"'"+''') T '''

        if rep_param["p_stock_available"] == 'Y':
            sql = sql+' WHERE closing_available_stock > 0'

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))


def fn_get_stockinventory_summary(p_app_user_id):
    try:
        rep_param = fn_get_reports_parameter(p_app_user_id)
        sql = '''SELECT sum (opening_quantity) total_opening_quantity,
       sum (opening_value) total_opening_value,
       sum (purchase_quantity) total_purchase_quantity,
       sum (purchase_value) total_purchase_value,
       sum (sales_quantity) total_sales_quantity,
       sum (sales_value) total_sales_value,
       sum (stock_return_quantity) total_stock_return_quantity,
       sum (stock_return_value) total_stock_return_value,
       sum (sales_return_quantity) total_sales_return_quantity,
       sum (sales_return_value) total_sales_return_value,
       sum (damage_quantity) total_damage_quantity,
       sum (damage_value) total_damage_value,
       sum (closing_quantity) total_closing_quantity,
       sum (closing_value) total_closing_value
  FROM (SELECT product_id,
               product_name,
               opening_available_stock opening_quantity,
               opening_purchase_rate opening_rate,
               product_opening_value opening_value,
               product_total_stock purchase_quantity,
               (CASE
                   WHEN total_purchase_amount > 0
                   THEN
                      ROUND ((total_purchase_amount / product_total_stock),
                             2)
                   ELSE
                      0
                END) purchase_rate,
               total_purchase_amount purchase_value,
               product_total_sales sales_quantity,
               (CASE
                   WHEN total_sales_amount > 0
                   THEN
                      ROUND ((total_sales_amount / product_total_sales), 2)
                   ELSE
                      0
                END) sales_rate,
               total_sales_amount sales_value,
               total_stock_return stock_return_quantity,
               (CASE
                   WHEN stock_return_amount > 0
                   THEN
                      ROUND ((stock_return_amount / total_stock_return), 2)
                   ELSE
                      0
                END) stock_return_rate,
               stock_return_amount stock_return_value,
               total_sales_return sales_return_quantity,
               (CASE
                   WHEN sales_return_amount > 0
                   THEN
                      ROUND ((sales_return_amount / total_sales_return), 2)
                   ELSE
                      0
                END) stock_return_rate,
               sales_return_amount sales_return_value,
               product_total_damage damage_quantity,
               (CASE
                   WHEN total_return_damage > 0
                   THEN
                      ROUND ((total_return_damage / product_total_damage), 2)
                   ELSE
                      0
                END) damage_rate,
               total_return_damage damage_value,
               closing_available_stock closing_quantity,
               (CASE
                   WHEN product_closing_value > 0
                   THEN
                      ROUND (
                         (product_closing_value / closing_available_stock),
                         2)
                   ELSE
                      0
                END) closing_rate,
               product_closing_value closing_value,
               product_end_balance,
               stock_return_amount,
               closing_purchase_rate,
               closing_available_stock,
               total_order_quantity
          FROM (SELECT report_column1
                          product_id,
                       report_column2
                          product_name,
                       CASt (report_column3 AS NUMERIC)
                          opening_purchase_rate,
                       CASt (report_column4 AS INTEGER)
                          opening_available_stock,
                       CASt (report_column5 AS NUMERIC)
                          product_opening_value,
                       CASt (report_column6 AS INTEGER)
                          product_total_stock,
                       CASt (report_column7 AS INTEGER)
                          total_order_quantity,
                       CASt (report_column8 AS INTEGER)
                          product_total_sales,
                       CASt (report_column9 AS INTEGER)
                          total_stock_return,
                       CASt (report_column10 AS INTEGER)
                          total_sales_return,
                       CASt (report_column11 AS INTEGER)
                          product_total_damage,
                       CASt (report_column12 AS NUMERIC)
                          product_end_balance,
                       CASt (report_column13 AS NUMERIC)
                          total_purchase_amount,
                       CASt (report_column14 AS NUMERIC)
                          total_sales_amount,
                       CASt (report_column15 AS NUMERIC)
                          stock_return_amount,
                       CASt (report_column16 AS NUMERIC)
                          sales_return_amount,
                       CASt (report_column17 AS NUMERIC)
                          total_return_damage,
                       CASt (report_column18 AS NUMERIC)
                          closing_purchase_rate,
                       CASt (report_column19 AS INTEGER)
                          closing_available_stock,
                       CASt (report_column20 AS NUMERIC)
                          product_closing_value
                  FROM appauth_report_table_tabular WHERE app_user_id='''+"'"+p_app_user_id+"'"+''') T '''

        if rep_param["p_stock_available"] == 'Y':
            sql = sql+' WHERE closing_available_stock > 0'

        sql = sql+' ) t'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))


def fn_get_salesnreturn_details(p_app_user_id):
    try:
        row = Report_Table_Tabular.objects.filter(app_user_id=p_app_user_id).values(client_id=F("report_column1"),
                                                                                    client_name=F("report_column2"), product_id=F("report_column3"), product_name=F("report_column4"),
                                                                                    transaction_date=F("report_column5"), sales_quantity=F("report_column6"), sales_rate=F("report_column7"),
                                                                                    sales_total_price=F("report_column8"), sales_discount_amount=F("report_column9"), sales_bill_amount=F("report_column10"),
                                                                                    returned_quantity=F("report_column11"), return_rate=F("report_column12"),
                                                                                    return_total_price=F("report_column13"), row_serial=F("report_column14"), total_row=F("report_column15")).order_by('id')
        return row
    except Exception as e:
        print(str(e))
        pass


def fn_get_salesnreturn_summary(p_app_user_id):
    data = dict()
    try:
        stock_summary = Report_Table_Tabular.objects.annotate(total_sales_quantity=Cast('report_column6', output_field=IntegerField()),
                                                              total_sales_price=Cast(
                                                                  'report_column8', output_field=FloatField()),
                                                              total_sales_discount=Cast(
                                                                  'report_column9', output_field=FloatField()),
                                                              total_sales_bill=Cast(
            'report_column10', output_field=FloatField()),
            total_returned_quantity=Cast(
                'report_column11', output_field=IntegerField()),
            total_return_price=Cast('report_column13', output_field=FloatField())).filter(app_user_id=p_app_user_id).aggregate(
            Sum('total_sales_quantity'), Sum('total_sales_price'), Sum(
                'total_sales_discount'), Sum('total_sales_bill'),
            Sum('total_returned_quantity'), Sum('total_return_price'))
        data['total_sales_quantity'] = stock_summary['total_sales_quantity__sum']
        data['total_sales_price'] = stock_summary['total_sales_price__sum']
        data['total_sales_discount'] = stock_summary['total_sales_discount__sum']
        data['total_sales_bill'] = stock_summary['total_sales_bill__sum']
        data['total_returned_quantity'] = stock_summary['total_returned_quantity__sum']
        data['total_return_price'] = stock_summary['total_return_price__sum']
        from_date = Report_Parameter.objects.get(
            app_user_id=p_app_user_id, parameter_name='p_from_date', report_name='sales_and_return_details')
        upto_date = Report_Parameter.objects.get(
            app_user_id=p_app_user_id, parameter_name='p_upto_date', report_name='sales_and_return_details')
        data['p_from_date'] = from_date.parameter_values
        data['p_upto_date'] = upto_date.parameter_values
        return data
    except Exception as e:
        print(str(e))
        return data


def fn_get_salesnreturnstmt_details(p_app_user_id):
    try:
        row = Report_Table_Tabular.objects.filter(app_user_id=p_app_user_id).values(client_id=F("report_column1"),
                                                                                    client_name=F("report_column2"), product_id=F("report_column3"), product_name=F("report_column4"),
                                                                                    transaction_date=F("report_column5"), sales_quantity=F("report_column6"), sales_rate=F("report_column7"),
                                                                                    sales_total_price=F("report_column8"), sales_discount_amount=F("report_column9"), sales_bill_amount=F("report_column10"),
                                                                                    returned_quantity=F("report_column11"), return_rate=F("report_column12"),
                                                                                    return_total_price=F("report_column13"), row_serial=F("report_column14"), total_row=F("report_column15"),
                                                                                    credit_balance=F("report_column16"), debit_balance=F("report_column17"), account_balance=F("report_column18")).order_by('id')
        return row
    except Exception as e:
        print(str(e))
        pass


def fn_get_salesnreturnstmt_summary(p_app_user_id):
    data = dict()
    try:
        stock_summary = Report_Table_Tabular.objects.annotate(total_sales_quantity=Cast('report_column6', output_field=IntegerField()),
                                                              total_sales_price=Cast(
                                                                  'report_column8', output_field=FloatField()),
                                                              total_sales_discount=Cast(
                                                                  'report_column9', output_field=FloatField()),
                                                              total_sales_bill=Cast(
            'report_column10', output_field=FloatField()),
            total_returned_quantity=Cast(
                'report_column11', output_field=IntegerField()),
            total_return_price=Cast(
                'report_column13', output_field=FloatField()),
            total_credit_balance=Cast(
                'report_column16', output_field=FloatField()),
            total_debit_balance=Cast('report_column17', output_field=FloatField())).filter(app_user_id=p_app_user_id).aggregate(
            Sum('total_sales_quantity'), Sum('total_sales_price'), Sum(
                'total_sales_discount'), Sum('total_sales_bill'),
            Sum('total_returned_quantity'), Sum('total_return_price'), Sum('total_credit_balance'), Sum('total_debit_balance'))
        data['total_sales_quantity'] = stock_summary['total_sales_quantity__sum']
        data['total_sales_price'] = stock_summary['total_sales_price__sum']
        data['total_sales_discount'] = stock_summary['total_sales_discount__sum']
        data['total_sales_bill'] = stock_summary['total_sales_bill__sum']
        data['total_returned_quantity'] = stock_summary['total_returned_quantity__sum']
        data['total_return_price'] = stock_summary['total_return_price__sum']
        data['total_credit_balance'] = stock_summary['total_credit_balance__sum']
        data['total_debit_balance'] = stock_summary['total_debit_balance__sum']
        return data
    except Exception as e:
        print(str(e))
        return data


def fn_get_stocknreturnstmt_details(p_app_user_id):
    try:
        row = Report_Table_Tabular.objects.filter(app_user_id=p_app_user_id).values(client_id=F("report_column1"),
                                                                                    client_name=F("report_column2"), product_id=F("report_column3"), product_name=F("report_column4"),
                                                                                    transaction_date=F("report_column5"), sales_quantity=F("report_column6"), sales_rate=F("report_column7"),
                                                                                    sales_total_price=F("report_column8"), sales_discount_amount=F("report_column9"), sales_bill_amount=F("report_column10"),
                                                                                    returned_quantity=F("report_column11"), return_rate=F("report_column12"),
                                                                                    return_total_price=F("report_column13"), row_serial=F("report_column14"), total_row=F("report_column15"),
                                                                                    credit_balance=F("report_column16"), debit_balance=F("report_column17"), account_balance=F("report_column18")).order_by('id')
        return row
    except Exception as e:
        print(str(e))
        pass


def fn_get_stocknreturnstmt_summary(p_app_user_id):
    data = dict()
    try:
        stock_summary = Report_Table_Tabular.objects.annotate(total_sales_quantity=Cast('report_column6', output_field=IntegerField()),
                                                              total_sales_price=Cast(
                                                                  'report_column8', output_field=FloatField()),
                                                              total_sales_discount=Cast(
                                                                  'report_column9', output_field=FloatField()),
                                                              total_sales_bill=Cast(
            'report_column10', output_field=FloatField()),
            total_returned_quantity=Cast(
                'report_column11', output_field=IntegerField()),
            total_return_price=Cast(
                'report_column13', output_field=FloatField()),
            total_credit_balance=Cast(
                'report_column16', output_field=FloatField()),
            total_debit_balance=Cast('report_column17', output_field=FloatField())).filter(app_user_id=p_app_user_id).aggregate(
            Sum('total_sales_quantity'), Sum('total_sales_price'), Sum(
                'total_sales_discount'), Sum('total_sales_bill'),
            Sum('total_returned_quantity'), Sum('total_return_price'), Sum('total_credit_balance'), Sum('total_debit_balance'))
        data['total_sales_quantity'] = stock_summary['total_sales_quantity__sum']
        data['total_sales_price'] = stock_summary['total_sales_price__sum']
        data['total_sales_discount'] = stock_summary['total_sales_discount__sum']
        data['total_sales_bill'] = stock_summary['total_sales_bill__sum']
        data['total_returned_quantity'] = stock_summary['total_returned_quantity__sum']
        data['total_return_price'] = stock_summary['total_return_price__sum']
        data['total_credit_balance'] = stock_summary['total_credit_balance__sum']
        data['total_debit_balance'] = stock_summary['total_debit_balance__sum']
        return data
    except Exception as e:
        print(str(e))
        return data


def fn_get_sales_details(p_app_user_id):
    try:
        row = Report_Table_Tabular.objects.filter(app_user_id=p_app_user_id).values(row_serial=F("report_column1"),
                                                                                    product_name=F(
                                                                                        "report_column4"),
                                                                                    product_model=F("report_column5"), sales_date=F("report_column3"), total_quantity=F("report_column8"),
                                                                                    unit_price=F("report_column7"), total_price=F("report_column9"))
        return row
    except Exception as e:
        print(str(e))
        pass


def fn_get_sales_summary(p_app_user_id):
    data = dict()
    try:
        stock_summary = Report_Table_Tabular.objects.annotate(total_quantity=Cast('report_column8', output_field=FloatField()),
                                                              total_price=Cast('report_column9', output_field=FloatField())).filter(app_user_id=p_app_user_id).aggregate(
            Sum('total_quantity'), Sum('total_price'))
        data['total_quantity'] = stock_summary['total_quantity__sum']
        data['total_price'] = stock_summary['total_price__sum']
        from_date = Report_Parameter.objects.get(
            app_user_id=p_app_user_id, parameter_name='p_from_date', report_name='sales_daily_sales_details')
        upto_date = Report_Parameter.objects.get(
            app_user_id=p_app_user_id, parameter_name='p_upto_date', report_name='sales_daily_sales_details')
        data['p_from_date'] = from_date.parameter_values
        data['p_upto_date'] = upto_date.parameter_values
        return data
    except Exception as e:
        print(str(e))
        return data


def fn_get_emi_details(p_app_user_id):
    try:
        rep_param = fn_get_reports_parameter(p_app_user_id)
        w_ason_date = datetime.datetime.strptime(
            rep_param["p_ason_date"], '%d-%m-%Y').strftime("%Y-%m-%d")
        sql = '''WITH
   emi_setup
   AS
      (SELECT e.client_id, a.account_number,
              a.account_title,
              a.phone_number,
              emi_reference_no,
              total_emi_amount,
              number_of_installment,
              emi_rate,
              emi_inst_amount inst_amount,
              emi_inst_repay_from_date inst_from_date,
              emi_inst_frequency inst_freq,
              installment_tot_repay_amt,
                             fn_get_noof_installment_due (
                                emi_inst_frequency,
                                emi_inst_repay_from_date,
                                '''+"'"+w_ason_date+"'"+''') total_installment_due
         FROM sales_emi_setup e, finance_accounts_balance a
        WHERE e.account_number = a.account_number '''

        if rep_param["p_emi_reporting_type"] == 'DUE_ONLY':
            sql = sql+' AND e.total_emi_due > 0'

        if rep_param["p_emi_reporting_type"] == 'FULL_PAY':
            sql = sql+' AND e.total_emi_due = 0'

        if rep_param["p_emi_reference_no"]:
            sql = sql+' and e.emi_reference_no='+"'" + \
                rep_param["p_emi_reference_no"]+"'"

        if rep_param["p_account_number"]:
            sql = sql+' and e.account_number='+"'" + \
                rep_param["p_account_number"]+"'"

        if rep_param["p_branch_code"]:
            sql = sql+' and e.branch_code='+rep_param["p_branch_code"]

        if rep_param["p_center_code"]:
            sql = sql+' and e.center_code='+"'" + \
                rep_param["p_center_code"]+"'"

        sql = sql+'''
        ), emi_details as(
SELECT s.client_id, s.account_number,
       s.account_title,
       s.phone_number,
       s.emi_reference_no,
       s.total_emi_amount,
       s.number_of_installment,s.installment_tot_repay_amt,
       s.emi_rate,
       s.inst_amount,
       s.inst_from_date,
       s.inst_freq,
       (case when s.total_installment_due>s.number_of_installment then s.number_of_installment else s.total_installment_due end)  total_due_inst,
       (case when s.total_installment_due>s.number_of_installment then s.number_of_installment else s.total_installment_due end)*s.inst_amount inst_due_amount,
       b.inst_receive_date,
       b.inst_receive_amount,
       (case when s.total_installment_due>s.number_of_installment then s.number_of_installment else s.total_installment_due end) total_installment_due,
       b.total_installment_payment,
       b.total_installment_overdue,
       b.total_installment_advance,
       b.total_emi_outstanding,
       b.emi_principal_outstanding,
       b.emi_profit_outstanding,
       b.emi_total_payment,
       b.emi_principal_payment,
       b.emi_profit_payment,
       b.total_advance_recover,
       b.principal_advance_recover,
       b.profit_advance_recover,
       b.total_due_recover,
       b.principal_due_recover,
       b.profit_due_recover,
       b.emi_total_overdue,
       b.emi_principal_overdue,
       b.emi_profit_overdue
  FROM emi_setup s left outer join
       (SELECT h.branch_code,
               h.account_number,
               h.emi_reference_no emi_reference_no,
               h.inst_receive_date,
               h.inst_receive_amount,
               h.total_installment_due,
               h.total_installment_payment,
               h.total_installment_overdue,
               h.total_installment_advance,
               h.total_emi_outstanding,
               h.emi_principal_outstanding,
               h.emi_profit_outstanding,
               h.emi_total_payment,
               h.emi_principal_payment,
               h.emi_profit_payment,
               h.total_advance_recover,
               h.principal_advance_recover,
               h.profit_advance_recover,
               h.total_due_recover,
               h.principal_due_recover,
               h.profit_due_recover,
               h.emi_total_overdue,
               h.emi_principal_overdue,
               h.emi_profit_overdue
          FROM sales_emi_history h,
               (  SELECT b.account_number,
                         b.emi_reference_no,
                         max (inst_receive_date) inst_receive_date
                    FROM sales_emi_history b, emi_setup e
                   WHERE     b.account_number = e.account_number
                         AND b.emi_reference_no = e.emi_reference_no
                         AND b.inst_receive_date <= '''+"'"+w_ason_date+"'"+'''
                GROUP BY b.account_number, b.emi_reference_no) l
         WHERE     h.account_number = l.account_number
               AND h.emi_reference_no = l.emi_reference_no
               AND h.inst_receive_date = l.inst_receive_date) b
 on(  s.account_number = b.account_number)
       AND s.emi_reference_no = b.emi_reference_no)
SELECT client_id, account_title,
       phone_number,
       emi_reference_no,
       total_emi_amount,
       number_of_installment,
       inst_amount,installment_tot_repay_amt,
       TO_CHAR(inst_from_date,'DD-MM-YYYY') inst_from_date,
       inst_freq,
       total_due_inst,
       inst_due_amount,
       TO_CHAR(inst_receive_date,'DD-MM-YYYY') inst_receive_date,
       inst_receive_amount,
       emi_total_payment,
       (CASE
           WHEN inst_due_amount - emi_total_payment > 0
           THEN
              inst_due_amount - emi_total_payment
           ELSE
              0
        END) inst_od_amount,
       (CASE
           WHEN emi_total_payment-inst_due_amount > 0
           THEN
              emi_total_payment-inst_due_amount
           ELSE
              0
        END) inst_adv_amount
  FROM emi_details order by inst_from_date'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))


def fn_get_sales_details_data(p_app_user_id):
    try:
        sql = '''SELECT report_column1 reporting_name,
         cast (report_column2 as numeric) total_purchase_value,
         cast (report_column3 as numeric) sales_price,
         cast (report_column4 as numeric) quantity,
         cast (report_column5 as numeric) returned_quantity,
         cast (report_column6 as numeric) total_price,
         cast (report_column7 as numeric) discount_amount,
         (cast (report_column6 as numeric)-cast (report_column7 as numeric)) net_price,
         cast (report_column8 as numeric) profit_amount,
         cast (report_column9 as numeric) loss_amount,
         cast (report_column10 as numeric) net_profit_loss
    FROM appauth_report_table_tabular
   WHERE app_user_id = '''+"'"+p_app_user_id+"'"+'''
ORDER BY id'''
        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))
        pass


def fn_get_sales_details_summary(p_app_user_id):
    try:
        sql = '''SELECT SUM(total_purchase_value) total_purchase_value, SUM(sales_price) sales_price, 
        SUM(quantity) quantity,SUM(returned_quantity) returned_quantity,SUM(total_price) total_price,
        SUM(discount_amount) discount_amount,SUM(profit_amount) profit_amount, SUM(net_price) net_price,
        SUM(loss_amount) loss_amount, SUM(net_profit_loss) net_profit_loss
FROM (  SELECT report_column1 reporting_name,
         cast (report_column2 as numeric) total_purchase_value,
         cast (report_column3 as numeric) sales_price,
         cast (report_column4 as numeric) quantity,
         cast (report_column5 as numeric) returned_quantity,
         cast (report_column6 as numeric) total_price,
         cast (report_column7 as numeric) discount_amount,
         (cast (report_column6 as numeric)-cast (report_column7 as numeric)) net_price,
         cast (report_column8 as numeric) profit_amount,
         cast (report_column9 as numeric) loss_amount,
         cast (report_column10 as numeric) net_profit_loss
    FROM appauth_report_table_tabular
   WHERE app_user_id = '''+"'"+p_app_user_id+"'"+'''
ORDER BY id) T'''
        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))
        pass


def fn_get_sales_centersalesdetails_data(p_app_user_id):
    try:
        sql = '''SELECT ROW_NUMBER ()
            OVER (ORDER BY report_column5) row_serial, 
            cast (report_column1 AS INTEGER) branch_code,
       report_column2 center_code,
       report_column3 branch_center_code,
       report_column4 center_name,
       report_column5 invoice_number,
       report_column6 invoice_date,
       report_column7 client_id,
       report_column8 customer_name,
       report_column9 customer_phone,
       report_column10 employee_id,
       (CASE
           WHEN CAST (report_column23 AS INTEGER) = 1 THEN 'Y'
           ELSE NULL
        END) row_span,
       CAST (report_column11 AS INTEGER) total_quantity,
       CAST (report_column12 AS NUMERIC) total_bill_amount,
       CAST (report_column13 AS NUMERIC) bill_amount,
       CAST (report_column14 AS NUMERIC) pay_amount,
       CAST (report_column15 AS NUMERIC) due_amount,
       CAST (report_column16 AS NUMERIC) advance_pay,
       CAST (report_column17 AS NUMERIC) total_discount_amount,
       CAST (report_column18 AS INTEGER) item_count,
       CAST (report_column19 AS NUMERIC) rowspan,
       CAST (report_column20 AS NUMERIC) total_profit_amount,
       CAST (report_column21 AS NUMERIC) total_loss_amount,
       report_column22 product_id,
       CAST (report_column23 AS INTEGER) serial_no,
       report_column24 product_name,
       CAST (report_column25 AS INTEGER) quantity,
       CAST (report_column26 AS NUMERIC) total_purchase_value,
       CAST (report_column27 AS NUMERIC) sales_rate,
       CAST (report_column28 AS INTEGER) returned_quantity,
       CAST (report_column29 AS NUMERIC) total_price,
       CAST (report_column30 AS NUMERIC) profit_amount,
       CAST (report_column31 AS NUMERIC) loss_amount,
       CAST (report_column32 AS NUMERIC) discount_amount,
       report_column33 emi_serial_number,
       CAST (report_column34 AS NUMERIC) emi_down_amount,
       CAST (report_column35 AS NUMERIC) total_emi_amount,
       CAST (report_column36 AS NUMERIC) emi_inst_amount,
       report_column37 emi_inst_frequency,
       report_column38 emi_inst_repay_from_date,
       report_column39 number_of_installment,
       report_column40 installment_exp_date,
       CAST (report_column41 AS NUMERIC) emi_rate,
       CAST (report_column42 AS NUMERIC) emi_profit_amount,
       CAST (report_column43 AS NUMERIC) emi_fee_amount,
       CAST (report_column44 AS NUMERIC) emi_ins_rate,
       CAST (report_column45 AS NUMERIC) emi_ins_fee_amount,
       CAST (report_column46 AS NUMERIC) emi_doc_fee_amount
  FROM appauth_report_table_tabular
   WHERE app_user_id = '''+"'"+p_app_user_id+"'"+'''
  order by report_column5,CAST (report_column23 AS INTEGER)'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))
        pass


def fn_get_sales_centersalesdetails_summary(p_app_user_id):
    try:
        sql = '''SELECT SUM(total_quantity) total_quantity, SUM(total_bill_amount) total_bill_amount, 
        SUM(bill_amount) bill_amount,SUM(pay_amount) pay_amount,SUM(due_amount) due_amount,
        SUM(advance_pay) advance_pay,SUM(total_discount_amount) total_discount_amount, SUM(total_quantity) total_product,
        SUM(total_profit_amount) total_profit_amount, SUM(total_loss_amount) total_loss_amount, SUM(emi_down_amount) emi_down_amount,
        SUM(total_emi_amount) total_emi_amount, SUM(emi_inst_amount) emi_inst_amount, SUM(emi_profit_amount) emi_profit_amount,
        SUM(emi_fee_amount) emi_fee_amount,SUM(emi_ins_rate) emi_ins_rate,SUM(emi_ins_fee_amount) emi_ins_fee_amount,
        SUM(emi_doc_fee_amount) emi_doc_fee_amount
FROM ( SELECT 
       CAST (report_column11 AS INTEGER) total_quantity,
       CAST (report_column12 AS NUMERIC) total_bill_amount,
       CAST (report_column13 AS NUMERIC) bill_amount,
       CAST (report_column14 AS NUMERIC) pay_amount,
       CAST (report_column15 AS NUMERIC) due_amount,
       CAST (report_column16 AS NUMERIC) advance_pay,
       CAST (report_column17 AS NUMERIC) total_discount_amount,
       CAST (report_column18 AS INTEGER) item_count,
       CAST (report_column19 AS NUMERIC) rowspan,
       CAST (report_column20 AS NUMERIC) total_profit_amount,
       CAST (report_column21 AS NUMERIC) total_loss_amount,
       CAST (report_column34 AS NUMERIC) emi_down_amount,
       CAST (report_column35 AS NUMERIC) total_emi_amount,
       CAST (report_column36 AS NUMERIC) emi_inst_amount,
       CAST (report_column42 AS NUMERIC) emi_profit_amount,
       CAST (report_column43 AS NUMERIC) emi_fee_amount,
       CAST (report_column44 AS NUMERIC) emi_ins_rate,
       CAST (report_column45 AS NUMERIC) emi_ins_fee_amount,
       CAST (report_column46 AS NUMERIC) emi_doc_fee_amount
  FROM appauth_report_table_tabular
   WHERE app_user_id = '''+"'"+p_app_user_id+"'"+'''
ORDER BY id) T'''

        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))
        pass
############packet return############


def fn_get_packet_return_rpt(p_app_user_id):
    try:
        rep_param = fn_get_reports_parameter(p_app_user_id)
        print(rep_param)
        sql = '''select   
  c.client_id  ,client_name,
 p.product_name  ,
  return_invoice  ,
  return_date,  
  receive_quantity  ,
  receive_value 
  from delar_sales_return_packet r,sales_clients c,sales_products p
  where r.product_id=p.product_id
  and r.client_id=c.client_id
  '''
        if rep_param["p_product_id"]:
                    sql = sql+' and p.product_id='+"'" + rep_param["p_product_id"]+"'"
        
        if rep_param["p_client_id"]:
                    sql = sql+' and c.client_id='+"'" + rep_param["p_client_id"]+"'"
        

        if rep_param["p_branch_code"]:
                    sql = sql+' and r.branch_code='+"'" + rep_param["p_branch_code"]+"'"

        print(sql)
        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))

###########
def fn_get_packet_return_rpt_sum(p_app_user_id):
    try:
        rep_param = fn_get_reports_parameter(p_app_user_id)
        print(rep_param)
        sql = '''select  
    sum(  receive_quantity)  total_quantity,
    sum(  receive_value ) total_price
    from delar_sales_return_packet 
    where branch_code=branch_code
  '''
        if rep_param["p_product_id"]:
                    sql = sql+' and product_id='+"'" + rep_param["p_product_id"]+"'"
        
        if rep_param["p_client_id"]:
                    sql = sql+' and client_id='+"'" + rep_param["p_client_id"]+"'"
        

        

        print(sql)
        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))



#######
# def fn_get_packet_return_rpt_sum(p_app_user_id):
        
#     try:
#         rep_param = fn_get_reports_parameter(p_app_user_id)

#         sql = ''' select  
#     sum(  receive_quantity)  total_quantity,
#     sum(  receive_value ) total_price
#     from delar_sales_return_packet '''

#         if rep_param["p_product_id"]:
#                     sql = sql+' and p.product_id='+"'" + rep_param["p_product_id"]+"'"
        
#         if rep_param["p_client_id"]:
#                     sql = sql+' and c.client_id='+"'" + rep_param["p_client_id"]+"'"
        

#         if rep_param["p_branch_code"]:
#                        sql=sql+' and  branch_code='+rep_param["p_branch_code"] 


      

#         results = fn_get_query_result(sql)
#         print(results)

#         return results
#     except Exception as e:
#         print(str(e))

############
def fn_get_employee_details_rpt(p_app_user_id):
    try:
        rep_param = fn_get_reports_parameter(p_app_user_id)
       
        print(rep_param)
        sql = '''SELECT m.employee_id,
      employee_name,
      m.order_number,
      m.order_date,
      p.product_name,
      ordered_quantity,
      ordered_total_price,
      delivered_quantity,
      delivered_total_price,
            ordered_quantity - delivered_quantity pending_qnty
        FROM sales_products p,
            sales_order_details d,
            sales_order_master m,
            appauth_employees e
        WHERE     m.order_number = d.order_number
            AND d.product_id = p.product_id
            AND m.employee_id = e.employee_id'''
        if rep_param["p_product_id"]:
                    sql = sql+' and p.product_id='+"'" + rep_param["p_product_id"]+"'"

        if rep_param["p_employee_id"]:
                    sql = sql+' and e.employee_id='+"'" + rep_param["p_employee_id"]+"'"

        # if rep_param["p_order_date"]:
        #             sql=sql+' and m.order_date=' +"'" + rep_param["p_order_date"]+"'"
                     

       

        # print(sql)
        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))


def fn_get_employee_details_rpt_summary(p_app_user_id):
    try:

        rep_param = fn_get_reports_parameter(p_app_user_id)
        sql = '''select sum(ordered_quantity) sum_ordered_quantity,
       sum(ordered_total_price) sum_ordered_total_price,
       sum(delivered_quantity) sum_delivered_quantity,
       sum(delivered_total_price) sum_delivered_total_price,
       sum(ordered_quantity - delivered_quantity) sum_pending_qnty
       from sales_order_details where branch_code=branch_code '''

        if rep_param["p_product_id"]:
                    sql = sql+' and product_id='+"'" + rep_param["p_product_id"]+"'"

        if rep_param["p_employee_id"]:
                    sql = sql+' and employee_id='+"'" + rep_param["p_employee_id"]+"'"   

        print(sql)
        results = fn_get_query_result(sql)
        return results

    except Exception as e:
        print(str(e))

#####
def fn_get_sales_details_rpt(p_app_user_id):
    try:
        rep_param = fn_get_reports_parameter(p_app_user_id)
       
        print(rep_param)
        sql = '''SELECT
    m.employee_id,
    employee_name,
    m.invoice_number,
    m.invoice_date,
    p.product_name,
    SUM(d.quantity) quantity,
    d.product_price,
    SUM( total_price) total_price,
    SUM(  sales_quantity) sales_quantity,
    SUM(  sales_amount) sales_amount,
    SUM( COALESCE(return_quantity, 0)) return_quantity,
    SUM( COALESCE(return_quantity, 0) * d.product_price) return_value,
    SUM( d.quantity - sales_quantity - COALESCE(return_quantity, 0)) pending_quantity,
    SUM( total_price - sales_amount - (COALESCE(return_quantity, 0) * d.product_price)) pending_value
FROM appauth_employees e,
     sales_products p,
     delar_srstage_details d,
     delar_srstage_master m
WHERE d.invoice_number = m.invoice_number 
and m.employee_id=e.employee_id
and p.product_id=d.product_id '''

        if rep_param["p_branch_code"]:
            sql=sql+' and  m.branch_code='+rep_param["p_branch_code"] 
        if rep_param["p_product_id"]:
            sql=sql+' and d.product_id='+"'" +rep_param["p_product_id"]+"'"
        if rep_param["p_employee_id"]:
            sql=sql+' and m.employee_id='+"'" +rep_param["p_employee_id"]+"'"

        # if w_from_date and w_upto_date:
        #             sql=sql+' and  m.invoice_date between '+"'" +str(w_from_date)+"'"+" and "+"'" +str(w_upto_date)+"'"
        sql=sql+' GROUP BY m.employee_id,   employee_name,  m.invoice_number,  m.invoice_date,  p.product_name,  d.product_price order by m.invoice_date asc'''
                     

       

        print(sql)
        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))



def fn_get_sales_details_summary(p_app_user_id):
    try:
        rep_param=fn_get_reports_parameter(p_app_user_id)
        sql = '''select sum(quantity) quantity,sum(product_price) product_price,

sum(total_price) total_price,sum(sales_quantity) sales_quantity,sum(sales_amount) sales_amount,

sum(return_quantity) return_quantity,SUM( COALESCE(return_quantity, 0) * d.product_price) return_value,
SUM( d.quantity - sales_quantity - COALESCE(return_quantity, 0)) pending_quantity,
    SUM( total_price - sales_amount - (COALESCE(return_quantity, 0) * d.product_price)) pending_value
    from delar_srstage_details d where branch_code=branch_code'''

        if rep_param["p_branch_code"]:
                    sql=sql+' and  branch_code='+rep_param["p_branch_code"] 
        if rep_param["p_product_id"]:
            sql=sql+' and d.product_id='+"'" +rep_param["p_product_id"]+"'"
        if rep_param["p_employee_id"]:
            sql=sql+' and d.employee_id='+"'" +rep_param["p_employee_id"]+"'"    
        results = fn_get_query_result(sql)
        return results

    except Exception as e:
        print(str(e))


#############sales_oder_reprt###

def fn_get_sales_order_rpt(p_app_user_id):
    try:
        rep_param = fn_get_reports_parameter(p_app_user_id)
        print(rep_param)
        sql = '''SELECT p.product_name,
       d.product_price,
       d.ordered_quantity,
       d.ordered_total_price,
       d.order_number,
       d.order_date,
       m.customer_name,
       m.customer_phone,
       m.customer_address,
       m.total_bill_amount,
       m.total_discount_amount,
       m.pay_amount,
       m.due_amount,
       (m.total_bill_amount-m.total_discount_amount) bill_after_discount
  FROM sales_order_details d, sales_products p,sales_order_master m
 WHERE d.product_id = p.product_id and
 d.order_number=m.order_number
  '''
        if rep_param["p_order_number"]:
                    sql = sql+' and d.order_number='+"'" + rep_param["p_order_number"]+"'"
        
        # if rep_param["p_branch_code"]:
        #             sql = sql+' and m.branch_code='+"'" + rep_param["p_branch_code"]+"'"

        print(sql)
        results = fn_get_query_result(sql)
        return results
    except Exception as e:
        print(str(e))



######### quotion ######
def fn_sales_quotation_dtl(p_app_user_id):
    try:
        rep_param = fn_get_reports_parameter(p_app_user_id)
     
        sql = '''SELECT p.product_name,
       q.quantity,
       u.unit_name,
       q.unit_price,
       q.total_price,
       s.quotation_date,
        s.vat_condition, 
        s.quotation_validity,
        s.warranty,
        s.subject
       
  FROM sales_products p, sales_quotation_details q,sales_quotation_master s,sales_products_unit u
 WHERE p.product_id = q.product_id AND q.quotation_id=s.quotation_id AND u.unit_id=q.unit
  '''
        if rep_param["p_quotation_id"]:
                    sql = sql+' and q.quotation_id='+"'" + rep_param["p_quotation_id"]+"'"
        

        print(sql)
        results = fn_get_query_result(sql)
        print(results)
        return results
    except Exception as e:
        print(str(e))



def fn_sales_quotation_summary(p_app_user_id):
    try:
        rep_param=fn_get_reports_parameter(p_app_user_id)
        sql = ''' select sum(total_price) price
    from sales_quotation_details q where app_user_id=app_user_id'''

        
        if rep_param["p_quotation_id"]:
            sql=sql+' and q.quotation_id='+"'" +rep_param["p_quotation_id"]+"'"
         
        results = fn_get_query_result(sql)
        return results

    except Exception as e:
        print(str(e))