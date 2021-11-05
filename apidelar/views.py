from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from rest_framework import generics
from django.db.models import Case, CharField, Value, When, F
from rest_framework.generics import ListAPIView
# Create your views here.

from delar.models import *

from .serializers import *
from finance.utils import fn_get_transaction_account_type, fn_get_transaction_account_type_screen


class Center_ApiView(generics.ListAPIView):
    serializer_class = Center_Serializer

    def get_queryset(self):
        branch_code = self.request.query_params.get('branch_code')
        center_region_id = self.request.query_params.get(
            'center_region_id', None)
        center_name = self.request.query_params.get('center_name', None)
        center_employee_id = self.request.query_params.get(
            'center_employee_id', None)
        center_status = self.request.query_params.get('center_status', None)

        queryset = Center.objects.filter().order_by('center_name')

        if center_region_id:
            queryset = queryset.filter(center_region_id=center_region_id)

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)

        if center_name:
            queryset = queryset.filter(center_name__icontains=center_name)

        if center_employee_id:
            queryset = queryset.filter(center_employee_id=center_employee_id)

        if center_status:
            queryset = queryset.filter(center_status=center_status)

        return queryset


class DelarSalesDetailsTempApiView(generics.ListAPIView):
    serializer_class = DelarSalesDetailsTempSerializer

    def get_queryset(self):
        app_user_id = self.request.session.get('app_user_id')
        queryset = Srstage_Details_Temp.objects.filter(
            app_user_id=app_user_id).order_by('-app_data_time')
        return queryset


class DelarSalesInvoiceApiView(generics.ListAPIView):
    serializer_class = DelarSalesInvoiceSerializer

    def get_queryset(self):
        invoice_from_date = self.request.query_params.get(
            'invoice_from_date', None)
        invoice_upto_date = self.request.query_params.get(
            'invoice_upto_date', None)
        invoice_number = self.request.query_params.get('invoice_number', None)
        employee_id = self.request.query_params.get('employee_id', None)
        
        branch_code = self.request.query_params.get('branch_code', None)
        queryset = Srstage_Master.objects.filter().order_by('-app_data_time')

        if invoice_number:
            queryset = queryset.filter(invoice_number=invoice_number)

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)
        if invoice_from_date and invoice_upto_date:
            queryset = queryset.filter(
                invoice_date__gte=invoice_from_date, invoice_date__lte=invoice_upto_date)

        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)

        return queryset


class DelarSalesreturnpacketApiView(generics.ListAPIView):
    serializer_class = DelarSalesreturnpacketSerializer

    def get_queryset(self):
        # app_user_id = self.request.session.get('app_user_id')
        return_invoice=self.request.query_params.get(
            'return_invoice', None)
        invoice_from_date = self.request.query_params.get(
            'invoice_from_date', None)
        invoice_upto_date = self.request.query_params.get(
            'invoice_upto_date', None)
        product_id=self.request.query_params.get('product_id',None)
        branch_code = self.request.query_params.get('branch_code', None)
        queryset = Sales_Return_Packet.objects.filter().order_by('-app_data_time')

        if return_invoice:
            queryset = queryset.filter(return_invoice=return_invoice)

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)
        if invoice_from_date and invoice_upto_date:
            queryset = queryset.filter(
                return_date__gte=invoice_from_date, return_date__lte=invoice_upto_date)

        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset

#########sr target######
class DelarSrDetailsTempApiView(generics.ListAPIView):
    serializer_class = Delar_sr_targetSerializer

    def get_queryset(self):
        app_user_id = self.request.session.get('app_user_id')
        queryset = SR_Target_Details_Temp.objects.filter(
            app_user_id=app_user_id).order_by('-app_data_time')
        return queryset