from appauth.models import *
from django.db import connection, transaction
from django.db.models import Count, Sum, Avg, Max, Min
import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from decimal import Decimal
import logging
import sys
from django.utils import timezone
from appauth.validations import *
logger = logging.getLogger(__name__)

from appauth.utils import get_inv_number, get_business_date
from finance.validations import *


def fn_get_transaction_type_id():
    branch_code = 100
    inventory_number = get_inv_number(
        20000, branch_code, '', 'Transaction Type ID Generate', 6)
    return inventory_number[0]


def fn_generate_account_number(p_branch_code):
    branch_code = 100
    inv_number = get_inv_number(
        20001, branch_code, '', 'Account Number Sequence', 8)
    account_number = '{:0<5}'.format(
        p_branch_code)+'{:0>8}'.format(inv_number[0])
    return account_number


def fn_generate_charges_id(p_branch_code):
    branch_code = 100
    inventory_number = get_inv_number(
        20005, branch_code, '', 'Charges ID', 6)
    return inventory_number[0]


def fn_get_account_type(p_account_type_code):
    credit_limit = 0.00
    account_ledger = None
    try:
        actype = Account_Type.objects.get(
            account_type_code=p_account_type_code)
        credit_limit = actype.maximum_credit_limit
        account_ledger = actype.account_ledger_code.gl_code

        return credit_limit, account_ledger
    except Account_Type.DoesNotExist:
        credit_limit = 0.00
        account_ledger = None
        return credit_limit, account_ledger


def get_client_account_type(p_client_type):
    account_required = None
    account_type = []
    try:
        client_type_info = Client_Type.objects.get(
            client_type_code=p_client_type)
        account_required = client_type_info.is_account_required

        account_types = Client_Account_Mapping.objects.filter(
            client_type_code=p_client_type).values("account_type_code")

        for actype in account_types:
            account_type.append(actype['account_type_code'])

        return account_required, account_type
    except Client_Type.DoesNotExist:
        account_required = None
        account_type = None
        return account_required, account_type


def fn_create_account(p_branch_code, p_center_code, p_app_user_id, p_client_id, p_client_type, p_client_name, p_client_address, p_phone_number, p_cbd=None, p_limit_amount=0.00):
    try:
        w_branch_code = p_branch_code
        account_required, account_type = get_client_account_type(
            p_client_type=p_client_type)

        if p_cbd is None or not p_cbd:
            cbd = get_business_date(p_branch_code, p_app_user_id)
        else:
            cbd = p_cbd

        logger.info("p_client_type {} account_type {} account_required ".format(
            p_client_type, account_type, account_required))

        if account_required:
            for ac_type in account_type:

                if ac_type:
                    if not fn_val_client_account_type_exists(p_client_id, ac_type):

                        account_number = fn_generate_account_number(
                            p_branch_code)
                        w_limit_amount, w_ledger_code = fn_get_account_type(
                            ac_type)

                        if p_limit_amount:
                            w_limit_amount = p_limit_amount

                        logger.info("Account number {} for client {} ".format(
                            account_number, p_client_id))

                        insert_accounts = Accounts_Balance(branch_code=w_branch_code, center_code=p_center_code, client_id=p_client_id, account_number=account_number,
                                                           account_ledger_code=w_ledger_code, is_account_active=True, account_type=ac_type, account_title=p_client_name,
                                                           account_address=p_client_address, phone_number=p_phone_number, account_opening_date=cbd, app_user_id=p_app_user_id, credit_limit=w_limit_amount)
                        insert_accounts.save()

            return True, None
        else:
            return True, None
    except Exception as e:
        logger.error("Error in fn_create_account line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(e).__name__, str(e)))
        return False, str(e)


def fn_get_account_info_byactype(p_client_id, p_account_type):
    try:
        acc = Accounts_Balance.objects.get(
            account_type=p_account_type, client_id=p_client_id)
        account_number = acc.account_number
        account_title = acc.account_title
        account_balance = acc.account_balance
        credit_limit = acc.credit_limit
    except Accounts_Balance.DoesNotExist:
        account_number = None
        account_title = None
        account_balance = 0
        credit_limit = 0

    return account_number, account_title, account_balance, credit_limit


def fn_get_account_ledger(p_account_number):
    account_ledger_code = None
    try:
        acc = Accounts_Balance.objects.get(account_number=p_account_number)
        account_ledger_code = acc.account_ledger_code
    except Accounts_Balance.DoesNotExist:
        account_ledger_code = None

    return account_ledger_code


def fn_update_account_closing(p_account_number, p_account_closing_date):
    status = False
    message = None
    try:
        acc = Accounts_Balance.objects.get(account_number=p_account_number)
        acc.account_closing_date = p_account_closing_date
        acc.save()
        status = True
        message = None
    except Accounts_Balance.DoesNotExist:
        status = False
        message = "Invalid Account Number "+str(p_account_number)
    except Exception as e:
        status = False
        message = str(e)
    return status, message


def fn_get_transaction_account_type(p_transaction_screen):
    account_type = None
    client_type = None

    try:
        row = Transaction_Type.objects.get(
            transaction_screen=p_transaction_screen)
        try:
            account_type = row.tran_account_type.account_type_code
        except Exception as e:
            account_type = None

        try:
            client_type = row.transaction_client_type.client_type_code
        except Exception as e:
            print(e)
            client_type = None

    except Transaction_Type.DoesNotExist:
        account_type = None
        client_type = None

    return account_type, client_type


def fn_get_transaction_account_type_screen(p_transaction_screen, p_tran_type_id):
    try:
        row = Transaction_Type.objects.get(
            transaction_screen=p_transaction_screen, tran_type_id=p_tran_type_id)
        try:
            account_type = row.tran_account_type.account_type_code
        except Exception as e:
            account_type = None
        try:
            client_type = row.transaction_client_type.client_type_code
        except Exception as e:
            client_type = None

    except Transaction_Type.DoesNotExist:
        account_type = None
        client_type = None

    return account_type, client_type


def fn_open_account_transaction_screen(p_transaction_screen, p_branch_code, p_center_code, p_app_user_id, p_client_id,
                                       p_client_name, p_client_address, p_phone_number, p_cbd, p_limit_amount=0.00):
    try:
        row = Client_Type.objects.filter(
            transaction_screen=p_transaction_screen)

        for client_type in row:
            status, error_message = fn_create_account(p_branch_code, p_center_code, p_app_user_id, p_client_id,
                                                      client_type.client_type_code, p_client_name, p_client_address,
                                                      p_phone_number, p_cbd, p_limit_amount)
            if not status:
                return False, error_message

        return True, None
    except Exception as e:
        return False, str(e)


def fn_generate_document_number(p_branch_code):
    inv_number = get_inv_number(
        20002, p_branch_code, p_branch_code, 'Document Number', 1)
    return 'S'+datetime.date.today().strftime("%m%d%Y")+str(inv_number[0])


def fn_get_accountinfo_byacnumber(p_account_number):
    try:
        acc = Accounts_Balance.objects.get(account_number=p_account_number)
        account_number = acc.account_number
        account_title = acc.account_title
        account_balance = acc.account_balance
        credit_limit = acc.credit_limit
        account_type = acc.account_type
        client_id = acc.client_id
        account_address = acc.account_address
        phone_number = acc.phone_number
        branch_code = acc.branch_code
        center_code = acc.center_code
    except Accounts_Balance.DoesNotExist:
        account_number = None
        account_title = None
        account_balance = 0
        credit_limit = 0
        account_type = None
        client_id = None
        account_address = None
        phone_number = None
        branch_code = None
        center_code = None
    return account_number, branch_code, center_code, phone_number, client_id, account_type, account_title, account_address, account_balance, credit_limit


def fn_get_client_accounts_info(p_client_id):
    message = ""
    index_number = 0
    try:
        accounts = Accounts_Balance.objects.filter(
            client_id=p_client_id).values("account_type", "account_balance")
        for account_info in accounts:
            index_number += 1
            actype = Account_Type.objects.get(
                account_type_code=account_info["account_type"])
            account_type_name = actype.account_type_name

            if index_number == 1:
                pass
            else:
                message = message+", "

            message = message+account_type_name+" Balance : " + \
                str(account_info["account_balance"])
        return message
    except Accounts_Balance.DoesNotExist:
        return "Invalid Account Number!"
    except Exception as e:
        return str(e)


def fn_get_client_accounts_balance(p_client_id):
    status = False
    total_balance = 0
    try:
        accounts = Accounts_Balance.objects.filter(
            client_id=p_client_id).values("account_type", "account_balance")
        for account_info in accounts:
            total_balance = total_balance+abs(account_info["account_balance"])

        status = True
        return status, total_balance
    except Accounts_Balance.DoesNotExist:
        return status, total_balance
    except Exception as e:
        return status, total_balance


def fn_get_client_accounts_debit_credit(p_client_id):
    status = False
    message = None
    total_debit_amount = 0
    total_credit_amount = 0
    try:
        accounts = Accounts_Balance.objects.filter(
            client_id=p_client_id).values("account_type", "account_balance", "total_debit_amount", "total_credit_amount")
        for account_info in accounts:
            total_debit_amount = total_debit_amount + \
                abs(account_info["total_debit_amount"])
            total_credit_amount = total_credit_amount + \
                abs(account_info["total_credit_amount"])

        status = True
        return status, message,  total_debit_amount, total_credit_amount
    except Accounts_Balance.DoesNotExist:
        message = "Invalid Customer!"
        return status, message,  total_debit_amount, total_credit_amount
    except Exception as e:
        message = str(e)
        return status, message,  total_debit_amount, total_credit_amount


def fn_get_accountinfo_bytran(p_client_id, p_tran_screen=None, p_tran_type=None, p_client_type_code=None):

    account_number = None
    account_title = None
    acc_type_code = None
    account_balance = 0
    credit_limit = 0
    account_summary = Accounts_Balance.objects.filter(
        client_id=p_client_id).aggregate(Count('phone_number'))
    total_account = account_summary['phone_number__count']

    if total_account == 1:
        acc = Accounts_Balance.objects.get(client_id=p_client_id)
        account_number = acc.account_number
        account_title = acc.account_title
        account_balance = acc.account_balance
        credit_limit = acc.credit_limit

        return account_number, account_title, account_balance, credit_limit

    if total_account == 0:
        return account_number, account_title, account_balance, credit_limit

    if p_tran_screen is not None and p_tran_type is not None:
        try:
            tran_type = Transaction_Type.objects.get(
                transaction_screen=p_tran_screen, tran_type_code=p_tran_type)
            acc_type_code = tran_type.tran_account_type.account_type_code
        except Transaction_Type.DoesNotExist:
            tran_type = None
    else:
        if p_tran_screen is not None:
            try:
                tran_type = Transaction_Type.objects.get(
                    transaction_screen=p_tran_screen)
                acc_type_code = tran_type.tran_account_type.account_type_code
            except Transaction_Type.DoesNotExist:
                tran_type = None

    if p_client_type_code and not acc_type_code:
        acc_type_code = get_client_account_type(p_client_type_code)
    try:
        acc = Accounts_Balance.objects.get(
            account_type=acc_type_code, client_id=p_client_id)
        account_number = acc.account_number
        account_title = acc.account_title
        account_balance = acc.account_balance
        credit_limit = acc.credit_limit
    except Client_Type.DoesNotExist:
        acc = None
    return account_number, account_title, account_balance, credit_limit


def get_account_info_byactype(p_client_id, p_acc_type):
    try:
        acc = Accounts_Balance.objects.get(
            account_type=p_acc_type, client_id=p_client_id)
        account_number = acc.account_number
        account_title = acc.account_title
        account_balance = acc.account_balance
        credit_limit = acc.credit_limit
    except Accounts_Balance.DoesNotExist:
        account_number = None
        account_title = None
        account_balance = 0
        credit_limit = 0

    return account_number, account_title, account_balance, credit_limit


def fn_get_transaction_gl(p_transaction_screen, p_tran_type_code):
    debit_gl_code = None
    credit_gl_code = None
    try:
        tran_type = Transaction_Type.objects.get(
            transaction_screen=p_transaction_screen, tran_type_id=p_tran_type_code)
        debit_gl_code = tran_type.debit_gl_code.gl_code
        credit_gl_code = tran_type.credit_gl_code.gl_code
        return credit_gl_code, debit_gl_code
    except Transaction_Type.DoesNotExist:
        debit_gl_code = None
        credit_gl_code = None
        return credit_gl_code, debit_gl_code


def fn_get_cash_gl_code():
    try:
        row = Application_Settings.objects.get()
        cash_gl_code = row.cash_gl_code
    except Accounts_Balance.DoesNotExist:
        cash_gl_code = None
    return cash_gl_code


def fn_cash_tran_posting(transaction_details):
    if transaction_details["tran_date"] is None:
        cbd = get_business_date(transaction_details["branch_code"])
    else:
        cbd = transaction_details["tran_date"]
    error_message = ''
    batch_number = 0

    try:
        transaction_type = Transaction_Type.objects.get(
            tran_type_code=transaction_details["tran_type"], transaction_screen=transaction_details["transaction_screen"])

        if transaction_type.default_debit_credit == 'C':
            transaction_ledger = transaction_type.credit_gl_code.gl_code
        else:
            transaction_ledger = transaction_type.debit_gl_code.gl_code

    except Transaction_Type.DoesNotExist:
        try:
            transaction_type = Transaction_Type.objects.get(
                transaction_screen=transaction_details["transaction_screen"])

            if transaction_type.default_debit_credit == 'C':
                transaction_ledger = transaction_type.credit_gl_code.gl_code
            else:
                transaction_ledger = transaction_type.debit_gl_code.gl_code

        except Transaction_Type.DoesNotExist:
            error_message = 'Transaction Debit/Credit is Not Define!'
            return False, error_message, batch_number

    cash_tran = Transaction_Table(branch_code=transaction_details["branch_code"], center_code=transaction_details["center_code"], transaction_date=cbd, batch_serial=1,
                                  account_number=transaction_details[
                                      "account_number"], tran_person_phone=transaction_details["account_phone"],
                                  tran_gl_code=transaction_details[
                                      "tran_gl_code"], contra_gl_code=transaction_details["contra_gl_code"],
                                  tran_debit_credit=transaction_details["tran_debit_credit"],
                                  tran_type=transaction_details["tran_type"], tran_amount=transaction_details["tran_amount"],
                                  tran_document_number=transaction_details["tran_document_number"],
                                  system_posted_tran=True, app_user_id=transaction_details["app_user_id"],
                                  transaction_narration=transaction_details["transaction_narration"])

    cash_tran.save()

    cursor = connection.cursor()
    cursor.callproc("fn_finance_post_cash_tran", [
                    transaction_details["branch_code"], transaction_details[
                        "center_code"], transaction_details["app_user_id"], transaction_details["tran_type"],
                    transaction_ledger, cbd, transaction_details[
                        "transaction_narration"], transaction_details["tran_type"],
                    transaction_details["transaction_screen"]])
    row = cursor.fetchone()
    batch_number = row[2]

    if row[0] != 'S':
        error_message = row[1]
        logger.error("Database Error in fn_cash_tran_posting line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
        return False, error_message, batch_number

    return True, error_message, batch_number


def fn_transfer_tran_posting(transaction_master, transaction_details):

    if transaction_master["tran_date"] is None:
        cbd = get_business_date(transaction_master["branch_code"])
    else:
        cbd = transaction_master["tran_date"]
    error_message = ''
    batch_number = 0
    batch_serial = 0
    rows = []
    for tran_row in transaction_details:
        batch_serial += 1
        tran_inst = Transaction_Table(branch_code=transaction_master["branch_code"], center_code=transaction_master["center_code"],
                                      transaction_date=cbd, batch_serial=batch_serial,
                                      account_number=tran_row["account_number"], tran_person_phone=tran_row["account_phone"],
                                      tran_gl_code=tran_row["tran_gl_code"], contra_gl_code=tran_row["contra_gl_code"],
                                      tran_debit_credit=tran_row["tran_debit_credit"],
                                      tran_type=transaction_master["tran_type"], tran_amount=tran_row["tran_amount"],
                                      tran_document_number=tran_row["tran_document_number"],
                                      system_posted_tran=True, app_user_id=transaction_master["app_user_id"],
                                      transaction_narration=tran_row["transaction_narration"])
        rows.append(tran_inst)

    Transaction_Table.objects.bulk_create(rows)

    cursor = connection.cursor()
    cursor.callproc("fn_finance_post_tran", [
                    transaction_master["branch_code"], transaction_master["center_code"], transaction_master["app_user_id"],
                    transaction_master["tran_type"], cbd, transaction_master["master_narration"],
                    transaction_master["transaction_screen"]])
    row = cursor.fetchone()
    batch_number = row[2]

    if row[0] != 'S':
        error_message = row[1]
        logger.error("Database Error in fn_post_tran line {} \nType: {} \nError:{}".format(
            sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
        return False, error_message, batch_number

    return True, error_message, batch_number


def fn_cancel_tran_batch(p_branch_code, p_app_user_id, p_transaction_date, p_batch_number, p_cancel_comments):
    error_message = None
    status = False
    cursor = connection.cursor()
    cursor.callproc("fn_finance_post_tran_cancel", [
                    p_branch_code, p_app_user_id, p_transaction_date, p_batch_number, p_cancel_comments])
    row = cursor.fetchone()
    if row[0] != 'S':
        error_message = row[1]
        status = False
        return status, error_message
    status = True
    return status, error_message


def fn_doc_number_validation(p_branch_code, p_doc_number, p_tran_type):
    param = Application_Settings.objects.get()
    if not param.transaction_doc_required:
        return True
    if Document_Register.objects.filter(branch_code=p_branch_code, doc_number=p_doc_number, tran_type=p_tran_type).exists():
        return True
    else:
        record = Document_Register(
            branch_code=p_branch_code, doc_number=p_doc_number, tran_type=p_tran_type)
        record.save()
        return False


def fn_deposit_receive_cancel(p_id, p_app_user_id):
    error_message = None
    status = False
    emi_tran = False
    try:
        dep_info = Deposit_Receive.objects.get(id=p_id)
        is_transfer = dep_info.is_transfer
        deposit_date = dep_info.deposit_date
        tran_batch_number = dep_info.tran_batch_number
        branch_code = dep_info.branch_code
        dep_info.cancel_amount = 0.00
        dep_info.cancel_by = p_app_user_id
        dep_info.cancel_on = timezone.now()

        if emi_tran:
            status = True
            return status, error_message
        else:
            status, error_message = fn_cancel_tran_batch(p_branch_code=branch_code, p_app_user_id=p_app_user_id,
                                                         p_transaction_date=deposit_date, p_batch_number=tran_batch_number, p_cancel_comments='Cancel by '+p_app_user_id)
            if status:
                if is_transfer:
                    dep_info.save()
                else:
                    dep_info.save()
            else:
                error_message = error_message
                status = False
                return status, error_message

        status = True
        return status, error_message
    except Deposit_Receive.DoesNotExist:
        error_message = "Invalid Deposit Receive Info!"
        status = False
        return status, error_message
    except Exception as e:
        error_message = str(e)
        status = False
        return status, error_message


def fn_deposit_payment_cancel(p_id, p_app_user_id):
    error_message = None
    status = False
    emi_tran = False
    try:
        dep_info = Deposit_Payment.objects.get(id=p_id)
        is_transfer = dep_info.is_transfer
        payment_date = dep_info.payment_date
        tran_batch_number = dep_info.tran_batch_number
        branch_code = dep_info.branch_code
        dep_info.cancel_amount = 0.00
        dep_info.cancel_by = p_app_user_id
        dep_info.cancel_on = timezone.now()

        if emi_tran:
            status = True
            return status, error_message
        else:
            status, error_message = fn_cancel_tran_batch(p_branch_code=branch_code, p_app_user_id=p_app_user_id,
                                                         p_transaction_date=payment_date, p_batch_number=tran_batch_number, p_cancel_comments='Cancel by '+p_app_user_id)
            if status:
                if is_transfer:
                    dep_info.save()
                else:
                    dep_info.save()
            else:
                error_message = error_message
                status = False
                return status, error_message

        status = True
        return status, error_message
    except Deposit_Receive.DoesNotExist:
        error_message = "Invalid Deposit Payment Info!"
        status = False
        return status, error_message
    except Exception as e:
        error_message = str(e)
        status = False
        return status, error_message


def fn_deposit_closing_cancel(p_id, p_app_user_id):
    error_message = None
    status = False
    emi_tran = False
    try:
        dep_info = Deposit_Closing.objects.get(id=p_id)
        closing_date = dep_info.closing_date
        tran_batch_number = dep_info.tran_batch_number
        branch_code = dep_info.branch_code
        dep_info.cancel_amount = 0.00
        dep_info.cancel_by = p_app_user_id
        dep_info.cancel_on = timezone.now()

        if emi_tran:
            status = True
            return status, error_message
        else:
            status, error_message = fn_cancel_tran_batch(p_branch_code=branch_code, p_app_user_id=p_app_user_id,
                                                         p_transaction_date=closing_date, p_batch_number=tran_batch_number, p_cancel_comments='Cancel by '+p_app_user_id)
            if status:
                dep_info.save()
            else:
                error_message = error_message
                status = False
                return status, error_message

        acc = Accounts_Balance.objects.get(
            account_number=dep_info.account_number)
        acc.account_closing_date = None
        acc.save()

        status = True
        return status, error_message
    except Deposit_Receive.DoesNotExist:
        error_message = "Invalid Deposit Closing Info!"
        status = False
        return status, error_message
    except Exception as e:
        error_message = str(e)
        status = False
        return status, error_message


def fn_set_account_statement(p_branch_code, p_account_number, p_tran_from_date, p_tran_upto_date, p_app_user_id):
    try:
        tran_from_date = p_tran_from_date
        tran_upto_date = p_tran_upto_date

        if not tran_from_date or tran_from_date is None:
            accounts = Accounts_Balance.objects.get(
                account_number=p_account_number)
            tran_from_date = accounts.account_opening_date

        if not tran_upto_date or tran_upto_date is None:
            tran_upto_date = get_business_date(p_branch_code, p_app_user_id)

        cursor = connection.cursor()
        cursor.callproc("fn_finance_query_account_statement", [
                        p_account_number, tran_from_date, tran_upto_date, p_app_user_id])
        row = cursor.fetchone()

        if row[0] != 'S':
            logger.error("Error in fn_finance_query_account_statement on line {} \nType: {} \nError:{}".format(
                sys.exc_info()[-1], type(row[1]).__name__, str(row[1])))
    except Exception as e:
        print(str(e))


def fn_get_actype_charge(p_actype_code, p_transaction_amount):
    with connection.cursor() as cursor:
        cursor.execute("select COALESCE(sum(charge_amount),0,00) charge_amount from fn_finance_get_charges(%s, %s,'',%s,%s);", [
                       p_transaction_amount, p_actype_code, False, False])
        row = cursor.fetchone()
    return row


def fn_get_charge_amount(p_charge_code, p_transaction_amount):
    with connection.cursor() as cursor:
        cursor.execute("select COALESCE(sum(charge_amount),0,00) charge_amount from fn_finance_get_charges(%s, '', %s,%s,%s);", [
                       p_transaction_amount, p_charge_code, False, False])
        row = cursor.fetchone()
    return row


def fn_get_account_opening_charge(p_actype_code, p_transaction_amount):
    with connection.cursor() as cursor:
        cursor.execute("select COALESCE(sum(charge_amount),0,00) charge_amount from fn_finance_get_charges(%s, %s,'',%s,%s);", [
                       p_transaction_amount, p_actype_code, True, False])
        row = cursor.fetchone()
    return row


def fn_get_account_closing_charge(p_actype_code, p_transaction_amount):
    with connection.cursor() as cursor:
        cursor.execute("select COALESCE(sum(charge_amount),0,00) charge_amount from fn_finance_get_charges(%s, %s,'',%s,%s);", [
                       p_transaction_amount, p_actype_code, False, True])
        row = cursor.fetchone()
    return row


def fn_deposit_transfer(data):
    status = False
    message = None
    try:
        receive = Deposit_Receive(branch_code=data["to_branch_code"], center_code=data["to_center_code"],
                                  client_id=data["to_client_id"], account_number=data[
                                      "to_account_number"], deposit_date=data["transaction_date"],
                                  deposit_amount=data["transaction_amount"], cancel_amount=0.00, tran_batch_number=data["tran_batch_number"],
                                  deposit_doc_num=data["tran_document_number"], dep_entry_day_sl=0, narration=data["narration"], is_transfer=True,
                                  app_user_id=data["app_user_id"])

        payment = Deposit_Payment(branch_code=data["from_branch_code"], center_code=data["from_center_code"],
                                  client_id=data["from_client_id"], account_number=data[
                                      "from_account_number"], payment_date=data["transaction_date"],
                                  payment_amount=data["transaction_amount"], cancel_amount=0.00, tran_batch_number=data["tran_batch_number"],
                                  payment_doc_num=data["tran_document_number"], dep_entry_day_sl=0, narration=data["narration"], is_transfer=True,
                                  app_user_id=data["app_user_id"])

        receive.save()
        payment.save()

    except Exception as e:
        status = False
        message = str(e)
    return status, message
