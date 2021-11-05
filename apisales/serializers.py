from rest_framework import serializers
import datetime

from sales.models import *
from sales.ecom_models import *
from delar.models import *

class User_Chart_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User_Chart
        fields = ('__all__')

class Ecom_Order_Master_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Ecom_Order_Master
        fields = ('__all__')


class StockMasterAuthQSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMasterAuthQ
        fields = ('__all__')


###############
class PurchaseMasterAuthQSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseMasterAuthQ
        fields = ('__all__')

class StockDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockDetails
        fields = ('__all__')

class StockMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMaster
        fields = ('__all__')

class SalesDetailsTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales_Details_Temp
        fields = ('__all__')

class SalesInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales_Master
        fields = ('__all__')

class SalesInvoiceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales_Details
        fields = ('__all__')

class SalesClientsSerializer(serializers.ModelSerializer):
    client_center = serializers.SerializerMethodField('get_center_name')
    class Meta:
        model = Clients
        fields = ('__all__')

    def get_center_name(self, obj):
        center = Center.objects.get(center_code=obj.center_code)
        return center.branch_center_code+"-"+center.center_name

class ProductPriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Price_List
        fields = ('__all__')

class ProductOfferListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Offer_List
        fields = ('__all__')

class ClientSecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delar_Security_Info
        fields = ('__all__')

class ProductOfferPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Offer_Package
        fields = ('__all__')

class SalesOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Master
        fields = ('__all__')

class SalesOrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Details
        fields = ('__all__')


class StockDetailsTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockDetailsTemp
        fields = ('__all__')

class SalesSupplier(serializers.ModelSerializer):
    class Meta:
        model = Supplier_Information
        fields = ('__all__')

class SearchProductListSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_product_id')
    text = serializers.SerializerMethodField('get_product_search_text')
    class Meta:
        model = products
        fields =  ['id', 'text']

    def get_product_id(self, obj):
        return obj.product_id

    def get_product_search_text(self, obj):
        return obj.product_search_text

class SearchClients(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_client_number')
    text = serializers.SerializerMethodField('get_client_details')
    class Meta:
        model = Clients
        fields =  ['id', 'text']

    def get_client_number(self, obj):
        return obj.client_id

    def get_client_details(self, obj):
        return obj.client_name

class st_group_model_serializers(serializers.ModelSerializer):
    class Meta:
        model = Products_Group
        fields = ('__all__')

class product_brand_model_serializers(serializers.ModelSerializer):
    class Meta:
        model = Products_Brand
        fields = ('__all__')

class product_unit_model_serializers(serializers.ModelSerializer):
    class Meta:
        model = Products_Unit
        fields = ('__all__')

class ProductsSerializer(serializers.ModelSerializer):
    brand_id=product_brand_model_serializers()
    product_group=st_group_model_serializers()
    class Meta:
        model = products
        fields = ('__all__')


class emisetup_model_serializers(serializers.ModelSerializer): 
    class Meta:
        model = Emi_Setup
        fields = ('__all__')   

class emircv_model_serializers(serializers.ModelSerializer):   
    class Meta:
        model = Emi_Receive
        fields = ('__all__')

class Emi_History_Model_Serializers(serializers.ModelSerializer):   
    class Meta:
        model = Emi_History
        fields = ('__all__')  

class showroom_model_serializers(serializers.ModelSerializer): 
    class Meta: 
        model = ShowRoom
        fields = ('__all__')

class Client_Profit_HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Client_Profit_History
        fields = ('__all__')

#############
class PurchaseDetailsTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase_Order_Dtl_Temp
        fields = ('__all__')


class Branch_transferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock_quantity_transfer
        fields = ('__all__')

class Quotation_Details_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation_Details
        fields = ('__all__')