from appauth.models import User_Settings
from sales.models import *
from django.db import connection, transaction
from django.db.models import Count, Sum, Avg, Max, Min
import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from decimal import Decimal
import logging
import sys
from django.utils import timezone
from sales.validations import *
logger = logging.getLogger(__name__)
from django.db.models import F

from appauth.utils import get_inv_number, get_business_date
from sales.validations import *
from finance.models import Application_Settings as Finance_Application_Settings, Client_Type, Accounts_Balance, Transaction_Type
from finance.utils import fn_get_accountinfo_bytran, fn_get_cash_gl_code, fn_cash_tran_posting, fn_transfer_tran_posting, fn_cancel_tran_batch
from delar.utils import fn_get_sr_available_stock

def fn_generate_product_id(p_branch_code):
    branch_code = 100
    inventory_number = get_inv_number(
        30000, branch_code, '', 'Product ID Generate', 6)
    return inventory_number[0]


def fn_generate_product_unit_id(p_branch_code):
    branch_code = 100
    inventory_number = get_inv_number(
        30000, branch_code, '', 'Product Unit ID Generate', 6)
    return inventory_number[0]

###### quotion ###########
def fn_get_quation_id1(p_branch_code):
    branch_code = 100
    inventory_number = get_inv_number(
        30000, branch_code, '', 'Product quotion ID Generate', 6)
    return inventory_number[0]



def fn_generate_invoice_number(p_branch_code):
    branch_code = 100
    inventory_number = get_inv_number(
        30001, branch_code, 'SL', 'Sales Invoice Number Generate', 6)
    return inventory_number[0]


def fn_generate_order_number(p_branch_code):
    branch_code = 100
    inventory_number = get_inv_number(
        30002, branch_code, 'OR', 'Sales Order Number Generate', 6)
    return inventory_number[0]


def fn_generate_client_id(p_branch_code):
    sequence_number = 100
    client_inv = get_inv_number(30003, sequence_number, '', 'Client Number', 8)
    return client_inv[0]


'''
def fn_generate_client_id(p_branch_code, p_center_code):
    sequence_number = int(p_branch_code)+int(p_center_code)
    client_inv = get_inv_number(30003, sequence_number, '', 'Client Number', 5)
    client_id = '{:0<4}'.format(
        p_branch_code)+"-"+'{:0<4}'.format(
        p_center_code)+"-"+'{:0>5}'.format(client_inv[0])
    return client_id
'''


def fn_generate_nominee_id(p_branch_code):
    branch_code = 100
    client_inv = get_inv_number(30004, branch_code, '', 'Nominee  ID', 6)
    return client_inv[0]


def fn_generate_showroom_id(p_branch_code):
    branch_code = 100
    client_inv = get_inv_number(30005, branch_code, '', 'Showroom  ID', 6)
    return client_inv[0]


def fn_generate_supplier_id(p_branch_code):
    branch_code = 100
    client_inv = get_inv_number(30006, branch_code, '', 'Supplier ID', 8)
    return client_inv[0]


def fn_generate_product_group_id(p_branch_code):
    branch_code = 100
    client_inv = get_inv_number(30007, branch_code, '', 'Product Group ID', 4)
    return client_inv[0]


def fn_generate_stock_ledger_code(p_branch_code):
    branch_code = 100
    client_inv = get_inv_number(
        30008, branch_code, '43', 'Product stock Ledger Code', 6)
    return client_inv[0]


def fn_generate_sales_ledger_code(p_branch_code):
    branch_code = 100
    client_inv = get_inv_number(
        30009, branch_code, '33', 'Product sales Ledger Code', 6)
    return client_inv[0]


def fn_generate_stock_ret_ledger_code(p_branch_code):
    branch_code = 100
    client_inv = get_inv_number(
        30010, branch_code, '14', 'Product Stock Return Ledger Code', 6)
    return client_inv[0]


def fn_generate_sales_ret_ledger_code(p_branch_code):
    branch_code = 100
    client_inv = get_inv_number(
        30011, branch_code, '24', 'Product Sales Return Ledger Code', 6)
    return client_inv[0]


def fn_generate_damage_ledger_code(p_branch_code):
    branch_code = 100
    client_inv = get_inv_number(
        30012, branch_code, '44', 'Product Damage Ledger Code', 6)
    return client_inv[0]


def fn_generate_product_brand_id(p_branch_code):
    branch_code = 100
    client_inv = get_inv_number(30013, branch_code, '', 'Product Brand ID', 4)
    return client_inv[0]


def fn_generate_memo_number(p_branch_code):
    branch_code = 100
    client_inv = get_inv_number(30014, branch_code, '', 'Memo Number', 1)
    return 'S'+datetime.date.today().strftime("%m%d%Y")+str(client_inv[0])


def fn_generate_stock_id(p_branch_code):
    branch_code = 100
    client_inv = get_inv_number(
        30015, branch_code, 'ST', 'Stock Voucher Number', 8)
    return client_inv[0]

    #################
def fn_generate_purchase_order_no(p_branch_code):
    branch_code = 100
    client_inv = get_inv_number(
        30015, branch_code, 'ST', 'Purchase order Number', 9)
    return client_inv[0]


def fn_get_total_stock(p_branch_code, p_product_id):
    product_available_stock = 0
    try:
        product_invstatus = Products_Inventory_Status.objects.get(
            product_id=p_product_id, branch_code=p_branch_code)
        product_available_stock = product_invstatus.product_available_stock
        return product_available_stock
    except Products_Inventory_Status.DoesNotExist:
        product_available_stock = 0
        return product_available_stock


def fn_get_product_id(p_product_bar_code):
    product_id = ''
    try:
        product_info = products.objects.get(
            product_bar_code=p_product_bar_code)
        product_id = product_info.product_id
        return product_id
    except products.DoesNotExist:
        return product_id


def fn_get_product_barcode(p_product_id):
    product_bar_code = ''
    try:
        product_info = products.objects.get(product_id=p_product_id)
        product_bar_code = product_info.product_bar_code
        return product_bar_code
    except products.DoesNotExist:
        return product_bar_code


def fn_get_product_details(p_product_id):
    product_bar_code = ''
    product_name = ''
    product_model = ''
    try:
        product_info = products.objects.get(product_id=p_product_id)
        product_bar_code = product_info.product_bar_code
        product_name = product_info.product_name
        product_model = product_info.product_model
        return product_bar_code, product_name, product_model
    except products.DoesNotExist:
        return product_bar_code, product_name, product_model


def fn_get_client_info(p_branch_code, p_client_id):
    client_type = None
    client_name = None
    try:
        client_info = Clients.objects.get(
            branch_code=p_branch_code, client_id=p_client_id)
        client_type = client_info.client_type
        client_name = client_info.client_name
        return client_type, client_name
    except Clients.DoesNotExist:
        client_type = None
        client_name = None
        return client_type, client_name


def fn_get_product_price(p_branch_code, p_app_user, p_client_id, p_product_id, p_tran_type_code):
    product_price = Decimal(0)
    discount_amount = Decimal(0)
    discount_percent = Decimal(0)
    stock_available = 0
    product_name = None
    discount_type = None
    product_model = None

    try:
        product_info = products.objects.get(
            product_id=p_product_id)
    except products.DoesNotExist:
        product_info = products.objects.get(
            product_bar_code=p_product_id)

    product_id = product_info.product_id

    if not fn_valid_product_code(p_branch_code, product_id):
        return round(product_price, 2), round(discount_amount, 2), round(discount_percent, 2), product_name, discount_type, stock_available, product_model

    client_type, client_name = fn_get_client_info(
        p_branch_code=p_branch_code, p_client_id=p_client_id)
    business_date = get_business_date(p_branch_code, p_app_user)

    stock_available = fn_get_total_stock(p_branch_code, product_id)
    sr_stock = fn_get_sr_available_stock(p_branch_code, product_id)
    stock_available = stock_available-sr_stock
    product_model = product_info.product_model

    try:
        price_list = Product_Price_List.objects.get(
            product_id=product_id, client_type_code=client_type)
        business_date = get_business_date(p_branch_code)
        product_price = price_list.product_sales_price
        product_name = price_list.product_name

        if price_list.sales_discount_fromdt and price_list.sales_discount_uptodt:

            if price_list.sales_discount_fromdt <= business_date <= price_list.sales_discount_uptodt:
                if price_list.sales_discount_type == 'F':
                    discount_amount = price_list.sales_discount_amount
                    discount_percent = Decimal(0)
                    discount_type = price_list.sales_discount_type
                elif price_list.sales_discount_type == 'P':
                    discount_amount = product_price * \
                        (price_list.sales_discount_percent/100)
                    discount_percent = price_list.sales_discount_percent
                    discount_type = price_list.sales_discount_type
            else:
                discount_amount = Decimal(0)
                discount_percent = Decimal(0)

        return round(product_price, 2), round(discount_amount, 2), round(discount_percent, 2), product_name, discount_type, stock_available, product_model

    except Exception as e:
        try:
            print('A')
            try:
                product_info = products.objects.get(
                    product_id=p_product_id)
            except products.DoesNotExist:
                product_info = products.objects.get(
                    product_bar_code=p_product_id)

            try:
                price_param = Products_Price_Type.objects.get(
                    tran_type_code=p_tran_type_code)
                if price_param.product_price == 'WHOL':
                    product_price = product_info.whole_sales_price
                else:
                    product_price = product_info.product_sales_price
            except Exception as e:
                product_price = product_info.product_sales_price

            #product_price = product_info.product_sales_price
            product_name = product_info.product_name
            sales_discount_maxamt = product_info.sales_discount_maxamt
            sales_discount_fromdt = product_info.sales_discount_fromdt
            sales_discount_uptodt = product_info.sales_discount_uptodt
            discount_type = product_info.sales_discount_type
            business_date = get_business_date(p_branch_code, p_app_user)

            if sales_discount_fromdt and sales_discount_uptodt:

                if sales_discount_fromdt <= business_date <= sales_discount_uptodt:
                    if discount_type == 'F':
                        discount_amount = product_info.sales_discount_maxamt
                        discount_percent = Decimal(0)
                    else:
                        discount_amount = Decimal(
                            (product_price*discount_percent)/100)
                        discount_percent = product_info.sales_discount_percent
                else:
                    discount_amount = Decimal(0)
                    discount_percent = Decimal(0)

            return round(product_price, 2), round(discount_amount, 2), round(discount_percent, 2), product_name, discount_type, stock_available, product_model

        except products.DoesNotExist:
            return round(product_price, 2), round(discount_amount, 2), round(discount_percent, 2), product_name, discount_type, stock_available, product_model


def fn_get_product_purchase_rate(p_branch_code, p_product_id):
    current_rate = Decimal(0)

    try:
        product_info = products.objects.get(
            product_id=p_product_id)
        current_rate = product_info.product_current_rate
    except products.DoesNotExist:
        product_info = products.objects.get(
            product_bar_code=p_product_id)
        current_rate = product_info.product_current_rate
    return current_rate


def fn_get_product_damage_gl(p_product_id):
    product_damage_gl = None
    product_stock_gl = None
    try:
        product_info = products.objects.get(
            product_id=p_product_id)
        product_damage_gl = product_info.product_damage_gl
        product_stock_gl = product_info.product_stock_gl
    except products.DoesNotExist:
        product_info = products.objects.get(
            product_bar_code=p_product_id)
        product_damage_gl = product_info.product_damage_gl
        product_stock_gl = product_info.product_stock_gl
    return product_damage_gl, product_stock_gl


def get_product_offer(p_branch_code, p_app_user, p_client_id, p_product_id, p_total_quantity, p_total_product_price):
    discount_amount = Decimal(0)
    discount_percent = Decimal(0)
    total_free_quantity = 0
    product_list = []
    client_type, client_name = fn_get_client_info(
        p_branch_code=p_branch_code, p_client_id=p_client_id)
    business_date = get_business_date(p_branch_code, p_app_user)

    offer_list = Product_Offer_List.objects.filter(branch_code=p_branch_code, product_id=p_product_id, client_type_code=client_type).values('offer_from_quantity',
                                                                                                                                            'offer_upto_quantity', 'offer_free_quantity', 'offer_from_amount', 'offer_upto_amount', 'offer_reduce_amount', 'sales_offer_fromdt',
                                                                                                                                            'sales_offer_uptodt', 'sales_offer_type')
    for data in offer_list:
        if data['sales_offer_type'] == 'Q':
            if data['offer_from_quantity'] <= p_total_quantity <= data['offer_upto_quantity'] and data['sales_offer_fromdt'] <= business_date <= data['sales_offer_uptodt']:
                total_free_quantity = data['offer_free_quantity']
            else:
                total_free_quantity = 0
        elif data['sales_offer_type'] == 'P':
            if data['offer_from_amount'] <= p_total_product_price <= data['offer_upto_amount'] and data['sales_offer_fromdt'] <= business_date <= data['sales_offer_uptodt']:
                discount_amount = data['offer_reduce_amount']
            else:
                discount_amount = Decimal(0)

    return total_free_quantity, round(discount_amount, 2), round(discount_percent, 2)


def add_free_product_to_list(p_branch_code, p_app_user, p_client_id, p_product_id, p_total_quantity):
    product_list = []
    client_phone = fn_get_client_phone(p_client_id)
    client_type, client_name = fn_get_client_info(
        p_branch_code=p_branch_code, p_client_id=p_client_id)
    business_date = get_business_date(p_branch_code, p_app_user)

    package_list = Product_Offer_Package.objects.filter(branch_code=p_branch_code, product_id=p_product_id, client_type_code=client_type).values(
        'offer_from_quantity', 'offer_upto_quantity', 'free_product_code', 'free_product_name', 'offer_free_quantity', 'sales_offer_fromdt',
        'sales_offer_uptodt')

    for data in package_list:
        if data['offer_from_quantity'] <= p_total_quantity <= data['offer_upto_quantity'] and data['sales_offer_fromdt'] <= business_date <= data['sales_offer_uptodt'] and data['offer_free_quantity'] > 0:
            row = Sales_Details_Temp(product_id=data['free_product_code'], product_name=data['free_product_name'], product_price=0, quantity=data['offer_free_quantity'],
                                     total_price=0, discount_rate=0, discount_amount=0, status='N', branch_code=p_branch_code, app_user_id=p_app_user, sales_customer_phone=client_phone)
            product_list.append(row)

    Sales_Details_Temp.objects.bulk_create(product_list)


def fn_get_client_details(p_client_id):
    client_id = None
    client_name = None
    client_present_address = None
    client_type = None
    try:
        client_info = Clients.objects.get(client_id=p_client_id)
        client_id = client_info.client_id
        client_name = client_info.client_name
        client_present_address = client_info.client_present_address
        client_type = client_info.client_type
        return client_id, client_name, client_present_address, client_type
    except Clients.DoesNotExist:
        client_type = None
        client_name = None
        return client_id, client_name, client_present_address, client_type


def fn_get_client_phone(p_client_id):
    client_phone = None
    try:
        client_info = Clients.objects.get(client_id=p_client_id)
        client_phone = client_info.client_phone
        return client_phone
    except Clients.DoesNotExist:
        try:
            client_info = Clients.objects.get(client_phone=p_client_id)
            client_phone = client_info.client_phone
            return client_phone
        except Clients.DoesNotExist:
            client_phone = None
            return client_phone
        except MultipleObjectsReturned:
            client_phone = None
            return client_phone
    except MultipleObjectsReturned:
        client_phone = None
        return client_phone


def get_product_cart_summary(app_user_id):
    """
    This function are used for the purpose of return item summary information for making new sales invoice.
    """
    item_summary = Sales_Details_Temp.objects.filter(app_user_id=app_user_id).aggregate(
        Sum('quantity'), Sum('discount_amount'), Sum('total_price'))
    total_quantity = item_summary['quantity__sum']
    total_discount = item_summary['discount_amount__sum']
    total_price = item_summary['total_price__sum']
    if total_discount is None:
        total_discount = 0
    if total_price is None:
        total_price = 0
    if total_quantity is None:
        total_quantity = 0
    return total_quantity, total_discount, total_price


def fn_get_stock_temp_summary(p_branch_code, app_user_id):
    quantity_count = StockDetailsTemp.objects.filter(
        branch_code=p_branch_code, app_user_id=app_user_id).aggregate(Sum('quantity'), Sum('total_price'))
    total_quantity = quantity_count['quantity__sum']
    total_price = quantity_count['total_price__sum']
    return total_quantity, total_price

    #########
def fn_get_purchase_order_temp_summary(p_branch_code, app_user_id):
    quantity_count = Purchase_Order_Dtl_Temp.objects.filter(
        branch_code=p_branch_code, app_user_id=app_user_id).aggregate(Sum('pur_qnty'), Sum('total_price'))
    total_quantity = quantity_count['pur_qnty__sum']
    total_price = quantity_count['total_price__sum']
    return total_quantity, total_price


def gn_get_stock_details(p_branch_code, p_product_id, p_stock_id, p_stock_date, p_stock_voucher, p_supplier_phone):
    stock_date = None
    voucher_number = None
    quantity = None
    purces_price = None

    try:
        stock_mast = StockMaster.objects.get((Q(voucher_number=p_stock_voucher) | Q(
            stock_id=p_stock_id)), branch_code=p_branch_code, supplier_phone=p_supplier_phone)
        stock_date = stock_mast.stock_date
        voucher_number = stock_mast.voucher_number
        try:
            stock_detail = StockDetails.objects.get(
                stock_id=p_stock_id, product_id=p_product_id)
            quantity = stock_detail.quantity
            purces_price = stock_detail.purces_price
        except StockDetails.DoesNotExist:
            return stock_date, voucher_number, quantity, purces_price
    except StockMaster.DoesNotExist:
        return stock_date, voucher_number, quantity, purces_price


def fn_get_invoice_details(p_product_id, p_invoice_number):
    sales_date = None
    total_quantity = None
    sales_price = None
    try:
        sales_mst = Sales_Master.objects.get(invoice_number=p_invoice_number)
        sales_date = sales_mst.invoice_date
    except Sales_Master.DoesNotExist:
        return sales_date, total_quantity, sales_price
    try:
        sales = Sales_Details.objects.get(
            invoice_number=p_invoice_number, product_id=p_product_id)
        total_quantity = sales.quantity
        sales_price = sales.total_price-sales.discount_amount
        return sales_date, total_quantity, sales_price
    except Sales_Details.DoesNotExist:
        return sales_date, total_quantity, sales_price


def fn_get_invoice_summary(p_invoice_number):
    sales_date = None
    bill_amount = None
    due_amount = None
    total_quantity = None
    customer_id = None
    try:
        sales_mst = Sales_Master.objects.get(
            invoice_number=p_invoice_number)
        sales_date = sales_mst.invoice_date
        bill_amount = sales_mst.bill_amount
        due_amount = sales_mst.due_amount
        total_quantity = sales_mst.total_quantity
        customer_id = sales_mst.customer_id
        return sales_date, bill_amount, due_amount, total_quantity, customer_id
    except Sales_Master.DoesNotExist:
        try:
            sales_mst = Sales_Master.objects.get(
                invoice_number=p_invoice_number)
            sales_date = sales_mst.invoice_date
            bill_amount = sales_mst.bill_amount
            due_amount = sales_mst.due_amount
            total_quantity = sales_mst.total_quantity
            customer_id = sales_mst.customer_id
            return sales_date, bill_amount, due_amount, total_quantity, customer_id
        except Exception as e:
            return sales_date, bill_amount, due_amount, total_quantity, customer_id


def fn_get_invoice_branch_center(p_invoice_number):
    branch_code = None
    center_code = None
    try:
        sales_mst = Sales_Master.objects.get(invoice_number=p_invoice_number)
        branch_code = sales_mst.branch_code
        center_code = sales_mst.center_code
        return branch_code, center_code
    except Sales_Master.DoesNotExist:
        branch_code = None
        center_code = None
        return branch_code, center_code


def fn_create_product_ledger(p_gl_for, p_product_name, p_product_model, p_branch_code, p_app_user_id):
    gl_code = ''
    com_info = Application_Settings.objects.get()
    parent_code = '0'
    expense_gl = False
    income_gl = False
    assets_gl = False
    liabilities_gl = False
    product_wise_ledger = com_info.product_wise_ledger
    if p_gl_for == 'stock':
        parent_code = com_info.product_stock_parent_gl
        if product_wise_ledger:
            gl_code = fn_generate_stock_ledger_code(p_branch_code)
        else:
            gl_code = com_info.product_stock_gl
        expense_gl = True
    elif p_gl_for == 'sales':
        parent_code = com_info.product_sales_parent_gl
        if product_wise_ledger:
            gl_code = fn_generate_sales_ledger_code(p_branch_code)
        else:
            gl_code = com_info.product_sales_gl
        income_gl = True
    elif p_gl_for == 'stock_ret':
        parent_code = com_info.product_stock_ret_parent_gl
        if product_wise_ledger:
            gl_code = fn_generate_stock_ret_ledger_code(p_branch_code)
        else:
            gl_code = com_info.stock_ret_gl
        assets_gl = True
    elif p_gl_for == 'sales_ret':
        parent_code = com_info.product_sales_ret_parent_gl
        if product_wise_ledger:
            gl_code = fn_generate_sales_ret_ledger_code(p_branch_code)
        else:
            gl_code = com_info.sales_ret_gl
        liabilities_gl = True
    elif p_gl_for == 'damage':
        parent_code = com_info.product_damage_parent_gl
        if product_wise_ledger:
            gl_code = fn_generate_damage_ledger_code(p_branch_code)
        else:
            gl_code = com_info.damage_gl
        expense_gl = True
    elif p_gl_for == 'profit':
        parent_code = com_info.product_damage_parent_gl
        if product_wise_ledger:
            gl_code = fn_generate_damage_ledger_code(p_branch_code)
        else:
            gl_code = com_info.profit_ledger
        expense_gl = True
    elif p_gl_for == 'loss':
        parent_code = com_info.product_damage_parent_gl
        if product_wise_ledger:
            gl_code = fn_generate_damage_ledger_code(p_branch_code)
        else:
            gl_code = com_info.loss_ledger
        expense_gl = True
    return gl_code


def get_emi_maturity_date(p_emi_freq, inst_number, from_date):
    try:

        day = 0
        month = 0
        year = 0
        if inst_number:
            inst_number = int(inst_number)
        else:
            inst_number = 1
        if p_emi_freq == 'W':
            day = 7 * inst_number
        elif p_emi_freq == 'M':
            month = 1 * inst_number
        elif p_emi_freq == 'Q':
            month = 3 * inst_number
        elif p_emi_freq == 'H':
            month = 6 * inst_number
        elif p_emi_freq == 'Y':
            year = 1 * inst_number
        with connection.cursor() as cursor:
            cursor.execute("SELECT CAST(date_trunc ('day', CAST('"+from_date+"'  AS DATE)) + INTERVAL '"+str(day) +
                           " day' + INTERVAL '"+str(month)+" month' + INTERVAL '"+str(year)+" year' AS DATE) maturity_date")
            result = cursor.fetchone()
        return result[0]
    except Exception as e:
        print(str(e))
        return None


def fn_get_emi_details(p_emi_reference_no, p_account_number):
    total_emi_amount = 0.00
    emi_inst_amount = 0.00
    number_of_installment = 0
    paid_installment_number = 0
    total_emi_payment = 0.00
    total_emi_due = 0.00
    try:
        emi_info = Emi_Setup.objects.get(
            emi_reference_no=p_emi_reference_no, account_number=p_account_number, emi_cancel_by__isnull=True)
        total_emi_amount = emi_info.emi_reference_amount + emi_info.emi_profit_amount
        emi_inst_amount = emi_info.emi_inst_amount
        number_of_installment = emi_info.number_of_installment
        total_emi_payment = emi_info.installment_tot_repay_amt+emi_info.emi_down_amount
        total_emi_due = total_emi_amount-total_emi_payment
        paid_installment_number = emi_info.installment_tot_repay_amt/emi_inst_amount
        return total_emi_amount, emi_inst_amount, number_of_installment, paid_installment_number, total_emi_payment, total_emi_due
    except Exception as e:
        print(str(e))
        return total_emi_amount, emi_inst_amount, number_of_installment, paid_installment_number, total_emi_payment, total_emi_due


def fn_get_emi_rate(p_emi_reference_no, p_account_number):
    emi_rate = 0.00
    try:
        emi_info = Emi_Setup.objects.get(
            emi_reference_no=p_emi_reference_no, account_number=p_account_number, emi_cancel_by__isnull=True)
        emi_rate = emi_info.emi_rate
        return emi_rate
    except Exception as e:
        print(str(e))
        return emi_rate


def fn_update_emi_receive(p_account_number, p_invoice_number, p_emi_amount, p_emi_receive_date):
    status = False
    error_message = None
    try:
        emi_info = Emi_Setup.objects.get(
            emi_reference_no=p_invoice_number, account_number=p_account_number, emi_cancel_by__isnull=True)

        if emi_info.last_emi_hist_update is None:
            w_last_balance_update = p_emi_receive_date
        else:
            if p_emi_receive_date < emi_info.last_emi_hist_update:
                w_last_balance_update = p_emi_receive_date
            else:
                w_last_balance_update = emi_info.last_emi_hist_update

        if emi_info.last_emi_payment_date is None:
            w_last_transaction_date = p_emi_receive_date
        else:
            if p_emi_receive_date > emi_info.last_emi_hist_update:
                w_last_transaction_date = p_emi_receive_date
            else:
                w_last_transaction_date = emi_info.last_emi_payment_date

        if not w_last_transaction_date or w_last_transaction_date is None:
            w_last_transaction_date = p_emi_receive_date

        emi_info.total_emi_due -= p_emi_amount
        emi_info.installment_tot_repay_amt += p_emi_amount
        emi_info.last_emi_payment_date = w_last_transaction_date
        emi_info.last_emi_hist_update = w_last_balance_update
        emi_info.is_balance_updated = False
        emi_info.save()
        status = True
        return status, error_message
    except Exception as e:
        error_message = str(e)
        status = False
        return status, error_message


def fn_validate_emi_amount(p_account_number, p_invoice_number, p_emi_amount, p_emi_receive_date):
    status = False
    error_message = None
    try:
        emi_info = Emi_Setup.objects.get(
            emi_reference_no=p_invoice_number, account_number=p_account_number, emi_cancel_by__isnull=True)
        if p_emi_receive_date < emi_info.emi_reference_date:
            error_message = "Transaction date " + \
                (str(p_emi_amount))+" can not be less then installment from date " + \
                str(emi_info.emi_reference_date)+"!"
            return status, error_message

        if p_emi_amount > emi_info.total_emi_due:
            error_message = "Transaction amount " + \
                (str(p_emi_amount))+" can not be more then total outstanding due amount " + \
                str(emi_info.total_emi_due)+"!"
            return status, error_message
        status = True
        return status, error_message
    except Exception as e:
        status = False
        error_message = str(e)
        return status, error_message


def fn_get_client_admission_fee():
    client_admission_fee = 0.00
    try:
        param = Application_Settings.objects.get()

        if param.client_admission_fee_auto:
            client_admission_fee = param.client_admission_fee
        return client_admission_fee
    except Exception as e:
        return client_admission_fee


def fn_get_client_emi_fee():
    emi_fee = 0.00
    emi_ins_rate = 0.00
    try:
        param = EMI_Settings.objects.get()

        if param.emi_fee_auto:
            emi_fee = param.emi_fee
            emi_ins_rate = param.emi_insurence_pct
        return emi_fee, emi_ins_rate
    except Exception as e:
        return emi_fee, emi_ins_rate


def fn_get_emi_gl_code():
    emi_receive = None
    emi_receivable = None
    try:
        row = EMI_Settings.objects.get()
        emi_receivable = row.emi_profit_receivable
        emi_receive = row.emi_profit_receive
    except EMI_Settings.DoesNotExist:
        emi_receive = None
        emi_receivable = None
    return emi_receivable, emi_receive


def fn_fees_history(p_client_id, p_branch_code, p_center_code, p_app_user_id, p_fee_type, p_fee_amount, p_tran_date, p_batch_number, p_transaction_narration, p_fee_memo_number=None):
    try:
        cbd = p_tran_date
        fees = Fees_History(branch_code=p_branch_code, center_code=p_center_code, fee_type=p_fee_type, fee_amount=p_fee_amount, cancel_amount=0.00,
                            fee_collection_date=cbd, transaction_batch_number=p_batch_number, app_user_id=p_app_user_id,
                            transaction_narration=p_transaction_narration, fee_memo_number=p_fee_memo_number,
                            client_id=p_client_id)
        fees.save()
        return True
    except Exception as e:
        print(str(e))
        return False


def fn_fees_history_cancel(p_branch_code, p_batch_number, p_fee_collection_date, p_app_user_id):
    try:

        fees = Fees_History.objects.filter(branch_code=p_branch_code, fee_collection_date=p_fee_collection_date,
                                           transaction_batch_number=p_batch_number).update(cancel_by=p_app_user_id, cancel_date=timezone.now(), cancel_amount=F('fee_amount'))
        fees.save()
        return True, None
    except Exception as e:
        print(str(e))
        return True, str(e)


def fn_update_invoice(p_invoice_number, p_down_amount):
    try:
        sales_mst = Sales_Master.objects.get(invoice_number=p_invoice_number)
        sales_mst.pay_amount += p_down_amount
        sales_mst.due_amount -= p_down_amount
        sales_mst.save()
        return True
    except Sales_Master.DoesNotExist:
        return False


def fn_cancel_invoice_update(p_invoice_number, p_down_amount):
    try:
        sales_mst = Sales_Master.objects.get(invoice_number=p_invoice_number)
        sales_mst.pay_amount -= p_down_amount
        sales_mst.due_amount += p_down_amount
        sales_mst.save()
        return True
    except Sales_Master.DoesNotExist:
        return False


def get_general_account(p_app_user_id):
    general_account = None
    try:
        app_user_info = Application_Settings.objects.get()
        general_account = app_user_info.quick_sales_account_number
        return general_account
    except User_Settings.DoesNotExist:
        app_user_info = None
        general_account = None
        return general_account


def fn_cancel_emi_receive_transaction(p_id, p_app_user_id):
    error_message = None
    status = False
    try:
        emi_rcv_info = Emi_Receive.objects.get(id=p_id)
        is_transfer = emi_rcv_info.is_transfer
        receive_date = emi_rcv_info.receive_date
        tran_batch_number = emi_rcv_info.tran_batch_number
        branch_code = emi_rcv_info.branch_code
        receive_document_number = emi_rcv_info.receive_document_number
        emi_reference_no = emi_rcv_info.emi_reference_no
        account_number = emi_rcv_info.account_number
        receive_amount = emi_rcv_info.receive_amount

        emi_rcv_info.receive_amount = 0.00
        emi_rcv_info.emi_cancel_by = p_app_user_id
        emi_rcv_info.emi_cancel_on = timezone.now()
        status, error_message = fn_cancel_tran_batch(p_branch_code=branch_code, p_app_user_id=p_app_user_id,
                                                     p_transaction_date=receive_date, p_batch_number=tran_batch_number, p_cancel_comments='Cancel by '+p_app_user_id)

        if status:
            status_emi, error_message_emi = fn_update_emi_receive(p_account_number=account_number, p_invoice_number=emi_reference_no,
                                                                  p_emi_amount=-receive_amount, p_emi_receive_date=receive_date)
            if status_emi:
                if is_transfer:
                    emi_rcv_info.save()
                else:
                    emi_rcv_info.save()
            else:
                error_message = error_message_emi
                status = False
                return status, error_message
        else:
            status = False
            return status, error_message
        status = True
        return status, error_message
    except Emi_Receive.DoesNotExist:
        error_message = "Invalid EMI Receive Info!"
        status = False
        return status, error_message
    except Exception as e:
        error_message = str(e)
        status = False
        return status, error_message


def fn_update_emibal_hist(p_account_number, p_emi_reference_no, p_ason_date):
    try:
        cursor = connection.cursor()
        cursor.callproc("fn_sales_emibal_hist", [
                        p_account_number, p_emi_reference_no, p_ason_date])
        row = cursor.fetchone()

        if row[0] != 'S':
            error_message = row[1]
            logger.error("Database Error in fn_sales_emibal_hist line {} \nType: {} \nError:{}".format(
                sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
            return False, error_message

        return True, 'Success'
    except Exception as e:
        return False, str(e)


def fn_get_default_client_type(p_transaction_screen):
    single_client = 'N'
    try:
        client_type = Client_Type.objects.filter(
            transaction_screen=p_transaction_screen, is_active=True, is_deleted=False).aggregate(Count('client_type_code'))
        total_client = client_type['client_type_code__count']
        if total_client == 1:
            single_client = 'Y'
            client_type = Client_Type.objects.get(
                transaction_screen=p_transaction_screen, is_active=True, is_deleted=False)
            return single_client, client_type.client_type_code
        else:
            return single_client, None
    except Exception as e:
        print(str(e))
        return single_client, None


def fn_get_charge_amount(p_transaction_amount):
    try:
        emi = EMI_Settings.objects.get()
        charge_code = emi.emi_fee_chargecd
        with connection.cursor() as cursor:
            cursor.execute("select COALESCE(sum(charge_amount),0,00) charge_amount from fn_finance_get_charges(%s, '', %s,%s,%s);", [
                p_transaction_amount, charge_code, False, False])
            row = cursor.fetchone()
        return row
    except Exception as e:
        return 0


def fn_client_closing(p_branch_code, p_client_id, p_closing_date):
    status = False
    message = None
    try:
        client_info = Clients.objects.get(
            branch_code=p_branch_code, client_id=p_client_id)
        client_info.closing_date = p_closing_date
        client_info.save()

        Accounts_Balance.objects.filter(client_id=p_client_id).update(
            account_closing_date=p_closing_date)
        status = True
        message = None
    except Clients.DoesNotExist:
        status = False
        message = "Invalid Client ID "+str(p_client_id)
    except Exception as e:
        status = False
        message = str(e)

    return status, message


def fn_client_remove(p_branch_code, p_client_id, p_closing_date):
    status = False
    message = None
    try:
        Clients.objects.filter(branch_code=p_branch_code,
                               client_id=p_client_id).delete()
        Accounts_Balance.objects.filter(client_id=p_client_id).update(
            account_closing_date=p_closing_date)
        status = True
        message = None
    except Clients.DoesNotExist:
        status = False
        message = "Invalid Client ID "+str(p_client_id)
    except Exception as e:
        status = False
        message = str(e)

    return status, message

def fn_get_sales_transaction_type(p_transaction_screen):
    single_tran = 'N'
    try:
        tran_type = Transaction_Type.objects.filter(
            transaction_screen=p_transaction_screen, is_active=True, is_deleted=False).aggregate(Count('tran_type_code'))
        total_tran = tran_type['tran_type_code__count']
        if total_tran == 1:
            single_tran = 'Y'
            tran_type = Transaction_Type.objects.get(transaction_screen=p_transaction_screen, is_active=True, is_deleted=False)
            return single_tran, tran_type.tran_type_id
        else:
            return single_tran, None
    except Exception as e:
        print(str(e))
        return single_tran, None
