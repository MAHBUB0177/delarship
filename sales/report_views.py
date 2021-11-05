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
from django.db.models import Count, Sum, Avg
from django.db.models import Q, F
import logging
import sys
logger = logging.getLogger(__name__)
from decimal import Decimal
from datetime import date, datetime, timedelta
import time

from .report_data import *
from sales.forms import CommonReportForm, Emi_History_Query
from appauth.views import get_global_data
from appauth.utils import fn_get_reports_parameter, get_business_date


def get_global_report_data(request):

    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    try:
        user_full_name = request.session['user_full_name']
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        company = Application_Settings.objects.get()
        application_title = request.session["application_title"]
        company_name = company.company_name
        company_address = company.company_address
        company_mobile = company.company_mobile
        company_email = company.company_email
        invoice_line1 = company.invoice_line1
        invoice_line2 = company.invoice_line2
        invoice_line3 = company.invoice_line3
        company_logo = company.company_logo
        if invoice_line1 is None:
            invoice_line1 = ''
        if invoice_line2 is None:
            invoice_line2 = ''
        if invoice_line3 is None:
            invoice_line3 = ''
    except Exception as e:
        return render(request, 'appauth/appauth-login.html')
    data = {
        'user': request.user,
        'user_full_name': user_full_name,
        'app_user_id': app_user_id,
        'branch_code': branch_code,
        'company_name': company_name,
        'company_address': company_address,
        'company_mobile': company_mobile,
        'company_email': company_email,
        'invoice_line1': invoice_line1,
        'invoice_line2': invoice_line2,
        'invoice_line3': invoice_line3,
        'application_title': application_title,
        'company_logo': company_logo
    }

    return data


class sales_report_invoice(TemplateView):
    template_name = 'sales_report/sales-report-invoice.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = CommonReportForm()
        context = get_global_data(request)
        context['form'] = form

        return render(request, self.template_name, context)

class sales_invoice_html_report(TemplateView):

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            comp = Application_Settings.objects.get()
            template_name = 'sales_report/'+comp.invoice_file_name
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            inv_dtl = fn_get_invoice_details(app_user_id)
            inv_mst = fn_get_invoice_master(app_user_id)
            data['row'] = inv_dtl
            data = {**data, **inv_mst}
            return render(request, template_name, data)
        except Exception as e:
            pass
        
############## order invoice ##########
class sales_order_invoice(TemplateView):
    template_name = 'sales_report/sales-order-report-invoice.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = CommonReportForm()
        context = get_global_data(request)
        context['form'] = form

        return render(request, self.template_name, context)

class sales_order_invoice_html_report(TemplateView):
    template_name = 'sales_report/sales-order-invoice-print-view.html'
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            comp = Application_Settings.objects.get()
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            ord_dtl = fn_get_sales_order_rpt(app_user_id)
            print(ord_dtl)
            # ord_mst = fn_get_sales_order_report_summary(app_user_id)
            data['row'] = ord_dtl
            # data['ord_mst'] = ord_mst

            data = {**data}
            return render(request, self.template_name, data)
        except Exception as e:
            pass

###########

class sales_report_daywisesales(TemplateView):
    template_name = 'sales_report/sales-report-daywisesales.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)

class sales_report_daywisesales_print_view(TemplateView):
    template_name = 'sales_report/sales-report-daywisesales-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_sales_details(app_user_id)
            sum_data = fn_get_sales_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data = { **data,**sum_data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            return render(request, self.template_name)

class sales_report_daywise_salesnreturn(TemplateView):
    template_name = 'sales_report/sales-report-daywise-salesnreturn.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)

class sales_report_daywise_salesnreturn_print_view(TemplateView):
    template_name = 'sales_report/sales-report-daywise-salesnreturn-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_salesnreturn_details(app_user_id)
            sum_data = fn_get_salesnreturn_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data = {**data, **sum_data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            return render(request, self.template_name)


class sales_report_daywise_salesnreturnstmt(TemplateView):
    template_name = 'sales_report/sales-report-daywise-salesnreturnstmt.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)



class sales_report_daywise_salesnreturnstmt_print_view(TemplateView):
    template_name = 'sales_report/sales-report-daywise-salesnreturnstmt-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_salesnreturnstmt_details(app_user_id)
            sum_data = fn_get_salesnreturnstmt_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data = {**data, **sum_data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            return render(request, self.template_name)

class sales_report_stockinventory(TemplateView):
    template_name = 'sales_report/sales-report-stockinventory.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class sales_report_stockinventory_print_view(TemplateView):
    template_name = 'sales_report/sales-report-stockinventory-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_stockinventory_details(app_user_id)
            sum_data = fn_get_stockinventory_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            print(e)
            return render(request, self.template_name)

class sales_report_daywisepurchase(TemplateView):
    template_name = 'sales_report/sales-report-daywisepurchase.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class sales_report_daywisepurchase_print_view(TemplateView):
    template_name = 'sales_report/sales-report-daywisepurchase-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_stock_details(app_user_id)
            sum_data = fn_get_stock_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data = {**data, **sum_data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            return render(request, self.template_name)


class sales_report_daywise_purchasenreturn(TemplateView):
    template_name = 'sales_report/sales-report-daywise-purchasenreturn.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)

class sales_report_daywise_purchasenreturn_print_view(TemplateView):
    template_name = 'sales_report/sales-report-daywise-purchasenreturn-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_stocknreturn_details(app_user_id)
            sum_data = fn_get_stocknreturn_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data = {**data, **sum_data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            return render(request, self.template_name)


class sales_report_daywise_purchasenreturnstmt(TemplateView):
    template_name = 'sales_report/sales-report-daywise-purchasenreturnstmt.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)

class sales_report_purchasenreturnstmt_print_view(TemplateView):
    template_name = 'sales_report/sales-report-daywise-purchasenreturnstmt-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_stocknreturnstmt_details(app_user_id)
            sum_data = fn_get_stocknreturnstmt_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data = {**data, **sum_data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            return render(request, self.template_name)

class sales_report_emidetails(TemplateView):
    template_name = 'sales_report/sales-report-emidetails.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = Emi_History_Query(initial={'ason_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


class sales_report_emidetails_print_view(TemplateView):
    template_name = 'sales_report/sales-report-emidetails-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_emi_details(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            return render(request, self.template_name)



class sales_report_profitnloss(TemplateView):
    template_name = 'sales_report/sales-report-profitnloss.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)

class sales_report_profitnloss_print_view(TemplateView):
    template_name = 'sales_report/sales-report-profitnloss-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_sales_details_data(app_user_id)
            sum_data = fn_get_sales_details_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)

            if rep_param["p_sales_report_type"]=='DT':
                rep_param["report_name"]="Date Wise Profit and Loss Report"
                rep_param["column_name"]="Date"
            elif rep_param["p_sales_report_type"]=='PR':
                rep_param["report_name"]="Product Wise Profit and Loss Report"
                rep_param["column_name"]="Product Name"
            elif rep_param["p_sales_report_type"]=='CS':
                rep_param["report_name"]="Customer Wise Profit and Loss Report"
                rep_param["column_name"]="Customer Name"
            elif rep_param["p_sales_report_type"]=='BR':
                rep_param["report_name"]="Branch Wise Profit and Loss Report"
                rep_param["column_name"]="Branch Name"
            elif rep_param["p_sales_report_type"]=='CN':
                rep_param["report_name"]="Region Wise Profit and Loss Report"
                rep_param["column_name"]="Region Name"
            elif rep_param["p_sales_report_type"]=='IN':
                rep_param["report_name"]="Invoice Wise Profit and Loss Report"
                rep_param["column_name"]="Invoice Number"

            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            return render(request, self.template_name)


class sales_report_salesdetails(TemplateView):
    template_name = 'sales_report/sales-report-salesdetails.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)

class sales_report_salesdetails_print_view(TemplateView):
    template_name = 'sales_report/sales-report-salesdetails-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_sales_details_data(app_user_id)
            sum_data = fn_get_sales_details_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)

            if rep_param["p_sales_report_type"]=='DT':
                rep_param["report_name"]="Date Wise Sales Details Report"
                rep_param["column_name"]="Date"
            elif rep_param["p_sales_report_type"]=='PR':
                rep_param["report_name"]="Product Wise Sales Details Report"
                rep_param["column_name"]="Product Name"
            elif rep_param["p_sales_report_type"]=='CS':
                rep_param["report_name"]="Customer Wise Sales Details Report"
                rep_param["column_name"]="Customer Name"
            elif rep_param["p_sales_report_type"]=='BR':
                rep_param["report_name"]="Branch Wise Sales Details Report"
                rep_param["column_name"]="Branch Name"
            elif rep_param["p_sales_report_type"]=='CN':
                rep_param["report_name"]="Region Wise Sales Details Report"
                rep_param["column_name"]="Region Name"
            elif rep_param["p_sales_report_type"]=='IN':
                rep_param["report_name"]="Invoice Wise Sales Details Report"
                rep_param["column_name"]="Invoice Number"

            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            return render(request, self.template_name)

class sales_report_centersalesdetails(TemplateView):
    template_name = 'sales_report/sales-report-centersalesdetails.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)

class sales_report_centersalesdetails_print_view(TemplateView):
    template_name = 'sales_report/sales-report-centersalesdetails-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_sales_centersalesdetails_data(app_user_id)
            sum_data = fn_get_sales_centersalesdetails_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            return render(request, self.template_name)


###########
class sales_report_packet_return(TemplateView):
    template_name = 'sales_report/delar-report-packet-return.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'from_date': cbd, 'upto_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)

class sales_report_packet_return_print_view(TemplateView):
    template_name = 'sales_report/delar-report-packet-return-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_packet_return_rpt(app_user_id)
            sum_data = fn_get_packet_return_rpt_sum(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = { **data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            return render(request, self.template_name)



#############sales- order-detalis#############
class sales_details_report(TemplateView):
    template_name = 'sales_report/sales-order-details-report.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={ 'order_date': cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class sales_details_report_print_view(TemplateView):
    template_name = 'sales_report/sales-employee-report-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_employee_details_rpt(app_user_id)
            sum_data = fn_get_employee_details_rpt_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = { **data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            return render(request, self.template_name)


##################
class sales_allocate_report(TemplateView):
    template_name = 'sales_report/sales-allocate-report.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={ 'from_date': cbd,'upto_date':cbd, 'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)


class sales_allocate_report_print_view(TemplateView):
    template_name = 'sales_report/sales-allocate-quantity-report-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_get_sales_details_rpt(app_user_id)
            sum_data = fn_get_sales_details_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = { **data, **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            return render(request, self.template_name)



####### quotion #####
class sales_report_quatation_view(TemplateView):
    template_name = 'sales_report/sales-report-quatation.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm()
        context = get_global_data(request)
        context['forms'] = forms

        return render(request, self.template_name, context)

class sales_report_quatation_print_view(TemplateView):
    template_name = 'sales_report/sales-report-quatation-print-view.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        try:
            app_user_id = request.session["app_user_id"]
            data = get_global_report_data(request)
            dtl_data = fn_sales_quotation_dtl(app_user_id)
            sum_data = fn_sales_quotation_summary(app_user_id)
            rep_param = fn_get_reports_parameter(app_user_id)
            data['dtl_data'] = dtl_data
            data['sum_data'] = sum_data
            data = {**data,  **rep_param}
            return render(request, self.template_name, data)
        except Exception as e:
            return render(request, self.template_name)