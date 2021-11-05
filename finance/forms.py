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


class GeneralLedgerForm(forms.ModelForm):
    parent_gl_name = forms.CharField(label='Parent Ledger Name', initial="",)

    def __init__(self, *args, **kwargs):
        super(GeneralLedgerForm, self).__init__(*args, **kwargs)
        self.fields['parent_gl_name'].widget.attrs['readonly'] = True
        self.fields['parent_gl_name'].initial = ""
        self.fields['parent_gl_name'].required = False

    class Meta:
        model = General_Ledger
        fields = ['gl_code', 'gl_name', 'parent_code', 'income_gl', 'expense_gl', 'debit_allowed', 'credit_allowed', 'sundry_flag',
                  'sundry_max_amount', 'gl_comments', 'assets_gl', 'liabilities_gl', 'is_leaf_node', 'reporting_gl_code', 'is_bank_account']

        widgets = {
            'gl_comments': Textarea(attrs={'rows': 1, 'cols': 60, }),
        }

        labels = {
            "gl_code": _("Ledger Code"),
            "gl_name": _("Ledger Name"),
            "reporting_gl_code": _("Reporting Ledger Code"),
            "is_leaf_node": _("Is Leaf Node"),
            "parent_code": _("Parent Ledger Code"),
            "income_gl": _("Income Ledger"),
            "expense_gl": _("Expense Ledger"),
            "debit_allowed": _("Debit Transaction Allowed"),
            "credit_allowed": _("Credit Transaction Allowed"),
            "sundry_flag": _("Sundray Ledger"),
            "is_bank_account": _("Is Bank Account"),
            "sundry_max_amount": _("Sundray Maximum Amount"),
            "gl_comments": _("Comments"),
        }


class Transaction_Type_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Transaction_Type_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = Transaction_Type
        fields = ['tran_type_code', 'tran_type_name', 'debit_gl_code', 'credit_gl_code', 'debit_allowed', 'credit_allowed', 
        'is_active', 'is_deleted','transaction_screen', 'is_account_required', 'tran_account_type', 'tran_debit_account_type', 
        'default_debit_credit','is_document_required', 'transaction_table', 'transaction_from_table','transaction_client_type']

        labels = {
            "tran_type_code": _("Transaction Type Code"),
            "tran_type_name": _("Transaction Type Name"),
            "debit_gl_code": _("Debit Ledger Code"),
            "credit_gl_code": _("Credit Ledger Code"),
            "debit_allowed": _("Debit Transaction Allowed"),
            "credit_allowed": _("Credit Transaction Allowed"),
            "default_debit_credit": _("Default Transaction Debit/Credit"),
            "is_active": _("IS Active"),
            "is_deleted": _("IS Delete"),
            "transaction_screen": _("Transaction Screen"),
            "is_account_required": _("Is Account Required"),
            "tran_account_type": _("Transaction Account Type"),
            "tran_debit_account_type": _("Transfer From Account"),
            "is_document_required": _("Is Document Number Required"),
            "transaction_table": _("Transaction Table"),
            "transaction_from_table": _("Transaction From Table"),
            "transaction_client_type": _("Transaction Client Type"),
        }


class Ledger_Transaction_Type_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Ledger_Transaction_Type_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = Ledger_Transaction_Type
        fields = ['tran_type_id', 'gl_code', ]

        labels = {
            "tran_type_id": _("Transaction Type"),
            "gl_code": _("Transaction Ledger"),
        }


class Cash_And_Bank_Ledger_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Cash_And_Bank_Ledger_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = Cash_And_Bank_Ledger
        fields = ['branch_code', 'gl_code','is_active','is_deleted', ]

        labels = {
            "branch_code": _("Branch Name"),
            "gl_code": _("Transaction Ledger"),
            "is_active": _("Is Active"),
            "is_deleted": _("Is Delete"),
        }


class Account_Type_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Account_Type_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = Account_Type
        fields = ['account_type_code', 'account_type_name', 'account_type_short_name', 'maximum_credit_limit', 'account_ledger_code',
                  'receivable_ledger', 'payable_ledger', 'income_ledger', 'expense_ledger', ]

        labels = {
            "account_type_code": _("AC Type Code"),
            "account_type_name": _("AC Type Name"),
            "account_type_short_name": _("Short Name"),
            "maximum_credit_limit": _("Maximum Credit Limit"),
            "account_ledger_code": _("Account Ledger"),
            "receivable_ledger": _("Receivable Ledger"),
            "payable_ledger": _("Payable Ledger"),
            "income_ledger": _("Income Ledger"),
            "expense_ledger": _("Expense Ledger"),
        }


class Client_Type_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Client_Type_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = Client_Type
        fields = ['client_type_code', 'client_type_name',
                  'is_account_required', 'transaction_screen', ]

        labels = {
            "client_type_code": _("Client Type Code"),
            "client_type_name": _("Client Type Name"),
            "is_account_required": _("Is Account Opening Required"),
            "transaction_screen": _("Transaction Screen"),
        }


class Client_Account_Mapping_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Client_Account_Mapping_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = Client_Account_Mapping
        fields = ['client_type_code', 'account_type_code', ]

        labels = {
            "client_type_code": _("Client Type"),
            "account_type_code": _("Account Type"),
        }

class TransactionTableForm(forms.ModelForm):
    current_balance = forms.CharField(label='Current Balance', initial="",)
    customer_name = forms.CharField(label='Customer Name', initial="",)
    customer_address = forms.CharField(label='Customer Address', initial="",)
    account_number = ChoiceFieldNoValidation(required=False, label='Transaction Account', choices=[])
    tran_gl_code = ChoiceFieldNoValidation(required=False, label='Transaction Ledger', choices=[])
    receipt_payment_ledger = ChoiceFieldNoValidation(required=False, label='Receipt/Payment Method', choices=[])
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)

    tran_type_list =[]
    tran_type = ChoiceFieldNoValidation(required=True, label='Transaction Type', choices=tran_type_list)

    def __init__(self, *args, **kwargs):
        super(TransactionTableForm, self).__init__(*args, **kwargs)
        self.fields['tran_gl_code'].widget.attrs['class'] = "chosen_ledger"
        self.fields['current_balance'].initial = ""
        self.fields['current_balance'].required = False
        self.fields['current_balance'].widget.attrs['readonly'] = True
        self.fields['tran_amount'].initial = ""
        self.fields['customer_name'].initial = ""
        self.fields['customer_name'].required = False
        self.fields['customer_name'].widget.attrs['readonly'] = True
        self.fields['customer_address'].required = False
 
        try:
            param = Application_Settings.objects.get()
        except Exception as e:
            print('Finance Application Settings Not Configured')
            param =None
        if param.transaction_doc_required:
            self.fields['tran_document_number'].required = True

    class Meta:
        model = Transaction_Table
        fields = [ "branch_code","tran_type","transaction_date", "tran_gl_code", "tran_person_phone","tran_person_name", "tran_debit_credit",
                    "account_number", "tran_amount","transaction_narration",'tran_document_number','tran_screen']
        widgets = {
            'transaction_narration': Textarea(attrs={'rows':1, 'cols':60,}),
            'transaction_date': DateInput(),
            'tran_screen': HiddenInput(),
        }

        labels = {
                    "transaction_date": _("Transaction Date"),
                    "branch_code": _("Branch Name"),
                    "tran_gl_code": _("Ledger Code"),
                    "customer_name": _("Customer Name"),
                    "current_balance": _("Current Balance"),
                    "tran_person_phone": _("Receiver/Payer Phone"),
                    "tran_person_name": _("Receiver/Payer Name"),
                    "tran_debit_credit": _("Debit/Credit"),
                    "tran_type": _("Transaction Type"),
                    "tran_amount": _("Transaction Amount"),
                    "transaction_narration": _("Comments"),
                    "tran_document_number": _("Document Number (Bank Cheque)"),
                }

class TransactionSearch(forms.Form):
    from_batch_number = forms.CharField(label="From Batch", widget=forms.TextInput(
    attrs={'placeholder': 'From Batch',  'id': 'id_from_batch_number'}
    ),required=False)
    upto_batch_number = forms.CharField(label="To Number", widget=forms.TextInput(
    attrs={'placeholder': 'To Batch',  'id': 'id_upto_batch_number'}
    ),required=False)
    tran_date = forms.DateField(label="Transaction Date",widget=DateInput(), required=True)
    tran_from_date = forms.DateField(label="From Date",widget=DateInput(), required=True)
    tran_upto_date = forms.DateField(label="Upto Date",widget=DateInput(), required=True)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    products_type =  forms.ChoiceField(label="Account Type", required=False)
    account_number =  forms.ChoiceField(label="Select Account", required=False)
    tran_ledger_code =  forms.ChoiceField(label="Select Ledger", required=False)

class AccountBalance(forms.Form):
    phone_number = forms.CharField(label="Phone Number", widget=forms.TextInput(
    attrs={ 'id': 'id_phone_number'}
    ),required=False)
    products_type =  forms.ChoiceField(label="Account Type", required=False)
    account_number =  forms.ChoiceField(label="Select Account", required=False)
    zero_balance = forms.ChoiceField(choices=YES_NO, label="Show Zero Balance", initial='N', widget=forms.Select(
        attrs={'name':'zero_balance', 'id': 'id_zero_balance'}
        ), required=True)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    center_code = ChoiceFieldNoValidation(label="Center Name", required=False)
    
class AccountStatementDetails(forms.Form):
    phone_number = forms.CharField(label="Phone Number", widget=forms.TextInput(
    attrs={ 'id': 'id_phone_number'}
    ),required=False)
    products_type =  forms.ChoiceField(label="Account Type", required=False)
    account_title = forms.CharField(label="Account Title", widget=forms.TextInput(
    attrs={ 'id': 'id_account_title', 'readonly':'readonly'}
    ),required=False)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    account_number =  forms.ChoiceField(label="Select Account", required=False)
    account_balance = forms.CharField(label="Current Balance", widget=forms.TextInput(
    attrs={'id': 'id_account_balance', 'readonly':'readonly'}
    ),required=False)
    from_date = forms.DateField(label="From Date",widget=DateInput(), required=True)
    upto_date = forms.DateField(label="Upto Date",widget=DateInput(), required=True)

class CommonReportForm(forms.Form):
    invoice_number = forms.CharField(label="Invoice Number", widget=forms.TextInput(
    attrs={ 'id': 'id_invoice_number'}
    ),required=False)
    phone_number = forms.CharField(label="Phone Number", widget=forms.TextInput(
    attrs={ 'id': 'id_phone_number'}
    ),required=False)
    supplier_account = ChoiceFieldNoValidation(label='Select Supplier', choices=[('', 'Select Supplier')], initial="")
    customer_account = ChoiceFieldNoValidation(label='Select Customer', choices=[('', 'Select Customer')], initial="")
    gl_code = ChoiceFieldNoValidation(label='Ledger Name', choices=[('', '----------')], initial="")
    products_type = forms.ChoiceField(label="Account Type", initial='A', widget=forms.Select(
        attrs={'name':'products_type', 'id': 'id_products_type'}
        ), required=False)
    account_title = forms.CharField(label="Account Title", widget=forms.TextInput(
    attrs={ 'id': 'id_account_title', 'readonly':'readonly'}
    ),required=False)
    client_id = ChoiceFieldNoValidation(label='Customer Name', choices=[('', '------------')], initial="", required=False)
    client_name = forms.CharField(label="Client Name", widget=forms.TextInput(
    attrs={ 'id': 'id_client_name'}
    ),required=False)
    product_id = forms.ChoiceField(label="Select Product", required=False, choices=[('', 'Select Product')], initial="", 
    widget=forms.Select(attrs={'name':'product_id', 'id': 'id_product_id'}
        ))
    account_number = forms.CharField(label="Account Number", widget=forms.TextInput(
    attrs={ 'id': 'id_account_number'}
    ),required=False)
    account_balance = forms.CharField(label="Current Balance", widget=forms.TextInput(
    attrs={'id': 'id_account_balance', 'readonly':'readonly'}
    ),required=False)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    center_code = ChoiceFieldNoValidation(label="Center Name", required=False)
    emi_reference_no = ChoiceFieldNoValidation(label="Invoice Number", required=False)
    from_date = forms.DateField(label="From Date",widget=DateInput(attrs={'id': 'id_from_date'}), required=False)
    upto_date = forms.DateField(label="Upto Date",widget=DateInput(attrs={'id': 'id_upto_date'}), required=False)
    ason_date = forms.DateField(label="Report Date",widget=DateInput(attrs={'id': 'id_ason_date'}), required=False)
    user_name = forms.CharField(label="User Name", widget=forms.TextInput(
    attrs={ 'id': 'id_user_id'}
    ),required=False)
    employee_name = forms.ChoiceField(label="Employee Name", required=False,choices=[('', '------------')], initial="",  widget=forms.Select(
        attrs={'name':'employee_name', 'id': 'id_employee_id'}
        ))
    app_user_id = forms.ChoiceField(label="User Name", required=False,choices=[('', '------------')], initial="")
    transfer_tran = forms.ChoiceField(choices=YES_NO, label="Show Transfer Transaction", initial='Y', widget=forms.Select(
        attrs={'name':'transfer_tran', 'id': 'id_transfer_tran'}
        ), required=True)
    posting_user = forms.CharField(label="Posting User ID", widget=forms.TextInput(
    attrs={ 'id': 'id_user_id'}
    ),required=False)
    empty_sheet = forms.ChoiceField(label="Empty Sheet", choices=[('Y', 'Yes'),('N', 'No')], initial='Y', widget=forms.Select(
        attrs={'name':'empty_sheet', 'id': 'id_empty_sheet'}
        ), required=False)
    deposit_statement = forms.ChoiceField(label="Deposit Statement", choices=[('Y', 'Yes'),('N', 'No')], initial='N', widget=forms.Select(
        attrs={'name':'deposit_statement', 'id': 'id_deposit_statement'}
        ), required=False)

class Tran_Telbal_Details_Form(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    res_teller_id = ChoiceFieldNoValidation(label="Responding Teller", required=False)
    def __init__(self, *args, **kwargs):
        super(Tran_Telbal_Details_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = Tran_Telbal_Details
        fields = ['branch_code', 'org_teller_id','res_teller_id', 'tran_debit_credit','tran_amount', 
        'cancel_amount','available_balance','transaction_date' ]

        labels = {
            "branch_code": _("Branch Name"),
            "org_teller_id": _("Orginating Teller"),
            "res_teller_id": _("Responding Teller"),
            "tran_debit_credit": _("Request Type"),
            "tran_amount": _("Transaction Amount"),
            "cancel_amount": _("Cancel Amount"),
            "available_balance": _("Available Balance"),
            "transaction_date": _("Available Balance"),
        }

class Tran_Telbal_Details_Query_Form(forms.Form):
    org_teller_id = ChoiceFieldNoValidation(label="Orginating Teller", required=False)
    res_teller_id = ChoiceFieldNoValidation(label="Responding Teller", required=False)
    auth_pending = forms.ChoiceField(choices=YES_NO, label="Only Authorization Pending", initial='Y', widget=forms.Select(
        attrs={'name':'auth_pending', 'id': 'id_auth_pending'}
        ), required=True)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    from_date = forms.DateField(label="From Date",widget=DateInput(attrs={'id': 'id_from_date'}), required=False)
    upto_date = forms.DateField(label="Upto Date",widget=DateInput(attrs={'id': 'id_upto_date'}), required=False)
    transaction_date = forms.DateField(label="Transaction Date",widget=DateInput(attrs={'id': 'id_transaction_date'}), required=False)

class Deposit_Receive_Model_Form(forms.ModelForm):
    account_balance  = forms.CharField(label='Account Balance', initial="",required=False)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", initial="------------",required=False)
    account_number = ChoiceFieldNoValidation(label="Customer Name", choices=[('', '------------')], initial="", required=True)
    def __init__(self, *args, **kwargs):
        super(Deposit_Receive_Model_Form, self).__init__(*args, **kwargs)
        self.fields['account_balance'].widget.attrs['readonly'] = True
        self.fields['account_balance'].required = False
        self.fields['deposit_amount'].initial = ""
        instance = getattr(self, 'instance', None)
        try:
            param = Application_Settings.objects.get()
        except Exception as e:
            print('Finance Application Settings Not Configured')
            param =None
        if param.transaction_doc_required:
            self.fields['deposit_doc_num'].required = True

        if instance and instance.pk:
            self.fields['branch_code'].widget.attrs['readonly'] = True
            self.fields['client_id'].widget.attrs['readonly'] = True
            try:
                param = Application_Settings.objects.get()
            except Exception as e:
                print('Finance Application Settings Not Configured')
                param =None
            if param.transaction_doc_required:
                self.fields['deposit_doc_num'].required = True

    class Meta:
        model = Deposit_Receive
        fields = ['branch_code','client_id','account_number','deposit_date','deposit_amount','deposit_doc_num','narration']

        widgets = {
            'deposit_date': DateInput(),
            'narration': Textarea(attrs={'rows':2, 'cols':60,}),
        }

        labels = {
                    "branch_code": _("Branch Name"),
                    "client_id": _("Client ID"),
                    "deposit_date": _("Deposit Date"),
                    "deposit_amount": _("Deposit Amount"),
                    "deposit_doc_num": _("Document Number"),
                    "narration": _("Comments"),
                }

class Deposit_Payment_Model_Form(forms.ModelForm):
    account_balance  = forms.CharField(label='Account Balance', initial="",required=False)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", initial="------------",required=False)
    account_number = ChoiceFieldNoValidation(label="Customer Name", choices=[('', '------------')], initial="", required=True)
    def __init__(self, *args, **kwargs):
        super(Deposit_Payment_Model_Form, self).__init__(*args, **kwargs)
        self.fields['account_balance'].widget.attrs['readonly'] = True
        self.fields['account_balance'].required = False
        self.fields['payment_amount'].initial = ""
        instance = getattr(self, 'instance', None)
        try:
            param = Application_Settings.objects.get()
        except Exception as e:
            print('Finance Application Settings Not Configured')
            param =None
        if param.transaction_doc_required:
            self.fields['payment_doc_num'].required = True

        if instance and instance.pk:
            self.fields['branch_code'].widget.attrs['readonly'] = True
            self.fields['client_id'].widget.attrs['readonly'] = True
            try:
                param = Application_Settings.objects.get()
            except Exception as e:
                print('Finance Application Settings Not Configured')
                param =None
            if param.transaction_doc_required:
                self.fields['payment_doc_num'].required = True

    class Meta:
        model = Deposit_Payment
        fields = ['branch_code','client_id','account_number','payment_date','payment_amount','payment_doc_num','narration']

        widgets = {
            'payment_date': DateInput(),
            'narration': Textarea(attrs={'rows':2, 'cols':60,}),
        }

        labels = {
                    "branch_code": _("Branch Name"),
                    "client_id": _("Client ID"),
                    "payment_date": _("Payment Date"),
                    "payment_amount": _("Payment Amount"),
                    "payment_doc_num": _("Document Number"),
                    "narration": _("Comments"),
                }

class Deposit_Transfer_Model_Form(forms.ModelForm):
    account_balance  = forms.CharField(label='Account Balance', initial="",required=False)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", initial="------------",required=False)
    from_account_number = ChoiceFieldNoValidation(label="From Customer Name", choices=[('', '------------')], initial="", required=True)
    to_account_number = ChoiceFieldNoValidation(label="To Customer Name", choices=[('', '------------')], initial="", required=True)
    def __init__(self, *args, **kwargs):
        super(Deposit_Transfer_Model_Form, self).__init__(*args, **kwargs)
        self.fields['account_balance'].widget.attrs['readonly'] = True
        self.fields['account_balance'].required = False
        self.fields['transaction_amount'].initial = ""
        instance = getattr(self, 'instance', None)
        try:
            param = Application_Settings.objects.get()
        except Exception as e:
            print('Finance Application Settings Not Configured')
            param =None
        if param.transaction_doc_required:
            self.fields['payment_doc_num'].required = True

        if instance and instance.pk:
            self.fields['branch_code'].widget.attrs['readonly'] = True
            self.fields['client_id'].widget.attrs['readonly'] = True
            try:
                param = Application_Settings.objects.get()
            except Exception as e:
                print('Finance Application Settings Not Configured')
                param =None
            if param.transaction_doc_required:
                self.fields['payment_doc_num'].required = True

    class Meta:
        model = Deposit_Transfer
        fields = ['branch_code','from_client_id','from_account_number','to_client_id','to_account_number',
        'transaction_date','transaction_amount','transaction_doc_num','narration']

        widgets = {
            'transaction_date': DateInput(),
            'narration': Textarea(attrs={'rows':2, 'cols':60,}),
        }

        labels = {
                    "branch_code": _("Branch Name"),
                    "from_client_id": _("From Client ID"),
                    "to_client_id": _("To Client ID"),
                    "transaction_date": _("Transfer Date"),
                    "transaction_amount": _("Transfer Amount"),
                    "transaction_doc_num": _("Document Number"),
                    "narration": _("Comments"),
                }

class Deposit_Closing_Model_Form(forms.ModelForm):
    account_balance  = forms.CharField(label='Account Balance', initial="",required=False)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", initial="------------",required=False)
    account_number = ChoiceFieldNoValidation(label="Customer Name", choices=[('', '------------')], initial="", required=False)
    def __init__(self, *args, **kwargs):
        super(Deposit_Closing_Model_Form, self).__init__(*args, **kwargs)
        self.fields['account_balance'].widget.attrs['readonly'] = True
        self.fields['account_balance'].required = False
        self.fields['closing_balance'].initial = ""
        self.fields['closing_balance'].widget.attrs['readonly'] = True
        instance = getattr(self, 'instance', None)
        try:
            param = Application_Settings.objects.get()
        except Exception as e:
            print('Finance Application Settings Not Configured')
            param =None
        if param.transaction_doc_required:
            self.fields['closing_doc_num'].required = True

        if instance and instance.pk:
            self.fields['branch_code'].widget.attrs['readonly'] = True
            self.fields['client_id'].widget.attrs['readonly'] = True
            try:
                param = Application_Settings.objects.get()
            except Exception as e:
                print('Finance Application Settings Not Configured')
                param =None
            if param.transaction_doc_required:
                self.fields['closing_doc_num'].required = True

    class Meta:
        model = Deposit_Closing
        fields = ['branch_code','client_id','account_number','closing_date','closing_balance','closing_doc_num','narration']

        widgets = {
            'closing_date': DateInput(),
            'narration': Textarea(attrs={'rows':2, 'cols':60,}),
        }

        labels = {
                    "branch_code": _("Branch Name"),
                    "client_id": _("Client ID"),
                    "closing_date": _("Closing Date"),
                    "closing_balance": _("Closing Balance"),
                    "closing_doc_num": _("Payment Document Number"),
                    "narration": _("Comments"),
                }


class ChargesModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChargesModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['charges_code'].widget.attrs['readonly'] = True

    class Meta:
        model = Charges
        fields = ['charges_code', 'charges_name', 'charge_type', 'charge_percentage', 'charge_amount','actype_code',
                  'account_opening_charge', 'account_closing_charge', 'status', 'effective_from_date', 'effective_upto_date',
                  'charges_ledger_code', 'comments', 'charge_from_amount', 'charge_upto_amount', 'member_admission_fee',
                  'loan_application_fee', 'loan_insurance_fee', 'pass_book_fee', 'penal_charge', 'others_fee']

        widgets = {
            'comments': Textarea(attrs={'rows': 1, 'cols': 60, }),
            'effective_from_date': DateInput(),
            'effective_upto_date': DateInput(),
        }

        labels = {
            "charges_code": _("Charge Code"),
            "charges_name": _("Charge Name"),
            "charge_type": _("Charge Type"),
            "actype_code": _("Account Type"),
            "charge_percentage": _("Percentage"),
            "charge_from_amount": _("From Amount"),
            "charge_upto_amount": _("Upto Amount"),
            "charge_amount": _("Charge Amount"),
            "account_opening_charge": _("AC Opening Charge"),
            "account_closing_charge": _("AC Closing Charge"),
            "member_admission_fee": _("Member Admission Fee"),
            "loan_application_fee": _("Loan Application Fee"),
            "loan_insurance_fee": _("Loan Insurance Fee"),
            "pass_book_fee": _("Pass Book Fee"),
            "penal_charge": _("Penal Charge"),
            "others_fee": _("Others Fee"),
            "status": _("Status"),
            "charges_ledger_code": _("Ledger Code"),
            "effective_from_date": _("Effective From Date"),
            "effective_upto_date": _("Effective Upto Date"),
            "comments": _("Comments"),
        }
