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
import base64
from django.core.files.base import ContentFile
import random
from appauth.utils import get_inv_number, get_business_date
from sales.validations import *
from finance.models import Application_Settings as Finance_Application_Settings

def base64_to_image(base64_string,product_name):
    format, imgstr = base64_string.split(';base64,')
    return ContentFile(base64.b64decode(imgstr), name=product_name+"-"+ str(random.randint(000, 999)) + ".webp")

def base64_to_image_slider(base64_string,name):
    format, imgstr = base64_string.split(';base64,')
    return ContentFile(base64.b64decode(imgstr), name=name+"-"+ str(random.randint(000, 999)) + ".png")

def fn_generate_invoice_number(p_branch_code):
    branch_code = 100
    inventory_number = get_inv_number(
        30001, branch_code, 'SL', 'Sales Invoice Number Generate', 6)
    return inventory_number[0]
    
def fn_generate_category_id(p_branch_code):
    branch_code = p_branch_code
    inventory_number = get_inv_number(
        100001, branch_code, 'CAT', 'Ecom Product ID Generate', 6)
    return inventory_number[0]

def fn_generate_subcategory_id(p_branch_code):
    branch_code = p_branch_code
    inventory_number = get_inv_number(
        200001, branch_code, 'SCT', 'Ecom Product ID Generate', 6)
    return inventory_number[0]


