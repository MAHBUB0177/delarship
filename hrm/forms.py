from django import forms
from crispy_forms.layout import Field
from django.forms import ModelForm, TextInput, Select, Textarea, IntegerField, ChoiceField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.widgets import HiddenInput
from django import forms
from django.db.models import fields
from django.forms.models import ModelForm
from django.http import request
from .models import *
from django.utils.translation import ugettext_lazy as _

from hrm.models import *

class DateInput(forms.DateInput):
    input_type = 'date'


class ChoiceFieldNoValidation(ChoiceField):
    def validate(self, value):
        pass

class CommonReportForm(forms.Form):
    #shift_id = ChoiceFieldNoValidation(label='Select Shift', choices=FNGOODS_SHIFT, initial=".....")
    employee_id = ChoiceFieldNoValidation(label='Select Employee', choices=[('', 'Select Employee')], required=False, initial="")
    desig_id = ChoiceFieldNoValidation(label='Select Designation', choices=[('', 'Select Designation')], required=False, initial="")
    month = ChoiceFieldNoValidation(label='Select Month', required=False,choices=MONTH_LIST, initial="")
    year = forms.CharField(label="Year", widget=forms.TextInput(
    ),required=True)
    month_year = ChoiceFieldNoValidation(label=' Month', choices=[('', 'Select Month')], required=False, initial="")
    branch_code = ChoiceFieldNoValidation(label='Branch Name', choices=[('', 'Branch Name')], initial="")
    
    dept_id = ChoiceFieldNoValidation(label='Select Department', choices=[('', 'Select Department')], required=False, initial="")
    from_date = forms.DateField(label="From Date",widget=DateInput(attrs={'id': 'p_from_date'}), required=False)
    upto_date = forms.DateField(label="Upto Date",widget=DateInput(attrs={'id': 'p_upto_date'}), required=False)
    ason_date = forms.DateField(label="Report Date",widget=DateInput(attrs={'id': 'p_ason_date'}), required=False)
    user_name = forms.CharField(label="User Name", widget=forms.TextInput(
    attrs={ 'id': 'p_user_id'}
    ),required=False)


class CompanyInformationForm(forms.ModelForm):
    class Meta:
        model=Company_Information
        fields=('company_name','country_id','division_id','district_id','upozila_id','office_address')
        labels={
            'company_name':_('Company Name'),
            'country_id':_('Country Name'),
            'division_id':_('Division Name'),
            'district_id':_("District Name"),
            'upozila_id':_('Upozela Name'),
            'office_address':_('Office Address')
        }


class CompanyOfficeForm(forms.ModelForm):
    class Meta:
        model=Company_Office
        fields=('office_name','country_id','division_id','district_id','upozila_id','office_address')
        labels={
            'office_name':_('Office Name'),
            'country_id':_('Country Name'),
            'division_id':_('Division Name'),
            'district_id':_("District Name"),
            'upozila_id':_('Upozela Name'),
            'office_address':_('Office Address')
        }

class DepartmentInfoForm(forms.ModelForm):
    class Meta:
        model=Department_Info
        fields=('department_name','total_employee','department_location','department_incharge')
        labels={
            'department_name': _("Department Name"),
            "total_employee":_("Total Employee"),
            "department":_("Department"),
            "department_incharge":_("Depatment Incharge")
        }

class ShiftInfoForm(forms.ModelForm):
    class Meta:
        model=Shift_Info
        fields=('shift_name','office_id','total_work_minute','work_start_time_sec','work_end_time_sec','work_start_grace_time_sec','work_end_time_grace_sec','refresh_start_time_sec','refresh_end_time_sec','ot_time_start','ot_time_end','max_ot_hour','duty_gap_time','morning_ot_time')
        labels={
            "shift_name":'Shift Name',
            "office_id":"Office Name",
            "total_work_minute":_("Total Work Minute"),
            "work_start_time_sec":_("Work Start Time Sec"),
            'work_end_time_sec':_("Work End Time Sec"),
            'work_start_grace_time_sec':_("Work Start  Grace Time Sec"),
            'work_end_time_grace_sec':_("Work End Grace Time Sec"),
            'refresh_start_time_sec':_("Refresh Start Time Sec"),
            'refresh_end_time_sec':_('Refresh End Time Sec'),
            'ot_time_start':_('OT Start Time'),
            'ot_time_end':_('OT End Time'),
            'max_ot_hour':_('Maximum OT Hour'),
            'duty_gap_time':_('OT Gap Time'),
            'morning_ot_time':_('Morning OT Time'),

        }


class EducationDegreeForm(forms.ModelForm):
    class Meta:
        model=Education_Degree
        fields=('degree_name','degree_duration')
        labels={
            'degree_name':'Degree Name',
            'degree_duration':'Degree Duration'
        }

class EmployeeDesignationForm(forms.ModelForm):
    class Meta:
        model=Employee_Designation
        fields=['desig_name','attendance_bonus','attendance_bonus_amt','production_bonus','production_bonus_amt','ot_hour_allow','ot_hour_rate','stamp_ded_allow','stamp_ded_amount','sales_comission']
        labels={
            'desig_name':'Designation  Name',
            'attendance_bonus':'Attendance Bonus Allow',
            'attendance_bonus_amt':'Bonus Amount',
            'production_bonus':'Prod Bonus Allow',
            'production_bonus_amt':'Bonus Amount',
            'ot_hour_allow':'OT Allow',
            'ot_hour_rate':'OT Rate',
            'stamp_ded_allow':'Stamp Charge Allow',
            'stamp_ded_amount':'Charge Amount' ,
            'sales_comission':'Sales Comission',
 
        }



class EmplyeeTypeForm(forms.ModelForm):
    class Meta:
        model=Employment_Type
        fields=['emptype_name']
        labels={ 
            'emptype_name':'create Employee Type'
        }

class SalaryScaleForm(forms.ModelForm):
    class Meta:
        model=Salary_Scale
        fields=('salscale_name','total_salary','deduction_pct','total_deduction','comments')
        labels={
            'salscale_name':'salary scale of Employee',
            'total_salary':'Total salary',
            'deduction_pct':'deduction_pct',

            'total_deduction':'Total deduction',
            'comments':'comments'
        }

class SalaryScaleDetailsForm(forms.ModelForm):
    class Meta:
        model=Salary_Scale_Details
        fields=('salscale_id','salsdtlcale_name','salary_amount','deduction_pct','total_deduction','comments')
        labels={
            'salscale_id':'salscale_id',
            'salsdtlcale_name':'salsdtlcale_name',
            'salary_amount':'salary_amount',
            'deduction_pct':'deduction_pct',
            'total_deduction':'total_deduction',
            'comments':'comments'
        }


class SalaryBonusDetailsForm(forms.ModelForm):
    class Meta:
        model=Salary_Scale_Bonous
        fields=('salscale_id','salsdtlcale_id','bonus_name','bonus_pct','bonus_amount','comments')
        labels={
            'salscale_id':'salscale_id',
            'salsdtlcale_id':'salsdtlcale_id',
            'bonus_pct':'bonus_pct',
            'bonus_name':'bonus_name',
            'bonus_amount':'bonus_amount',
            'comments':'comments'
        }

class ExtraAllowanceDetailsForm(forms.ModelForm):
    class Meta:
        model=Extra_Allowance
        fields=('allowance_name','allowance_amount','comments')
        labels={
            'allowance_name':'allowance_name',
            'allowance_amount':'allowance_amount',
            'comments':'comments',
        }

class BankInfoDetailsForm(forms.ModelForm):
    class Meta:
        model=Bank_Info
        fields=('bank_name','bank_address','bank_phone','bank_email')
        labels={
            'bank_name':_('bank_name'),
            'bank_address':_('bank_address'),
            'bank_phone':_('bank_phone'),
            'bank_email':_('bank_email'),
        }
class DateInput(forms.DateInput):
   input_type = 'date'



class EmployeeDetailsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeDetailsForm, self).__init__(*args, **kwargs)
        # self.fields['contract_start_date'].widget = DatePickerInput()



    class Meta:
        model=Employee_Details
        fields=('employee_name','salary_gross','employee_father_name','employee_mother_name','employee_blood_group','employee_sex','employee_religion','employee_marital_status','employee_national_id','country_id','division_id','district_id','upozila_id','employee_present_address','employee_permanent_address','employee_phone_own','employee_phone_office','employee_phone_home','passport_no','driving_licence','employee_tin','email_personal','employee_joining_date','employee_date_of_birth','employee_status','eme_contact_name','eme_contact_relation','eme_contact_phone','eme_contact_address','office_id','emptype_id','salscale','designation_id','email_official','reporting_to','current_shift','office_location','card_number','salary_bank','salary_bank_ac','contract_start_date','contract_exp_date','last_inc_date','next_inc_date','service_end_date','last_transfer_date','next_transfer_date','job_confirm_date','pf_confirm_date','gf_confirm_date','wf_confirm_date','last_promotion_date','department_id')
        labels={
            'employee_name':_("Employee Name"),
            'employee_father_name':_("Father Name"),
            'employee_mother_name':_("Mother Name"),
            'employee_blood_group':_("Blood Group"),
            'employee_sex':_("Gender"),
            'employee_religion':_("Religion"),
            'employee_marital_status':_("Marital Status"),
            'employee_national_id':_("Nationality"),
            'country_id':_("Country"),
            'division_id':_("division"),
            'district_id':_("District"),
            'upozila_id':_("Upozila"),
            'employee_present_address':_("Present Address"),
            'employee_permanent_address':_("Permanent Address"),
            'employee_phone_own':_("Phone own")
            ,'employee_phone_office':_("Phone Office"),
            'employee_phone_home':_("Phone Home"),
            'passport_no':_("Passport No"),
            'driving_licence':_("Driving Licence"),
            'employee_tin':_("Tin No"),
            'email_personal':_("Email"),
            'employee_joining_date':_("Joining Date"),
            'employee_date_of_birth':_("Date of Birth"),
            'employee_status':_("Employee Status"),
            'eme_contact_name':_("Optional Contact Name"),
            'eme_contact_relation':_("Optional Contact relation"),
            'eme_contact_phone':_("Optional Contact Phone"),
            'eme_contact_address':_("Optional Contact Address"),
            'office_id':_("Office ID"),
            'emptype_id':_("Employee Type")
            ,'salscale':_("Salary Scale"),
            'salary_gross':_("Gross Salary"),
            'designation_id':_("Designation"),
            'email_official':_("Email Office official"),
            'reporting_to':_("Reporting To"),
            'current_shift':_("Current Shift"),
            'office_location':_("Office Location"),
            'card_number':_("Card Number"),
            'salary_bank':_("Salary Bank"),
            'salary_bank_ac':_("Salary Bank Account NO"),
            'contract_start_date':_('Contract Start Date'),
            'contract_exp_date':_('Contract Expire Date'),
            'last_inc_date':_("Last Incriment Date"),
            'next_inc_date':_("Next Incriment Date"),
            'service_end_date':_("Service End Date"),
            'last_transfer_date':_("Last Transfer Date"),
            'next_transfer_date':_("Next Transfer Date"),
            'job_confirm_date':_("Job Confirm Date"),
            'pf_confirm_date':_("P.f. Confirm Date"),
            'gf_confirm_date':_("G.f. Confirm Date"),
            'wf_confirm_date':_("W.f. Confirm Date"),
            'last_promotion_date':_("Last Promotion Date"),
            'department_id':_("Department Id")
        }

        widgets = {'employee_date_of_birth': DateInput(),
                    'service_end_date': DateInput(),
                   'contract_start_date': DateInput() ,
                   'contract_exp_date': DateInput(),
                   'next_inc_date': DateInput(),
                   'job_confirm_date': DateInput(),
                    'pf_confirm_date': DateInput(),
                    'gf_confirm_date': DateInput(),
                    'wf_confirm_date': DateInput(),
                    'last_promotion_date': DateInput(),
                    'last_inc_date': DateInput(),
                    'last_transfer_date': DateInput(),
                    'next_transfer_date': DateInput(),
                   }


        




class EmployeeExperinceInfoForm(forms.ModelForm):
    class Meta:
        model=Employee_Experience
        fields={
        'employee_id',
        'serial_no','company_name','company_address','company_type','position','department','responsibility','achievement','phone_number','email','contact_person','emp_id','start_date','end_date'
        }
        labels={
        'serial_no':_('Serial No'),
        'company_name':_('Comapany Name'),
        'company_address':_('Company Address'),
        'company_type':_('Comapany Type'),
        'position':_('Position'),
        'department':_('Department'),
        'responsibility':_('Responsibility'),
        'achievement':_('Achivement'),
        'phone_number':_('Phone Number'),
        'email':_('Email'),
        'contact_person':_('Contact Person'),
        'emp_id':_('Employee Id'),
        'start_date':_('Start Date'),
        'end_date':_('End Date'),
        }
        widgets = {'start_date': DateInput(),
                    'end_date': DateInput()}

class EmployeeNomineeForm(forms.ModelForm):
    class Meta:
        model = Employee_Nominee
        fields = {
            'employee_id','nominee_serial','nominee_name','nominee_sex','nominee_father_name','nominee_mother_name','nominee_present_addr','nominee_permanent_addr','nominee_birth_date',
            'country_id','nominee_nid_num','nominee_religion','nominee_blood_group','nominee_mobile_num'
        }
        labels ={
            'employee_id':_('Employee')
            ,'nominee_serial':_('Nominee NO'),
            'nominee_name':_('Nominee Name'),
            'nominee_sex':_('Gander'),'nominee_father_name':_('Father Name'),'nominee_mother_name':_('Mother Name'),'nominee_present_addr':_('Present Address'),'nominee_permanent_addr':_('Permanent Address'),'nominee_birth_date':_('Birth Date'),
            'country_id':_('Country')
            ,'nominee_nid_num':_('NID'),
            'nominee_religion':_('Religion'),
            'nominee_blood_group':_('Blood Group'),
            'nominee_mobile_num':_('Mobile NO')
        }
        widgets = {'nominee_birth_date': DateInput(),
                    }


class EmployeeDocumentTypeForm(forms.ModelForm):
    class Meta:
        model =Employee_Document_Type
        fields={
            'document_type_name'
        }


class EmployeeDocumentForm(forms.ModelForm):
    class Meta:
        model=Employee_Document
        fields={
            'employee_id','document_type','document_location','file_no',
            'status'
        }
        labels={
            'employee_id':_('Employee'),
            'document_type':_('Document Type'),
            'document_location':_('Document'),
            'file_no':_('File No')
            ,'status':_('Status'),
        }



class LeaveInfoForm(forms.ModelForm):
    class Meta:
        model =Leave_Info
        fields ={
            'leave_name','prefix_name','leave_encasement','holiday_check'

        }
        labels ={
                        
                        'leave_name':_('Leave Name'),
                        'prefix_name':_('Prefix'),
                        'leave_encasement':_('Leave Encasement'),
                        'holiday_check':_('Holiday Check'),
        }
class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model=Leave_Application
        fields ={
            'leave_id','employee_id','application_date',
            'from_date','upto_date','join_date','approval_status','leave_reason','application_to','approve_by','approval_comments'
        }

        labels={
            'leave_id':_('Leave'),
            'employee_id':_('Employee'),
            'application_date':('Application Date'),
            'from_date':_('From Date'),
            'upto_date':_('Upto Date'),
            'join_date':_('Join Date'),
            'approval_status':_('Approval Status'),
            'leave_reason':_('Leave Reason'),
            'application_to':_('Application To'),
            'approve_by':_('Approve By'),
            'approval_comments':_('Approval Comments'),
        }
        widgets = {
            'from_date': DateInput(),
            'upto_date': DateInput(),
            'join_date': DateInput(),
            'application_date': DateInput(),
            
                    }
class EmployeeTrainingForm(forms.ModelForm):
    class Meta:
        model = Employee_Training
        fields ={'employee_id','schedule_id','institute_name','training_name','training_description','from_date','upto_date',}
        labels ={
            "employee_id":_('Employee'),
            'schedule_id':_('Schedule'),
            'institute_name':_('Institute Name'),
            'training_name':_('Training Name'),
            'training_description':_('Training Description'),
            'from_date':_('From Date'),
            'upto_date':_('Upto Date'),
        }
        widgets = {
            'from_date': DateInput(),
            'upto_date': DateInput(),
                    }
class PayBillForm(forms.ModelForm):
    class Meta:
        model=Pay_Bill
        fields={
            'bill_date','bill_comments','bill_doc_detail',
            'bill_amount','approval_amount','prepare_by','checked_by','approve_by','checked_status','approve_status','checked_date','approve_date','attached_file'
        }
        labels={
            'bill_date':_('Bill Date'),
            'bill_comments':_('Comments'),
            'bill_doc_detail':_('Document Detail'),
            'bill_amount':_('Amount'),
            'approval_amount':_('Approve Amount'),
            'prepare_by':_('Prepare By'),
            'checked_by':_('Check By'),
            'approve_by':_('Approve By'),
            'checked_status':_('Checked Status'),
            'approve_status':_('Approve Status'),
            'checked_date':_('Checked Date'),
            'approve_date':_("Approve Date"),
            'attached_file':_('Files')
        }
        widgets = {
            'bill_date': DateInput(),

            'checked_date': DateInput(),
            'approve_date': DateInput(),
                    }

class AdvanceSalary(forms.ModelForm):
    class Meta:
        model=Advance_Salary
        fields=('employee_id','amount','remarks','month_year')
        labels={
            'employee_id': _("Employee Name"),
            "amount":_("Amount"),
            "remarks":_("Remarks"),
            "month_year":_("Entry Date")
        }
        widgets = {
            'month_year': DateInput(),
                    }

class OthersDeduction(forms.ModelForm):
    class Meta:
        model=Others_Deduction
        fields=('employee_id','amount','remarks','month_year')
        labels={
            'employee_id': _("Employee Name"),
            "amount":_("Amount"),
            "remarks":_("Remarks"),
            "month_year":_("Entry Date")
        }
        widgets = {
            'month_year': DateInput(),
                    }

class AllowancePayment(forms.ModelForm): 
    class Meta:
        model=Allowance_Payment
        fields=('employee_id','amount','remarks','month_year','allowance_id')
        labels={
            'employee_id': _("Employee Name"),
            'allowance_id': _("Allowance Name"),
            "amount":_("Amount"),
            "remarks":_("Remarks"),
            "month_year":_("Entry Date")
        }
        widgets = {
            'month_year': DateInput(),
                    }

#############################################
class Salary_sheet_Model_Form(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    dept_id = ChoiceFieldNoValidation(required=False, label='Department Name', choices=[('', '------------')], initial="")
    # desig_name = ChoiceFieldNoValidation(required=False, label='Designation Name', choices=[('', 'select_designation')], initial="")
    month_year = ChoiceFieldNoValidation(required=True, label='Month Year', choices=[('', 'Select_Month')], initial="")


    class Meta:
        model = Salary_Sheet
        fields = ['branch_code','dept_id','month_year']

    
        


class Holyday_Type_Form(forms.ModelForm): 
    class Meta:
        model=Holyday_Type
        fields=['type_name']
        labels={
            'type_name': _("Type Name")
            
        }



class Holyday_Info_Form(forms.ModelForm): 
    class Meta:
        model=Holyday_Info
        fields=('fiscal_year','holiday_type_id','holiday_from_date','holiday_end_date','holiday_desc','month')
        labels={
            'fiscal_year': _("Fiscal Year"),
            'holiday_type_id': _("Holiday Type Id"),
            "month":_("Month"),
        }
        widgets = {
         
           
            'holiday_from_date':DateInput(),
            'holiday_end_date':DateInput(),
           
                    }  


class Employee_Holyday_Form(forms.ModelForm): 
    class Meta:
        model=Employee_Holyday
        fields=('employee_id','holiday_type_id','holiday_from_date','holiday_end_date',)
        labels={
            'fiscal_year': _("Fiscal Year"),
            'holiday_type_id': _("Holiday Type Id"),
            "month":_("Month"),
        }
        widgets = {
           
            'holiday_from_date':DateInput(),
            'holiday_end_date':DateInput(),
           
                    }  