from django.db import models

# Create your models here.
from appauth.models import STATUS_LIST, BLOOD_GROUP, GENDER_LIST, RELIGION_LIST, MARITAL_STATUS, CASH_RECEIVE_PAYMENT, TRAN_DEBIT_CREDIT, FIXED_PERCENT, DAY_MONTH_YEAR, DOCUMENT_TYPES, EDU_LIST, WEEK_DAY_LIST
from appauth.models import Loc_Country, Loc_Division, Loc_District, Loc_Upazila, Branch

TRANSACTION_SCREEN = (
    ('', '---------'),
    ('STOCK_PAYMENT', 'Purchase Payment'),
    ('QUICK_PURCHASE', 'Purchase Entry'),
    ('SALES_ENTRY', 'Sales Entry'),
    ('SUPP_ACCOUNT', 'Supplier Account'),
    ('CLIENT_ACCOUNT', 'Customer Account'),
    ('CASH_TRANSACTION', 'Account Cash Transaction'),
    ('TRANSFER_TRAN', 'Transfer Transaction'),
    ('ORDER_CREATE', 'Create Order'),
    ('SALES_RETURN', 'Sales Return'),
    ('STOCK_RETURN', 'Purchase Return'),
    ('DEP_RECEIVE', 'Deposits Receive'),
    ('DEP_PAYMENT', 'Deposits Payment'),
    ('EMI_RECEIVE', 'EMI Receive'),
    ('EMI_TRANSFER', 'EMI Transfer From Deposit'),
    ('DPS_RECEIVE', 'DPS Receive'),
    ('EMP_ENTRY', 'Employee Entry'),
    ('CLIENT_ENTRY', 'Customer Entry'),
    ('ADMIN_ENTRY', 'Admin Entry'),
    ('SUPPLIER_ENTRY', 'Supplier Entry'),
    ('ACCOUNT_TRANSFER', 'Customer Balance Transfer'),
    ('LEDCASH_TRAN', 'Ledger Transaction'),
    ('LEDTRF_TRAN', 'Ledger Transfer Transaction'),
)

class Application_Settings(models.Model):
    cash_gl_code = models.CharField(max_length=13, null=False)
    asset_main_gl = models.CharField(max_length=13, null=False)
    liabilities_main_gl = models.CharField(max_length=13, null=False)
    income_main_gl = models.CharField(max_length=13, null=False)
    expenses_main_gl = models.CharField(max_length=13, null=False)
    profit_and_loss_ledger = models.CharField(max_length=13, null=False)
    past_year_adj_ledger = models.CharField(max_length=13, null=False)
    transaction_doc_required = models.BooleanField(
        default=False, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cash_gl_code


class General_Ledger(models.Model):
    gl_code = models.CharField(max_length=13, null=False, primary_key=True)
    gl_name = models.CharField(max_length=200, null=False)
    reporting_gl_code = models.CharField(max_length=13, null=False)
    parent_code = models.ForeignKey('General_Ledger', on_delete=models.CASCADE,
                                    null=True, blank=True, db_column='parent_code', related_name='gl_parent_code')
    income_gl = models.BooleanField(blank=True, default=False)
    expense_gl = models.BooleanField(blank=True, default=False)
    assets_gl = models.BooleanField(blank=True, default=False)
    liabilities_gl = models.BooleanField(blank=True, default=False)
    is_leaf_node = models.BooleanField(blank=False, default=False)
    debit_allowed = models.BooleanField(blank=True, default=True)
    credit_allowed = models.BooleanField(blank=True, default=True)
    maintain_by_system = models.BooleanField(blank=True, default=False)
    sundry_flag = models.BooleanField(blank=True, default=False)
    is_bank_account = models.BooleanField(blank=True, default=False)
    sundry_max_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    gl_comments = models.TextField(null=True, blank=True)
    closer_date = models.DateTimeField(blank=True, null=True)
    auth_by = models.CharField(max_length=20, null=True, blank=True)
    auth_on = models.DateTimeField(null=True, blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.gl_code+' - '+self.gl_name

class Account_Type(models.Model):
    account_type_code = models.CharField(max_length=13, primary_key=True)
    account_type_name = models.CharField(max_length=200, null=False)
    account_type_short_name = models.CharField(max_length=20, null=False)
    maximum_credit_limit = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    account_ledger_code = models.ForeignKey(General_Ledger, on_delete=models.CASCADE, null=True,
                                            blank=True, db_column='account_ledger_code', related_name='act_account_ledger_code')
    receivable_ledger = models.ForeignKey(General_Ledger, on_delete=models.CASCADE, null=True,
                                          blank=True, db_column='receivable_ledger', related_name='act_receivable_ledger')
    payable_ledger = models.ForeignKey(General_Ledger, on_delete=models.CASCADE, null=True,
                                       blank=True, db_column='payable_ledger', related_name='act_payable_ledger')
    income_ledger = models.ForeignKey(General_Ledger, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='income_ledger', related_name='act_income_ledger')
    expense_ledger = models.ForeignKey(General_Ledger, on_delete=models.CASCADE, null=True,
                                       blank=True, db_column='expense_ledger', related_name='act_expense_ledger')
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account_type_code+" - " + self.account_type_name


class Client_Type(models.Model):
    client_type_code = models.CharField(max_length=20, primary_key=True)
    client_type_name = models.CharField(max_length=200, blank=False)
    is_account_required = models.BooleanField(blank=True, default=False)
    transaction_screen = models.CharField(
        max_length=200, null=True, choices=TRANSACTION_SCREEN, default='')
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client_type_code+" - " + self.client_type_name


class Transaction_Type(models.Model):
    tran_type_id = models.CharField(max_length=13, primary_key=True)
    tran_type_code = models.CharField(max_length=13, null=False)
    tran_type_name = models.CharField(max_length=200, null=False)
    debit_gl_code = models.ForeignKey(General_Ledger, on_delete=models.CASCADE, null=True,
                                      blank=True, db_column='debit_gl_code', related_name='trn_debit_gl_code')
    credit_gl_code = models.ForeignKey(General_Ledger, on_delete=models.CASCADE, null=True,
                                       blank=True, db_column='credit_gl_code', related_name='trn_credit_gl_code')
    default_debit_credit = models.CharField(
        max_length=1, null=True, choices=TRAN_DEBIT_CREDIT, default='')
    debit_allowed = models.BooleanField(blank=True, default=True)
    credit_allowed = models.BooleanField(blank=True, default=True)
    is_account_required = models.BooleanField(blank=True, default=False)
    is_document_required = models.BooleanField(blank=True, default=False)
    tran_account_type = models.ForeignKey(Account_Type, on_delete=models.CASCADE, null=True,
                                          blank=True, db_column='tran_account_type', related_name='trn_tran_account_type')
    tran_debit_account_type = models.ForeignKey(Account_Type, on_delete=models.CASCADE, null=True,
                                                blank=True, db_column='tran_debit_account_type', related_name='trn_tran_debit_account_type')
    transaction_screen = models.CharField(
        max_length=200, null=True, choices=TRANSACTION_SCREEN, default='')
    transaction_table = models.CharField(max_length=200, null=True, blank=True)
    transaction_from_table = models.CharField(
        max_length=200, null=True, blank=True)
    transaction_client_type = models.ForeignKey(Client_Type, on_delete=models.CASCADE, null=True,
                                                blank=True, db_column='transaction_client_type', related_name='trn_transaction_client_type')
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.tran_type_code+' - '+self.tran_type_name+' - '+self.transaction_screen


class Ledger_Transaction_Type(models.Model):
    tran_type_id = models.ForeignKey(
        Transaction_Type, on_delete=models.CASCADE, db_column='tran_type_id', related_name='ltt_tran_type_id')
    gl_code = models.ForeignKey(
        General_Ledger, on_delete=models.CASCADE, db_column='gl_code', related_name='ltt_gl_code')
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.gl_code


class Client_Account_Mapping(models.Model):
    client_type_code = models.ForeignKey(Client_Type, on_delete=models.CASCADE, null=False,
                                         blank=False, db_column='client_type_code', related_name='cat_client_type_code')
    account_type_code = models.ForeignKey(Account_Type, on_delete=models.CASCADE, null=False,
                                          blank=False, db_column='account_type_code', related_name='cat_account_type_code')
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.client_type_code)+" - " + self.account_type_code


class Cash_And_Bank_Ledger(models.Model):
    branch_code = models.ForeignKey(
        Branch, on_delete=models.CASCADE, db_column='branch_code', related_name='cab_branch_code')
    gl_code = models.ForeignKey(General_Ledger, on_delete=models.CASCADE,
                                db_column='gl_code', related_name='cab_tran_gl_code')
    last_transaction_date = models.DateField(null=True, blank=True)
    last_balance_update = models.DateField(null=True, blank=True)
    is_balance_updated = models.BooleanField(default=False)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Branch Code : "+str(self.branch_code)+" Ledger Code : "+str(self.gl_code)


class Ledger_Balance(models.Model):
    branch_code = models.IntegerField(blank=True)
    gl_code = models.ForeignKey(General_Ledger, on_delete=models.CASCADE,
                                null=True, blank=True, db_column='gl_code', related_name='glb_gl_code')
    total_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    gl_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    unauth_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    unauth_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    transfer_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    transfer_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    last_transaction_date = models.DateField(null=True, blank=True)
    last_balance_update = models.DateField(null=True, blank=True)
    last_monbal_update = models.DateField(null=True, blank=True)
    last_monbal_recpay_update = models.DateField(null=True, blank=True)
    is_balance_updated = models.BooleanField(default=False)
    is_monbal_updated = models.BooleanField(default=False)
    is_monbal_recpay_updated = models.BooleanField(default=False)
    auth_by = models.CharField(max_length=20, null=True, blank=True)
    auth_on = models.DateTimeField(null=True, blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Ledger_Balance_Hist(models.Model):
    branch_code = models.IntegerField(blank=True)
    transaction_date = models.DateField(null=True, blank=True)
    gl_code = models.CharField(max_length=13, null=False)
    total_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    gl_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cum_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cum_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Ledger_Balmon_Hist(models.Model):
    branch_code = models.IntegerField(blank=True)
    gl_code = models.CharField(max_length=13, null=False)
    transaction_date = models.DateField(null=True, blank=True)
    transaction_month = models.IntegerField(null=True)
    transaction_year = models.IntegerField(null=True)
    transaction_year_month = models.IntegerField(null=True)
    total_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    gl_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cum_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cum_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

class Led_Rec_Pay_Bal_Hist(models.Model):
    branch_code = models.IntegerField(blank=True)
    transaction_date = models.DateField(null=True, blank=True)
    gl_code = models.CharField(max_length=13, null=False)
    total_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    gl_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cum_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cum_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Led_Rec_Pay_Balmon_Hist(models.Model):
    branch_code = models.IntegerField(blank=True)
    gl_code = models.CharField(max_length=13, null=False)
    transaction_date = models.DateField(null=True, blank=True)
    transaction_month = models.IntegerField(null=True)
    transaction_year = models.IntegerField(null=True)
    transaction_year_month = models.IntegerField(null=True)
    total_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    gl_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cum_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cum_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Ledger_Report_Param(models.Model):
    branch_code = models.IntegerField(blank=True)
    gl_code = models.CharField(max_length=13, null=True)
    gl_level = models.IntegerField(blank=True, null=True)
    gl_name = models.CharField(max_length=100, null=True)
    reporting_gl_code = models.CharField(max_length=100, null=True)
    parent_code = models.CharField(max_length=100, null=True)
    gl_level_class = models.CharField(max_length=200, null=True)
    income_gl = models.BooleanField(blank=True, default=False)
    expense_gl = models.BooleanField(blank=True, default=False)
    assets_gl = models.BooleanField(blank=True, default=False)
    liabilities_gl = models.BooleanField(blank=True, default=False)
    is_leaf_node = models.BooleanField(blank=False, default=False)
    maintain_by_system = models.BooleanField(blank=True, default=False)
    sundry_flag = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)


class Ledger_Report_Balance(models.Model):
    branch_code = models.IntegerField(blank=True)
    gl_code = models.CharField(max_length=13, null=True)
    ason_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    ason_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    ason_gl_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    asof_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    asof_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    asof_gl_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    this_month_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    this_month_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    this_month_gl_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    past_month_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    past_month_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    past_month_gl_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    this_quarter_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    this_quarter_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    this_quarter_gl_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    past_quarter_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    past_quarter_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    past_quarter_gl_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    this_halfyear_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    this_halfyear_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    this_halfyear_gl_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    past_halfyear_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    past_halfyear_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    past_halfyear_gl_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    this_year_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    this_year_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    this_year_gl_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    past_year_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    past_year_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    past_year_gl_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    this_period_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    this_period_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    this_period_gl_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)


class Accounts_Balance(models.Model):
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20, blank=True)
    client_id = models.CharField(max_length=15, null=True)
    products_code = models.CharField(max_length=13, null=True, blank=True)
    account_type = models.CharField(max_length=13, null=True, blank=True)
    account_number = models.CharField(max_length=13, primary_key=True)
    account_title = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    account_address = models.CharField(max_length=200, null=True)
    account_ledger_code = models.CharField(
        max_length=13, null=True, blank=True)
    is_account_active = models.BooleanField(default=True)
    account_opening_date = models.DateField()
    account_closing_date = models.DateField(null=True, blank=True)
    last_transaction_date = models.DateField(null=True, blank=True)
    last_balance_update = models.DateField(null=True, blank=True)
    last_monbal_update = models.DateField(null=True, blank=True)
    is_balance_updated = models.BooleanField(default=False)
    credit_limit = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    total_debit_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_credit_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    account_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    unauth_debit_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    unauth_credit_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    account_comments = models.CharField(max_length=300, null=True, blank=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Accounts_Balance_Hist(models.Model):
    branch_code = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True,
                                    blank=True, db_column='branch_code', related_name='abh_branch_code')
    account_number = models.CharField(max_length=13, null=True, blank=True)
    transaction_date = models.DateField(null=True, blank=True)
    total_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    account_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cum_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cum_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Accounts_Balmon_Hist(models.Model):
    branch_code = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True,
                                    blank=True, db_column='branch_code', related_name='amb_branch_code')
    transaction_month = models.IntegerField(null=True)
    transaction_year = models.IntegerField(null=True)
    account_number = models.CharField(max_length=13, null=True, blank=True)
    total_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    account_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cum_debit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cum_credit_sum = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Account_Charges(models.Model):
    charges_code = models.CharField(max_length=13, null=False)
    charges_name = models.CharField(max_length=200, null=False)
    account_number = models.CharField(
        max_length=13, null=False, blank=False, default='0')
    charge_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    charge_date = models.DateField(null=True, blank=True)
    narration = models.CharField(max_length=300, null=True)
    tran_branch_code = models.IntegerField(null=True)
    tran_batch_number = models.IntegerField(null=True)
    tran_batch_date = models.DateField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Cash_Transaction(models.Model):
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20, blank=True)
    transaction_date = models.DateField()
    batch_number = models.IntegerField(default=0)
    day_serial_no = models.IntegerField(default=0)
    receive_payment = models.CharField(
        max_length=2, choices=CASH_RECEIVE_PAYMENT, default='', blank=False)
    transaction_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    transaction_narration = models.CharField(
        max_length=200, null=True, blank=True)
    auth_by = models.CharField(max_length=20, null=True, blank=True)
    auth_on = models.DateTimeField(null=True, blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    cancel_remarks = models.CharField(max_length=200, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Transaction_Telbal(models.Model):
    branch_code = models.IntegerField(blank=True)
    teller_id = models.CharField(max_length=20, primary_key=True, blank=True)
    cash_od_allowed = models.BooleanField(blank=True, default=False, null=True)
    credit_limit_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    debit_limit_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_credit_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_debit_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cash_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Tran_Telbal_Details(models.Model):
    branch_code = models.IntegerField(blank=True)
    org_teller_id = models.CharField(max_length=20, null=True, blank=True)
    res_teller_id = models.CharField(max_length=20, null=True, blank=True)
    tran_debit_credit = models.CharField(
        max_length=2, choices=CASH_RECEIVE_PAYMENT, default='', blank=False)
    transaction_date = models.DateField(blank=True)
    tran_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cancel_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    available_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    auth_by = models.CharField(max_length=20, null=True, blank=True)
    auth_on = models.DateTimeField(null=True, blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    cancel_remarks = models.CharField(max_length=200, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Transaction_Master(models.Model):
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20, blank=True)
    transaction_date = models.DateField()
    batch_number = models.IntegerField(default=0)
    tran_type = models.CharField(max_length=13, null=False)
    total_credit_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_debit_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    tran_source_table = models.CharField(max_length=50, null=False)
    tran_source_key = models.CharField(max_length=100, null=False)
    transaction_narration = models.CharField(max_length=200, null=True)
    system_posted_tran = models.BooleanField(
        blank=True, default=False, null=True)
    auth_by = models.CharField(max_length=20, null=True, blank=True)
    auth_on = models.DateTimeField(null=True, blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    cancel_remarks = models.CharField(max_length=200, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Transaction_Details(models.Model):
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20, blank=True)
    transaction_date = models.DateField()
    batch_number = models.IntegerField(default=0)
    batch_serial = models.IntegerField(default=0)
    tran_type = models.CharField(max_length=13, null=False)
    account_number = models.CharField(max_length=13, null=False)
    tran_gl_code = models.CharField(max_length=13, null=False)
    contra_gl_code = models.CharField(max_length=13, null=False)
    tran_debit_credit = models.CharField(
        max_length=2, choices=TRAN_DEBIT_CREDIT, default='', blank=False)
    tran_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cancel_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    available_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    charge_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    charge_code = models.CharField(max_length=20, null=True, blank=True)
    tran_document_prefix = models.CharField(max_length=10, null=True)
    tran_document_number = models.CharField(max_length=10, null=True)
    tran_person_phone = models.CharField(max_length=15, null=True, blank=True)
    tran_person_name = models.CharField(max_length=200, null=True, blank=True)
    tran_sign_verified = models.BooleanField(
        blank=True, default=False, null=True)
    system_posted_tran = models.BooleanField(
        blank=True, default=False, null=True)
    transaction_narration = models.CharField(
        max_length=200, null=True, blank=True)
    auth_by = models.CharField(max_length=20, null=True, blank=True)
    auth_on = models.DateTimeField(null=True, blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    cancel_remarks = models.CharField(max_length=200, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Transaction_Ibr(models.Model):
    transaction_id = models.CharField(
        max_length=20, null=False, blank=True, primary_key=True)
    org_branch_code = models.IntegerField(null=True)
    res_branch_code = models.IntegerField(null=True)
    transaction_date = models.DateField(null=True, blank=True)
    org_batch_number = models.IntegerField(default=0)
    res_batch_number = models.IntegerField(default=0)
    org_gl_code = models.CharField(max_length=13, null=False, blank=True)
    res_gl_code = models.CharField(max_length=13, null=False, blank=True)
    tran_status = models.CharField(max_length=2, null=False, blank=True)
    tran_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cancel_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    transaction_narration = models.CharField(
        max_length=200, null=True, blank=True)
    auth_by = models.CharField(max_length=20, null=True, blank=True)
    auth_on = models.DateTimeField(null=True, blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    cancel_remarks = models.CharField(max_length=200, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Transaction_Table(models.Model):
    branch_code = models.IntegerField(null=True, blank=True)
    center_code = models.CharField(max_length=20, blank=True, null=True)
    transaction_date = models.DateField(blank=True)
    batch_serial = models.IntegerField(default=0, blank=True)
    account_number = models.CharField(
        max_length=13, null=False, blank=True, default='0')
    tran_gl_code = models.CharField(
        max_length=13, null=False, default='0',  blank=True)
    contra_gl_code = models.CharField(
        max_length=13, default='0', null=True, blank=True)
    tran_debit_credit = models.CharField(
        max_length=2, choices=TRAN_DEBIT_CREDIT, default='', blank=True)
    tran_screen = models.CharField(max_length=20, null=True, blank=True)
    tran_type = models.CharField(max_length=13, null=False)
    tran_amount = models.DecimalField(max_digits=22, decimal_places=2)
    charge_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    charge_code = models.CharField(max_length=20, null=True, blank=True)
    available_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    tran_person_phone = models.CharField(max_length=15, null=True, blank=True)
    tran_person_name = models.CharField(max_length=200, null=True, blank=True)
    tran_document_prefix = models.CharField(
        max_length=10, null=True, blank=True)
    tran_document_number = models.CharField(
        max_length=10, null=True, blank=True)
    tran_sign_verified = models.BooleanField(
        blank=True, default=False, null=True)
    system_posted_tran = models.BooleanField(
        blank=True, default=False, null=True)
    transaction_narration = models.CharField(
        max_length=200, null=True, blank=True)
    tran_balance_check_required = models.BooleanField(
        blank=True, default=True, null=True)
    tran_auth_required = models.BooleanField(
        blank=True, default=False, null=True)
    back_date_transaction = models.CharField(
        max_length=1, null=True, blank=True)
    auth_by = models.CharField(max_length=20, null=True, blank=True)
    auth_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Transfer_Tran(models.Model):
    transaction_date = models.DateField()
    from_client_id = models.CharField(
        max_length=13, null=True, blank=True, default='0')
    from_client_name = models.CharField(max_length=200, null=True, blank=True)
    from_client_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    from_account_number = models.CharField(
        max_length=13, null=False, blank=True, default='0')
    to_client_id = models.CharField(
        max_length=13, null=True, blank=True, default='0')
    to_client_name = models.CharField(max_length=200, null=True, blank=True)
    to_client_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    to_account_number = models.CharField(
        max_length=13, null=False, blank=True, default='0')
    from_gl_code = models.CharField(
        max_length=13, null=True, default='0', blank=True)
    from_gl_name = models.CharField(max_length=200, null=True, blank=True)
    from_gl_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    to_gl_code = models.CharField(
        max_length=13, null=True, default='0', blank=True)
    to_gl_name = models.CharField(max_length=200, null=True, blank=True)
    to_gl_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    tran_type = models.CharField(max_length=13, null=False, blank=True)
    tran_screen = models.CharField(max_length=50, null=False, blank=True)
    tran_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    tran_document_number = models.CharField(
        max_length=100, null=True, blank=True)
    tran_sign_verified = models.BooleanField(
        blank=True, default=False, null=True)
    system_posted_tran = models.BooleanField(
        blank=True, default=False, null=True)
    transaction_narration = models.CharField(
        max_length=200, null=True, blank=True)
    back_date_transaction = models.CharField(
        max_length=1, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Charges(models.Model):
    charges_id = models.CharField(max_length=13, blank=True, primary_key=True)
    charges_code = models.CharField(max_length=13, null=False)
    charges_name = models.CharField(max_length=200, null=False)
    actype_code = models.CharField(max_length=13, null=False)
    charge_type = models.CharField(max_length=2, choices=FIXED_PERCENT, default='')
    charge_percentage = models.DecimalField(max_digits=22,decimal_places=2,default=0.00)
    charge_from_amount = models.DecimalField(max_digits=22,decimal_places=2,default=0.00)
    charge_upto_amount = models.DecimalField(max_digits=22,decimal_places=2,default=0.00)
    charge_amount = models.DecimalField(max_digits=22,decimal_places=2,default=0.00)
    account_opening_charge = models.BooleanField(blank=True,default=False)
    account_closing_charge = models.BooleanField(blank=True,default=False)
    member_admission_fee = models.BooleanField(blank=True,default=False)
    loan_application_fee = models.BooleanField(blank=True,default=False)
    loan_insurance_fee = models.BooleanField(blank=True,default=False)
    pass_book_fee = models.BooleanField(blank=True,default=False)
    penal_charge = models.BooleanField(blank=True,default=False)
    others_fee = models.BooleanField(blank=True,default=False)
    status = models.CharField(max_length=2,null=True, choices=STATUS_LIST, default='A')
    effective_from_date = models.DateField(null=True)
    effective_upto_date = models.DateField(null=True)
    charges_ledger_code = models.ForeignKey(General_Ledger, on_delete=models.PROTECT,related_name='crg_charges_ledger_code',db_column='charges_ledger_code', blank=True, null=True)
    comments =  models.CharField(max_length=300, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Deposit_Receive(models.Model):
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20, blank=True)
    client_id = models.CharField(max_length=20, default='', blank=True)
    account_number = models.CharField(max_length=13, null=True, blank=True)
    deposit_date = models.DateField(null=True, blank=True)
    deposit_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    cancel_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    tran_batch_number = models.IntegerField(null=True)
    deposit_doc_num = models.CharField(max_length=50, null=True, blank=True)
    dep_entry_day_sl = models.IntegerField(null=True, blank=True)
    narration = models.CharField(max_length=200, null=False, blank=True)
    is_transfer = models.BooleanField(default=False)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Deposit_Payment(models.Model):
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20, blank=True)
    client_id = models.CharField(max_length=20, default='', blank=True)
    account_number = models.CharField(max_length=13, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    payment_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    cancel_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    tran_batch_number = models.IntegerField(null=True)
    payment_doc_num = models.CharField(max_length=50, null=True, blank=True)
    dep_entry_day_sl = models.IntegerField(null=True, blank=True)
    narration = models.CharField(max_length=200, null=False, blank=False)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    is_transfer = models.BooleanField(default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

class Deposit_Closing(models.Model):
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20, blank=True)
    client_id = models.CharField(max_length=20, default='', blank=True)
    account_number = models.CharField(max_length=13, null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)
    closing_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    cancel_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    tran_batch_number = models.IntegerField(null=True)
    closing_doc_num = models.CharField(max_length=50, null=True, blank=True)
    narration = models.CharField(max_length=200, null=False, blank=False)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Deposit_Transfer(models.Model):
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20, blank=True)
    from_client_id = models.CharField(max_length=20, default='', blank=True)
    from_account_number = models.CharField(max_length=13, null=True, blank=True)
    to_client_id = models.CharField(max_length=20, default='', blank=True)
    to_account_number = models.CharField(max_length=13, null=True, blank=True)
    transaction_date = models.DateField(null=True, blank=True)
    transaction_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    cancel_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    tran_batch_number = models.IntegerField(null=True)
    transaction_doc_num = models.CharField(max_length=50, null=True, blank=True)
    narration = models.CharField(max_length=200, null=False, blank=False)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Document_Register(models.Model):
    branch_code = models.CharField(max_length=20)
    doc_number = models.CharField(max_length=200)
    tran_type = models.CharField(max_length=200)
