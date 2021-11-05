from .models import *
from django.db import connection, transaction
from django.db.models import Count, Sum, Avg
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


def fn_is_ledger_exist(p_gl_code):
    if General_Ledger.objects.filter(gl_code=p_gl_code).exists():
        return True
    else:
        return False


def fn_is_reporting_ledger_exist(p_reporting_gl_code):
    if General_Ledger.objects.filter(reporting_gl_code=p_reporting_gl_code).exists():
        return True
    else:
        return False


def fn_val_account_number(p_account_number):
    if Accounts_Balance.objects.filter(account_number=p_account_number).exists():
        return True
    else:
        return False


def fn_val_client_account_type_exists(p_client_id, p_account_type):
    if Accounts_Balance.objects.filter(client_id=p_client_id, account_type=p_account_type).exists():
        return True
    else:
        return False


def fn_val_ledger_code(p_gl_code):
    if General_Ledger.objects.filter(gl_code=p_gl_code).exists():
        return True
    else:
        return False



def fn_val_check_charges_exist(p_charges_code):
    if Charges.objects.filter(charges_code=p_charges_code).exists():
        return True
    else:
        return False