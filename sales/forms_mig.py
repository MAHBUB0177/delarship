from django import forms
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


class DateInput(forms.DateInput):
    input_type = 'date'


class ChoiceFieldNoValidation(ChoiceField):
    def validate(self, value):
        pass


class clients_model_form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(clients_model_form, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['branch_code'].required = False

    class Meta:
        model = Clients
        fields = [ 'client_name', 'client_type', 'client_father_name', 'client_mother_name','branch_code',
                  'client_blood_group', 'client_sex', 'client_religion', 'client_marital_status', 'client_national_id',
                  'client_present_address', 'client_permanent_address', 'client_phone', 'client_email', 'client_joining_date',
                  'client_education', 'client_date_of_birth', 'client_birth_place', 'client_monthly_income']

        widgets = {
            'client_present_address': Textarea(attrs={'rows': 2, 'cols': 60, }),
            'client_permanent_address': Textarea(attrs={'rows': 2, 'cols': 60, }),
            'client_date_of_birth': DateInput(),
            'client_joining_date': DateInput(),
        }

        labels = {
            "client_name": _("Clients Name"),
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
            "client_monthly_income": _("Monthly Income"),
            "branch_code": _("Branch Name"),
        }

class ClientSearch(forms.Form):
    client_name = forms.CharField(label="Client Name", widget=forms.TextInput(
    attrs={'placeholder': '',  'id': 'id_client_name'}
    ),required=False)
    client_id = forms.CharField(label="Client ID", widget=forms.TextInput(
    attrs={'placeholder': '',  'id': 'id_client_id'}
    ),required=False)
    client_phone = forms.CharField(label="Client Phone", widget=forms.TextInput(
    attrs={'placeholder': '',  'id': 'id_client_phone'}
    ),required=False)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)

class ClientDocumentsModelForms(forms.ModelForm):
    class Meta:
        model = Client_Photo_Sign
        fields = ['client_id','document_type','document_location',]

        labels = {
                    "client_id": _("Phone Number"),
                    "document_type": _("Document Type"),
                    "document_location":_("Image"),
                }


class Supplier_Model_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Supplier_Model_Form, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            self.fields['branch_code'].required = False

    class Meta:
        model = Supplier_Information
        fields = ['supp_name','supp_address','supp_mobile','supp_email','supp_web','supp_key_person','supp_fax',
        'branch_code','supp_grade']

        widgets = {
            'supp_address': Textarea(attrs={'rows':2, 'cols':60,}),
        }

        labels = {
                    "supp_id": _("Supplier ID"),
                    "supp_name": _("Supplier Name"),
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
        fields = ['group_name','is_active']

        labels = {
                    "group_name": _("Group Name"),
                    "is_active":_("Is Active"),
                }

class Products_Brand_Form(forms.ModelForm):
    class Meta:
        model = Products_Brand
        fields = ['brand_name','is_active']

        labels = {
                    "group_name": _("Brand Name"),
                    "is_active":_("Is Active"),
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
        fields =["product_name","product_model","product_group","product_purces_price","product_sales_price","product_tax_rate","product_stock_alert",
        "product_life_time","product_status","product_narration","sales_discount_type","sales_discount_percent",
        "sales_discount_maxamt","sales_discount_minamt","sales_discount_fromdt","sales_discount_uptodt","brand_id",
        'product_bar_code', "is_active"]

        widgets = {
            'product_naration': Textarea(attrs={'rows':2, 'cols':60,}),
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
                    "product_naration": _("Comments"),
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
                    "is_active": _("Is Active")
                }


class Products_Search_Forms(forms.Form):
    product_name = forms.CharField(label="Product Name", widget=forms.TextInput(
    attrs={'placeholder': '',  'id': 'id_product_name'}
    ),required=False)
    product_model = forms.CharField(label="Product Model", widget=forms.TextInput(
    attrs={'placeholder': '',  'id': 'id_product_model'}
    ),required=False)
    product_bar_code = forms.CharField(label="Products Barcode", widget=forms.TextInput(
    attrs={'placeholder': '',  'id': 'id_product_bar_code'}
    ),required=False)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)

class Sales_Purchase_Master_Form(forms.ModelForm):
    show_room_list =[]
    show_room = ChoiceFieldNoValidation(required=False, label='Show Room', choices=show_room_list)

    def __init__(self, *args, **kwargs):
       super(Sales_Purchase_Master_Form, self).__init__(*args, **kwargs)
       self.fields['total_quantity'].widget.attrs['readonly'] = True
       self.fields['total_price'].widget.attrs['readonly'] = True
       self.fields['supplier_id'].required = False

    class Meta:
        model = StockMaster
        fields = ["branch_code","supplier_id","stock_date","voucher_number","show_room","total_pay","payment_comments","total_quantity",
                "total_price","due_amount","comments","discount_amount"]
        widgets = {
            'comments': Textarea(attrs={'rows':1, 'cols':60,}),
            'stock_date': DateInput(),
        }
        labels = {
                    "voucher_number": _("Voucher Number"),
                    "stock_date": _("Purchase Date"),
                    "show_room": _("Show Room"),
                    "discount_amount": _("Discount Receive"),
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
        fields = ['product_name','quantity','product_id','product_bar_code','product_model','purces_price','total_price',
        'discount_amount',]

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
    total_price_after_disc = forms.DecimalField(label='Price After Discount', initial=0.00,)
    tran_type_code = ChoiceFieldNoValidation(required=True, label='Payment Type', choices=[])
    supplier_id = ChoiceFieldNoValidation(required=True, label='Supplier', choices=[])
    account_number = ChoiceFieldNoValidation(required=False, label='Select Supplier', choices=[])

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
        fields = ["supplier_id","stock_date","voucher_number","show_room","tran_type_code","total_pay","payment_comments","total_quantity",
                "total_price","due_amount","comments","stock_id","branch_code","discount_amount",]
        widgets = {
            'comments': Textarea(attrs={'rows':1, 'cols':60,}),
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
    attrs={ 'id': 'id_stock_id'}
    ),required=False)
    from_date = forms.DateField(label="Purchase Date",widget=DateInput(), required=True)
    upto_date = forms.DateField(label="Purchase Date",widget=DateInput(), required=True)
    stock_date = forms.DateField(label="Purchase Date",widget=DateInput(), required=True)
    product_id = forms.CharField(label="Product ID", widget=forms.TextInput(
    attrs={  'id': 'id_product_id'}
    ),required=False)
    supplier_phone = forms.CharField(label="Supplier Phone", widget=forms.TextInput(
    attrs={  'id': 'id_supplier_phone'}
    ),required=False)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)


class PurchaseReturnModelForm(forms.ModelForm):

    product_name  = forms.CharField(label='Product Name', initial="",)
    supplier_name = forms.CharField(label='Supplier Name', initial="",)
    product_id = ChoiceFieldNoValidation(label='Select Product', choices=[('', 'Select Product')], initial="")
    supplier_account = ChoiceFieldNoValidation(label='Select Supplier', choices=[('', 'Select Supplier')], initial="")

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
        fields =["stock_id","return_date","product_id","tran_batch_number","returned_quantity","return_amount","return_voucher","stock_date",
        "return_reason","stock_voucher","supplier_id",'branch_code']

        widgets = {
            'return_date': DateInput(),
            'stock_date': DateInput(),
            'return_reason': Textarea(attrs={'rows':2, 'cols':60,}),
        }

        labels = {  "product_id": _("Product Code"),
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


class CommonReportForm(forms.Form):
    invoice_number = forms.CharField(
        label="Invoice Number", widget=forms.TextInput(), required=False)
    phone_number = forms.CharField(
        label="Phone Number", widget=forms.TextInput(), required=False)
    account_number = ChoiceFieldNoValidation(label='Select', choices=[
                                               ('', 'Select')], initial="")
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
    transfer_tran = forms.ChoiceField(choices=YES_NO, label="Show Transfer Transaction", initial='Y', widget=forms.Select(
    ), required=True)
    posting_user = forms.CharField(label="Posting User ID", widget=forms.TextInput(
    ), required=False)
