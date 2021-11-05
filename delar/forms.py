from logging import exception
from django import forms
from django.db.models import fields
from django.forms import widgets
from crispy_forms.layout import Field
from django.forms import ModelForm, TextInput, Select, Textarea, IntegerField, ChoiceField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.widgets import HiddenInput
from django.utils.translation import ugettext_lazy as _

from .models import *

YES_NO = (
    ('Y', 'Yes'),
    ('N', 'No')
)


SALES_REPORT_TYPE = (
    ('DT', 'Date Wise'),
    ('PR', 'Product Wise'),
    ('CS', 'Customer Wise'),
    ('BR', 'Branch Wise'),
    ('CN', 'Center Wise'),
    ('IN', 'Invoice Wise')
)


class DateInput(forms.DateInput):
    input_type = 'date'


class ChoiceFieldNoValidation(ChoiceField):
    def validate(self, value):
        pass


class Center_Model_Form(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)

    def __init__(self, *args, **kwargs):
        super(Center_Model_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = Center
        fields = ['branch_code', 'center_code', 'center_name', 'center_referred_by', 'center_address', 'center_region_id',
                  'center_open_date',  'center_employee_id', 'center_phone_number',
                  'center_day', 'center_status', 'center_closure_date']

        widgets = {
            'center_address': Textarea(attrs={'rows': 2, 'cols': 60, }),
            'center_closure_date': DateInput(),
            'center_open_date': DateInput(),
        }

        labels = {
            "center_code": _("Region Code"),
            "center_name": _("Region Name"),
            "center_referred_by": _("Referred By"),
            "center_address": _("Address"),
            "center_region_id": _("Region Location"),
            "center_open_date": _("Open Date"),
            "center_employee_id": _("Field Officer Name"),
            "center_phone_number": _("Region Phone"),
            "center_day": _("Sales Day"),
            "center_status": _("Status")
        }


class SalesMasterModelForm(forms.ModelForm):
    employee_id = ChoiceFieldNoValidation(
        label='Executive Name',  required=True, initial="----------",)
    branch_code = ChoiceFieldNoValidation(
        label="Branch Name", required=False, initial="----------")

    def __init__(self, *args, **kwargs):
        super(SalesMasterModelForm, self).__init__(*args, **kwargs)
        self.fields['total_quantity'].widget.attrs['readonly'] = True
        self.fields['bill_amount'].widget.attrs['readonly'] = True
        self.fields['due_amount'].widget.attrs['readonly'] = True
        self.fields['total_bill_amount'].widget.attrs['readonly'] = True

    class Meta:
        model = Srstage_Master
        fields = ['branch_code', 'invoice_number', 'invoice_date', 'employee_id', 'total_quantity', 'returned_quantity',
                  'total_sales_quantity', 'total_sales_amount', 'total_sales_discount_amount', 'total_bill_amount', 'bill_amount',
                  'pay_amount', 'due_amount', 'advance_pay', 'status', 'invoice_comments']

        widgets = {
            'total_quantity': forms.HiddenInput(),
            'total_bill_amount': forms.HiddenInput(),
            'bill_amount': forms.HiddenInput(),
            'due_amount': forms.HiddenInput(),
            'tran_type_code': forms.HiddenInput(),
            'advance_pay': forms.HiddenInput(),
            'invoice_date': DateInput(),
            'employee_id': forms.HiddenInput(),
        }

        labels = {
            "invoice_date": _("Invoice Date"),
            "employee_id": _("Executive Name"),
            "tran_type_code": _("Payment Method"),
            "total_quantity": _("Quantity"),
            "total_bill_amount": _("Total Bill"),
            "bill_amount": _("Bill After Discount"),
            "pay_amount": _("Total Receive Amount"),
            "due_amount": _("Due Amount"),
            "advance_pay": _("Advance Pay"),
            "invoice_comments": _("Comments"),
        }


class SalesDetailsModelForm(forms.ModelForm):
    stock_available = forms.IntegerField(label='Available Stock', initial="",)
    product_id = ChoiceFieldNoValidation(label='Select Product', choices=[
                                         ('', 'Select Product')], initial="")

    def __init__(self, *args, **kwargs):
        super(SalesDetailsModelForm, self).__init__(*args, **kwargs)
        self.fields['total_price'].widget.attrs['readonly'] = True
        self.fields['product_price'].widget.attrs['readonly'] = True
        self.fields['invoice_number'].widget.attrs['readonly'] = True
        self.fields['discount_rate'].widget.attrs['readonly'] = True
        self.fields['sales_account_number'].widget.attrs['readonly'] = True
        self.fields['profit_amount'].widget.attrs['readonly'] = True
        self.fields['discount_amount'].widget.attrs['readonly'] = True
        self.fields['stock_available'].widget.attrs['readonly'] = True
        self.fields['stock_available'].initial = ""
        self.fields['stock_available'].required = False

        try:
            edit_param = Application_Settings.objects.get()
        except Exception as e:
            edit_param = None
            print('Application Settings Not Define')

        if edit_param is not None:
            if edit_param.sales_price_editable:
                self.fields['product_price'].widget.attrs['readonly'] = False

            if edit_param.sales_discount_rate_editable:
                self.fields['discount_rate'].widget.attrs['readonly'] = False

            if edit_param.sales_discount_amount_editable:
                self.fields['discount_amount'].widget.attrs['readonly'] = False

        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['product_price'].widget.attrs['readonly'] = True
            self.fields['discount_rate'].widget.attrs['readonly'] = True
            self.fields['discount_amount'].widget.attrs['readonly'] = True
            self.fields['product_id'].widget.attrs['readonly'] = True
            self.fields['product_name'].widget.attrs['readonly'] = True
            self.fields['quantity'].widget.attrs['readonly'] = True

    class Meta:
        model = Srstage_Details_Temp

        fields = ['invoice_number', 'product_id', 'product_name', 'serial_no', 'service_type', 'service_start_date',
                  'service_end_date', 'service_card_no', 'product_price', 'quantity', 'total_price', 'profit_amount', 'discount_rate',
                  'discount_amount', 'status', 'comments', 'sales_account_number', 'details_branch_code', 'product_model',
                  'product_bar_code', 'details_branch_code']

        widgets = {
            'profit_amount': forms.HiddenInput(),
            'sales_account_number': forms.HiddenInput(),
            'details_branch_code': forms.HiddenInput(),
            'product_model': forms.HiddenInput(),
            'product_name': forms.HiddenInput(),
            'service_start_date': DateInput(),
            'service_end_date': DateInput(),
            'comments': Textarea(attrs={'rows': 2, 'cols': 60, }),
        }

        labels = {
            "product_id": _("Product Code"),
            "service_type": _("Service Type"),
            "service_start_date": _("Service Start Date"),
            "service_end_date": _("Service End Date"),
            "service_card_no": _("Service Card Number"),
            "product_price": _("Price"),
            "quantity": _("Quantity"),
            "total_price": _("Total Price"),
            "discount_rate": _("Discount Rate"),
            "discount_amount": _("Discount Amount"),
            "comments": _("Comments"),
            "product_model": _("Product Model"),
            "product_bar_code": _("Barcode"),
        }


class SalesDetailsModelFormEdit(forms.ModelForm):

    product_name = forms.CharField(label='Product Name', initial="",)
    stock_available = forms.IntegerField(label='Available Stock', initial="",)

    def __init__(self, *args, **kwargs):
        super(SalesDetailsModelFormEdit, self).__init__(*args, **kwargs)
        self.fields['total_price'].widget.attrs['readonly'] = True
        self.fields['product_price'].widget.attrs['readonly'] = True
        self.fields['invoice_number'].widget.attrs['readonly'] = True
        self.fields['discount_rate'].widget.attrs['readonly'] = True
        self.fields['sales_account_number'].widget.attrs['readonly'] = True
        self.fields['profit_amount'].widget.attrs['readonly'] = True
        self.fields['discount_amount'].widget.attrs['readonly'] = True
        self.fields['product_name'].widget.attrs['readonly'] = True
        self.fields['product_name'].initial = ""
        self.fields['product_name'].required = False
        self.fields['stock_available'].widget.attrs['readonly'] = True
        self.fields['stock_available'].initial = ""
        self.fields['stock_available'].required = False

        try:
            edit_param = Application_Settings.objects.get()
        except Exception as e:
            print('Application Settings Not Define')

        if edit_param.sales_price_editable:
            self.fields['product_price'].widget.attrs['readonly'] = False

        if edit_param.sales_discount_rate_editable:
            self.fields['discount_rate'].widget.attrs['readonly'] = False

        if edit_param.sales_discount_amount_editable:
            self.fields['discount_amount'].widget.attrs['readonly'] = False

        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['product_price'].widget.attrs['readonly'] = True
            self.fields['discount_rate'].widget.attrs['readonly'] = True
            self.fields['discount_amount'].widget.attrs['readonly'] = True
            self.fields['product_id'].widget.attrs['readonly'] = True
            self.fields['product_name'].widget.attrs['readonly'] = True
            self.fields['quantity'].widget.attrs['readonly'] = True

    class Meta:
        model = Srstage_Details_Temp

        fields = ['invoice_number', 'product_id', 'product_name', 'serial_no', 'service_type', 'service_start_date', 'service_end_date', 'service_card_no',
                  'product_price', 'quantity', 'total_price', 'profit_amount', 'discount_rate', 'discount_amount', 'status', 'comments', 'sales_account_number', ]

        widgets = {
            'profit_amount': forms.HiddenInput(),
            'sales_account_number': forms.HiddenInput(),
            'service_start_date': DateInput(),
            'service_end_date': DateInput(),
            'comments': Textarea(attrs={'rows': 2, 'cols': 60, }),
        }

        labels = {
            "product_id": _("Product Code"),
            "service_type": _("Service Type"),
            "service_start_date": _("Service Start Date"),
            "service_end_date": _("Service End Date"),
            "service_card_no": _("Service Card Number"),
            "product_price": _("Price"),
            "quantity": _("Quantity"),
            "total_price": _("Total Price"),
            "discount_rate": _("Discount Rate"),
            "discount_amount": _("Discount Amount"),
            "comments": _("Comments"),
        }


class ClientCenterTransfer(forms.Form):
    branch_code = ChoiceFieldNoValidation(
        required=False, label='Branch Name', choices=[('', '------------')], initial="")
    client_id = ChoiceFieldNoValidation(required=False, label='Customer Name', choices=[
                                        ('', '------------')], initial="")
    present_center_code = ChoiceFieldNoValidation(
        required=False, label='Present Center', choices=[('', '------------')], initial="")
    new_center_code = ChoiceFieldNoValidation(
        required=False, label='Transfer Center', choices=[('', '------------')], initial="")


class Sales_Return_PacketForm(forms.ModelForm):
    client_id = ChoiceFieldNoValidation(required=False, label='Customer Name', choices=[
                                        ('', '------------')], initial="")
    product_id = ChoiceFieldNoValidation(required=False, label='Product Name', choices=[
                                         ('', '------------')], initial="")
    employee_id = ChoiceFieldNoValidation(
        required=False, label='Executive Name', choices=[('', '------------')], initial="")

    def __init__(self, *args, **kwargs):
        super(Sales_Return_PacketForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Sales_Return_Packet
        fields = ['branch_code', 'client_id', 'product_id', 'return_date', 'tran_type_code',
                  'tran_batch_number', 'receive_quantity', 'receive_value', 'status', 'employee_id']
        labels = {
            'product_id': _('Product Name'),


        }


class SR_Target_master_Form(forms.ModelForm):
    employee_id=ChoiceFieldNoValidation(required=True,label=' Employee',choices=[('','Select Employee')],initial="")

    class Meta:
        model = SR_Target
        fields = ['transaction_id', 'employee_id', 'target_from_date','branch_code',
                  'target_to_date', 'target_amount', 'comments', 'target_type', ]

        widgets = {
            'comments': Textarea(attrs={'rows': 1, 'cols': 60, }),
            'target_from_date': DateInput(),
            'target_to_date': DateInput

        }

        labels = {
            "transaction_id": _("Transaction Id"),

            "target_from_date": _("Form Date"),
            "target_to_date": _("To Date"),
            "target_amount": _(" Target Amount"),
            "comments": _("Comments "),
            "target_type": _("Target Type"),

        }


class SR_Target_Details_Form(forms.ModelForm):

    product_id=ChoiceFieldNoValidation(required=True,label=' Product',choices=[('','Select Product')],initial="")
    unit_id=ChoiceFieldNoValidation(required=True,label=' Unit',choices=[('','Select Unit')],initial="")
    def __init__(self, *args, **kwargs):
        super(SR_Target_Details_Form, self).__init__(*args, **kwargs)
        self.fields['unit_id'].required = True
    class Meta:
        model = SR_Target_Details_Temp
        fields = ['transaction_id', 'product_id',  'unit_id',  'total_quantity', 'unit_price',
                  'total_price', 'is_deleted']

        labels = {
            "transaction_id": _("Transaction Id"),
            "total_quantity": _("Quantity "),
            "unit_price": _("Unit Price"),
            "total_price": _("Total Price"),
            'is_deleted' : _("Status")

        }
