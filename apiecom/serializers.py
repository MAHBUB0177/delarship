from rest_framework import serializers
import datetime

from ecom.models import *

class User_Chart_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User_Chart
        fields = ('__all__')

class Ecom_Slider_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Ecom_Slider
        fields = ('__all__')

class Ecom_Order_Master_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Ecom_Order_Master
        fields = ('__all__')

class Ecom_Product_category_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Ecom_Product_Categories
        fields = ('__all__')

class Ecom_Product_Subcategory_Serializer(serializers.ModelSerializer):
    categories_id=Ecom_Product_category_Serializer()
    class Meta:
        model = Ecom_Product_Sub_Categories
        fields = ('__all__')