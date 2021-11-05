from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from rest_framework import generics
from django.db.models import Case, CharField, Value, When, F
from rest_framework.generics import ListAPIView
# Create your views here.

from appauth.models import *

from apifinance.serializers import *
from finance.utils import fn_get_transaction_account_type, fn_get_transaction_account_type_screen


class General_Ledger_ApiView(generics.ListAPIView):
    serializer_class = General_Ledger_Serializer

    def get_queryset(self):
        gl_code = self.request.query_params.get('gl_code', None)
        gl_name = self.request.query_params.get('gl_name', None)

        queryset = General_Ledger.objects.filter().order_by('gl_name')

        if gl_code:
            queryset = queryset.filter(gl_code=gl_code)
        if gl_name:
            queryset = queryset.filter(client_name__icontains=gl_name)
        return queryset


class Transaction_Type_ApiView(generics.ListAPIView):
    serializer_class = Transaction_Type_Serializer

    def get_queryset(self):

        queryset = Transaction_Type.objects.filter().order_by('tran_type_name')

        return queryset


class Ledger_Transaction_Type_ApiView(generics.ListAPIView):
    serializer_class = Ledger_Transaction_Type_Serializer

    def get_queryset(self):

        queryset = Ledger_Transaction_Type.objects.filter().order_by('tran_type_id')

        return queryset


class Cash_And_Bank_Ledger_ApiView(generics.ListAPIView):
    serializer_class = Cash_And_Bank_Ledger_Serializer

    def get_queryset(self):

        queryset = Cash_And_Bank_Ledger.objects.filter().order_by('branch_code', 'gl_code')

        return queryset


class Account_Type_ApiView(generics.ListAPIView):
    serializer_class = Account_Type_Serializer

    def get_queryset(self):

        queryset = Account_Type.objects.filter().order_by('account_type_code')

        return queryset


class Client_Type_ApiView(generics.ListAPIView):
    serializer_class = Client_Type_Serializer

    def get_queryset(self):

        queryset = Client_Type.objects.filter().order_by('client_type_name')

        return queryset


class Client_Account_Mapping_ApiView(generics.ListAPIView):
    serializer_class = Client_Account_Mapping_Serializer

    def get_queryset(self):

        queryset = Client_Account_Mapping.objects.filter().order_by('client_type_code')

        return queryset


class Transaction_Table_ApiView(generics.ListAPIView):
    serializer_class = Transaction_Table_Serializer

    def get_queryset(self):
        branch_code = self.request.session.get('branch_code')
        app_user_id = self.request.session.get('app_user_id')
        queryset = Transaction_Table.objects.filter(
            app_user_id=app_user_id).order_by('-app_data_time')

        return queryset


class Transaction_Master_ApiView(generics.ListAPIView):
    serializer_class = Transaction_Master_Serializer

    def get_queryset(self):
        tran_from_date = self.request.query_params.get('tran_from_date', None)
        tran_upto_date = self.request.query_params.get('tran_upto_date', None)
        branch_code = self.request.query_params.get('branch_code', None)
        from_batch_number = self.request.query_params.get(
            'from_batch_number', None)
        upto_batch_number = self.request.query_params.get(
            'upto_batch_number', None)

        if tran_from_date == tran_upto_date:
            tran_date = tran_from_date
        else:
            tran_date = None

        queryset = Transaction_Master.objects.filter().order_by('-app_data_time').extra(
            select={'tran_date': 'transaction_date'}).values('id', 'branch_code', 'tran_date', 'batch_number', 'total_debit_amount',
                                                             'transaction_narration', 'cancel_by', 'app_user_id', 'auth_by')

        if tran_date:
            queryset = queryset.filter(transaction_date=tran_date)

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)

        if from_batch_number:
            queryset = queryset.filter(batch_number__gte=from_batch_number)

        if upto_batch_number:
            queryset = queryset.filter(batch_number__lte=upto_batch_number)

        if tran_from_date and tran_upto_date:
            queryset = queryset.filter(
                transaction_date__gte=tran_from_date, transaction_date__lte=tran_upto_date)

        return queryset


class Finance_Query_Table_ApiView(generics.ListAPIView):
    serializer_class = Finance_Query_Table_Serializer

    def get_queryset(self):
        app_user_id = self.request.session.get('app_user_id')
        queryset = Query_Table.objects.filter(app_user_id=app_user_id)

        return queryset


class Search_Accounts_ApiView(generics.ListAPIView):
    serializer_class = Search_Accounts_Serializer

    def get_queryset(self):
        input_text = self.request.query_params.get('q', None)
        account_type = self.request.query_params.get('account_type', None)
        tran_screen = self.request.query_params.get('tran_screen', None)
        transaction_type = self.request.query_params.get(
            'transaction_type', None)

        if transaction_type and tran_screen:
            account_type, client_type = fn_get_transaction_account_type_screen(
                tran_screen, transaction_type)

        if not transaction_type and not account_type and tran_screen:
            account_type, client_type = fn_get_transaction_account_type(
                tran_screen)

        # if input_text:
        #     queryset = Accounts_Balance.objects.filter(client_id=input_text, account_type=account_type,
        #                                                account_closing_date__isnull=True).order_by('account_title')
        if input_text:
            queryset = Accounts_Balance.objects.filter(account_title__icontains=input_text, account_type=account_type,
                                                       account_closing_date__isnull=True).order_by('account_title')
        return queryset


class Search_Accounts_Name_ApiView(generics.ListAPIView):
    serializer_class = Search_Accounts_Serializer

    def get_queryset(self):
        input_text = self.request.query_params.get('q', None)
        account_type = self.request.query_params.get('account_type', None)
        tran_screen = self.request.query_params.get('tran_screen', None)
        transaction_type = self.request.query_params.get(
            'transaction_type', None)

        if transaction_type and tran_screen:
            account_type, client_type = fn_get_transaction_account_type_screen(
                tran_screen, transaction_type)

        if not transaction_type and not account_type and tran_screen:
            account_type, client_type = fn_get_transaction_account_type(
                tran_screen)

        if input_text:
            queryset = Accounts_Balance.objects.filter(account_title__icontains=input_text, account_type=account_type,
                                                       account_closing_date__isnull=True).order_by('account_title')
        return queryset


class Accounts_Balance_ApiView(generics.ListAPIView):
    serializer_class = Accounts_Balance_Serializer

    def get_queryset(self):
        client_id = self.request.query_params.get('client_id', None)
        phone_number = self.request.query_params.get('phone_number', None)
        account_number = self.request.query_params.get('account_number', None)
        branch_code = self.request.query_params.get('branch_code', None)
        account_type = self.request.query_params.get('products_type', None)
        queryset = Accounts_Balance.objects.filter().order_by('account_title')

        if client_id:
            queryset = queryset.filter(client_id=client_id)

        if phone_number:
            queryset = queryset.filter(phone_number=phone_number)

        if account_number:
            queryset = queryset.filter(account_number=account_number)

        if account_type:
            queryset = queryset.filter(account_type=account_type)

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)

        return queryset


class Tran_Telbal_Details_ApiView(generics.ListAPIView):
    serializer_class = Tran_Telbal_Details_Serializer

    def get_queryset(self):
        org_teller_id = self.request.query_params.get('org_teller_id', None)
        transaction_date = self.request.query_params.get(
            'transaction_date', None)
        branch_code = self.request.query_params.get('branch_code', None)
        auth_pending = self.request.query_params.get('auth_pending', None)

        queryset = Tran_Telbal_Details.objects.filter(
            org_teller_id=org_teller_id).order_by('transaction_date')

        if transaction_date:
            queryset = queryset.filter(transaction_date=transaction_date)

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)

        if auth_pending == 'Y':
            queryset = queryset.filter(auth_by__isnull=True)

        return queryset


class Deposit_Receive_ApiView(generics.ListAPIView):
    serializer_class = Deposit_Receive_Serializer

    def get_queryset(self):
        account_number = self.request.query_params.get('account_number', None)
        branch_code = self.request.query_params.get('branch_code', None)
        from_date = self.request.query_params.get('from_date', None)
        upto_date = self.request.query_params.get('upto_date', None)

        if from_date == upto_date:
            deposit_date = upto_date
            from_date = None
            upto_date = None

        queryset = Deposit_Receive.objects.filter(is_transfer=False).order_by('-deposit_date')

        if account_number:
            queryset = queryset.filter(account_number=account_number)

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)

        if deposit_date:
            queryset = queryset.filter(deposit_date=deposit_date)

        if from_date:
            queryset = queryset.filter(deposit_date__gte=from_date)

        if upto_date:
            queryset = queryset.filter(deposit_date__lte=upto_date)

        return queryset


class Deposit_Payment_ApiView(generics.ListAPIView):
    serializer_class = Deposit_Payment_Serializer

    def get_queryset(self):
        account_number = self.request.query_params.get('account_number', None)
        branch_code = self.request.query_params.get('branch_code', None)
        from_date = self.request.query_params.get('from_date', None)
        upto_date = self.request.query_params.get('upto_date', None)

        if from_date == upto_date:
            payment_date = upto_date
            from_date = None
            upto_date = None

        queryset = Deposit_Payment.objects.filter(is_transfer=False).order_by('-payment_date')

        if account_number:
            queryset = queryset.filter(account_number=account_number)

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)

        if payment_date:
            queryset = queryset.filter(payment_date=payment_date)

        if from_date:
            queryset = queryset.filter(payment_date__gte=from_date)

        if upto_date:
            queryset = queryset.filter(payment_date__lte=upto_date)

        return queryset


class Deposit_Closing_ApiView(generics.ListAPIView):
    serializer_class = Deposit_Closing_Serializer

    def get_queryset(self):
        account_number = self.request.query_params.get('account_number', None)
        branch_code = self.request.query_params.get('branch_code', None)
        from_date = self.request.query_params.get('from_date', None)
        upto_date = self.request.query_params.get('upto_date', None)

        if from_date == upto_date:
            closing_date = upto_date
            from_date = None
            upto_date = None

        queryset = Deposit_Closing.objects.filter().order_by('-closing_date')

        if account_number:
            queryset = queryset.filter(account_number=account_number)

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)

        if closing_date:
            queryset = queryset.filter(closing_date=closing_date)

        if from_date:
            queryset = queryset.filter(closing_date__gte=from_date)

        if upto_date:
            queryset = queryset.filter(closing_date__lte=upto_date)

        return queryset


class Deposit_Transfer_ApiView(generics.ListAPIView):
    serializer_class = Deposit_Transfer_Serializer

    def get_queryset(self):
        from_account_number = self.request.query_params.get('from_account_number', None)
        to_account_number = self.request.query_params.get('to_account_number', None)
        branch_code = self.request.query_params.get('branch_code', None)

        queryset = Deposit_Transfer.objects.filter().order_by('id')

        if from_account_number:
            queryset = queryset.filter(from_account_number=from_account_number)

        if to_account_number:
            queryset = queryset.filter(to_account_number=to_account_number)

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)

        return queryset

class Charges_ApiView(generics.ListAPIView):
    serializer_class = Charges_Serializer

    def get_queryset(self):
        charges_code = self.request.query_params.get('charges_code')
        actype_code = self.request.query_params.get('actype_code')

        queryset = Charges.objects.filter().order_by('charges_name')

        if charges_code:
            queryset = queryset.filter(charges_code=charges_code)

        if actype_code:
            queryset = queryset.filter(actype_code=actype_code)

        return queryset
