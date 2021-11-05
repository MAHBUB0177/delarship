from django import forms
from crispy_forms.layout import Field
from django.forms import ModelForm, TextInput, Select, Textarea, IntegerField, ChoiceField, BooleanField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class ChoiceFieldNoValidation(ChoiceField):
    def validate(self, value):
        pass


class AppUserModelForm(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False, initial="----------")
    def __init__(self, *args, **kwargs):
        super(AppUserModelForm, self).__init__(*args, **kwargs)
        self.fields['employee_name'].widget.attrs['readonly'] = True
        self.fields['employee_name'].required = False

        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['app_user_id'].widget.attrs['readonly'] = True
            self.fields['employee_name'].widget.attrs['readonly'] = False

    class Meta:
        model = User_Settings
        fields = ['employee_id', 'app_user_id', 'django_user_id', 'is_active', 'employee_name', 'branch_code', 'head_office_admin',
                  'daily_debit_limit', 'daily_credit_limit']

        labels = {
            "employee_id": _("Select Employee"),
            "app_user_id": _("User ID"),
            "django_user_id": _("User Name"),
            "is_active": _("Active"),
            "branch_code": _("Branch"),
            "employee_name": _("Employee Name"),
            "head_office_admin": _("Head Office User"),
            "daily_debit_limit": _("Withdraw Limit"),
            "daily_credit_limit": _("Deposit Limit"),
        }


class AppUserEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AppUserEditForm, self).__init__(*args, **kwargs)
        self.fields['app_user_id'].widget.attrs['readonly'] = True
        self.fields['employee_id'].widget.attrs['readonly'] = True

        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['employee_id'].widget.attrs['readonly'] = True
            self.fields['app_user_id'].widget.attrs['readonly'] = True
            self.fields['employee_name'].required = False

    class Meta:
        model = User_Settings
        fields = ['employee_id', 'app_user_id', 'is_active', 'branch_code', 'head_office_admin', 'employee_name',
                  'daily_debit_limit', 'daily_credit_limit']

        labels = {
            "employee_id": _("Employee Name"),
            "app_user_id": _("User Name"),
            "is_active": _("Active"),
            "branch_code": _("Branch"),
            "head_office_admin": _("Head Office User"),
            "daily_debit_limit": _("Withdraw Limit"),
            "daily_credit_limit": _("Deposit Limit"),
        }


class AppUserSearch(forms.Form):
    app_user_name = forms.CharField(label="User Name", widget=forms.TextInput(
        attrs={'placeholder': 'User Name',  'id': 'id_app_user_name'}
    ), required=False)
    user_phone_number = forms.CharField(label="Phone Number", widget=forms.TextInput(
        attrs={'placeholder': '',  'id': 'id_user_phone_number'}
    ), required=False)


class BranchModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BranchModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['branch_code'].widget.attrs['readonly'] = True

    class Meta:
        model = Branch
        fields = ['branch_code', 'branch_name', 'branch_address', 'manager_phone', 'status',
                  'country_id', 'division_id', 'district_id', 'upozila_id', 'union_id', 'manager_id', 'opening_date', ]
        widgets = {
            'opening_date': DateInput(),
        }
        labels = {
            "branch_code": _("Branch Code"),
            "branch_name": _("Branch Name"),
            "opening_date": _("Opening Date"),
            "country_id": _("Country"),
            "division_id": _("Division"),
            "district_id": _("District"),
            "upozila_id": _("Upozila"),
            "union_id": _("Union/City Corp"),
            "manager_id": _("Branch Manager"),
            "branch_address": _("Address"),
            "manager_phone": _("Manager Phone"),
            "status": _("Status"),
        }


class Country_Model_Form(forms.ModelForm):

    class Meta:
        model = Loc_Country
        fields = ['country_name']
        labels = {
            "country_name": _("Country Name"),
        }


class Employees_Model_Form(forms.ModelForm):
    desig_id = ChoiceFieldNoValidation(label='Designation', choices=[
                                         ('', 'Select designation')], initial="")
    department_id = ChoiceFieldNoValidation(label='Department', choices=[
                                         ('', 'Select department')], initial="")
    def __init__(self, *args, **kwargs):
        super(Employees_Model_Form, self).__init__(*args, **kwargs)
        self.fields['employee_id'].widget.attrs['readonly'] = True

        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['employee_id'].widget.attrs['readonly'] = True

    class Meta:
        model = Employees
        fields = ['employee_id', 'employee_name', 'branch_code', 'employee_sex', 'father_name', 'mother_name', 'joining_date',
                  'present_address', 'permanent_address', 'birth_date', 'nid_number', 'employee_religion', 'blood_group', 'employee_education',
                  'marital_status', 'mobile_num', 'alternate_phone',  'is_active', 'is_deleted','desig_id','basic_salary','house_rent',
                  'travel_allowance','attent_allowance','pf_cutting','welfare_cutting' ,'department_id']

        widgets = {
            'present_address': Textarea(attrs={'rows': 2, 'cols': 60, }),
            'permanent_address': Textarea(attrs={'rows': 2, 'cols': 60, }),
            'birth_date': DateInput(),
            'joining_date': DateInput(),
        }

        labels = {
            "employee_id": _("Employee ID"),
            "employee_name": _("Employee Name"),
            "branch_code": _("Branch Code"),
            "employee_sex": _("Gender"),
            "father_name": _("Father Name"),
            "mother_name": _("Mother Name"),
            "joining_date": _("Joining Date"),
            "present_address": _("Present Address"),
            "permanent_address": _("Permanent Address"),
            "birth_date": _("Date Of Birth"),
            "nid_number": _("National ID"),
            "employee_religion": _("Religion"),
            "blood_group": _("Blood Group"),
            "employee_education": _("Education"),
            "marital_status": _("Merital Status"),
            "mobile_num": _("Mobile Number"),
            "alternate_phone": _("Emergency Mobile Number"),
            "is_active": _("Employee Is Active"),
            "is_deleted": _("Employee Is Delete"),
            "house_rent": _("House Rent"),
            "basic_salary": _("Basic Salary"),
            "travel_allowance": _("Travel allowance"),
            "attent_allowance": _("Atten Allowence"),
            "pf_cutting" : _("Pf Cutting"),
            "welfare_cutting" : _("Welfare Cutting"),
            "department_id": _("Department Id")
        }
