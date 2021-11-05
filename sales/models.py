from os import truncate
from django.db import models

# Create your models here.
from appauth.models import Employees, Loc_Region, STATUS_LIST, BLOOD_GROUP, GENDER_LIST, RELIGION_LIST, MARITAL_STATUS, CASH_RECEIVE_PAYMENT, TRAN_DEBIT_CREDIT, FIXED_PERCENT, DAY_MONTH_YEAR, DOCUMENT_TYPES, EDU_LIST, WEEK_DAY_LIST, GENDER_LIST
from appauth.models import Loc_Country, Loc_Division, Loc_District, Loc_Upazila, Branch

# Create your models here.

SALES_DISCOUNT = (
    ('P', 'Percentage'),
    ('F', 'Fixed Amount'),
)

OFFER_TYPE = (
    ('', 'Select'),
    ('Q', 'Q-Quantity'),
    ('P', 'P-Price'),
)

SALES_STATUS = (
    ('N', 'Yet to Invoice'),
    ('H', 'Hold Invoice'),
    ('I', 'Invoice Complete'),
    ('C', 'Cancel'),
    ('R', 'Return Item'),
)

ORDER_STATUS = (
    ('N', 'Yet to Place'),
    ('P', 'Order Placed'),
    ('A', 'Order Approved'),
    ('C', 'Order Cancel'),
    ('R', 'Order Return'),
)

STOCK_STATUS = (
    ('N', 'Yet to Settled'),
    ('Y', 'Settled'),
    ('W', 'Waiting for Approval'),
    ('J', 'Reject Stock'),
    ('C', 'Cancel'),
    ('S', 'In Stock'),
    ('R', 'Returned'),
    ('P', 'Partial Returned'),
    ('D', 'Damage'),
)

INSTFRQ_LIST = (
    ('', 'Choose...'),
    ('W', 'Weekly'),
    ('M', 'Monthly'),
    ('Q', 'Quarterly'),
    ('H', 'Half Yearly'),
    ('Y', 'Yearly'),
)

SUPP_GRADE = (
    ('', 'Choose'),
    ('A', 'Excellent'),
    ('B', 'Best'),
    ('C', 'Good')
)


class Application_Settings(models.Model):
    company_code = models.CharField(max_length=10, null=False)
    company_name = models.CharField(max_length=300, null=False)
    company_address = models.CharField(max_length=300, null=True, blank=True)
    company_mobile = models.CharField(max_length=50, null=True, blank=True)
    company_email = models.CharField(max_length=100, null=True, blank=True)
    company_logo = models.ImageField(upload_to='logo/')
    barcode_enable = models.BooleanField(default=False)
    invoice_file_name = models.CharField(max_length=200, null=True, blank=True)
    invoice_line1 = models.CharField(max_length=100, null=True, blank=True)
    invoice_line2 = models.CharField(max_length=100, null=True, blank=True)
    invoice_line3 = models.CharField(max_length=100, null=True, blank=True)
    application_title = models.CharField(max_length=200, null=True, blank=True)
    quick_sales_entry_customer = models.BooleanField(default=False)
    quick_payment_type = models.CharField(max_length=20, null=True, blank=True)
    quick_sales_client_id = models.CharField(
        max_length=20, null=True, blank=True)
    quick_sales_account_number = models.CharField(
        max_length=20, null=True, blank=True)
    quick_sales_client_name = models.CharField(
        max_length=200, null=True, blank=True)
    quick_sales_client_address = models.CharField(
        max_length=200, null=True, blank=True)
    emi_profit_receivable = models.CharField(max_length=13, null=False)
    emi_profit_receive = models.CharField(max_length=13, null=False)
    product_wise_ledger = models.BooleanField(default=False)
    product_stock_gl = models.CharField(max_length=13, null=False)
    stock_due_gl = models.CharField(max_length=13, null=False)
    product_sales_gl = models.CharField(max_length=13, null=False)
    sales_due_gl = models.CharField(max_length=13, null=False)
    stock_ret_gl = models.CharField(max_length=13, null=False)
    sales_ret_gl = models.CharField(max_length=13, null=False)
    invoice_discount_gl = models.CharField(max_length=13, null=False)
    damage_gl = models.CharField(max_length=13, null=False)
    product_stock_parent_gl = models.CharField(max_length=13, null=False)
    product_sales_parent_gl = models.CharField(max_length=13, null=False)
    product_stock_ret_parent_gl = models.CharField(max_length=13, null=False)
    product_sales_ret_parent_gl = models.CharField(max_length=13, null=False)
    product_damage_parent_gl = models.CharField(max_length=13, null=False)
    profit_and_loss_ledger = models.CharField(max_length=13, null=False)
    profit_ledger = models.CharField(max_length=13, null=False)
    loss_ledger = models.CharField(max_length=13, null=False)
    stock_in_hand_ledger = models.CharField(max_length=13, null=False)
    cost_of_good_sold_ledger = models.CharField(max_length=13, null=False)
    sales_price_editable = models.BooleanField(default=False)
    sales_discount_rate_editable = models.BooleanField(default=False)
    sales_discount_amount_editable = models.BooleanField(default=False)
    sales_executive_phone_editable = models.BooleanField(default=False)
    payment_document_mandatory = models.BooleanField(default=False)
    sales_payment_document_lebel = models.CharField(max_length=100, null=False)
    client_admission_fee_auto = models.BooleanField(default=False)
    client_admission_fee = models.DecimalField(
        null=True, blank=True, max_digits=22, decimal_places=2, default=0.00)
    client_admission_fee_ledger = models.CharField(
        max_length=20, null=True, blank=True)
    transaction_from_date = models.DateField(null=True, blank=True)
    transaction_doc_required = models.BooleanField(
        default=False, null=True, blank=True)

    def __str__(self):
        return str(self.company_name)


class EMI_Settings(models.Model):
    emi_profit_receivable = models.CharField(max_length=13, null=False)
    emi_profit_receive = models.CharField(max_length=13, null=False)
    emi_fee_auto = models.BooleanField(default=False)
    emi_fee = models.DecimalField(
        null=True, blank=True, max_digits=22, decimal_places=2, default=0.00)
    emi_fee_ledger = models.CharField(max_length=20, null=True, blank=True)
    emi_fee_chargecd = models.CharField(
        max_length=20, null=True, blank=True)
    emi_down_payment = models.BooleanField(default=False)
    emi_min_down_payment_pct = models.DecimalField(
        null=True, blank=True, max_digits=22, decimal_places=2, default=0.00)
    emi_doc_fee_enable = models.BooleanField(default=False)
    emi_doc_fee_ledger = models.CharField(max_length=20, null=True, blank=True)
    emi_insurance_readonly = models.BooleanField(default=False)
    emi_insurance_enable = models.BooleanField(default=False)
    emi_insurance_ledger = models.CharField(
        max_length=20, null=True, blank=True)


class Clients(models.Model):
    client_id = models.CharField(max_length=20, primary_key=True, blank=True)
    #branch_client_id = models.CharField(max_length=50, blank=True)
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20)
    #center_code = models.ForeignKey(Center, on_delete=models.PROTECT,related_name='cli_center_code', db_column='center_code', blank=True, null=False)
    client_name = models.CharField(max_length=200)
    client_type = models.CharField(max_length=20, default='')
    client_referred_by = models.CharField(max_length=15, null=True, blank=True)
    client_father_name = models.CharField(max_length=200)
    client_mother_name = models.CharField(max_length=200, blank=True, null=True)
    client_blood_group = models.CharField(
        max_length=5, default='', choices=BLOOD_GROUP, blank=True)
    client_sex = models.CharField(
        max_length=5, null=True, choices=GENDER_LIST, default='', blank=True)
    client_religion = models.CharField(
        max_length=5, default='', choices=RELIGION_LIST, blank=True)
    client_marital_status = models.CharField(
        max_length=5, null=True, default='', choices=MARITAL_STATUS, blank=True)
    client_national_id = models.CharField(
        max_length=200, null=True, blank=True)
    client_present_address = models.TextField(null=True, blank=False)
    client_permanent_address = models.TextField(null=True, blank=True)
    client_phone = models.CharField(max_length=15, null=True)
    client_email = models.CharField(max_length=30, null=True, blank=True)
    client_joining_date = models.DateField()
    closing_date = models.DateField(null=True, blank=True)
    client_education = models.CharField(
        max_length=50, null=True, choices=EDU_LIST, default='', blank=True)
    client_date_of_birth = models.DateField(null=True, blank=True)
    client_status = models.CharField(
        max_length=5, null=True, choices=STATUS_LIST, default='A', blank=True)
    client_birth_place = models.ForeignKey(Loc_District, on_delete=models.CASCADE,
                                           null=True, blank=True, db_column='district_id', related_name='cli_district_id')
    client_monthly_income = models.DecimalField(null=True, blank=True, max_digits=22, decimal_places=2, default=0.00)
    client_annual_income = models.DecimalField(null=True, blank=True, max_digits=22, decimal_places=2, default=0.00)
    client_admit_fee = models.DecimalField(null=True, blank=True, max_digits=22, decimal_places=2, default=0.00)
    client_admit_fee_batch = models.IntegerField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.client_name)


class Supplier_Information(models.Model):
    supp_id = models.CharField(max_length=20, primary_key=True)
    branch_code = models.IntegerField(blank=True)
    supp_name = models.CharField(max_length=100, null=False)
    proprietor_name = models.CharField(max_length=100, null=True, blank=True)
    joining_date = models.DateField()
    account_number = models.CharField(max_length=20, null=True, blank=True)
    supp_address = models.CharField(max_length=300, null=True, blank=True)
    supp_mobile = models.CharField(max_length=20, null=True)
    supp_email = models.CharField(max_length=100, null=True, blank=True)
    supp_web = models.CharField(max_length=100, null=True, blank=True)
    supp_key_person = models.CharField(max_length=100, null=True, blank=True)
    supp_fax = models.CharField(max_length=20, null=True, blank=True)
    supp_grade = models.CharField(
        max_length=20, choices=SUPP_GRADE, default='', null=True, blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.supp_name)


class Nominee_Information(models.Model):
    client_id = models.ForeignKey(
        Clients, on_delete=models.CASCADE, db_column='client_id', related_name='nmi_client_id')
    nominee_serial = models.CharField(max_length=20, null=True, blank=True)
    nominee_name = models.CharField(max_length=100, null=False)
    nominee_sex = models.CharField(
        max_length=20, choices=GENDER_LIST, null=False)
    nominee_father_name = models.CharField(max_length=100, null=False)
    nominee_mother_name = models.CharField(max_length=20, null=False)
    nominee_present_addr = models.CharField(max_length=300, null=False)
    nominee_permanent_addr = models.CharField(max_length=300, null=False)
    nominee_birth_date = models.DateField(null=True, blank=True)
    nominee_nid_num = models.CharField(max_length=20, null=False)
    nominee_religion = models.CharField(
        max_length=20, choices=RELIGION_LIST, null=False)
    nominee_blood_group = models.CharField(
        max_length=4, default='', choices=BLOOD_GROUP, blank=True)
    nominee_education = models.CharField(
        max_length=20, choices=EDU_LIST, null=False)
    nominee_marital_status = models.CharField(
        max_length=2, choices=MARITAL_STATUS, null=False)
    nominee_mobile_num = models.CharField(max_length=20, null=False)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.nominee_name)


class Client_Photo_Sign(models.Model):
    client_id = models.ForeignKey(
        Clients, on_delete=models.CASCADE, db_column='client_id', related_name='cps_client_id')
    document_type = models.CharField(
        max_length=2, choices=DOCUMENT_TYPES, default='')
    document_location = models.ImageField(upload_to='sign_image/')
    status = models.CharField(max_length=2, null=True,
                              choices=STATUS_LIST, default='A', blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Products_Group(models.Model):
    group_id = models.CharField(max_length=20, blank=True, primary_key=True)
    group_name = models.CharField(max_length=200, null=False)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.group_id)+" "+str(self.group_name)


class Products_Brand(models.Model):
    brand_id = models.CharField(max_length=20, blank=True, primary_key=True)
    brand_name = models.CharField(max_length=200, null=False)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.brand_id)+" "+str(self.brand_name)

class Products_Unit(models.Model):
    unit_id = models.CharField(max_length=20, blank=True, primary_key=True)
    unit_name = models.CharField(max_length=200, null=False)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return str(self.unit_name)

        
class products(models.Model):
    product_id = models.CharField(max_length=20, primary_key=True, blank=True)
    product_name = models.CharField(max_length=200)
    product_model = models.CharField(max_length=200, blank=True, null=True)
    product_group = models.ForeignKey(
        Products_Group, on_delete=models.CASCADE, db_column='product_group', related_name='pro_product_group', null=True, blank=True)
    brand_id = models.ForeignKey(Products_Brand, on_delete=models.CASCADE, db_column='brand_id', related_name='pro_brand_id', null=True, blank=True)
    product_bar_code = models.CharField(max_length=200, blank=True, null=True)
    product_search_text = models.CharField(
        max_length=400, blank=True, null=True)
    product_current_rate = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    product_purces_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    product_sales_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    emi_sales_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    whole_sales_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    sales_discount_type = models.CharField(
        max_length=1, null=True, choices=SALES_DISCOUNT, default='P')
    sales_discount_percent = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    sales_discount_maxamt = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    sales_discount_minamt = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    sales_discount_fromdt = models.DateField(blank=True, null=True)
    sales_discount_uptodt = models.DateField(blank=True, null=True)
    product_tax_rate = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    product_total_stock = models.IntegerField(null=True, default=0, blank=True)
    product_total_sales = models.IntegerField(null=True, default=0, blank=True)
    total_stock_return = models.IntegerField(
        null=True, default=0, blank=True)
    total_sales_return = models.IntegerField(
        null=True, default=0, blank=True)
    product_total_damage = models.IntegerField(
        null=True, default=0, blank=True)
    product_available_stock = models.IntegerField(
        null=True, default=0, blank=True)
    product_last_stock_date = models.DateField(null=True, blank=True)
    total_order_quantity = models.IntegerField(null=True, default=0)
    last_order_date = models.DateField(null=True, blank=True)
    product_last_sale_date = models.DateField(null=True, blank=True)
    product_last_return_date = models.DateField(null=True, blank=True)
    product_stock_alert = models.IntegerField(null=True, default=0, blank=True)
    product_life_time = models.IntegerField(null=True, default=0)
    product_status = models.CharField(
        max_length=2, null=True, choices=STATUS_LIST, default='A')
    total_purchase_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_sales_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    stock_return_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    sales_return_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_return_damage = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    product_narration = models.CharField(max_length=200, null=True, blank=True)
    update_unauth_product = models.BooleanField(blank=True, default=False)
    product_stock_gl = models.CharField(max_length=13, null=False, blank=True)
    product_sales_gl = models.CharField(max_length=13, null=False, blank=True)
    product_order_gl = models.CharField(max_length=13, null=True, blank=True)
    product_profit_gl = models.CharField(max_length=13, null=True, blank=True)
    product_loss_gl = models.CharField(max_length=13, null=True, blank=True)
    product_stock_ret_gl = models.CharField(
        max_length=13, null=False, blank=True)
    product_sales_ret_gl = models.CharField(
        max_length=13, null=False, blank=True)
    product_damage_gl = models.CharField(max_length=13, null=False, blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product_name)+" ("+str(self.product_model)+")"

class Products_Price_Type(models.Model):
    tran_type_code = models.CharField(max_length=20, null=False, blank=False)
    product_price = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return str(self.tran_type_code)


class Products_Inventory_Status(models.Model):
    branch_code = models.IntegerField(blank=True)
    product_id = models.CharField(max_length=20, null=False, blank=True)
    product_total_stock = models.IntegerField(null=True, default=0, blank=True)
    total_order_quantity = models.IntegerField(null=True, default=0)
    product_total_sales = models.IntegerField(null=True, default=0, blank=True)
    total_stock_return = models.IntegerField(null=True, default=0, blank=True)
    total_sales_return = models.IntegerField(null=True, default=0, blank=True)
    product_total_damage = models.IntegerField(
        null=True, default=0, blank=True)
    product_available_stock = models.IntegerField(
        null=True, default=0, blank=True)
    product_purchase_rate = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    last_stock_date = models.DateField(null=True, blank=True)
    last_order_date = models.DateField(null=True, blank=True)
    last_sale_date = models.DateField(null=True, blank=True)
    last_stock_return_date = models.DateField(null=True, blank=True)
    last_sales_return_date = models.DateField(null=True, blank=True)
    last_damage_date = models.DateField(null=True, blank=True)
    inv_balance_upto_date = models.DateField(null=True, blank=True)
    total_purchase_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_sales_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    stock_return_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    sales_return_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_damage_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    damage_receive_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cost_of_good_sold = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_discount_receive = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_discount_pay = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    is_balance_updated = models.BooleanField(default=False, null=True, blank=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

class Products_Inventory_Hist(models.Model):
    branch_code = models.IntegerField(blank=True)
    product_id = models.CharField(max_length=20, null=False, blank=True)
    inv_balance_date = models.DateField(null=True, blank=True)
    product_total_stock = models.IntegerField(null=True, default=0, blank=True)
    total_order_quantity = models.IntegerField(null=True, default=0)
    product_total_sales = models.IntegerField(null=True, default=0, blank=True)
    total_stock_return = models.IntegerField(null=True, default=0, blank=True)
    total_sales_return = models.IntegerField(null=True, default=0, blank=True)
    product_total_damage = models.IntegerField(
        null=True, default=0, blank=True)
    product_available_stock = models.IntegerField(
        null=True, default=0, blank=True)
    product_purchase_rate = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_purchase_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_purchase_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_sales_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_sales_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    stock_return_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    sales_return_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_damage_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cost_of_good_sold = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cost_of_good_sold_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_discount_receive = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_discount_pay = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Product_Price_List(models.Model):
    branch_code = models.IntegerField(blank=True)
    product_id = models.CharField(max_length=20, null=False)
    product_name = models.CharField(max_length=200)
    client_type_code = models.CharField(max_length=20, blank=False)
    product_sales_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    sales_discount_type = models.CharField(
        max_length=1, null=True, choices=SALES_DISCOUNT, default='P')
    sales_discount_percent = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    sales_discount_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    sales_discount_fromdt = models.DateField(blank=True, null=True)
    sales_discount_uptodt = models.DateField(blank=True, null=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Product_Offer_List(models.Model):
    branch_code = models.IntegerField(blank=True)
    product_id = models.CharField(max_length=20, null=False)
    product_name = models.CharField(max_length=200)
    client_type_code = models.CharField(max_length=20, blank=False)
    sales_offer_type = models.CharField(
        max_length=1, null=True, choices=OFFER_TYPE, default='')
    offer_from_quantity = models.IntegerField(null=True, default=0)
    offer_upto_quantity = models.IntegerField(null=True, default=0)
    offer_free_quantity = models.IntegerField(null=True, default=0)
    offer_from_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    offer_upto_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    offer_reduce_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    sales_offer_fromdt = models.DateField(blank=True, null=True)
    sales_offer_uptodt = models.DateField(blank=True, null=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Product_Offer_Package(models.Model):
    branch_code = models.IntegerField(blank=True)
    product_id = models.CharField(max_length=20, null=False)
    product_name = models.CharField(max_length=200, blank=False, null=True)
    client_type_code = models.CharField(max_length=20, blank=False)
    offer_from_quantity = models.IntegerField(null=True, default=0)
    offer_upto_quantity = models.IntegerField(null=True, default=0)
    free_product_code = models.CharField(max_length=20, blank=False, null=True)
    free_product_name = models.CharField(max_length=200, blank=False)
    offer_free_quantity = models.IntegerField(null=True)
    sales_offer_fromdt = models.DateField(blank=True, null=True)
    sales_offer_uptodt = models.DateField(blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class ShowRoom(models.Model):
    showroom_id = models.CharField(max_length=20, blank=True, null=True)
    show_room_name = models.CharField(max_length=100)
    show_room_address = models.TextField(blank=True)
    comments = models.TextField(blank=True)

    def __str__(self):
        return str(self.show_room_name)

class StockMaster(models.Model):
    branch_code = models.IntegerField(blank=True)
    stock_id = models.CharField(max_length=10, null=False)
    supplier_id = models.CharField(max_length=20, null=False)
    stock_date = models.DateField(null=True)
    tran_type_code = models.CharField(
        max_length=13, null=True, default='CS', blank=True)
    tran_batch_number = models.IntegerField(default=0, null=True, blank=True)
    voucher_number = models.CharField(max_length=20, blank=True, null=True)
    show_room = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=2, choices=STOCK_STATUS, default='W')
    payment_comments = models.CharField(max_length=200, blank=True, null=True)
    total_quantity = models.IntegerField()
    returned_quantity = models.IntegerField(blank=True, default=0, null=True)
    returned_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    cancel_quantity = models.IntegerField(blank=True, default=0, null=True)
    cancel_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    total_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    total_pay = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    due_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    discount_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    comments = models.TextField(blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class StockMasterAuthQ(models.Model):
    branch_code = models.IntegerField(blank=True)
    stock_id = models.CharField(max_length=10, null=False, blank=True)
    supplier_id = models.CharField(max_length=20, null=False)
    stock_date = models.DateField(null=True, blank=True)
    voucher_number = models.CharField(max_length=20, blank=True, null=True)
    show_room = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(
        max_length=2, choices=STOCK_STATUS, default='W', blank=True, null=True)
    tran_type_code = models.CharField(
        max_length=13, null=True, default='CS', blank=True)
    payment_comments = models.CharField(max_length=200, blank=True, null=True)
    total_quantity = models.IntegerField(null=True, blank=True)
    returned_quantity = models.IntegerField(blank=True, default=0, null=True)
    returned_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    cancel_quantity = models.IntegerField(blank=True, default=0, null=True)
    cancel_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    total_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    total_pay = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    due_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    discount_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    comments = models.TextField(blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class StockDetails(models.Model):
    branch_code = models.IntegerField(blank=True)
    stock_id = models.CharField(max_length=10, null=False)
    supplier_id = models.CharField(max_length=20, null=False)
    product_id = models.CharField(max_length=10, null=False)
    purces_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=2, choices=STOCK_STATUS, default='S', null=True)
    quantity = models.IntegerField(blank=True, null=True)
    returned_quantity = models.IntegerField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)
    stock_date = models.DateField(auto_now_add=True)
    comments = models.TextField(blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class StockDetailsTemp(models.Model):
    branch_code = models.IntegerField(blank=True)
    product_id = models.ForeignKey(
        products, on_delete=models.CASCADE, db_column='product_id', related_name='sdt_product_id')
    product_name = models.CharField(max_length=200, null=False, blank=False)
    product_model = models.CharField(max_length=100, null=True, blank=True)
    product_bar_code = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField()
    purces_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    status = models.CharField(max_length=2, choices=STOCK_STATUS, default='N')
    comments = models.CharField(max_length=200, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class StockPaymentDetails(models.Model):
    branch_code = models.IntegerField(blank=True)
    stock_id = models.CharField(max_length=10, null=False, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    pay_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    payment_date = models.DateField(auto_now_add=True, blank=True)
    payment_comments = models.CharField(max_length=200, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Stock_Return_Details(models.Model):
    branch_code = models.IntegerField(blank=True)
    product_id = models.CharField(max_length=30, null=False)
    supplier_id = models.CharField(max_length=20, null=False)
    return_date = models.DateField(blank=True, null=True)
    stock_id = models.CharField(max_length=10, null=False, blank=True)
    stock_date = models.DateField(blank=True, null=True)
    stock_voucher = models.CharField(max_length=20, blank=True, null=True)
    tran_type_code = models.CharField(
        max_length=13, null=True, default='CS', blank=True)
    tran_batch_number = models.IntegerField(default=0, null=True, blank=True)
    returned_quantity = models.IntegerField()
    return_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    return_voucher = models.CharField(max_length=20, blank=True)
    return_reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Product_Damage_Details(models.Model):
    branch_code = models.IntegerField(blank=True)
    product_id = models.CharField(max_length=30, null=False)
    supplier_id = models.CharField(max_length=20, null=False, blank=True)
    damage_date = models.DateField(null=True, blank=True)
    tran_batch_number = models.IntegerField(default=0, null=True, blank=True)
    damage_quantity = models.IntegerField()
    damage_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    receive_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    comments = models.TextField(blank=True, null=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Sales_Master(models.Model):
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20, blank=True)
    invoice_number = models.CharField(max_length=20, null=True, blank=True)
    order_number = models.CharField(max_length=20, null=True, blank=True)
    invoice_date = models.DateField()
    tran_type_code = models.CharField(
        max_length=13, null=True, default='CS', blank=True)
    tran_batch_number = models.IntegerField(default=0, null=True, blank=True)
    customer_id = models.CharField(max_length=20, null=True, blank=True)
    customer_name = models.CharField(max_length=200, null=True, blank=True)
    customer_phone = models.CharField(max_length=20, null=True, blank=True)
    customer_address = models.CharField(max_length=500, null=True, blank=True)
    employee_id = models.CharField(max_length=20, blank=True)
    payment_document = models.CharField(max_length=100, blank=True)
    total_quantity = models.IntegerField(blank=True)
    returned_quantity = models.IntegerField(null=True, blank=True, default=0)
    returned_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    total_bill_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    bill_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    pay_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    due_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    advance_pay = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    total_discount_rate = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    total_discount_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    invoice_discount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    sms_notification = models.BooleanField(
        default=False, null=True, blank=True)
    email_notification = models.BooleanField(
        default=False, null=True, blank=True)
    status = models.CharField(
        max_length=2, choices=SALES_STATUS, default='N', null=True, blank=True)
    invoice_comments = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=22, decimal_places=12, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=22, decimal_places=12, null=True, blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Sales_Return_Details(models.Model):
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20, blank=True)
    client_id = models.CharField(max_length=20, null=True, blank=True)
    product_id = models.CharField(max_length=30, null=False)
    return_invoice = models.CharField(max_length=20, null=True, blank=True)
    return_date = models.DateField()
    sales_invoice = models.CharField(max_length=20, null=True, blank=True)
    sales_date = models.DateField(null=True, blank=True)
    tran_type_code = models.CharField(
        max_length=13, null=True, default='CS', blank=True)
    tran_batch_number = models.IntegerField(default=0, null=True, blank=True)
    returned_quantity = models.IntegerField()
    return_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    purchase_value = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    return_reason = models.TextField(null=True, blank=True)
    status = models.CharField(null=True, max_length=2,
                              choices=SALES_STATUS, default='N', blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Order_Master(models.Model):
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20, blank=True)
    employee_id = models.CharField(max_length=20, null=False, blank=False)
    order_number = models.CharField(max_length=20, null=True, blank=True)
    order_date = models.DateField()
    customer_id = models.CharField(max_length=20, null=True, blank=True)
    account_number = models.CharField(max_length=13, null=True, blank=True)
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    customer_address = models.CharField(max_length=500, blank=True, null=True)
    executive_phone = models.CharField(max_length=20, blank=True, null=True)
    total_quantity = models.IntegerField(blank=True)
    returned_quantity = models.IntegerField(null=True, blank=True, default=0)
    total_bill_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    bill_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    pay_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    due_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    advance_pay = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    total_discount_rate = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    total_discount_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    tran_type_code = models.CharField(
        max_length=13, null=True, default='CS', blank=True)
    tran_batch_number = models.IntegerField(default=0, null=True, blank=True)
    status = models.CharField(
        max_length=2, choices=ORDER_STATUS, default='N', null=True, blank=True)
    order_comments = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=22, decimal_places=12, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=22, decimal_places=12, null=True, blank=True)
    delivary_date = models.DateField(null=False,blank=False)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Order_Details(models.Model):
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20, blank=True)
    order_number = models.CharField(max_length=20, null=True, blank=True)
    order_date = models.DateField(null=True, blank=True)
    product_id = models.CharField(max_length=10, null=True, blank=True)
    serial_no = models.IntegerField(null=True, blank=True, default=0)
    service_type = models.CharField(max_length=10, null=True, blank=True)
    service_start_date = models.DateField(null=True, blank=True)
    service_end_date = models.DateField(null=True, blank=True)
    service_card_no = models.CharField(max_length=200, null=True, blank=True)
    ordered_product_price = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    product_price = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    quantity = models.IntegerField()
    ordered_quantity = models.IntegerField(null=True, blank=True)
    delivered_quantity = models.IntegerField(null=True, blank=True)
    total_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    ordered_total_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    delivered_total_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    profit_amount = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    discount_rate = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    ordered_discount_rate = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    delivered_discount_rate = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    discount_amount = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    ordered_discount_amount = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    delivered_discount_amount = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    status = models.CharField(null=True, max_length=2,
                              choices=ORDER_STATUS, default='N', blank=True)
    comments = models.TextField(null=True, blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_on = models.DateField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Sales_Details(models.Model):
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20, blank=True)
    invoice_number = models.CharField(max_length=20, null=True, blank=True)
    client_id = models.CharField(max_length=20, null=True, blank=True)
    product_id = models.CharField(max_length=10, null=False, blank=True)
    serial_no = models.IntegerField(null=True, blank=True, default=0)
    service_type = models.CharField(max_length=10, null=True, blank=True)
    service_start_date = models.DateField(null=True, blank=True)
    service_end_date = models.DateField(null=True, blank=True)
    service_card_no = models.CharField(max_length=200, null=True, blank=True)
    purchase_rate = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    product_price = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    quantity = models.IntegerField()
    returned_quantity = models.IntegerField(null=True, blank=True, default=0)
    total_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    profit_amount = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    discount_rate = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    discount_amount = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    status = models.CharField(null=True, max_length=2,
                              choices=SALES_STATUS, default='N', blank=True)
    comments = models.TextField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Sales_Details_Temp(models.Model):
    details_branch_code = models.CharField(
        max_length=20, blank=True, null=True)
    invoice_number = models.CharField(max_length=20, null=True, blank=True)
    product_id = models.CharField(max_length=10, null=False, blank=True)
    product_bar_code = models.CharField(max_length=200, blank=True, null=True)
    product_name = models.CharField(max_length=200)
    product_model = models.CharField(max_length=100, null=True, blank=True)
    sales_account_number = models.CharField(
        max_length=20, blank=True, null=True)
    serial_no = models.IntegerField(null=True, blank=True, default=0)
    service_type = models.CharField(max_length=10, null=True, blank=True)
    service_start_date = models.DateField(null=True, blank=True)
    service_end_date = models.DateField(null=True, blank=True)
    service_card_no = models.CharField(max_length=200, null=True, blank=True)
    product_price = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    quantity = models.IntegerField()
    total_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    profit_amount = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    discount_rate = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    discount_amount = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    status = models.CharField(null=True, max_length=2,
                              choices=SALES_STATUS, default='N', blank=True)
    comments = models.TextField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Client_Profit_History(models.Model):
    branch_code = models.IntegerField(blank=True)
    client_id = models.ForeignKey(
        Clients, on_delete=models.CASCADE, db_column='client_id', related_name='clp_client_id')
    profit_from_date = models.DateField(null=True)
    profit_upto_date = models.DateField(null=True)
    profit_from_account = models.CharField(max_length=13, null=False)
    profit_to_account = models.CharField(max_length=13, null=False)
    total_purchase_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_sales_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_customer_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_supplier_balance = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    profit_or_loss_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    transaction_date = models.DateField()
    batch_number = models.IntegerField(default=0)
    bill_payment_batch = models.IntegerField(default=0)
    cancel_date = models.DateField(null=True, blank=True)
    cancel_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Client_Balance(models.Model):
    client_id = models.CharField(max_length=20, default='')
    account_number = models.CharField(max_length=13, null=False)
    total_purchase_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_purchase_payment = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_purchase_quantity = models.IntegerField(default=0)
    total_sales_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_sales_payment = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_sales_quantity = models.IntegerField(default=0)
    total_order_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_order_payment = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_order_quantity = models.IntegerField(default=0)
    total_sales_return_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_sales_return_quantity = models.IntegerField(default=0)
    total_order_return_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_order_return_quantity = models.IntegerField(default=0)
    total_purchase_return_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_purchase_return_quantity = models.IntegerField(default=0)
    total_damage_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_damage_quantity = models.IntegerField(default=0)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client_id


class Delar_Security_Info(models.Model):
    client_id = models.ForeignKey(
        Clients, on_delete=models.CASCADE, db_column='client_id', related_name='dsi_client_id')
    branch_code = models.IntegerField(blank=True)
    phone_number = models.CharField(max_length=15, null=False)
    client_type_code = models.CharField(max_length=20, blank=False)
    credit_limit = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    tin_number = models.CharField(max_length=200, null=False, blank=True)
    trade_licence_number = models.CharField(
        max_length=200, null=True, blank=True)
    guarantor_number = models.CharField(max_length=15, null=True, blank=True)
    cheque_number = models.CharField(max_length=200, null=True, blank=True)
    cheque_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    cheque_date = models.CharField(max_length=200, null=True, blank=True)
    bank_name = models.CharField(max_length=200, null=True, blank=True)
    branch_name = models.CharField(max_length=200, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Emi_Setup(models.Model):
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20, blank=True)
    client_id = models.CharField(max_length=13, null=True, blank=True)
    account_number = models.CharField(max_length=13, null=True, blank=True)
    emi_serial_number = models.IntegerField(
        blank=True, null=True)  # Disburse Serial
    emi_reference_no = models.CharField(
        max_length=200, null=False)  # Invoice Number
    emi_reference_date = models.DateField(
        null=True, blank=True)  # Invoice Date
    emi_reference_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)  # Invoice Amount
    emi_down_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    reference_due_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_emi_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_emi_due = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    emi_inst_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    emi_inst_frequency = models.CharField(
        max_length=10, choices=INSTFRQ_LIST, null=False)
    emi_inst_repay_from_date = models.DateField(null=True, blank=True)
    number_of_installment = models.IntegerField(default=1)
    installment_tot_repay_amt = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    installment_exp_date = models.DateField(null=True, blank=True)
    installment_lastpay_date = models.DateField(null=True, blank=True)
    emi_rate = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    emi_profit_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    emi_fee_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    emi_ins_rate = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    emi_ins_fee_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    emi_doc_fee_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    emi_setup_batch = models.IntegerField(blank=True, null=True)
    emi_closer_date = models.DateField(null=True, blank=True)
    emi_reschedule_date = models.DateField(null=True, blank=True)
    last_emi_hist_update = models.DateField(null=True, blank=True)
    last_emi_payment_date = models.DateField(null=True, blank=True)
    is_balance_updated = models.BooleanField(default=False)
    emi_cancel_by = models.CharField(max_length=20, null=True, blank=True)
    emi_cancel_on = models.DateTimeField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

class Emi_Receive(models.Model):
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20, blank=True)
    client_id = models.CharField(max_length=13, null=True, blank=True)
    account_number = models.CharField(max_length=13, null=True, blank=True)
    emi_reference_no = models.CharField(max_length=20, null=False)
    receive_date = models.DateField(null=True, blank=True)
    entry_day_sl = models.IntegerField(null=True, blank=True)
    receive_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    transaction_narration = models.CharField(
        max_length=200, null=True, blank=True)
    tran_batch_number = models.IntegerField(null=True)
    penalty_charge = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    receive_document_number = models.CharField(
        max_length=50, null=True, blank=True)
    is_transfer = models.BooleanField(default=False)
    emi_cancel_by = models.CharField(max_length=20, null=True, blank=True)
    emi_cancel_on = models.DateField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Emi_History(models.Model):
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20, blank=True)
    account_number = models.CharField(max_length=13, null=True, blank=True)
    emi_reference_no = models.CharField(max_length=20, null=False)
    emi_rate = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    emi_inst_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    inst_receive_date = models.DateField(null=True, blank=True)
    inst_receive_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    total_installment_due = models.IntegerField(blank=True, null=True)
    total_installment_payment = models.IntegerField(blank=True, null=True)
    total_installment_overdue = models.IntegerField(blank=True, null=True)
    total_installment_advance = models.IntegerField(blank=True, null=True)
    total_emi_outstanding = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    emi_principal_outstanding = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    emi_profit_outstanding = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    emi_total_payment = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    emi_principal_payment = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    emi_profit_payment = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    total_advance_recover = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    principal_advance_recover = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    profit_advance_recover = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    total_due_recover = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    principal_due_recover = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    profit_due_recover = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    emi_total_overdue = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    emi_principal_overdue = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    emi_profit_overdue = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class all_trandtl  (models.Model):
    center_code = models.CharField(max_length=20, null=True)
    center_name = models.CharField(max_length=200, null=True)
    client_id = models.CharField(max_length=200, null=True)
    client_name = models.CharField(max_length=200, null=True)
    invoice_date = models.DateField(null=True, blank=True)
    invoice_number = models.CharField(max_length=20, null=True)
    product_name = models.CharField(max_length=200, null=True)
    product_model = models.CharField(max_length=200, null=True)
    product_quantity = models.CharField(max_length=200, null=True)
    product_price = models.CharField(max_length=200, null=True)
    total_price = models.IntegerField(null=True, blank=True)
    pay_amount = models.IntegerField(null=True, blank=True)
    due_amount = models.IntegerField(null=True, blank=True)
    instrepay_repay_amt = models.IntegerField(null=True, blank=True)
    instrepay_repay_freq = models.CharField(max_length=200, null=True)
    nof_installment = models.IntegerField(null=True, blank=True)
    instrepay_tot_repay_amt = models.IntegerField(null=True, blank=True)
    instrcv_inv_number = models.CharField(max_length=200, null=True)
    instrcv_entry_date = models.DateField(null=True, blank=True)
    instrcv_instlmnt = models.IntegerField(null=True, blank=True)
    instrcv_ref_num = models.CharField(max_length=200, null=True)
    deposit_date = models.DateField(null=True, blank=True)
    deposit_amount = models.IntegerField(null=True, blank=True)
    deposit_memo_num = models.CharField(max_length=200,  null=True, blank=True)
    dpsrcv_date = models.DateField(null=True, blank=True)
    dpsrcv_amount = models.IntegerField(null=True, blank=True)
    dpsrcv_memo_num = models.CharField(max_length=200, null=True, blank=True)
    app_user_id = models.CharField(max_length=200, null=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Client_Id_Changes_Hist(models.Model):
    old_client_id = models.CharField(max_length=100)
    new_client_id = models.CharField(max_length=100)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.new_client_id


class Fees_History(models.Model):
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20, blank=True)
    client_id = models.CharField(
        max_length=20, default='', null=True, blank=True)
    fee_type = models.CharField(max_length=20)
    fee_amount = models.DecimalField(
        null=True, blank=True, max_digits=22, decimal_places=2, default=0.00)
    cancel_amount = models.DecimalField(
        null=True, blank=True, max_digits=22, decimal_places=2, default=0.00)
    fee_collection_date = models.DateField(null=True, blank=True)
    transaction_narration = models.CharField(
        max_length=200, null=True, blank=True)
    fee_memo_number = models.CharField(
        max_length=20, default='', null=True, blank=True)
    transaction_batch_number = models.IntegerField(null=True, blank=True)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_date = models.DateField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fee_type


class Client_Closing(models.Model):
    client_id = models.CharField(max_length=100)
    closing_date = models.DateField(null=False, blank=False)
    closing_reason = models.CharField(max_length=200)
    cancel_by = models.CharField(max_length=20, null=True, blank=True)
    cancel_date = models.DateField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client_id



######################## Purchase order ################

class Purchase_Order_Mst(models.Model):
   branch_code = models.CharField(max_length=20, null=True, blank=True)
   purchase_ord_no = models.CharField(max_length=20, null=True, blank=True)
   purchase_type = models.CharField(max_length=20, null=True, blank=True)
   purchase_date = models.DateField()
   payment_comments = models.CharField(max_length=200, blank=True, null=True)
   supplier_id = models.CharField(max_length=20, null=False)
   discount_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
   unit_price = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
   total_pay = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
   due_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
   g_total_price = models.DecimalField(null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
   status = models.CharField(max_length=2, choices=STOCK_STATUS, default='W')
   product_id  = models.CharField(max_length=20, null=True, blank=True)
   origin  = models.CharField(max_length=20, null=True, blank=True)
   total_pur_qnty = models.IntegerField(blank=True)
   voucher_number = models.CharField(max_length=20, blank=True, null=True)
   show_room = models.CharField(max_length=20, blank=True, null=True)
   comments = models.TextField(blank=True, null=True)
   app_user_id = models.CharField(max_length=20, null=False)
   


class PurchaseMasterAuthQ(models.Model):
   branch_code = models.CharField(max_length=20, null=True, blank=True)
   purchase_ord_no = models.CharField(max_length=20, null=True, blank=True)
   purchase_type = models.CharField(max_length=20, null=True, blank=True)
   purchase_date = models.DateField()
   payment_comments = models.CharField(max_length=200, blank=True, null=True)
   supplier_id = models.CharField(max_length=20, null=False)
   discount_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
   unit_price = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
   total_pay = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
   due_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
   status = models.CharField(
        max_length=2, choices=STOCK_STATUS, default='W', blank=True, null=True)    
   g_total_price = models.DecimalField(null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
   product_id  = models.CharField(max_length=20, null=True, blank=True)
   origin  = models.CharField(max_length=20, null=True, blank=True)
   total_pur_qnty = models.IntegerField(blank=True)
   voucher_number = models.CharField(max_length=20, blank=True, null=True)
   show_room = models.CharField(max_length=20, blank=True, null=True)
   comments = models.TextField(blank=True, null=True)
   app_user_id = models.CharField(max_length=20, null=False)
   


class Purchase_Order_Dtl(models.Model):
 
    branch_code = models.CharField(max_length=20, null=True, blank=True)
    purchase_ord_no = models.CharField(max_length=20, null=True, blank=True)
    purchase_type = models.CharField(max_length=20, null=True, blank=True)
    purchase_date = models.DateField()
    product_id  = models.CharField(max_length=20, null=True, blank=True)
    unit_price = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    g_total_price = models.DecimalField(null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    supplier_id = models.CharField(max_length=20, null=False)
    status = models.CharField(
        max_length=2, choices=STOCK_STATUS, default='S', null=True)
    total_pur_qnty = models.IntegerField(blank=True)
    discount_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True, blank=True)
    voucher_number = models.CharField(max_length=20, blank=True, null=True)
    show_room = models.CharField(max_length=20, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=False)
    


class Purchase_Order_Dtl_Temp(models.Model):
    branch_code = models.CharField(max_length=20, null=True, blank=True)	
    product_id = models.ForeignKey(
        products, on_delete=models.CASCADE, db_column='product_id', related_name='sdt_product_id1')
    origin  = models.CharField(max_length=20, null=True, blank=True)
    pur_qnty=  models.IntegerField(blank=True)
    discount_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    unit_price = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    total_price = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)

class Purchase_Bill(models.Model):
    purchase_ord_no  = models.CharField(max_length=20, null=True, blank=True)
    bill_date  = models.DateField()
    purchase_date = models.DateField()
    supllier_id = models.CharField(max_length=20, null=False)
    bill_id = models.CharField(max_length=20, null=False)
    submission_date  = models.DateField()
    bill_amount  = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    payment_amount = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    pending_amount = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    remarks = models.CharField(max_length=200, null=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)



class Stock_quantity_transfer(models.Model):
    

    from_branch_code=models.ForeignKey(Branch, on_delete=models.PROTECT,related_name='sqt_branch_code',db_column='from_branch_code', blank=True, null=True)
    to_branch_code=models.ForeignKey(Branch,on_delete=models.PROTECT,related_name='sqt_branch_code1',db_column='to_branch_code',blank=True,null=True)
    product_id=models.ForeignKey(products,on_delete=models.PROTECT,related_name='sqt_product_id',db_column='product_id',blank=True,null=True)
    product_name=models.CharField(max_length=20,null=True)
    stock_quantity=models.IntegerField(blank=True)
    trf_quantity=models.IntegerField(blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time=models.DateTimeField(auto_now_add=True)



class Sales_commission(models.Model):
    employee_id=models.CharField(max_length=200,null=True,blank=True)
    sales_month=models.CharField(max_length=200,null=True,blank=True)
    sales_quantity=models.BigIntegerField(blank=True)
    total_price=models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)

class Sales_barcode(models.Model):
    product_id=models.ForeignKey(products,on_delete=models.PROTECT,related_name='bcode_product_id',db_column='product_id',blank=True,null=True)
    barcode_image= models.ImageField(upload_to='barcode/', blank=True)
    print_qty= models.IntegerField(default=0)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time=models.DateTimeField(auto_now_add=True)

###########
class Quotation_Master(models.Model):
    quotation_id = models.CharField(max_length=20, null=False)
    quotation_date=models.DateField(null=True, blank=True)
    vat_condition=models.CharField(max_length=20, null=False)
    supplier_id = models.CharField(max_length=20, null=False)
    product_id = models.CharField(max_length=20, null=True)
    edd_date=models.DateField(null=True, blank=True)
    quotation_validity = models.IntegerField(null=True, blank=True)
    warranty = models.IntegerField(null=True, blank=True)
    subject = models.CharField(max_length=200, null=False)
    remarks = models.CharField(max_length=200, null=False)
    is_active  = models.BooleanField(default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

class Quotation_Details(models.Model):
    quotation_id = models.CharField(max_length=20, null=False)
    product_id = models.CharField(max_length=20, null=False)
    unit = models.CharField(max_length=20, null=False)
    quantity = models.IntegerField(null=True, blank=True)
    quotation_date=models.DateField(null=True, blank=True)
    unit_price = models.DecimalField(
    max_digits=22, decimal_places=2, default=0.00)
    total_price = models.DecimalField(
    max_digits=22, decimal_places=2, default=0.00)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

class Quotation_Condition(models.Model):
    quotation_id = models.CharField(max_length=20, null=False)
    cond_id = models.CharField(max_length=20, null=False)
    cond_state  = models.BooleanField(default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)
