from rest_framework import serializers
import datetime

from delar.models import *
from appauth.models import Query_Table


class Center_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = ('__all__')


class DelarSalesDetailsTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = Srstage_Details_Temp
        fields = ('__all__')


class DelarSalesInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Srstage_Master
        fields = ('__all__')

#############


class DelarSalesreturnpacketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales_Return_Packet
        fields = ('__all__')
###########


class Delar_sr_targetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SR_Target_Details_Temp
        fields = ('__all__')
