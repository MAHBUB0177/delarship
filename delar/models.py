from django.db import models

# Create your models here.
from appauth.models import Employees, Loc_Region, STATUS_LIST, BLOOD_GROUP, GENDER_LIST, RELIGION_LIST, MARITAL_STATUS, CASH_RECEIVE_PAYMENT, TRAN_DEBIT_CREDIT, FIXED_PERCENT, DAY_MONTH_YEAR, DOCUMENT_TYPES, EDU_LIST, WEEK_DAY_LIST, GENDER_LIST
from appauth.models import Loc_Country, Loc_Division, Loc_District, Loc_Upazila, Branch

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

target_type=(
    ('A' ,'By Amount'),
    ('P', 'By Product'),
)


class Application_Settings(models.Model):
    sales_price_editable = models.BooleanField(default=False)
    sales_discount_rate_editable = models.BooleanField(default=False)
    sales_discount_amount_editable = models.BooleanField(default=False)

class Center(models.Model):
    branch_code = models.IntegerField(blank=True)
    center_code = models.CharField(max_length=20, primary_key=True, blank=True)
    branch_center_code = models.CharField(max_length=20, blank=True)
    center_name = models.CharField(max_length=100, null=False)
    center_referred_by = models.CharField(
        max_length=200, null=True, blank=True)
    center_address = models.CharField(max_length=300, null=False)
    center_region_id = models.ForeignKey(Loc_Region, on_delete=models.PROTECT,
                                         related_name='cnt_center_region_id', db_column='center_region_id', blank=True, null=True)
    center_open_date = models.DateField(null=True, blank=True)
    center_employee_id = models.ForeignKey(
        Employees, on_delete=models.PROTECT, related_name='brn_center_employee_id', db_column='center_employee_id', blank=True, null=True)
    center_phone_number = models.CharField(max_length=200, null=False)
    center_day = models.CharField(
        max_length=20, choices=WEEK_DAY_LIST, default='', null=True, blank=True)
    center_status = models.CharField(
        max_length=20, choices=STATUS_LIST, default='A', null=True, blank=True)
    center_close_by = models.CharField(max_length=20, null=False)
    center_closure_date = models.DateField(null=True, blank=True)
    center_search_text = models.CharField(max_length=500, null=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.center_code+"-"+self.center_name

class Employee_Center_Permit(models.Model):
    branch_code = models.CharField(max_length=20, null=True, blank=True)
    employee_id = models.CharField(max_length=20, null=False, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

class Products_Packet_Mapping(models.Model):
    product_id = models.CharField(max_length=20, null=False, blank=True)
    packet_product_id = models.CharField(max_length=20, null=False, blank=True)
    quantity_ratio = models.IntegerField(null=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_id

class Stock_Return_Packet(models.Model):
    branch_code = models.CharField(max_length=20, null=True, blank=True)
    supplier_id = models.CharField(
        max_length=20, default='', null=True, blank=True)
    product_id = models.CharField(max_length=30, null=False)
    return_invoice = models.CharField(max_length=20, null=True, blank=True)
    return_date = models.DateField()
    tran_type_code = models.CharField(
        max_length=13, null=True, default='CS', blank=True)
    tran_batch_number = models.IntegerField(default=0, null=True, blank=True)
    payment_quantity = models.IntegerField()
    payment_value = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    status = models.CharField(null=True, max_length=2,
                              choices=SALES_STATUS, default='N', blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Sales_Return_Packet(models.Model):
    branch_code = models.CharField(max_length=20, null=True, blank=True)
    client_id = models.CharField(
        max_length=20, default='', null=True, blank=True)
    product_id = models.CharField(max_length=30, null=False)
    employee_id=models.CharField(max_length=20,null=True,blank=True)
    return_invoice = models.CharField(max_length=20, null=True, blank=True)
    return_date = models.DateField()
    tran_type_code = models.CharField(
        max_length=13, null=True, default='CS', blank=True)
    tran_batch_number = models.IntegerField(default=0, null=True, blank=True)
    receive_quantity = models.IntegerField()
    receive_value = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    status = models.CharField(null=True, max_length=2,
                              choices=SALES_STATUS, default='N', blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Srstage_Master(models.Model):
    branch_code = models.IntegerField(null=True)
    invoice_number = models.CharField(max_length=20, null=True, blank=True)
    invoice_date = models.DateField()
    employee_id = models.CharField(max_length=20, null=False, blank=True)
    total_quantity = models.IntegerField(blank=True)
    returned_quantity = models.IntegerField(null=True, blank=True, default=0)
    total_sales_quantity = models.IntegerField(
        null=True, blank=True, default=0)
    total_sales_amount = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    total_sales_discount_amount = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
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
    status = models.CharField(
        max_length=2, choices=ORDER_STATUS, default='N', null=True, blank=True)
    invoice_comments = models.TextField(blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Srstage_Details(models.Model):
    branch_code = models.IntegerField(null=True)
    employee_id = models.CharField(max_length=20, null=False, blank=True)
    invoice_number = models.CharField(max_length=20, null=True, blank=True)
    invoice_date = models.DateField(null=True, blank=True)
    product_id = models.CharField(max_length=10, null=True, blank=True)
    product_price = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    return_quantity = models.IntegerField(null=True, blank=True, default=0)
    sales_quantity = models.IntegerField(null=True, blank=True, default=0)
    sales_amount = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    sales_discount_amount = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    total_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    profit_amount = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    discount_rate = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    discount_amount = models.DecimalField(
        null=True, max_digits=22, decimal_places=2, default=0.00, blank=True)
    status = models.CharField(null=True, max_length=2,
                              choices=ORDER_STATUS, default='N', blank=True)
    comments = models.TextField(null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Srstage_Details_Temp(models.Model):
    details_branch_code = models.CharField(
        max_length=20, blank=True, null=True)
    employee_id = models.CharField(max_length=20, null=False, blank=True)
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

class Srstage_Inventory_Status(models.Model):
    branch_code = models.IntegerField(blank=True)
    employee_id = models.CharField(max_length=20, null=False, blank=True)
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
    total_packet_receive= models.IntegerField(
        null=True, default=0, blank=True)
    total_packet_payment= models.IntegerField(
        null=True, default=0, blank=True)
    packet_payment_value = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    packet_receive_value = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Srstage_Inventory_Hist(models.Model):
    branch_code = models.IntegerField(blank=True)
    employee_id = models.CharField(max_length=20, null=False, blank=True)
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
    packet_payment_value = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    packet_receive_value = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_packet_payment= models.IntegerField(
        null=True, default=0, blank=True)
    total_packet_receive= models.IntegerField(
        null=True, default=0, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Srstage_Inventory_Sum(models.Model):
    employee_id = models.CharField(max_length=20, null=False, blank=True)
    product_total_stock = models.IntegerField(null=True, default=0, blank=True)
    total_order_quantity = models.IntegerField(null=True, default=0)
    product_total_sales = models.IntegerField(null=True, default=0, blank=True)
    total_stock_return = models.IntegerField(null=True, default=0, blank=True)
    total_sales_return = models.IntegerField(null=True, default=0, blank=True)
    product_total_damage = models.IntegerField(
        null=True, default=0, blank=True)
    product_available_stock = models.IntegerField(
        null=True, default=0, blank=True)
    total_packet_receive = models.IntegerField(
        null=True, default=0, blank=True)
    total_packet_payment = models.IntegerField(
        null=True, default=0, blank=True)
    total_purchase_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_sales_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_return_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    stock_return_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    sales_return_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_damage_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    cost_of_good_sold = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_discount_receive = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_discount_pay = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    packet_receive_value = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    packet_payment_value = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    packet_payment_value = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    packet_receive_value = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_packet_payment= models.IntegerField(
        null=True, default=0, blank=True)
    total_packet_receive= models.IntegerField(
        null=True, default=0, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Clients_Inventory_Status(models.Model):
    branch_code = models.IntegerField(blank=True)
    client_id = models.CharField(max_length=20, null=False, blank=True)
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
    packet_payment_value = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    packet_receive_value = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_packet_payment= models.IntegerField(
        null=True, default=0, blank=True)
    total_packet_receive= models.IntegerField(
        null=True, default=0, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)


class Clients_Inventory_Hist(models.Model):
    branch_code = models.IntegerField(blank=True)
    client_id = models.CharField(max_length=20, null=False, blank=True)
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
    packet_payment_value = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    packet_receive_value = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    total_packet_payment= models.IntegerField(
        null=True, default=0, blank=True)
    total_packet_receive= models.IntegerField(
        null=True, default=0, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

class Clients_Security_Info(models.Model):
    branch_code = models.IntegerField(blank=True)
    client_id = models.CharField(max_length=20, default='')
    phone_number = models.CharField(max_length=15, null=False)
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

class Client_Center_Trf_Hist(models.Model):
    client_id = models.CharField(max_length=100)
    old_center_code = models.CharField(max_length=100)
    new_center_code = models.CharField(max_length=100)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client_id



class SR_Target(models.Model):
    branch_code = models.IntegerField(blank=True)
    transaction_id = models.CharField(max_length=20, null=True, blank=True)
    employee_id = models.CharField(max_length=20, blank=True, null=True)
    target_from_date = models.DateField(null=True)
    target_to_date = models.DateField(null=True)
    target_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, null=True)
    comments = models.TextField(blank=True,null=True)
    target_type  = models.CharField(max_length=20, blank=True, null=True,choices=target_type) 
    app_user_id = models.CharField(max_length=20, null=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

class SR_Target_Details(models.Model):
    transaction_id = models.CharField(max_length=20, null=True, blank=True)
    branch_code =  models.IntegerField( null=True, blank=True)
    product_id = models.CharField(max_length=30, null=True)
    unit_id = models.CharField(max_length=30, null=True)
    total_quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=22,decimal_places=2, default=0.00, blank=True, null=True)
    total_price = models.DecimalField(max_digits=22,decimal_places=2, default=0.00, blank=True, null=True)
    is_deleted = models.BooleanField(blank=True,default=False,null=True)
    app_user_id = models.CharField(max_length=20, null=True)
    app_data_time = models.DateTimeField(auto_now_add=True)


class SR_Target_Details_Temp(models.Model):
    transaction_id = models.CharField(max_length=20,null=True, blank=True)
    branch_code = models.IntegerField( null=True, blank=True)
    product_id = models.CharField(max_length=30, null=True)
    unit_id = models.CharField(max_length=30, null=True)
    total_quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=22,decimal_places=2, default=0.00, blank=True, null=True)
    total_price = models.DecimalField(max_digits=22,decimal_places=2, default=0.00, blank=True, null=True)
    is_deleted = models.BooleanField(blank=True,default=False,null=True)
    app_user_id = models.CharField(max_length=20, null=True)
    app_data_time = models.DateTimeField(auto_now_add=True)