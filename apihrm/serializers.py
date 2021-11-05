from django.db.models import fields
from rest_framework import serializers
import datetime

from hrm import models

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department_Info
        fields = ('__all__')


class DesigntaionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee_Designation
        fields = ('__all__')

class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company_Information
        fields = ('__all__')


class OfficeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company_Office
        fields = ('__all__')


class ShiftInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shift_Info
        fields = ('__all__')


class EmployeeDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Education_Degree
        fields=('__all__')


class EmployeeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Employment_Type
        fields=('__all__')

class salaryScaleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Salary_Scale
        fields=('__all__')

class salaryScaleDetailsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Salary_Scale_Details
        fields=('__all__')


class salaryBonusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Salary_Scale_Bonous
        fields=('__all__')

class ExtraAlownceSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Extra_Allowance
        fields=('__all__')




class BankTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Bank_Info
        fields=('__all__')




class EmpInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Employee_Details
        fields=('__all__')



class EmpExperianceSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Employee_Experience
        fields=('__all__')



class EmpNomineeSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Employee_Nominee
        fields=('__all__')

class EmpDocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Employee_Document_Type
        fields=('__all__')

class EmpDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Employee_Document
        fields=('__all__')

class EmpLeaveInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Leave_Info
        fields=('__all__')


class EmpLeaveApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Leave_Application
        fields=('__all__')

class EmpTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Employee_Training
        fields=('__all__')

class PayBillSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Pay_Bill
        fields=('__all__')

class AdvanceSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Advance_Salary
        fields=('__all__')


class AllowancePaySerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Allowance_Payment
        fields=('__all__')

class DeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Others_Deduction
        fields=('__all__')


######################
class Holiday_TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Holyday_Type
        fields=('__all__')

class Holiday_InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Holyday_Info
        fields=('__all__')

class Employee_HolydaySerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Employee_Holyday
        fields=('__all__')
