from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from rest_framework import generics
from django.db.models import Case, CharField, Value, When, F
from rest_framework.generics import ListAPIView
# Create your views here.

from appauth.models import *

from apiauth.serializers import *

class BranchApiView(generics.ListAPIView):
    serializer_class = BranchSerializer
    def get_queryset(self):
        branch_code = self.request.query_params.get('branch_code',None)
        branch_name = self.request.query_params.get('branch_name',None)

        queryset = Branch.objects.filter().order_by('branch_name')

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)

        return queryset

class Country_Api_View(generics.ListAPIView):
    serializer_class = CountrySerializer
    def get_queryset(self):
        country_id = self.request.query_params.get('country_id',None)

        queryset = Loc_Country.objects.filter().order_by('country_name')

        if country_id:
            queryset = queryset.filter(country_id=country_id)

        return queryset

class Employee_Api_View(generics.ListAPIView):
    serializer_class = Employee_Serializer
    def get_queryset(self):
        employee_name = self.request.query_params.get('employee_name',None)

        queryset = Employees.objects.filter().order_by('employee_name')

        if employee_name:
            queryset = queryset.filter(employee_name__icontains=employee_name)

        return queryset

class User_Settings_Api_View(generics.ListAPIView):
    serializer_class = User_Settings_Serializer

    def get_queryset(self):
        app_user_id = self.request.query_params.get('app_user_id', None)
        employee_id = self.request.query_params.get(
            'employee_id', None)
        queryset = User_Settings.objects.filter().order_by('app_user_id')

        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)

        if app_user_id:
            queryset = queryset.filter(app_user_id=app_user_id)

        return queryset