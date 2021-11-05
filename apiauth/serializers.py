from rest_framework import serializers
import datetime

from appauth.models import *

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('__all__')

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Loc_Country
        fields = ('__all__')

class Employee_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ('__all__')

class User_Settings_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User_Settings
        fields = ('__all__')