from django.db import models

# Create your models here.

STATUS_LIST = (
    ('A', 'Active'),
    ('I', 'Inactive')
)

BLOOD_GROUP =( 
    ('', '---------'),
    ('A+', 'A+'),
    ('B+', 'B+'),
    ('O+', 'O+'),
    ('AB+', 'AB+'),
    ('A-', 'A-'),
    ('O-', 'O-'),
    ('B-', 'B-'),
    ('AB-', 'AB-')
)

GENDER_LIST = (
    ('', '---------'),
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Others')
)

RELIGION_LIST  = (
    ('', '---------'),
    ('I', 'Islam'),
    ('H', 'Hinduism'),
    ('B', 'Buddhists'),
    ('C', 'Christians'),
    ('A', 'Animists')
)

MARITAL_STATUS = (
    ('', '---------'),
    ('M', 'Married'),
    ('S', 'Single'),
    ('D', 'Divorced'),
    ('O', 'Others')
)

CASH_RECEIVE_PAYMENT =  (
    ('', '---------'), 
    ('C', 'C-Receive'), 
    ('D', 'D-Payment'),
)

TRAN_DEBIT_CREDIT  = (
    ('', '---------'), 
    ('D', 'D-Debit'), 
    ('C', 'C-Credit'),
)

FIXED_PERCENT = (
    ('P', 'P-Percentage'), 
    ('F', 'F-Fixed Amount'),
    ('N', 'N-Not Applicable'),
)

DAY_MONTH_YEAR = (
    ('', '---------'), 
    ('D', 'D-Daily'),
    ('W', 'W-Weekly'),
    ('M', 'M-Monthly'),
    ('Q', 'Q-Quarterly'),
    ('H', 'H-Half Yearly'),
    ('Y', 'Y-Yearly'),
    ('N', 'N-Not Applicable'),
)

DOCUMENT_TYPES = (
    ('', '---------'), 
    ('P', 'Photo'),
    ('S', 'Signature Card'),
)

EDU_LIST = (
    ('', '---------'),
    ('PSC', 'PSC'),
    ('JSC', 'JSC'),
    ('SSC', 'SSC'),
    ('HSC', 'HSC'),
    ('Honors', 'Honors'),
    ('Masters', 'Masters'),
    ('NA', 'Not Applicable')
)

WEEK_DAY_LIST = (
    ('', '---------'),
    ('0', 'Sunday'),
    ('1', 'Monday'),
    ('2', 'Tuesday'),
    ('3', 'Wednesday'),
    ('4', 'Thursday'),
    ('5', 'Friday'),
    ('6', 'Saturday')
)

GENDER_LIST = (
    ('', '---------'),
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Others')
)

class Loc_Country(models.Model):
    country_id =models.CharField(max_length=20,  blank=True, primary_key=True)
    country_name = models.CharField(max_length=200, null=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.country_name
    
class Loc_Division(models.Model):
    division_id = models.CharField(max_length=20,  blank=True, primary_key=True)
    division_name = models.CharField(max_length=200, null=False)
    country_id = models.ForeignKey(Loc_Country, on_delete=models.PROTECT, blank=True, null=True, related_name='div_country_id',db_column='country_id')
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.division_name

class Loc_District(models.Model):
    district_id =models.CharField(max_length=20,  blank=True, primary_key=True)
    district_name = models.CharField(max_length=200, null=False)
    division_id = models.ForeignKey(Loc_Division, on_delete=models.PROTECT, blank=True, null=True, related_name='dis_division_id',db_column='division_id')
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.district_name

class Loc_Upazila(models.Model):
    upozila_id =models.CharField(max_length=20, blank=True, primary_key=True)
    upozila_name = models.CharField(max_length=200, null=False)
    district_id = models.ForeignKey(Loc_District, on_delete=models.PROTECT, blank=True, null=True, related_name='lup_district_id',db_column='district_id')
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.upozila_name

class Loc_Union(models.Model):
    union_id =models.CharField(max_length=20, blank=True, primary_key=True)
    union_name = models.CharField(max_length=200, null=False)
    upozila_id = models.ForeignKey(Loc_Upazila, on_delete=models.PROTECT,related_name='uni_upozila_id',db_column='upozila_id', blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.union_name

class Loc_Region(models.Model):
    region_id =models.CharField(max_length=20, blank=True, primary_key=True)
    region_name = models.CharField(max_length=200, null=False)
    union_id = models.ForeignKey(Loc_Union, on_delete=models.PROTECT,related_name='reg_union_id',db_column='union_id', blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.region_name

class Branch(models.Model):
    branch_code = models.IntegerField(blank=True, primary_key=True)
    branch_name = models.CharField(max_length=200)
    manager_id = models.CharField(max_length=20, blank=True, null=True)
    opening_date = models.DateField(null=True,blank=True)
    closing_date = models.DateField(null=True,blank=True)
    country_id = models.ForeignKey(Loc_Country, on_delete=models.PROTECT,related_name='brn_country_id',db_column='country_id', blank=True, null=True)
    division_id = models.ForeignKey(Loc_Division, on_delete=models.PROTECT,related_name='brn_division_id',db_column='division_id', blank=True, null=True)
    district_id = models.ForeignKey(Loc_District, on_delete=models.PROTECT,related_name='brn_district_id',db_column='district_id', blank=True, null=True)
    upozila_id = models.ForeignKey(Loc_Upazila, on_delete=models.PROTECT,related_name='brn_upozila_id',db_column='upozila_id', blank=True, null=True)
    union_id = models.ForeignKey(Loc_Union, on_delete=models.PROTECT,related_name='brn_union_id',db_column='union_id', blank=True, null=True)
    branch_address = models.CharField(max_length=500)
    manager_phone = models.CharField(max_length=200)
    current_business_day = models.DateField(null=True)
    previous_business_day = models.DateField(null=True)
    business_clossing_in_progress = models.BooleanField(blank=True, default=False)
    business_day_close_by = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=2,null=True, choices=STATUS_LIST, default='A')
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.branch_code) + "-"+self.branch_name

class Global_Parameters(models.Model):
    company_code = models.CharField(null=True,blank=True,max_length=20)
    company_name = models.CharField(null=True,blank=True,max_length=200)
    company_address = models.CharField(null=True,blank=True,max_length=200)
    head_office_code = models.IntegerField(null=True)
    application_title = models.CharField(null=True,blank=True,max_length=200)
    cash_gl_code = models.CharField(max_length=13, null=True)
    current_business_day = models.DateField(null=True)
    previous_business_day = models.DateField(null=True)
    business_clossing_in_progress = models.BooleanField(blank=True, default=False)
    business_day_close_by =  models.IntegerField(null=True, blank=True) 
    is_friday_holiday = models.BooleanField(blank=True, default=False,null=True)
    is_saturday_holiday = models.BooleanField(blank=True, default=False,null=True)
    is_sunday_holiday = models.BooleanField(blank=True, default=False,null=True)
    is_monday_holiday = models.BooleanField(blank=True, default=False,null=True)
    is_tuesday_holiday = models.BooleanField(blank=True, default=False,null=True)
    is_wednesday_holiday = models.BooleanField(blank=True, default=False,null=True)
    is_thursday_holiday = models.BooleanField(blank=True, default=False,null=True)

    def __str__(self):
        return self.company_name

class Employees(models.Model):
    employee_id  = models.CharField(max_length=20, primary_key=True, blank=True)
    employee_name = models.CharField(max_length=100)
    branch_code = models.ForeignKey(Branch, on_delete=models.PROTECT,related_name='emp_branch_code',db_column='branch_code', blank=True, null=True)
    employee_sex = models.CharField(max_length=20,choices=GENDER_LIST, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    mother_name = models.CharField(max_length=200, null=True, blank=True)
    joining_date  = models.DateField(null=True, blank=True)
    present_address = models.CharField(max_length=300, null=True, blank=True)
    permanent_address = models.CharField(max_length=300, null=True, blank=True)
    birth_date  = models.DateField(null=True, blank=True)
    nid_number = models.CharField(max_length=20, null=True, blank=True)
    employee_religion = models.CharField(max_length=20,choices=RELIGION_LIST, null=True, blank=True)
    blood_group = models.CharField(max_length=4, default='',choices=BLOOD_GROUP, null=True, blank=True)
    employee_education= models.CharField(max_length=20,choices=EDU_LIST, null=True, blank=True)
    marital_status = models.CharField(max_length=2, choices=MARITAL_STATUS, null=True, blank=True)
    mobile_num= models.CharField(max_length=20)
    alternate_phone= models.CharField(max_length=200, null=True, blank=True)
    desig_id = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(blank=True,default=True)
    is_deleted = models.BooleanField(blank=True,default=False)
    account_number = models.CharField(max_length=13, null=True, blank=True)
    basic_salary=models.DecimalField(max_digits=22,decimal_places=2,default=0.00, blank=True)
    house_rent=models.IntegerField(blank=True,null=True)
    travel_allowance=models.IntegerField(blank=True,null=True)
    attent_allowance=models.IntegerField(blank=True,null=True)
    pf_cutting=models.IntegerField(blank=True,null=True)
    department_id=models.CharField(max_length=20,null=True,blank=True)
    welfare_cutting=models.IntegerField(blank=True,null=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.employee_id)+"-"+str(self.employee_name)

class User_Settings(models.Model):
    employee_id = models.ForeignKey(Employees, on_delete=models.PROTECT,related_name='usr_employee_id',db_column='employee_id', blank=True, null=True)
    app_user_id = models.CharField(max_length=20, primary_key=True)
    branch_code = models.IntegerField(blank=True, null= False)
    django_user_id = models.IntegerField(blank=True, null= True)
    employee_name = models.CharField(max_length=200, null=True, blank=True)
    reset_user_password = models.BooleanField(default=True, null=True,blank=True)
    lock_user = models.BooleanField(default=False, null=True,blank=True)
    password_expire_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(blank=True,default=True)
    is_deleted = models.BooleanField(blank=True,default=False)
    account_number = models.CharField(max_length=13,blank=True, null=True)
    general_account = models.CharField(max_length=13,blank=True, null=True)
    cash_gl_code = models.CharField(max_length=13, blank=True, null=True)
    head_office_admin = models.BooleanField(blank=True,default=False)
    daily_debit_limit = models.DecimalField(max_digits=22,decimal_places=2,default=0.00)
    daily_credit_limit = models.DecimalField(max_digits=22,decimal_places=2,default=0.00)
    def __str__(self):
        return self.employee_name

class Application_Log(models.Model):
    program_name = models.CharField(null=True,blank=True,max_length=200)
    account_number  = models.CharField(null=True,blank=True,max_length=20)
    error_message =  models.CharField(null=True,blank=True,max_length=500)
    error_time = models.DateTimeField(auto_now_add=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.program_name+' '+ self.error_time

class Eodsod_Process(models.Model):
    branch_code = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, db_column='branch_code', related_name='epr_branch_code') 
    process_name = models.CharField(max_length=200, null=True)
    function_name = models.CharField(max_length=200, null=True)
    process_status = models.CharField(max_length=1, null=True)
    process_date = models.DateField(null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)
    error_message =  models.CharField(max_length=500, null=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return +self.process_name+" >> "+str(self.process_date)+" >> "+str(self.app_data_time)

class Eodsod_Process_List(models.Model):
    process_name = models.CharField(max_length=200, null=True)
    function_name = models.CharField(max_length=200, null=True)
    serial_number =  models.IntegerField(null=True, blank=True)
    is_enable = models.BooleanField(default=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.serial_number) +' >> '+self.process_name + ' >>  ' + self.function_name

class Inventory_Number(models.Model):
    inv_code = models.IntegerField()
    branch_code = models.IntegerField()
    inv_prefix = models.CharField(max_length=3)
    inv_length = models.IntegerField(null=True, default=1)
    last_used_number = models.IntegerField()
    inv_naration = models.CharField(max_length=200)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.inv_naration

class Report_Configuration(models.Model):
    server_name = models.CharField(max_length=200, null=False)
    server_ip = models.CharField(max_length=200, null=False)
    report_url = models.CharField(max_length=200, null=False)
    company_file_path = models.CharField(max_length=200, null=False)
    company_info_report = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.report_url

class Report_Parameter(models.Model):
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    report_name =  models.CharField(max_length=100, null=False)
    parameter_name = models.CharField(max_length=100, null=False)
    parameter_values = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.app_user_id+ ' >> '+ self.report_name+ ' >> '+ self.parameter_name+ ' >> '+ self.parameter_values

class Report_Parameter_Mapping(models.Model):
    report_name =  models.CharField(max_length=100, null=False)
    parameter_name = models.CharField(max_length=100, null=False)
    parameter_values = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.report_name+ ' >> '+ self.parameter_name+ ' >> '+ self.parameter_values

class Report_Table_Tabular(models.Model):
    report_column1 = models.CharField(null=True,blank=True,max_length=500)
    report_column2 = models.CharField(null=True,blank=True,max_length=500)
    report_column3 = models.CharField(null=True,blank=True,max_length=500)
    report_column4 = models.CharField(null=True,blank=True,max_length=500)
    report_column5 = models.CharField(null=True,blank=True,max_length=500)
    report_column6 = models.CharField(null=True,blank=True,max_length=500)
    report_column7 = models.CharField(null=True,blank=True,max_length=500)
    report_column8 = models.CharField(null=True,blank=True,max_length=500)
    report_column9 = models.CharField(null=True,blank=True,max_length=500)
    report_column10 = models.CharField(null=True,blank=True,max_length=500)
    report_column11 = models.CharField(null=True,blank=True,max_length=500)
    report_column12 = models.CharField(null=True,blank=True,max_length=500)
    report_column13 = models.CharField(null=True,blank=True,max_length=500)
    report_column14 = models.CharField(null=True,blank=True,max_length=500)
    report_column15 = models.CharField(null=True,blank=True,max_length=500)
    report_column16 = models.CharField(null=True,blank=True,max_length=500)
    report_column17 = models.CharField(null=True,blank=True,max_length=500)
    report_column18 = models.CharField(null=True,blank=True,max_length=500)
    report_column19 = models.CharField(null=True,blank=True,max_length=500)
    report_column20 = models.CharField(null=True,blank=True,max_length=500)
    report_column21 = models.CharField(null=True,blank=True,max_length=500)
    report_column22 = models.CharField(null=True,blank=True,max_length=500)
    report_column23 = models.CharField(null=True,blank=True,max_length=500)
    report_column24 = models.CharField(null=True,blank=True,max_length=500)
    report_column25 = models.CharField(null=True,blank=True,max_length=500)
    report_column26 = models.CharField(null=True,blank=True,max_length=500)
    report_column27 = models.CharField(null=True,blank=True,max_length=500)
    report_column28 = models.CharField(null=True,blank=True,max_length=500)
    report_column29 = models.CharField(null=True,blank=True,max_length=500)
    report_column30 = models.CharField(null=True,blank=True,max_length=500)
    report_column31 = models.CharField(null=True,blank=True,max_length=500)
    report_column32 = models.CharField(null=True,blank=True,max_length=500)
    report_column33 = models.CharField(null=True,blank=True,max_length=500)
    report_column34 = models.CharField(null=True,blank=True,max_length=500)
    report_column35 = models.CharField(null=True,blank=True,max_length=500)
    report_column36 = models.CharField(null=True,blank=True,max_length=500)
    report_column37 = models.CharField(null=True,blank=True,max_length=500)
    report_column38 = models.CharField(null=True,blank=True,max_length=500)
    report_column39 = models.CharField(null=True,blank=True,max_length=500)
    report_column40 = models.CharField(null=True,blank=True,max_length=500)
    report_column41 = models.CharField(null=True,blank=True,max_length=500)
    report_column42 = models.CharField(null=True,blank=True,max_length=500)
    report_column43 = models.CharField(null=True,blank=True,max_length=500)
    report_column44 = models.CharField(null=True,blank=True,max_length=500)
    report_column45 = models.CharField(null=True,blank=True,max_length=500)
    report_column46 = models.CharField(null=True,blank=True,max_length=500)
    report_column47 = models.CharField(null=True,blank=True,max_length=500)
    report_column48 = models.CharField(null=True,blank=True,max_length=500)
    report_column49 = models.CharField(null=True,blank=True,max_length=500)
    report_column50 = models.CharField(null=True,blank=True,max_length=500)
    report_column51 = models.CharField(null=True,blank=True,max_length=500)
    report_column52 = models.CharField(null=True,blank=True,max_length=500)
    report_column53 = models.CharField(null=True,blank=True,max_length=500)
    report_column54 = models.CharField(null=True,blank=True,max_length=500)
    report_column55 = models.CharField(null=True,blank=True,max_length=500)
    report_column56 = models.CharField(null=True,blank=True,max_length=500)
    report_column57 = models.CharField(null=True,blank=True,max_length=500)
    report_column58 = models.CharField(null=True,blank=True,max_length=500)
    report_column59 = models.CharField(null=True,blank=True,max_length=500)
    report_column60 = models.CharField(null=True,blank=True,max_length=500)
    #report_json1 = models.JSONField(null=True)
    #report_json2 = models.JSONField(null=True)
    #report_json3 = models.JSONField(null=True)
    #report_json4 = models.JSONField(null=True)
    #report_json5 = models.JSONField(null=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True, null=True)

class Query_Table(models.Model):
    int_column1 = models.IntegerField(null=True,blank=True)
    int_column2 = models.IntegerField(null=True,blank=True)
    int_column3 = models.IntegerField(null=True,blank=True)
    int_column4 = models.IntegerField(null=True,blank=True)
    int_column5 = models.IntegerField(null=True,blank=True)
    int_column6 = models.IntegerField(null=True,blank=True)
    int_column7 = models.IntegerField(null=True,blank=True)
    int_column8 = models.IntegerField(null=True,blank=True)
    int_column9 = models.IntegerField(null=True,blank=True)
    int_column10 = models.IntegerField(null=True,blank=True)
    chr_column1 = models.CharField(null=True,blank=True,max_length=200)
    chr_column2 = models.CharField(null=True,blank=True,max_length=200)
    chr_column3 = models.CharField(null=True,blank=True,max_length=200)
    chr_column4 = models.CharField(null=True,blank=True,max_length=200)
    chr_column5 = models.CharField(null=True,blank=True,max_length=200)
    chr_column6 = models.CharField(null=True,blank=True,max_length=200)
    chr_column7 = models.CharField(null=True,blank=True,max_length=200)
    chr_column8 = models.CharField(null=True,blank=True,max_length=200)
    chr_column9 = models.CharField(null=True,blank=True,max_length=200)
    chr_column10 = models.CharField(null=True,blank=True,max_length=200)
    dec_column1 = models.DecimalField(null=True,blank=True,max_digits=22, decimal_places=2, default=0.00)
    dec_column2 = models.DecimalField(null=True,blank=True,max_digits=22, decimal_places=2, default=0.00)
    dec_column3 = models.DecimalField(null=True,blank=True,max_digits=22, decimal_places=2, default=0.00)
    dec_column4 = models.DecimalField(null=True,blank=True,max_digits=22, decimal_places=2, default=0.00)
    dec_column5 = models.DecimalField(null=True,blank=True,max_digits=22, decimal_places=2, default=0.00)
    dec_column6 = models.DecimalField(null=True,blank=True,max_digits=22, decimal_places=2, default=0.00)
    dec_column7 = models.DecimalField(null=True,blank=True,max_digits=22, decimal_places=2, default=0.00)
    dec_column8 = models.DecimalField(null=True,blank=True,max_digits=22, decimal_places=2, default=0.00)
    dec_column9 = models.DecimalField(null=True,blank=True,max_digits=22, decimal_places=2, default=0.00)
    dec_column10 = models.DecimalField(null=True,blank=True,max_digits=22, decimal_places=2, default=0.00)
    dat_column1 = models.DateField(null=True,blank=True)
    dat_column2 = models.DateField(null=True,blank=True)
    dat_column3 = models.DateField(null=True,blank=True)
    dat_column4 = models.DateField(null=True,blank=True)
    dat_column5 = models.DateField(null=True,blank=True)
    bool_column1 = models.BooleanField(blank=True, default=False,null=True)
    bool_column2 = models.BooleanField(blank=True, default=False,null=True)
    bool_column3 = models.BooleanField(blank=True, default=False,null=True)
    bool_column4 = models.BooleanField(blank=True, default=False,null=True)
    bool_column5 = models.BooleanField(blank=True, default=False,null=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)

class Report_Table_Group(models.Model):
    report_column1 = models.CharField(null=True,blank=True,max_length=500)
    report_column2 = models.CharField(null=True,blank=True,max_length=500)
    report_column3 = models.CharField(null=True,blank=True,max_length=500)
    report_column4 = models.CharField(null=True,blank=True,max_length=500)
    report_column5 = models.CharField(null=True,blank=True,max_length=500)
    report_column6 = models.CharField(null=True,blank=True,max_length=500)
    report_column7 = models.CharField(null=True,blank=True,max_length=500)
    report_column8 = models.CharField(null=True,blank=True,max_length=500)
    report_column9 = models.CharField(null=True,blank=True,max_length=500)
    report_column10 = models.CharField(null=True,blank=True,max_length=500)
    report_column11 = models.CharField(null=True,blank=True,max_length=500)
    report_column12 = models.CharField(null=True,blank=True,max_length=500)
    report_column13 = models.CharField(null=True,blank=True,max_length=500)
    report_column14 = models.CharField(null=True,blank=True,max_length=500)
    report_column15 = models.CharField(null=True,blank=True,max_length=500)
    report_column16 = models.CharField(null=True,blank=True,max_length=500)
    report_column17 = models.CharField(null=True,blank=True,max_length=500)
    report_column18 = models.CharField(null=True,blank=True,max_length=500)
    report_column19 = models.CharField(null=True,blank=True,max_length=500)
    report_column20 = models.CharField(null=True,blank=True,max_length=500)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True, null=True)

class Holiday_List(models.Model):
    holiday_date = models.DateField(blank=True)
    holiday_description = models.CharField(max_length=200, null=False)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

class Dashboard_Matrix(models.Model):
    matrix_key =  models.CharField(max_length=100, null=False)
    matrix_value = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.matrix_key+ ' >> '+ self.matrix_key
