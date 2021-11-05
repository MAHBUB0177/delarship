from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from rest_framework import generics
from django.db.models import Case, CharField, Value, When, F
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
import datetime
from django.contrib.auth import get_user_model
User = get_user_model()

from appauth.utils import fn_is_head_office_user

from .serializers import *
from ecom.models import *

class User_Chart_ApiView(generics.ListAPIView):
    serializer_class = User_Chart_Serializer

    def get_queryset(self):
        queryset =  User_Chart.objects.filter().order_by('product_name')

        return queryset

class Ecom_Slider_ApiView(generics.ListAPIView):
    serializer_class = Ecom_Slider_Serializer

    def get_queryset(self):
        title = self.request.query_params.get('title', None)
        queryset =  Ecom_Slider.objects.filter().order_by('title')
        return queryset

class Ecom_Order_Master_ApiView(generics.ListAPIView):
    serializer_class = Ecom_Order_Master_Serializer

    def get_queryset(self):
        order_date = self.request.query_params.get('order_date', None)
        order_number = self.request.query_params.get('order_number', None)
        customer_phone = self.request.query_params.get('customer_phone', None)
        executive_phone = self.request.query_params.get('executive_phone', None)
        branch_code = self.request.session.get('branch_code')
        queryset = Ecom_Order_Master.objects.filter().order_by('app_data_time')

        if order_date:
            queryset = queryset.filter(invoice_date=order_date)
            
        if order_number:
            queryset = queryset.filter(invoice_number=order_number)

        if customer_phone:
            queryset = queryset.filter(customer_phone=customer_phone)

        if executive_phone:
            queryset = queryset.filter(executive_phone=executive_phone)

        return queryset

class Ecom_Product_Category_ApiView(generics.ListAPIView):
    serializer_class = Ecom_Product_category_Serializer

    def get_queryset(self):
        categories_id = self.request.query_params.get('categories_id', None)
        branch_code = self.request.session.get('branch_code')
        queryset = Ecom_Product_Categories.objects.filter().order_by('categories_id')

        if categories_id:
            queryset = queryset.filter(categories_id=categories_id)
        return queryset

class Ecom_Product_Subcategory_ApiView(generics.ListAPIView):
    serializer_class = Ecom_Product_Subcategory_Serializer

    def get_queryset(self):
        subcategories_id = self.request.query_params.get('subcategories_id', None)
        branch_code = self.request.session.get('branch_code')
        queryset = Ecom_Product_Sub_Categories.objects.filter().order_by('categories_id')

        if subcategories_id:
            queryset = queryset.filter(subcategories_id=subcategories_id)
        return queryset

