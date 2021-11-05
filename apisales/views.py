from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from rest_framework import generics
from django.db.models import Case, CharField, Value, When, F
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
import datetime
from django.contrib.auth import get_user_model
User = get_user_model()

from sales.models import *
from appauth.utils import fn_is_head_office_user

from .serializers import *
from sales.ecom_models import *


class StockMasterAuthQAPIView(generics.ListAPIView):
    serializer_class = StockMasterAuthQSerializer

    def get_queryset(self):
        app_user_id = self.request.session.get('app_user_id')
        branch_code = self.request.session.get('branch_code')
        queryset = StockMasterAuthQ.objects.filter(
            status='W').order_by('-app_data_time')
        if not fn_is_head_office_user(app_user_id):
            queryset = queryset.filter(branch_code=branch_code)

        return queryset


##################
class PurchaseMasterAuthQAPIView(generics.ListAPIView):
    serializer_class = PurchaseMasterAuthQSerializer

    def get_queryset(self):
        app_user_id = self.request.session.get('app_user_id')
        branch_code = self.request.session.get('branch_code')
        queryset = PurchaseMasterAuthQ.objects.filter(
            status='W').order_by('-app_user_id')
        if not fn_is_head_office_user(app_user_id):
            queryset = queryset.filter(branch_code=branch_code)

        return queryset


class StockDetailsAPIView(generics.ListAPIView):
    serializer_class = StockDetailsSerializer

    def get_queryset(self):
        stock_date = self.request.query_params.get('stock_date', None)
        stock_id = self.request.query_params.get('stock_id', None)
        product_id = self.request.query_params.get('product_id', None)
        branch_code = self.request.query_params.get('branch_code', None)
        from_date = self.request.query_params.get('from_date', None)
        upto_date = self.request.query_params.get('upto_date', None)

        if from_date == upto_date:
            stock_date = upto_date
            from_date = None
            upto_date = None

        if not branch_code:
            branch_code = None

        queryset = StockDetails.objects.filter().order_by('-app_data_time')
        if stock_id:
            queryset = queryset.filter(stock_id=stock_id)

        if stock_date:
            queryset = queryset.filter(stock_date=stock_date)

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)

        if stock_date:
            queryset = queryset.filter(stock_date=stock_date)

        if from_date:
            queryset = queryset.filter(stock_date__gte=from_date)

        if upto_date:
            queryset = queryset.filter(stock_date__lte=upto_date)

        if product_id:
            queryset = queryset.filter(product_id=product_id)

        return queryset


class StockMasterAPIViewSearch(generics.ListAPIView):
    serializer_class = StockMasterSerializer

    def get_queryset(self):
        stock_date = self.request.query_params.get('stock_date', None)
        stock_id = self.request.query_params.get('stock_id', None)
        branch_code = self.request.query_params.get('branch_code', None)
        from_date = self.request.query_params.get('from_date', None)
        upto_date = self.request.query_params.get('upto_date', None)
        supplier_phone = self.request.query_params.get('supplier_phone', None)

        if from_date == upto_date:
            stock_date = upto_date
            from_date = None
            upto_date = None

        if not branch_code:
            branch_code = None

        queryset = StockMaster.objects.filter().order_by('-app_data_time')

        if stock_id:
            queryset = queryset.filter(stock_id=stock_id)

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)

        if stock_date:
            queryset = queryset.filter(stock_date=stock_date)

        if from_date:
            queryset = queryset.filter(stock_date__gte=from_date)

        if upto_date:
            queryset = queryset.filter(stock_date__lte=upto_date)

        if supplier_phone:
            queryset = queryset.filter(supplier_phone=supplier_phone)

        return queryset


class ProductsApiView(generics.ListAPIView):
    serializer_class = ProductsSerializer

    def get_queryset(self):
        product_model = self.request.query_params.get('product_model', None)
        product_bar_code = self.request.query_params.get(
            'product_bar_code', None)
        product_name = self.request.query_params.get('product_name', None)
        group_id = self.request.query_params.get('group_id', None)
        brand_id = self.request.query_params.get('brand_id', None)
        product_id = self.request.query_params.get('product_id', None)
        queryset = products.objects.filter().order_by('product_name')

        if product_model:
            queryset = queryset.filter(product_model=product_model)
        if product_name:
            queryset = queryset.filter(product_name__icontains=product_name)
        if product_bar_code:
            queryset = queryset.filter(product_bar_code=product_bar_code)
        if group_id:
            queryset = queryset.filter(product_group=group_id)
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        if product_id:
            queryset = queryset.filter(product_id=product_id)

        return queryset


class SalesDetailsTempApiView(generics.ListAPIView):
    serializer_class = SalesDetailsTempSerializer

    def get_queryset(self):
        app_user_id = self.request.session.get('app_user_id')
        queryset = Sales_Details_Temp.objects.filter(
            app_user_id=app_user_id).order_by('-app_data_time')
        return queryset


class SalesInvoiceApiView(generics.ListAPIView):
    serializer_class = SalesInvoiceSerializer

    def get_queryset(self):
        invoice_from_date = self.request.query_params.get(
            'invoice_from_date', None)
        invoice_upto_date = self.request.query_params.get(
            'invoice_upto_date', None)
        invoice_number = self.request.query_params.get('invoice_number', None)
        customer_phone = self.request.query_params.get('customer_phone', None)
        branch_code = self.request.query_params.get('branch_code', None)
        center_code = self.request.query_params.get('center_code', None)
        executive_phone = self.request.query_params.get(
            'executive_phone', None)
        queryset = Sales_Master.objects.filter().order_by('-app_data_time')

        if invoice_number:
            queryset = queryset.filter(invoice_number=invoice_number)

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)

        if center_code:
            queryset = queryset.filter(center_code=center_code)

        if invoice_from_date and invoice_upto_date:
            queryset = queryset.filter(
                invoice_date__gte=invoice_from_date, invoice_date__lte=invoice_upto_date)

        if customer_phone:
            queryset = queryset.filter(customer_phone=customer_phone)

        if executive_phone:
            queryset = queryset.filter(executive_phone=executive_phone)

        return queryset


class SalesInvoiceDetailsApiView(generics.ListAPIView):
    serializer_class = SalesInvoiceDetailsSerializer

    def get_queryset(self):
        invoice_number = self.request.query_params.get('invoice_number', None)
        queryset = Sales_Details.objects.filter().order_by('-app_data_time')

        if invoice_number:
            queryset = queryset.filter(invoice_number=invoice_number)

        return queryset


class SalesClientsApiView(generics.ListAPIView):
    serializer_class = SalesClientsSerializer

    def get_queryset(self):
        branch_code = self.request.query_params.get('branch_code')
        client_phone = self.request.query_params.get('client_phone', None)
        client_id = self.request.query_params.get('client_id', None)
        client_name = self.request.query_params.get('client_name', None)
        center_code = self.request.query_params.get('center_code', None)

        queryset = Clients.objects.filter().extra(
            select={'order_client_id': 'CAST(client_id AS bigint)'}
        ).order_by('order_client_id')

        if client_phone:
            queryset = queryset.filter(client_phone=client_phone)

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)

        if client_id:
            queryset = queryset.filter(client_id=client_id)

        if center_code:
            queryset = queryset.filter(center_code=center_code)

        if client_name:
            queryset = queryset.filter(client_name__icontains=client_name)

        return queryset


class ProductPriceListApiView(generics.ListAPIView):
    serializer_class = ProductPriceListSerializer

    def get_queryset(self):
        branch_code = self.request.session.get('branch_code')
        app_user_id = self.request.session.get('app_user_id')
        product_id = self.request.query_params.get('product_id', None)

        queryset = Product_Price_List.objects.filter(
            product_id=product_id).order_by('branch_code')

        return queryset


class ProductOfferListApiView(generics.ListAPIView):
    serializer_class = ProductOfferListSerializer

    def get_queryset(self):
        branch_code = self.request.session.get('branch_code')
        app_user_id = self.request.session.get('app_user_id')
        product_id = self.request.query_params.get('product_id', None)

        queryset = Product_Offer_List.objects.filter(
            product_id=product_id).order_by('branch_code')

        return queryset


class ClientSecurityApiView(generics.ListAPIView):
    serializer_class = ClientSecuritySerializer

    def get_queryset(self):
        branch_code = self.request.session.get('branch_code')
        app_user_id = self.request.session.get('app_user_id')
        client_phone = self.request.query_params.get('client_phone', None)

        queryset = Delar_Security_Info.objects.filter(
            phone_number=client_phone).order_by('branch_code')

        return queryset


class ProductOfferPackageApiView(generics.ListAPIView):
    serializer_class = ProductOfferPackageSerializer

    def get_queryset(self):
        branch_code = self.request.session.get('branch_code')
        app_user_id = self.request.session.get('app_user_id')
        product_id = self.request.query_params.get('product_id', None)

        queryset = Product_Offer_Package.objects.filter(
            product_id=product_id).order_by('branch_code')

        return queryset


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs_count = User.objects.all().count()
        labels = ["Users", "Blue", "Yellow", "Green", "Purple", "Orange"]
        default_items = [qs_count, 23, 2, 3, 12, 2]
        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)


class SalesDashboardData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        stock_sales_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]
        stock_sales_stock_data = [80, 149, 300, 500, 100, 200, 158]
        stock_sales_sales_data = [80, 149, 300, 500, 100, 200, 158]
        data = {
            "stock_sales_labels": stock_sales_labels,
            "stock_sales_stock_data": stock_sales_stock_data,
            "stock_sales_sales_data": stock_sales_sales_data,
        }
        return Response(data)


class SalesOrderApiView(generics.ListAPIView):
    serializer_class = SalesOrderSerializer

    def get_queryset(self):
        order_date = self.request.query_params.get('order_date', None)
        order_number = self.request.query_params.get('order_number', None)
        customer_phone = self.request.query_params.get('customer_phone', None)
        executive_phone = self.request.query_params.get(
            'executive_phone', None)
        order_status = self.request.query_params.get(
            'order_status', None)
        branch_code = self.request.session.get('branch_code')

        from_date = self.request.query_params.get('from_date', None)
        upto_date = self.request.query_params.get('upto_date', None)

        if from_date == upto_date:
            order_date = upto_date
            from_date = None
            upto_date = None

        queryset = Order_Master.objects.filter().order_by('-app_data_time')

        if order_status:
            queryset = queryset.filter(status=order_status)

        if order_date:
            queryset = queryset.filter(order_date=order_date)

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)

        if order_number:
            queryset = queryset.filter(order_number=order_number)

        if customer_phone:
            queryset = queryset.filter(customer_phone=customer_phone)

        if executive_phone:
            queryset = queryset.filter(executive_phone=executive_phone)

        if from_date:
            queryset = queryset.filter(order_date__gte=from_date)

        if upto_date:
            queryset = queryset.filter(order_date__lte=upto_date)

        return queryset


class SalesOrderDetailsApiView(generics.ListAPIView):
    serializer_class = SalesOrderDetailsSerializer

    def get_queryset(self):
        order_number = self.request.query_params.get('order_number', None)
        branch_code = self.request.session.get('branch_code')
        queryset = Order_Details.objects.filter().order_by('-app_data_time')

        if order_number:
            queryset = queryset.filter(invoice_number=order_number)

        return queryset


class StockDetailsTempApiView(generics.ListAPIView):
    serializer_class = StockDetailsTempSerializer

    def get_queryset(self):
        branch_code = self.request.session.get('branch_code')
        app_user_id = self.request.session.get('app_user_id')
        queryset = StockDetailsTemp.objects.filter(
            app_user_id=app_user_id).order_by('-app_data_time')
        return queryset


class SalesSupplierApiView(generics.ListAPIView):
    serializer_class = SalesSupplier

    def get_queryset(self):
        supp_mobile = self.request.query_params.get('supp_mobile', None)
        supp_name = self.request.query_params.get('supp_name', None)
        branch_code = self.request.query_params.get('branch_code', None)

        queryset = Supplier_Information.objects.filter().order_by('supp_name')

        if supp_mobile:
            queryset = queryset.filter(supp_mobile=supp_mobile)

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)

        if supp_name:
            queryset = queryset.filter(supp_name__icontains=supp_name)

        return queryset


class SearchProductListApiView(generics.ListAPIView):
    serializer_class = SearchProductListSerializer

    def get_queryset(self):
        branch_code = self.request.session.get('branch_code')
        app_user_id = self.request.session.get('app_user_id')
        input_text = self.request.query_params.get('q', None)
        if input_text:
            queryset = products.objects.filter(
                product_search_text__icontains=input_text).order_by('product_search_text')
        return queryset


class SearchClientsListApiView(generics.ListAPIView):
    serializer_class = SearchClients

    def get_queryset(self):
        input_text = self.request.query_params.get('q', None)
        branch_code = self.request.query_params.get('branch_code', None)

        # if input_text:
        #     queryset = Clients.objects.filter(
        #         client_id=input_text, closing_date__isnull=True).order_by('client_name')
        if input_text:
            queryset = Clients.objects.filter(
                client_name__icontains=input_text, closing_date__isnull=True).order_by('client_name')

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)

        return queryset


class st_group_model_apiview(generics.ListAPIView):
    serializer_class = st_group_model_serializers

    def get_queryset(self):
        queryset = Products_Group.objects.filter().order_by('group_name')

        return queryset


class product_brand_model_apiview(generics.ListAPIView):
    serializer_class = product_brand_model_serializers

    def get_queryset(self):
        queryset = Products_Brand.objects.filter().order_by('brand_name')

        return queryset

class product_unit_model_apiview(generics.ListAPIView):
    serializer_class = product_unit_model_serializers

    def get_queryset(self):
        queryset = Products_Unit.objects.filter().order_by('unit_name')

        return queryset
class Emi_Setup_Apiview(generics.ListAPIView):
    serializer_class = emisetup_model_serializers

    def get_queryset(self):
        emi_reference_no = self.request.query_params.get(
            'emi_reference_no', None)
        client_id = self.request.query_params.get('client_id', None)
        account_number = self.request.query_params.get('account_number', None)
        emi_reference_no = emi_reference_no.upper()

        queryset = Emi_Setup.objects.filter().order_by('emi_serial_number')

        if emi_reference_no:
            queryset = queryset.filter(emi_reference_no=emi_reference_no)

        if account_number:
            queryset = queryset.filter(account_number=account_number)

        if client_id:
            queryset = queryset.filter(client_id=client_id)

        return queryset


class Emi_Receive_ApiView(generics.ListAPIView):
    serializer_class = emircv_model_serializers

    def get_queryset(self):
        account_number = self.request.query_params.get('account_number', None)
        emi_reference_no = self.request.query_params.get(
            'emi_reference_no', None)
        branch_code = self.request.query_params.get('branch_code', None)
        queryset = Emi_Receive.objects.filter().order_by('-app_data_time')

        if account_number:
            queryset = queryset.filter(account_number=account_number)

        if emi_reference_no:
            queryset = queryset.filter(emi_reference_no=emi_reference_no)

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)

        return queryset


class showroom_model_apiview(generics.ListAPIView):
    serializer_class = showroom_model_serializers

    def get_queryset(self):
        queryset = ShowRoom.objects.filter().order_by('show_room_name')

        return queryset


class Client_Profit_HistoryApiView(generics.ListAPIView):
    serializer_class = Client_Profit_HistorySerializer

    def get_queryset(self):
        client_id = self.request.query_params.get('client_id', None)
        from_date = self.request.query_params.get('from_date', None)
        upto_date = self.request.query_params.get('upto_date', None)
        queryset = Client_Profit_History.objects.filter().order_by('transaction_date')

        if client_id:
            queryset = queryset.filter(client_id=client_id)

        if from_date and upto_date:
            queryset = queryset.filter(
                transaction_date__gte=from_date, transaction_date__lte=upto_date)

        return queryset


class User_Chart_ApiView(generics.ListAPIView):
    serializer_class = User_Chart_Serializer

    def get_queryset(self):
        queryset = User_Chart.objects.filter().order_by('product_name')

        return queryset


class Ecom_Order_Master_ApiView(generics.ListAPIView):
    serializer_class = Ecom_Order_Master_Serializer

    def get_queryset(self):
        order_date = self.request.query_params.get('order_date', None)
        order_number = self.request.query_params.get('order_number', None)
        customer_phone = self.request.query_params.get('customer_phone', None)
        executive_phone = self.request.query_params.get(
            'executive_phone', None)
        branch_code = self.request.session.get('branch_code')
        queryset = Ecom_Order_Master.objects.filter().order_by('app_data_time')

        if order_date:
            queryset = queryset.filter(invoice_date=order_date)

        if order_number:
            queryset = queryset.filter(invoice_number=order_number)

        if customer_phone:
            queryset = queryset.filter(customer_phone=customer_phone)

        if executive_phone:
            queryset = queryset.filter(executive_phone=executive_phone)

        return queryset


class Emi_History_ApiView(generics.ListAPIView):
    serializer_class = Emi_History_Model_Serializers

    def get_queryset(self):
        branch_code = self.request.query_params.get('branch_code', None)
        account_number = self.request.query_params.get('account_number', None)
        emi_reference_no = self.request.query_params.get(
            'emi_reference_no', None)
        executive_phone = self.request.query_params.get(
            'executive_phone', None)
        from_date = self.request.query_params.get('from_date', None)
        upto_date = self.request.query_params.get('upto_date', None)
        queryset = Emi_History.objects.filter().order_by('app_data_time')
        inst_receive_date = None

        if from_date == upto_date:
            inst_receive_date = upto_date
            from_date = None
            upto_date = None

        if branch_code:
            queryset = queryset.filter(branch_code=branch_code)

        if account_number:
            queryset = queryset.filter(account_number=account_number)

        if emi_reference_no:
            queryset = queryset.filter(emi_reference_no=emi_reference_no)

        if inst_receive_date:
            queryset = queryset.filter(inst_receive_date=inst_receive_date)

        if from_date:
            queryset = queryset.filter(inst_receive_date__gte=from_date)

        if upto_date:
            queryset = queryset.filter(inst_receive_date__lte=upto_date)

        return queryset
#################
class PurchaseDetailsTempApiView(generics.ListAPIView):
    serializer_class = PurchaseDetailsTempSerializer

    def get_queryset(self):
        branch_code = self.request.session.get('branch_code')
        app_user_id = self.request.session.get('app_user_id')
        queryset = Purchase_Order_Dtl_Temp.objects.filter(
            app_user_id=app_user_id).order_by('product_id')
        return queryset


##########
class BranchTransferApiView(generics.ListAPIView):
    serializer_class = Branch_transferSerializer

    def get_queryset(self):
        app_user_id = self.request.session.get('app_user_id')
        product_name = self.request.query_params.get('product_name', None)

        queryset = Stock_quantity_transfer.objects.filter().order_by('product_name')

        
        if product_name:
            queryset = queryset.filter(product_name=product_name)

        return queryset

####### quotion ###########
class sales_quotation_apiview(generics.ListAPIView):
    serializer_class = Quotation_Details_Serializer

    def get_queryset(self):
        queryset = Quotation_Details.objects.filter().order_by('-app_user_id')

        return queryset