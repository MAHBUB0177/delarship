from datetime import date
from logging import exception
from django import forms
from crispy_forms.layout import Field
from django.forms import ModelForm, TextInput, Select, Textarea, IntegerField, ChoiceField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.widgets import HiddenInput, Widget
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
    ('CN', 'Region Wise'),
    ('IN', 'Invoice Wise')
)

class DateInput(forms.DateInput):
    input_type = 'date'


class ChoiceFieldNoValidation(ChoiceField):
    def validate(self, value):
        pass


class clients_model_form(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    center_code = ChoiceFieldNoValidation(label="Region Name", required=False)
    client_type = ChoiceFieldNoValidation(label="Clients Type", required=True)
    transaction_doc_number = forms.CharField(label="Memo Number", required=False)

    def __init__(self, *args, **kwargs):
        super(clients_model_form, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['branch_code'].required = False

    class Meta:
        model = Clients
        fields = ['client_name', 'client_type', 'client_father_name', 'client_mother_name', 'branch_code','client_referred_by',
                  'client_blood_group', 'client_sex', 'client_religion', 'client_marital_status', 'client_national_id',
                  'client_present_address', 'client_permanent_address', 'client_phone', 'client_email', 'client_joining_date',
                  'client_education', 'client_date_of_birth', 'client_birth_place', 'client_monthly_income', 'client_annual_income',
                  'client_admit_fee', 'center_code']

        widgets = {
            'client_present_address': Textarea(attrs={'rows': 2, 'cols': 60, }),
            'client_permanent_address': Textarea(attrs={'rows': 2, 'cols': 60, }),
            'client_date_of_birth': DateInput(),
            'client_joining_date': DateInput(),
        }

        labels = {
            "client_name": _("Clients Name"),
            "center_code": _("Region Name"),
            "client_type": _("Clients Type"),
            "client_father_name": _("Father Name"),
            "client_mother_name": _("Mothers Name"),
            "client_blood_group": _("Blood Group"),
            "client_sex": _("Gender"),
            "client_religion": _("Religion"),
            "client_marital_status": _("Marital Status"),
            "client_national_id": _("National ID"),
            "client_present_address": _("Present Address"),
            "client_permanent_address": _("Permanent Address"),
            "client_phone": _("Mobile"),
            "client_email": _("Email"),
            "client_joining_date": _("Open Date"),
            "client_education": _("Education"),
            "client_date_of_birth": _("Birth Date"),
            "client_birth_place": _("Birthday Place"),
            "client_monthly_income": _("Monthly Sales"),
            "client_annual_income": _("Annual Sales"),
            "client_admit_fee": _("Admission Fee"),
            "branch_code": _("Branch Name"),
            "client_referred_by": _("Referred By"),
        }


class ClientSearch(forms.Form):
    client_name = forms.CharField(label="Client Name", widget=forms.TextInput(
        attrs={'placeholder': '',  'id': 'id_client_name'}
    ), required=False)
    client_id = forms.CharField(label="Client ID", widget=forms.TextInput(
        attrs={'placeholder': '',  'id': 'id_client_id'}
    ), required=False)
    client_phone = forms.CharField(label="Client Phone", widget=forms.TextInput(
        attrs={'placeholder': '',  'id': 'id_client_phone'}
    ), required=False)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    center_code = ChoiceFieldNoValidation(label="Region Name", required=False)


class ClientDocumentsModelForms(forms.ModelForm):
    class Meta:
        model = Client_Photo_Sign
        fields = ['client_id', 'document_type', 'document_location', ]

        labels = {
            "client_id": _("Phone Number"),
            "document_type": _("Document Type"),
            "document_location": _("Image"),
        }


class Supplier_Model_Form(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)

    def __init__(self, *args, **kwargs):
        super(Supplier_Model_Form, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['branch_code'].required = False

    class Meta:
        model = Supplier_Information
        fields = ['supp_name', 'proprietor_name', 'supp_address', 'supp_mobile', 'supp_email', 'supp_web', 'supp_key_person', 'supp_fax',
                  'branch_code', 'supp_grade','joining_date']

        widgets = {
            'supp_address': Textarea(attrs={'rows': 2, 'cols': 60, }),
            'joining_date': DateInput(),
        }

        labels = {
            "supp_id": _("Supplier ID"),
            "joining_date": _("Supplier Open Date"),
            "supp_name": _("Supplier Name"),
            "proprietor_name": _("Proprietor Name"),
            "supp_address": _("Supplier Address"),
            "supp_mobile": _("Mobile Number"),
            "supp_email": _("Email Address"),
            "supp_web": _("Web Address"),
            "supp_key_person": _("Contact Person Name"),
            "supp_fax": _("FAX Number"),
            "supp_grade": _("Supplier Grade"),
            "branch_code": _("Branch Name")
        }


class Products_Group_Form(forms.ModelForm):
    class Meta:
        model = Products_Group
        fields = ['group_name', 'is_active']

        labels = {
            "group_name": _("Group Name"),
            "is_active": _("Is Active"),
        }


class Products_Brand_Form(forms.ModelForm):
    class Meta:
        model = Products_Brand
        fields = ['brand_name', 'is_active']

        labels = {
            "group_name": _("Brand Name"),
            "is_active": _("Is Active"),
        }
class Products_Unit_Form(forms.ModelForm):
    class Meta:
        model = Products_Unit
        fields = ['unit_name', 'is_active']

        labels = {
            "unit_name": _("Unit Name"),
            "is_active": _("Is Active"),
        }

class ProductsModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductsModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['product_group'].initial = instance.product_group
            self.fields['brand_id'].initial = instance.brand_id

    class Meta:
        model = products
        fields = ["product_name", "product_model", "product_group", "product_purces_price", "product_sales_price", "product_tax_rate", "product_stock_alert",
                  "product_life_time", "product_status", "product_narration", "sales_discount_type", "sales_discount_percent",
                  "sales_discount_maxamt", "sales_discount_minamt", "sales_discount_fromdt", "sales_discount_uptodt", "brand_id",
                  'product_bar_code', "is_active", "emi_sales_price", "whole_sales_price"]

        widgets = {
            'product_naration': Textarea(attrs={'rows': 2, 'cols': 60, }),
            'sales_discount_fromdt': DateInput(),
            'sales_discount_uptodt': DateInput(),
        }

        labels = {
            "product_name": _("Product Name"),
            "product_model": _("Product Model"),
            "brand_id": _("Product Brand"),
            "product_group": _("Product Group"),
            "product_purces_price": _("Purchase Price"),
            "product_sales_price": _("Sales Price"),
            "product_tax_rate": _("Tax Rate"),
            "product_stock_alert": _("Stock Alert"),
            "product_life_time": _("Product Life (Days)"),
            "product_status": _("Status"),
            "product_narration": _("Product Description"),
            "sales_discount_type": _("Discount Type"),
            "sales_discount_percent": _("Discount Percent"),
            "sales_discount_maxamt": _("Discount Amount"),
            "sales_discount_minamt": _("Discount Minimum Amount"),
            "sales_discount_fromdt": _("Discount From Date"),
            "sales_discount_uptodt": _("Discount Upto Date"),
            "product_stock_gl": _("Stock Ledger"),
            "product_sales_gl": _("Sales Ledger"),
            "product_order_gl": _("Order Ledger"),
            "product_profit_gl": _("Profit Ledger"),
            "product_loss_gl": _("Loss Ledger"),
            "product_bar_code": _("Barcode"),
            "branch_code": _("Branch Name"),
            "is_active": _("Is Active"),
            "whole_sales_price": _("Wholesale Price"),
            "emi_sales_price": _("EMI Price"),
        }

class Products_Search_Forms(forms.Form):
    product_name = forms.CharField(label="Product Name", widget=forms.TextInput(
        attrs={'placeholder': '',  'id': 'id_product_name'}
    ), required=False)
    product_model = forms.CharField(label="Product Model", widget=forms.TextInput(
        attrs={'placeholder': '',  'id': 'id_product_model'}
    ), required=False)
    product_bar_code = forms.CharField(label="Products Barcode", widget=forms.TextInput(
        attrs={'placeholder': '',  'id': 'id_product_bar_code'}
    ), required=False)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    group_id = ChoiceFieldNoValidation(label="Group Name", required=False)
    brand_id = ChoiceFieldNoValidation(label="Brand Name", required=False)

class Sales_Purchase_Master_Form(forms.ModelForm):
    show_room_list = []
    show_room = ChoiceFieldNoValidation(
        required=False, label='Show Room', choices=show_room_list)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    account_number = ChoiceFieldNoValidation(
        label="Supplier Name", required=False)
    receipt_payment_ledger = ChoiceFieldNoValidation(
        label="Payment Method", required=False)

    def __init__(self, *args, **kwargs):
        super(Sales_Purchase_Master_Form, self).__init__(*args, **kwargs)
        self.fields['total_quantity'].widget.attrs['readonly'] = True
        self.fields['total_price'].widget.attrs['readonly'] = True
        self.fields['supplier_id'].required = False

    class Meta:
        model = StockMaster
        fields = ["branch_code", "supplier_id", "stock_date", "voucher_number", "show_room", "total_pay", "payment_comments", "total_quantity",
                  "total_price", "due_amount", "comments", "discount_amount", "account_number"]
        widgets = {
            'comments': Textarea(attrs={'rows': 1, 'cols': 60, }),
            'stock_date': DateInput(),
        }

        labels = {
            "voucher_number": _("Voucher Number"),
            "stock_date": _("Purchase Date"),
            "show_room": _("Show Room"),
            "discount_amount": _("Discount Receive"),
            "total_quantity": _("Total Quantity"),
            "total_price": _("Total Price"),
            "branch_code": _("Branch Name"),
        }


class Sales_Purchase_Details_Form(forms.ModelForm):
    dtl_total_price = forms.DecimalField(label='Total Price', initial="",)

    def __init__(self, *args, **kwargs):
        super(Sales_Purchase_Details_Form, self).__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs['readonly'] = True
        self.fields['product_model'].widget.attrs['readonly'] = True

    class Meta:
        model = StockDetailsTemp
        fields = ['product_name', 'quantity', 'product_id', 'product_bar_code', 'product_model', 'purces_price', 'total_price',
                  'discount_amount', ]

        widgets = {
            'product_model': forms.HiddenInput(),
        }

        labels = {
            "product_id": _("Product Name"),
            "product_name": _("Product Name"),
            "product_model": _("Product Model"),
            "quantity": _("Quantity"),
            "product_bar_code": _("Barcode"),
            "purces_price": _("Purchase Rate"),
            "total_price": _("Total Price"),
            "discount_amount": _("Discount Amount"),
        }


class StockMasterAuthQForm(forms.ModelForm):
    supplier_name = forms.CharField(label='Supplier Name', initial="",)
    total_price_after_disc = forms.DecimalField(
        label='Price After Discount', initial=0.00,)
    tran_type_code = ChoiceFieldNoValidation(
        required=True, label='Payment Type', choices=[])
    supplier_id = ChoiceFieldNoValidation(
        required=True, label='Supplier', choices=[])
    account_number = ChoiceFieldNoValidation(
        required=False, label='Select Supplier', choices=[])

    def __init__(self, *args, **kwargs):
        super(StockMasterAuthQForm, self).__init__(*args, **kwargs)
        self.fields['total_quantity'].widget.attrs['readonly'] = True
        self.fields['stock_date'].widget.attrs['readonly'] = True
        self.fields['show_room'].widget.attrs['readonly'] = True
        self.fields['total_price'].widget.attrs['readonly'] = True
        self.fields['due_amount'].widget.attrs['readonly'] = True
        self.fields['total_price_after_disc'].widget.attrs['readonly'] = True
        self.fields['discount_amount'].widget.attrs['readonly'] = True
        self.fields['tran_type_code'].initial = "CS"
        self.fields['supplier_name'].widget.attrs['readonly'] = True
        self.fields['supplier_name'].initial = ""
        self.fields['supplier_name'].required = False
        self.fields['supplier_id'].required = False

    class Meta:
        model = StockMasterAuthQ
        fields = ["supplier_id", "stock_date", "voucher_number", "show_room", "tran_type_code", "total_pay", "payment_comments", "total_quantity",
                  "total_price", "due_amount", "comments", "stock_id", "branch_code", "discount_amount", ]
        widgets = {
            'comments': Textarea(attrs={'rows': 1, 'cols': 60, }),
            'stock_date': DateInput(),
            'stock_id': forms.HiddenInput(),
            'branch_code': forms.HiddenInput(),
            'show_room': forms.HiddenInput(),
        }
        labels = {
            "voucher_number": _("Voucher Number"),
            "stock_date": _("Purchase Date"),
            "supplier_id": _("Supplier ID"),
            "show_room": _("Show Room"),
            "tran_type_code": _("Payment Type"),
            "total_pay": _("Total Pay"),
            "payment_comments": _("Payment Details"),
            "total_quantity": _("Quantity"),
            "total_price": _("Total Price"),
            "due_amount": _("Due Amount"),
            "discount_amount": _("Discount Receive"),
        }


class Search_Purchase_List(forms.Form):
    stock_id = forms.CharField(label="Purchase ID", widget=forms.TextInput(
        attrs={'id': 'id_stock_id'}
    ), required=False)
    from_date = forms.DateField(
        label="Purchase From Date", widget=DateInput(), required=True)
    upto_date = forms.DateField(
        label="Purchase Upto Date", widget=DateInput(), required=True)
    stock_date = forms.DateField(
        label="Purchase Date", widget=DateInput(), required=True)
    product_id = forms.CharField(label="Product ID", widget=forms.TextInput(
        attrs={'id': 'id_product_id'}
    ), required=False)
    supplier_phone = forms.CharField(label="Supplier Phone", widget=forms.TextInput(
        attrs={'id': 'id_supplier_phone'}
    ), required=False)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)

class Search_Damage_List(forms.Form):
    from_date = forms.DateField(
        label="Damage From Date", widget=DateInput(), required=True)
    upto_date = forms.DateField(
        label="Damage Upto Date", widget=DateInput(), required=True)
    product_id = forms.CharField(label="Product ID", widget=forms.TextInput(
        attrs={'id': 'id_product_id'}
    ), required=False)
    supplier_id = ChoiceFieldNoValidation(required=True, label='Select Supplier', choices=[('', '------------')], initial="")
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)

class Search_Sales_Return_List(forms.Form):
    from_date = forms.DateField(
        label="Damage From Date", widget=DateInput(), required=True)
    upto_date = forms.DateField(
        label="Damage Upto Date", widget=DateInput(), required=True)
    product_id = forms.CharField(label="Product ID", widget=forms.TextInput(
        attrs={'id': 'id_product_id'}
    ), required=False)
    client_id = ChoiceFieldNoValidation(required=True, label='Select Customer', choices=[('', '------------')], initial="")
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    center_code = ChoiceFieldNoValidation(label="Region Name", required=False)

class SalesMasterModelForm(forms.ModelForm):
    executive_name = forms.CharField(label='Executive Name', initial="",)
    input_account_number = forms.CharField(
        label='Account Number', initial="", widget=forms.HiddenInput())
    account_number = ChoiceFieldNoValidation(
        required=True, label='Select Customer', choices=[('', '------------')], initial="")
    tran_type_list = []
    type_code = ChoiceFieldNoValidation(
        required=True, label='Payment Type', choices=tran_type_list)
    branch_code = ChoiceFieldNoValidation(
        label="Branch Name", required=False, initial="----------")
    center_code = ChoiceFieldNoValidation(
        label="Region Name", required=False, choices=[('', '------------')], initial="")
    employee_id = ChoiceFieldNoValidation(
        label="Executive Name", required=False, choices=[('', '------------')], initial="")

    def __init__(self, *args, **kwargs):
        super(SalesMasterModelForm, self).__init__(*args, **kwargs)
        self.fields['total_quantity'].widget.attrs['readonly'] = True
        self.fields['bill_amount'].widget.attrs['readonly'] = True
        self.fields['due_amount'].widget.attrs['readonly'] = True
        self.fields['advance_pay'].widget.attrs['readonly'] = True
        self.fields['total_bill_amount'].widget.attrs['readonly'] = True
        self.fields['executive_name'].widget.attrs['readonly'] = True
        self.fields['executive_name'].initial = ""
        self.fields['pay_amount'].initial = ""
        self.fields['executive_name'].required = False
        self.fields['type_code'].initial = "CS"
        self.fields['type_code'].required = False
        self.fields['account_number'].required = False
        self.fields['input_account_number'].required = False
        self.fields['input_account_number'].widget.attrs['readonly'] = True
        self.fields['employee_id'].widget.attrs['readonly'] = True

        try:
            param = Application_Settings.objects.get()
        except Exception as e:
            print('Application Settings Not Define')

        if param.sales_executive_phone_editable:
            self.fields['employee_id'].widget.attrs['readonly'] = False
        if param.payment_document_mandatory:
            self.fields['payment_document'].required = True

    class Meta:
        model = Sales_Master
        fields = ['invoice_number', 'invoice_date', 'customer_id', 'customer_name', 'customer_phone', 'customer_address', 'employee_id', 'total_quantity',
                  'total_bill_amount', 'bill_amount', 'pay_amount', 'due_amount', 'advance_pay', 'total_discount_rate', 'total_discount_amount', 'status', 'invoice_comments', 'latitude', 'longitude', 'tran_type_code', 'branch_code', 'payment_document', 'email_notification',
                  'sms_notification', 'invoice_discount']

        widgets = {
            'customer_id': forms.HiddenInput(),
            'customer_phone': forms.HiddenInput(),
            'total_quantity': forms.HiddenInput(),
            'total_bill_amount': forms.HiddenInput(),
            'bill_amount': forms.HiddenInput(),
            'due_amount': forms.HiddenInput(),
            'tran_type_code': forms.HiddenInput(),
            'advance_pay': forms.HiddenInput(),
            'total_discount_rate': forms.HiddenInput(),
            'total_discount_amount': forms.HiddenInput(),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'invoice_date': DateInput(),
            #'employee_id': forms.HiddenInput(),
            'payment_document': forms.HiddenInput(),
            'input_account_number': forms.HiddenInput(),
            'email_notification': forms.HiddenInput(),
            'sms_notification': forms.HiddenInput(),
        }

        sales_payment_document_lebel = None

        try:
            edit_param = Application_Settings.objects.get()
            sales_payment_document_lebel = edit_param.sales_payment_document_lebel
        except Exception as e:
            edit_param = None
            print('Application Settings Not Define')

        labels = {
            "invoice_date": _("Invoice Date"),
            "customer_id": _("Client ID"),
            "customer_name": _("Client Name"),
            "customer_phone": _("Client Phone"),
            "customer_address": _("Address"),
            "employee_id": _("Executive Phone"),
            "payment_document": _(sales_payment_document_lebel),
            "tran_type_code": _("Payment Method"),
            "total_quantity": _("Quantity"),
            "total_bill_amount": _("Total Bill"),
            "bill_amount": _("Bill After Discount"),
            "pay_amount": _("Total Receive Amount"),
            "due_amount": _("Due Amount"),
            "advance_pay": _("Advance Pay"),
            "total_discount_rate": _("Dis Rate"),
            "total_discount_amount": _("Dis Amount"),
            "invoice_comments": _("Comments"),
            "latitude": _("Latitude"),
            "longitude": _("Longitude"),
            "invoice_discount": _("Invoice Discount"),
            "email_notification": _("Send Email"),
            "sms_notification": _("Send SMS"),
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
        model = Sales_Details_Temp

        fields = ['invoice_number', 'product_id', 'product_name', 'serial_no', 'service_type', 'service_start_date', 'service_end_date', 'service_card_no', 'product_price', 'quantity', 'total_price', 'profit_amount', 'discount_rate', 'discount_amount', 'status', 'comments', 'sales_account_number',
                  'details_branch_code', 'product_model', 'product_bar_code', 'details_branch_code']

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
        model = Sales_Details_Temp

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


class QuickSalesModelForm(forms.ModelForm):
    executive_name = forms.CharField(label='Executive Name', initial="",)
    input_account_number = forms.CharField(
        label='Account Number', initial="", widget=forms.HiddenInput())
    account_number = forms.CharField(
        label='Account Number', initial="-----------", widget=forms.HiddenInput())
    tran_type_list = []
    type_code = forms.CharField(
        label='Payment Type', initial="", widget=forms.HiddenInput())
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    center_code = ChoiceFieldNoValidation(
        label="Region Name", required=False, initial="----------", widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(QuickSalesModelForm, self).__init__(*args, **kwargs)
        self.fields['total_quantity'].widget.attrs['readonly'] = True
        self.fields['bill_amount'].widget.attrs['readonly'] = True
        self.fields['due_amount'].widget.attrs['readonly'] = True
        self.fields['advance_pay'].widget.attrs['readonly'] = True
        self.fields['total_bill_amount'].widget.attrs['readonly'] = True
        self.fields['executive_name'].widget.attrs['readonly'] = True
        self.fields['executive_name'].initial = ""
        self.fields['pay_amount'].initial = ""
        self.fields['executive_name'].required = False
        self.fields['type_code'].initial = "CS"
        self.fields['type_code'].required = False
        self.fields['account_number'].required = False
        self.fields['input_account_number'].required = False
        self.fields['input_account_number'].widget.attrs['readonly'] = True
        self.fields['account_number'].widget.attrs['readonly'] = True
        self.fields['employee_id'].widget.attrs['readonly'] = True

        try:
            param = Application_Settings.objects.get()
        except Exception as e:
            print('Application Settings Not Define')

        if param.sales_executive_phone_editable:
            self.fields['employee_id'].widget.attrs['readonly'] = False
        if param.payment_document_mandatory:
            self.fields['payment_document'].required = True

    class Meta:
        model = Sales_Master
        fields = ['invoice_number', 'invoice_date', 'customer_id', 'customer_name', 'customer_phone', 'customer_address', 'employee_id', 'total_quantity',
                  'total_bill_amount', 'bill_amount', 'pay_amount', 'due_amount', 'advance_pay', 'total_discount_rate', 'total_discount_amount', 'status', 'invoice_comments', 'latitude', 'longitude', 'tran_type_code', 'branch_code', 'payment_document', 'email_notification',
                  'sms_notification', 'invoice_discount']

        widgets = {
            'customer_id': forms.HiddenInput(),
            'total_quantity': forms.HiddenInput(),
            'total_bill_amount': forms.HiddenInput(),
            'bill_amount': forms.HiddenInput(),
            'due_amount': forms.HiddenInput(),
            'tran_type_code': forms.HiddenInput(),
            'advance_pay': forms.HiddenInput(),
            'total_discount_rate': forms.HiddenInput(),
            'total_discount_amount': forms.HiddenInput(),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'invoice_date': DateInput(),
            'employee_id': forms.HiddenInput(),
            'payment_document': forms.HiddenInput(),
            'type_code': forms.HiddenInput(),
            'email_notification': forms.HiddenInput(),
            'sms_notification': forms.HiddenInput(),
            'type_code': forms.HiddenInput(),
        }

        sales_payment_document_lebel = None

        try:
            edit_param = Application_Settings.objects.get()
            sales_payment_document_lebel = edit_param.sales_payment_document_lebel
        except Exception as e:
            edit_param = None
            print('Application Settings Not Define')

        labels = {
            "invoice_date": _("Invoice Date"),
            "customer_id": _("Client ID"),
            "customer_name": _("Client Name"),
            "customer_phone": _("Client Phone"),
            "customer_address": _("Address"),
            "employee_id": _("Employee Name"),
            "payment_document": _(sales_payment_document_lebel),
            "tran_type_code": _("Payment Method"),
            "total_quantity": _("Quantity"),
            "total_bill_amount": _("Total Bill"),
            "bill_amount": _("Bill After Discount"),
            "pay_amount": _("Total Receive Amount"),
            "due_amount": _("Due Amount"),
            "advance_pay": _("Advance Pay"),
            "total_discount_rate": _("Dis Rate"),
            "total_discount_amount": _("Dis Amount"),
            "invoice_comments": _("Comments"),
            "latitude": _("Latitude"),
            "longitude": _("Longitude"),
            "invoice_discount": _("Invoice Discount"),
            "email_notification": _("Send Email"),
            "sms_notification": _("Send SMS"),
        }


class Emi_Setup_Model_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Emi_Setup_Model_Form, self).__init__(*args, **kwargs)
        self.fields['installment_tot_repay_amt'].widget.attrs['readonly'] = True
        self.fields['client_id'].widget.attrs['readonly'] = True
        self.fields['emi_reference_amount'].widget.attrs['readonly'] = True
        self.fields['total_emi_amount'].widget.attrs['readonly'] = True
        self.fields['installment_tot_repay_amt'].widget.attrs['readonly'] = True
        self.fields['emi_inst_amount'].widget.attrs['readonly'] = True
        self.fields['emi_profit_amount'].widget.attrs['readonly'] = True
        self.fields['reference_due_amount'].widget.attrs['readonly'] = True
        self.fields['emi_reference_date'].widget.attrs['readonly'] = True
        self.fields['installment_exp_date'].widget.attrs['readonly'] = True
        self.fields['emi_down_amount'].initial = ""
        instance = getattr(self, 'instance', None)

        try:
            param = EMI_Settings.objects.get()
        except Exception as e:
            param = None
            print('EMI Settings Not Define')

        if param:

            if param.emi_fee_auto:
                self.fields['emi_fee_amount'].widget.attrs['readonly'] = True

            if param.emi_insurance_readonly:
                self.fields['emi_ins_fee_amount'].widget.attrs['readonly'] = True
                self.fields['emi_ins_rate'].widget.attrs['readonly'] = True

            if instance and instance.pk:
                self.fields['installment_tot_repay_amt'].widget.attrs['readonly'] = True
                self.fields['client_id'].widget.attrs['readonly'] = True
                self.fields['emi_reference_amount'].widget.attrs['readonly'] = True
                self.fields['total_emi_amount'].widget.attrs['readonly'] = True
                self.fields['installment_tot_repay_amt'].widget.attrs['readonly'] = True
                self.fields['emi_inst_amount'].widget.attrs['readonly'] = True
                self.fields['emi_fee_amount'].widget.attrs['readonly'] = True
                self.fields['reference_due_amount'].widget.attrs['readonly'] = True
                self.fields['emi_reference_date'].widget.attrs['readonly'] = True

            if param.emi_fee_auto:
                self.fields['emi_fee_amount'].widget.attrs['readonly'] = True
  
    class Meta:
        model = Emi_Setup
        fields = ['emi_reference_no', 'emi_reference_date', 'emi_reference_amount', 'emi_down_amount', 'client_id',
                  'reference_due_amount', 'total_emi_amount', 'total_emi_due', 'emi_inst_amount', 'emi_inst_frequency',
                  'emi_inst_repay_from_date', 'number_of_installment', 'installment_tot_repay_amt', 'installment_exp_date',
                  'emi_rate', 'emi_profit_amount', 'emi_fee_amount', 'emi_ins_rate', 'emi_ins_fee_amount', 'emi_doc_fee_amount', ]

        widgets = {
            'emi_reference_date': DateInput(),
            'installment_exp_date': DateInput(),
            'emi_inst_repay_from_date': DateInput(),
        }

        try:
            param = EMI_Settings.objects.get()
        except Exception as e:
            param = None
            print('EMI Settings Not Define')
        
        print(param)
        
        if param:
            if not param.emi_fee_auto:
                widgets['emi_fee_amount'] = forms.HiddenInput()

            if not param.emi_down_payment:
                widgets['emi_down_amount'] = forms.HiddenInput()

            if not param.emi_doc_fee_enable:
                widgets['emi_doc_fee_amount'] = forms.HiddenInput()

            if not param.emi_insurance_enable:
                widgets['emi_ins_fee_amount'] = forms.HiddenInput()
                widgets['emi_ins_rate'] = forms.HiddenInput()

        labels = {
            "emi_reference_no": _("Invoice Number"),
            "emi_reference_date": _("Invoice Date"),
            "reference_due_amount": _("Invoice Due Amount"),
            "client_id": _("Client ID"),
            "emi_reference_amount": _("Total Bill Amount"),
            "total_emi_amount": _("Total EMI Amount"),
            "instrepay_sl_num": _("Installment Serial"),
            "emi_inst_amount": _("Installment Amount"),
            "emi_inst_frequency": _("Installment Frequency"),
            "emi_inst_repay_from_date": _("1st Installment Date"),
            "number_of_installment": _("No of Installment"),
            "installment_tot_repay_amt": _("Total Installment"),
            "installment_exp_date": _("Installment Expiry Date"),
            "emi_rate": _("EMI Rate"),
            "emi_profit_amount": _("EMI Profit Amount"),
            "emi_fee_amount": _("EMI Form Fees"),
            "emi_ins_fee_amount": _("EMI Fee"),
            "emi_ins_rate": _("EMI Fee Rate"),
            "emi_down_amount": _("Down Payment"),
            "emi_doc_fee_amount": _("Document Fee"),
        }


class Emi_Receive_Model_Form(forms.ModelForm):
    emi_reference_no = ChoiceFieldNoValidation(label='Select Invoice', choices=[
                                               ('', 'Select Invoice')], initial="")
    account_number = ChoiceFieldNoValidation(label='Select Customer', choices=[
                                             ('', '------------')], initial="")
    client_name = forms.CharField(label='Client Name', initial="",)
    total_emi_amount = forms.CharField(label='Total EMI Amount', initial="",)
    number_of_installment = forms.CharField(
        label='Total Installment', initial="",)
    total_emi_payment = forms.CharField(label='Total EMI Paid', initial="",)
    total_emi_due = forms.CharField(label='Total EMI Due', initial="",)
    paid_installment_number = forms.CharField(
        label='Total Installment Paid', initial="",)

    def __init__(self, *args, **kwargs):
        super(Emi_Receive_Model_Form, self).__init__(*args, **kwargs)
        self.fields['client_name'].widget.attrs['readonly'] = True
        self.fields['client_name'].required = False
        self.fields['total_emi_amount'].widget.attrs['readonly'] = True
        self.fields['total_emi_amount'].required = False
        self.fields['number_of_installment'].widget.attrs['readonly'] = True
        self.fields['number_of_installment'].required = False
        self.fields['total_emi_payment'].widget.attrs['readonly'] = True
        self.fields['total_emi_payment'].required = False
        self.fields['total_emi_due'].widget.attrs['readonly'] = True
        self.fields['total_emi_due'].required = False
        self.fields['paid_installment_number'].widget.attrs['readonly'] = True
        self.fields['paid_installment_number'].required = False
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['branch_code'].widget.attrs['readonly'] = True
            self.fields['account_number'].widget.attrs['readonly'] = True
            self.fields['emi_reference_no'].required = False

    class Meta:
        model = Emi_Receive
        fields = ['branch_code', 'account_number', 'emi_reference_no',
                  'receive_date', 'entry_day_sl', 'receive_amount', 'receive_document_number']

        widgets = {
            'receive_date': DateInput(),
            'entry_day_sl': forms.HiddenInput(),
        }

        labels = {
            "branch_code": _("Branch Name"),
            "account_number": _("Select Customer"),
            "emi_reference_no": _("Invoice Number"),
            "receive_date": _("Installment Date"),
            "entry_day_sl": _("Installment Serial"),
            "receive_amount": _("Installment Amount"),
            "receive_document_number": _("Memo Number"),
        }


class PurchaseReturnModelForm(forms.ModelForm):

    product_name = forms.CharField(label='Product Name', initial="",)
    supplier_name = forms.CharField(label='Supplier Name', initial="",)
    product_id = ChoiceFieldNoValidation(label='Select Product', choices=[
                                         ('', 'Select Product')], initial="")
    supplier_account = ChoiceFieldNoValidation(label='Select Supplier', choices=[
                                               ('', 'Select Supplier')], initial="")
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)

    def __init__(self, *args, **kwargs):
        super(PurchaseReturnModelForm, self).__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs['readonly'] = True
        self.fields['product_name'].initial = ""
        self.fields['product_name'].required = False
        self.fields['supplier_name'].widget.attrs['readonly'] = True
        self.fields['supplier_name'].initial = ""
        self.fields['return_amount'].initial = ""
        self.fields['supplier_name'].required = False
        self.fields['supplier_id'].required = False

    class Meta:
        model = Stock_Return_Details
        fields = ["stock_id", "return_date", "product_id", "tran_batch_number", "returned_quantity", "return_amount", "return_voucher", "stock_date",
                  "return_reason", "stock_voucher", "supplier_id", 'branch_code']

        widgets = {
            'return_date': DateInput(),
            'stock_date': DateInput(),
            'return_reason': Textarea(attrs={'rows': 2, 'cols': 60, }),
        }

        labels = {"product_id": _("Product Code"),
                  "return_date": _("Return Date"),
                  "tran_batch_number": _("Batch Number"),
                  "returned_quantity": _("Quantity"),
                  "return_amount": _("Return Amount"),
                  "return_voucher": _("Return ID"),
                  "stock_date": _("Purchase Date"),
                  "stock_voucher": _("Purchase Invoice"),
                  "return_reason": _("Return Reason"),
                  "supplier_id": _("Supplier"),
                  "stock_id": _("Purchase ID"),
                  }

class Product_Damage_ModelForm(forms.ModelForm):
    product_id = ChoiceFieldNoValidation(label='Select Product', choices=[
                                         ('', '-----------')], initial="")
    supplier_account = ChoiceFieldNoValidation(label='Select Supplier', choices=[
                                               ('', '-----------')], initial="")
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)

    def __init__(self, *args, **kwargs):
        super(Product_Damage_ModelForm, self).__init__(*args, **kwargs)
        self.fields['damage_amount'].initial = ""
        self.fields['damage_amount'].widget.attrs['readonly'] = True
        self.fields['damage_amount'].required = True

    class Meta:
        model = Product_Damage_Details
        fields = ["branch_code", "product_id", "damage_date", "damage_quantity", "damage_amount","receive_amount","comments"]

        widgets = {
            'damage_date': DateInput(),
            'comments': Textarea(attrs={'rows': 2, 'cols': 60, }),
        }

        labels = {"product_id": _("Select Product"),
                  "damage_date": _("Damage Date"),
                  "damage_quantity": _("Damage Quantity"),
                  "damage_amount": _("Damage Value"),
                  "receive_amount": _("Receive Amount"),
                  "comments": _("Comments"),
                  }


class Emi_History_Query(forms.Form):
    emi_reference_no = ChoiceFieldNoValidation(label='Select Invoice', choices=[
                                               ('', 'Select Invoice')], initial="")
    account_number = ChoiceFieldNoValidation(label='Select Customer', choices=[
                                             ('', '------------')], initial="")
    from_date = forms.DateField(
        label="From Date", widget=DateInput(), required=True)
    upto_date = forms.DateField(
        label="Upto Date", widget=DateInput(), required=True)
    ason_date = forms.DateField(
        label="Due Date", widget=DateInput(), required=True)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    center_code = ChoiceFieldNoValidation(
        label="Region Name", required=False, choices=[('', '------------')], initial="")
    employee_id = ChoiceFieldNoValidation(
        label="Field Officer Name", required=False, choices=[('', '------------')], initial="")
    emi_reporting_type = ChoiceFieldNoValidation(
        label="Reporting Type", required=False, choices=[('DUE_ONLY', 'Due Only'),('FULL_PAY', 'Fully Paid')
        ,('ALL', 'All')], initial="DUE_ONLY")

class SalesReturnModelForm(forms.ModelForm):

    product_name = forms.CharField(label='Product Name', initial="",)
    product_id = ChoiceFieldNoValidation(label='Select Product', choices=[
                                         ('', 'Select Product')], initial="")
    account_number = ChoiceFieldNoValidation(label='Select Customer', choices=[
        ('', 'Select Customer')], initial="")
    sales_invoice = ChoiceFieldNoValidation(label='Select Invoice', choices=[
                                            ('', 'Select Invoice')], initial="")
    total_quantity = forms.IntegerField(label='Total Quantity', initial=0)
    total_bill_amount = forms.IntegerField(label='Total Bill', initial=0.00)

    def __init__(self, *args, **kwargs):
        super(SalesReturnModelForm, self).__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs['readonly'] = True
        self.fields['product_name'].initial = ""
        self.fields['product_name'].required = False
        self.fields['total_quantity'].widget.attrs['readonly'] = True
        self.fields['total_bill_amount'].widget.attrs['readonly'] = True
        self.fields['total_quantity'].required = False
        self.fields['total_bill_amount'].required = False

    class Meta:
        model = Sales_Return_Details
        fields = ["return_invoice", "return_date", "product_id", "tran_batch_number", "returned_quantity",
                  "return_amount", "sales_invoice", "sales_date", "return_reason", "client_id"]

        widgets = {
            'client_id': forms.HiddenInput(),
            'return_date': DateInput(),
            'sales_date': DateInput(),
            'return_reason': Textarea(attrs={'rows': 2, 'cols': 60, }),
        }

        labels = {"product_id": _("Product Code"),
                  "return_date": _("Return Date"),
                  "tran_batch_number": _("Batch Number"),
                  "returned_quantity": _("Return Quantity"),
                  "return_amount": _("Return Amount"),
                  "sales_invoice": _("Invoice Number"),
                  "sales_date": _("Sales Date"),
                  "return_reason": _("Return Reason"),
                  }


class OrderMasterModelForm(forms.ModelForm):
    employee_id = ChoiceFieldNoValidation(label='Executive Name',  required=True,choices=[('', '------------')], initial="")    
    input_account_number = forms.CharField(
        label='Account Number', initial="", widget=forms.HiddenInput())
    account_number = ChoiceFieldNoValidation(
        required=True, label='Select Customer', choices=[])
    tran_type_list = []
    type_code = forms.CharField(
        label='Payment Type', initial="", widget=forms.HiddenInput())
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    center_code = ChoiceFieldNoValidation(
        label="Region Name", required=False, choices=[('', '------------')], initial="")

    def __init__(self, *args, **kwargs):
        super(OrderMasterModelForm, self).__init__(*args, **kwargs)
        self.fields['total_quantity'].widget.attrs['readonly'] = True
        self.fields['bill_amount'].widget.attrs['readonly'] = True
        self.fields['due_amount'].widget.attrs['readonly'] = True
        self.fields['advance_pay'].widget.attrs['readonly'] = True
        self.fields['total_bill_amount'].widget.attrs['readonly'] = True
        self.fields['type_code'].widget.attrs['readonly'] = True
        self.fields['type_code'].required = False
        self.fields['input_account_number'].required = False
        self.fields['input_account_number'].widget.attrs['readonly'] = True
        self.fields['account_number'].required = False
        self.fields['order_date'].widget.attrs['readonly'] =True
        self.fields['employee_id'].required=True

    class Meta:
        model = Order_Master
        fields = ['order_number', 'order_date', 'customer_id', 'customer_name', 'customer_phone', 'customer_address', 
        'executive_phone', 'total_quantity','total_bill_amount', 'bill_amount', 'pay_amount', 'due_amount', 
        'advance_pay', 'total_discount_rate', 'total_discount_amount', 'status', 'order_comments', 'latitude', 
        'longitude', 'tran_type_code', 'employee_id','branch_code','center_code','delivary_date']

        widgets = {
            # 'employee_id': forms.HiddenInput(),
            'customer_id': forms.HiddenInput(),
            'executive_phone': forms.HiddenInput(),
            'total_quantity': forms.HiddenInput(),
            'total_bill_amount': forms.HiddenInput(),
            'bill_amount': forms.HiddenInput(),
            'due_amount': forms.HiddenInput(),
            'advance_pay': forms.HiddenInput(),
            'total_discount_rate': forms.HiddenInput(),
            'total_discount_amount': forms.HiddenInput(),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'order_date': DateInput(),
            'delivary_date':DateInput(),
            'input_account_number': forms.HiddenInput(),
            'type_code': forms.HiddenInput(),
            'tran_type_code': forms.HiddenInput(),
        }

        labels = {
            "invoice_date": _("Invoice Date"),
            "customer_id": _("Client ID"),
            "customer_name": _("Client Name"),
            "customer_phone": _("Client Phone"),
            "customer_address": _("Address"),
            "executive_phone": _("Executive Phone"),
            "total_quantity": _("Quantity"),
            "total_bill_amount": _("Total Bill"),
            "bill_amount": _("Bill After Discount"),
            "pay_amount": _("Total Receive Amount"),
            "due_amount": _("Due Amount"),
            "employee_id": _("Executive Name"),
            "advance_pay": _("Advance Pay"),
            "total_discount_rate": _("Dis Rate"),
            "total_discount_amount": _("Dis Amount"),
            "invoice_comments": _("Comments"),
            "latitude": _("Latitude"),
            "longitude": _("Longitude"),
        }


class InvoiceSearch(forms.Form):
    invoice_number = forms.CharField(label="Invoice Number", widget=forms.TextInput(
        attrs={'id': 'id_invoice_number'}
    ), required=False)
    return_invoice = forms.CharField(label="Return Invoice Number", widget=forms.TextInput(
        attrs={'id': 'id_return_invoice_number'}
    ), required=False)
    customer_phone = forms.CharField(label="Customer Phone", widget=forms.TextInput(
        attrs={'id': 'id_customer_phone'}
    ), required=False)
    product_id = ChoiceFieldNoValidation(required=False, label='Product Name', choices=[('', '------------')], initial="")
    employee_id = ChoiceFieldNoValidation(required=False, label='Employee Name', choices=[('', '------------')], initial="")
    invoice_date = forms.DateField(
        label="Invoice Date", widget=DateInput(), required=True)
    invoice_from_date = forms.DateField(
        label="Invoice From Date", widget=DateInput(), required=True)
    invoice_upto_date = forms.DateField(
        label="Invoice Upto Date", widget=DateInput(), required=True)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    center_code = ChoiceFieldNoValidation(label="Region Name", required=False)


class OrderSearchForm(forms.Form):
    order_number = forms.CharField(label="Order Number", widget=forms.TextInput(
        attrs={'id': 'id_order_number'}
    ), required=False)
    customer_phone = forms.CharField(label="Customer Phone", widget=forms.TextInput(
        attrs={'id': 'id_customer_phone'}
    ), required=False)
    executive_phone = forms.CharField(label="Executive Phone", widget=forms.TextInput(
        attrs={'id': 'id_executive_phone'}
    ), required=False)
    order_date = forms.DateField(
        label="Order Date", widget=DateInput(), required=True)
    from_date = forms.DateField(
        label="From Date", widget=DateInput(), required=True)
    upto_date = forms.DateField(
        label="Upto Date", widget=DateInput(), required=True)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    center_code = ChoiceFieldNoValidation(
        label="Region Name", required=False, choices=[('', '------------')], initial="")
    order_status = ChoiceFieldNoValidation(
        label="Order Status", required=True, choices=[('', 'All'),('P', 'Waiting For Acceptance'),('A', 'Waiting For Delivery')], initial="P")


class CommonReportForm(forms.Form):
    invoice_number = forms.CharField(
        label="Invoice Number", widget=forms.TextInput(), required=False)

    quotation_id=forms.CharField(
        label="quotation Number", widget=forms.TextInput(), required=False)
    order_number=forms.CharField(
        label="Order Number", widget=forms.TextInput(), required=False)
    phone_number = forms.CharField(
        label="Phone Number", widget=forms.TextInput(), required=False)
    account_number = ChoiceFieldNoValidation(label='Select Name', choices=[
        ('', 'Select Name')], initial="")
    customer_account = ChoiceFieldNoValidation(label='Select Customer', choices=[
                                               ('', 'Select Customer')], initial="")
    acc_type_code = forms.ChoiceField(
        label="Account Type", initial='A', widget=forms.Select(), required=False)
    product_id = forms.ChoiceField(label="Select Product", required=False, choices=[('', 'Select Product')], initial="",
                                   widget=forms.Select(attrs={'name': 'product_id', 'id': 'id_product_id'}))
    account_balance = forms.CharField(label="Current Balance", widget=forms.TextInput(
        attrs={'id': 'id_account_balance', 'readonly': 'readonly'}), required=False)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    center_code = forms.ChoiceField(label="Center Name", required=False,  choices=[
                                    ('', 'Select Center')], widget=forms.Select())
    order_date = forms.DateField(
        label="Order Date", widget=DateInput(), required=True)
    from_date = forms.DateField(
        label="From Date", widget=DateInput(), required=False)
    upto_date = forms.DateField(
        label="Upto Date", widget=DateInput(), required=False)
    ason_date = forms.DateField(
        label="Report Date", widget=DateInput(), required=False)
    user_name = forms.CharField(label="User Name", widget=forms.TextInput(
    ), required=False)
    employee_name = forms.ChoiceField(label="Employee Name", required=False, widget=forms.Select(
    ))
    employee_id = ChoiceFieldNoValidation(
        label="Employee Name", required=False, choices=[('', 'Select Employee')], initial="")
    client_id = ChoiceFieldNoValidation(required=False, label='Client Name', choices=[('', '------------')], initial="")
    transfer_tran = forms.ChoiceField(choices=YES_NO, label="Show Transfer Transaction", initial='Y', widget=forms.Select(
    ), required=True)
    posting_user = forms.CharField(label="Posting User ID", widget=forms.TextInput(
    ), required=False)
    sales_report_type = forms.ChoiceField(choices=SALES_REPORT_TYPE, label="Reporting Type", initial='DT', widget=forms.Select(
    ), required=True)
    group_id = ChoiceFieldNoValidation(label="Group Name", required=False)
    brand_id = ChoiceFieldNoValidation(label="Brand Name", required=False)
    stock_available = forms.ChoiceField(choices=YES_NO, label="Stock Available Only", initial='Y', widget=forms.Select(
    ), required=True)

class Client_Id_Changes_Form(forms.Form):
    branch_code = ChoiceFieldNoValidation(required=False, label='Branch Name', choices=[('', '------------')], initial="")
    client_id = ChoiceFieldNoValidation(required=False, label='Customer Name', choices=[('', '------------')], initial="")
    new_client_id = forms.CharField(label="New Customer ID", widget=forms.TextInput(), required=False)


class Client_Closing_ModelForm(forms.ModelForm):
    client_id = ChoiceFieldNoValidation(label='Select Customer', choices=[
                                        ('', '-----------')], initial="")
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    balance_message = forms.CharField(
        label="Account Balance", widget=forms.TextInput(), required=True)
    def __init__(self, *args, **kwargs):
        super(Client_Closing_ModelForm, self).__init__(*args, **kwargs)
        self.fields['closing_reason'].initial = ""
        self.fields['closing_reason'].required = True
        self.fields['balance_message'].widget.attrs['readonly'] = True

    class Meta:
        model = Client_Closing
        fields = ["client_id", "closing_date", "closing_reason", ]

        widgets = {
            'closing_date': DateInput(),
            'closing_reason': Textarea(attrs={'rows': 2, 'cols': 60, }),
        }

        labels = {"client_id": _("Customer ID"),
                  "closing_date": _("Closing Date"),
                  "closing_reason": _("Closing Reason"),
                  }







class Purchase_Order_MstForm(forms.ModelForm):
    show_room_list = []
    show_room = ChoiceFieldNoValidation(
        required=False, label='Show Room', choices=show_room_list)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    account_number = ChoiceFieldNoValidation(
        label="Supplier Name", required=False)
   

    def __init__(self, *args, **kwargs):
        super(Purchase_Order_MstForm, self).__init__(*args, **kwargs)
        self.fields['total_pur_qnty'].widget.attrs['readonly'] = True
        self.fields['g_total_price'].widget.attrs['readonly'] = True
        self.fields['supplier_id'].required = False

    class Meta:
        model = Purchase_Order_Mst
       
        fields = [ "branch_code",'purchase_type', 'purchase_date', 'supplier_id',  'g_total_price', 
         'total_pur_qnty', 'account_number','show_room','comments','voucher_number','discount_amount']
        widgets = {
            'comments': Textarea(attrs={'rows': 1, 'cols': 60, }),
            'purchase_date': DateInput(),
        }

        labels = {
           
            "purchase_type": _("Purchase Type "),
            "purchase_date": _("Purchase Date"),
            "supplier_id": _("Supplier Name"),
            "g_total_price": _("Total Price"),
            "total_pur_qnty": _("Total Quantity"),
            "branch_code": _("Branch Name"),
            
           
        }

class PurchaseMasterAuthQForm(forms.ModelForm):
    supplier_name = forms.CharField(label='Supplier Name', initial="",)
    total_price_after_disc = forms.DecimalField(
        label='Price After Discount', initial=0.00,)
    purchase_type = ChoiceFieldNoValidation(
        required=True, label='Payment Type', choices=[])
    supplier_id = ChoiceFieldNoValidation(
        required=True, label='Supplier', choices=[])
    account_number = ChoiceFieldNoValidation(
        required=False, label='Select Supplier', choices=[])

    def __init__(self, *args, **kwargs):
        super(PurchaseMasterAuthQForm, self).__init__(*args, **kwargs)
        self.fields['total_pur_qnty'].widget.attrs['readonly'] = True
        self.fields['purchase_date'].widget.attrs['readonly'] = True
        self.fields['show_room'].widget.attrs['readonly'] = True
        self.fields['g_total_price'].widget.attrs['readonly'] = True
        self.fields['due_amount'].widget.attrs['readonly'] = True
        self.fields['total_price_after_disc'].widget.attrs['readonly'] = True
        self.fields['discount_amount'].widget.attrs['readonly'] = True
        self.fields['purchase_type'].initial = "CS"
        self.fields['supplier_name'].widget.attrs['readonly'] = True
        self.fields['supplier_name'].initial = ""
        self.fields['supplier_name'].required = False
        self.fields['supplier_id'].required = False    
    
    class Meta:
        model = PurchaseMasterAuthQ
        fields = ["supplier_id", "purchase_date", "voucher_number", "show_room", "purchase_type", "total_pay", "payment_comments", "total_pur_qnty",
                  "g_total_price", "due_amount", "comments", "purchase_ord_no", "branch_code", "discount_amount", ]
        widgets = {
            'comments': Textarea(attrs={'rows': 1, 'cols': 60, }),
            'purchase_date': DateInput(),
            'purchase_ord_no': forms.HiddenInput(),
            'branch_code': forms.HiddenInput(),
            'show_room': forms.HiddenInput(),
        }
        labels = {
            "voucher_number": _("Voucher Number"),
            "purchase_date": _("Purchase Date"),
            "supplier_id": _("Supplier ID"),
            "show_room": _("Show Room"),
            "purchase_type": _("Payment Type"),
            "total_pay": _("Total Pay"),
            "payment_comments": _("Payment Details"),
            "total_pur_qnty": _("Quantity"),
            "total_price": _("Total Price"),
            "due_amount": _("Due Amount"),
            "discount_amount": _("Discount Receive"),
        }



class Purchase_Order_Dtl_TempForm(forms.ModelForm):

    class Meta:
        model = Purchase_Order_Dtl_Temp
        fields = ['product_id', 'origin', 'pur_qnty', 'unit_price', 'total_price','discount_amount'  ]
        labels = {
            "product_id": _("Product Name"),
            "origin": _("Origin"),
            "pur_qnty": _("Quantity"),
            "unit_price": _("Purchase rate"),
            "total_price": _("Total Price"),
        }


class Purchase_BillForm(forms.ModelForm):

    class Meta:
        model = Purchase_Bill
        fields = ['supllier_id', 'bill_id', 'submission_date', 'bill_amount', 'pending_amount','remarks','bill_date','purchase_date'  ]

        
        Widget={
            'submission_date':DateInput(),
            'bill_date':DateInput(),
            'purchase_date':DateInput(),

    }

        labels = {
            "supllier_id": _("Supplier Name"),
            "bill_amount": _("Bill Amount"),
            "pending_amount": _("Pending Amount"),
            "remarks": _("Remars"),
            "total_price": _("Total Price"),
            
        }



class Stock_quantity_transferFrom(forms.ModelForm):
    product_name  = ChoiceFieldNoValidation(required=False, label='Product Name', choices=[('', '------------')], initial="")

    class Meta:
        model = Stock_quantity_transfer
        fields={'from_branch_code','to_branch_code','product_name','stock_quantity','trf_quantity','product_id'}
        labels={
            'from_branch_code': _("From Branch Code"),
            'to_branch_code': _('To Branch Code'),
            "product_name" : _("Product Name"),
            "stock_quantity" : _("Stock Quantity"),
            "trf_quantity" : _("Transfer Quantity")

        }

# class Stock_quantity_transferFrom(forms.ModelForm):
#     # product_name = forms.ChoiceField(label="Select Product", required=False, choices=[('', 'Select Product')], initial="",
#     #                                widget=forms.Select(attrs={'name': 'product_id', 'id': 'id_product_id'}))
#     class Meta:
#         model:Stock_quantity_transfer
#         fields={'from_branch_code','to_branch_code','product_id','product_name','stock_quantity','trf_quantity'}
#         labels={
#             'from_branch_code': _("From Branch Code"),
#             'to_branch_code': _('To Branch Code'),
#             "product_name" : _("Product Name"),
#             "stock_quantity" : _("Stock Quantity"),
#             "trf_quantity" : _("Transfer Quantity")

#         }


###########
class Quotation_Details_Form(forms.ModelForm):
    product_id=ChoiceFieldNoValidation(label="Product",required=True,choices=[('',"select_product")],initial="")
    unit=ChoiceFieldNoValidation(label="Unit",required=True,choices=[('',"select_unit")],initial="")
            
    class Meta:
        model = Quotation_Details
        fields = [ 'unit', 'quantity','unit_price','total_price','product_id','quotation_date']
        widgets = {
            
            'quotation_date': DateInput(),
        }
        labels = {

            "unit": _("Unit "),
            "quantity":_("Quantity"),
            "unit_price":_("Unit Price"),
            "total_price":_("Total Price"),
     
            

        }


class Quotation_Master_Form(forms.ModelForm):
    supplier_id=ChoiceFieldNoValidation(label="Supplier",required=True,choices=[('',"select_supplier")],initial="")
    def __init__(self, *args, **kwargs):
        super(Quotation_Master_Form, self).__init__(*args, **kwargs)
        # self.fields['product_id'].widget.attrs['readonly'] = True
        # self.fields['product_id'].widget.attrs['id'] = "id_product_id2"
        
    class Meta:
        model = Quotation_Master
        fields = [ 'quotation_date', 'vat_condition','supplier_id','edd_date','quotation_validity','warranty',
        'subject','remarks','is_active',]


        widgets = {
            
            'quotation_date': DateInput(),
            'edd_date':DateInput()
        }
    
        labels = {

            "vat_condition": _("Vat Condition"),
            "quotation_validity":_("Quation Validity"),
            "warranty":_("Warranty"),
            "subject":_("Subject "),
            "is_active":_("Active"),
            "remarks":_("remarks"),
            
     
            

        }