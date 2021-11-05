# from django.shortcuts import render

# from django.http import HttpResponse


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

from logging import exception
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Context
from django.shortcuts import render
from django.views.generic.base import TemplateView
from appauth.views import get_global_data
from django.contrib.auth.models import User
from hrm.models import *

from .forms import *
from .utils import *
from django.http import JsonResponse, request
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.db import transaction
from .validations import *
from appauth.views import get_global_data

from finance.utils import fn_get_cash_gl_code, fn_transfer_tran_posting, fn_get_transaction_account_type

from finance.utils import fn_get_account_info_byactype

# Create your views here.

#----------------------------hrm-view-start------------------------------
#X-X-X-X-X-X-X-X-X-X-X-X------hrm-view-end-------X-X-X-X-X-X-X-X-X-X-X-X

# company info start
@method_decorator(login_required, name='dispatch')
class hrm_company_info_view(TemplateView):
    template_name="hrm/hrm-company-create.html"

    def get(self,request):
        form=CompanyInformationForm()
        context=get_global_data(request)
        context['form']=form
        context['title']='Company Information'
        return render(request,self.template_name,context)

@transaction.atomic
def hrm_company_info_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method == 'POST':
        form=CompanyInformationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post=form.save(commit=False)
                    company_id=fn_get_company_id()
                    data['company_id']=company_id
                    post.app_user_id=app_user_id
                    post.company_id=company_id
                    post.save()
                    data['form_is_valid']=True
                    data['success_message']="company creata successfully"
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

@transaction.atomic
def hrm_company_info_edit(request,id):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    instance_data=get_object_or_404(Company_Information,company_id=id)
    template_name='hrm/hrm-company-edit.html'
    data=dict()
    if request.method == "POST":
        form=CompanyInformationForm(request.POST,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj= form.save(commit=False)
                    obj.save()
                    data['success_message']="updated successfully!"
                    data['error_message']=''
                    data['form_is_valid']=True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid']=False
            data['error_message']=form.errors.as_json()
            return JsonResponse(data)

    else:
        form=CompanyInformationForm(instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['id']=id
        context['title']='Company information'
        data['html_form']=render_to_string(
            template_name,context,request=request
        )

    return JsonResponse(data)
# company info end



# office info start

@method_decorator(login_required, name='dispatch')
class hrm_office_info(TemplateView):
    template_name='hrm/hrm-offcie-create.html'

    def get(self,request):
        form=CompanyOfficeForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Office Information"
        return render(request,self.template_name,context)

@login_required
@transaction.atomic
def hrm_office_info_insert(request):
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method=="POST":
        form=CompanyOfficeForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post=form.save(commit=False)
                    office_id=fn_get_office_id()
                    post.app_user_id=app_user_id
                    post.office_id=office_id
                    post.save()
                    data['form_is_valid']=True
                    data['success_message']="office create successfully"
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

@login_required
@transaction.atomic
def hrm_office_info_edit(request,id):
    instance_data=get_object_or_404(Company_Office,office_id=id)
    template_name='hrm/hrm-office-edit.html'
    data=dict()
    if request.method=="POST":
        form=CompanyOfficeForm(request.POST,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    form_obj=form.save(commit=False)
                    form_obj.save()
                    data['success_message']="update Successfully"
                    data['error_message']=''
                    data['form_is_valid']=True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['form_is_valid']=False
            data['error_message']=form.errors.as_json()
            return JsonResponse(data)

    else:
        form=CompanyOfficeForm(instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['id']=id
        context['title']="Office Information"
        data['html_form']=render_to_string(
            template_name,context,request=request
        )
    return JsonResponse(data)
# office info end


# departmnet info start 
class Department_info_view(LoginRequiredMixin,TemplateView):
    template_name="hrm/hrm-department_info.html"

    def get(self,request):
        if not request.user.is_authenticated:
            return render(request,'appauth/appauth-login.html')
        form=DepartmentInfoForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Departments"
        return render(request,self.template_name,context)

@transaction.atomic
def department_info_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id'] 
    if request.method == 'POST':
        form=DepartmentInfoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post=form.save(commit=False)
                    department_id=fn_get_departmnet_id()
                    post.app_user_id=app_user_id
                    post.department_id=department_id
                    post.save()
                    data['form_is_valid']=True
                    data['department_id']=department_id
                    data['success_message']="Department added successfully"
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

def department_info_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
        
    instance_data = get_object_or_404(Department_Info, department_id=id)
    template_name = 'hrm/hrm-department-edit.html'
    data = dict()
    if request.method == 'POST':
        form = DepartmentInfoForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = DepartmentInfoForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['title']="Departments"

        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)
# departmnet info end

#hrm-office-Shift start
class hrm_office_shift_view(LoginRequiredMixin,TemplateView):
    template_name="hrm/hrm-shift-info.html"

    def get(self,request):
        form=ShiftInfoForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Office Shift"

        return render(request,self.template_name,context)


@transaction.atomic
def hrm_office_shift_info_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id'] 
    if request.method == 'POST':
        form=ShiftInfoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post=form.save(commit=False)
                    shift_id=fn_get_shift_id()
                    post.app_user_id=app_user_id
                    post.shift_id=shift_id
                    post.save()
                    data['form_is_valid']=True
                    data['shift_id']=shift_id
                    data['success_message']="shift added successfully"
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def hrm_office_shift_edit(request,id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data=get_object_or_404(Shift_Info,shift_id=id)
    template_name='hrm/hrm-shift-edit.html'
    data=dict()
    if request.method == 'POST':
        form =ShiftInfoForm(request.POST,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    form_obj=form.save(commit=False)
                    form_obj.save()
                    data['success_message']="update successfully"
                    data["error_message"]=''
                    data['form_is_valid']=True
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

    else:
        form=ShiftInfoForm(instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['id']=id
        context['title']="Office Shift"
        data["html_form"]=render_to_string(
            template_name,context,request=request
        )
    return JsonResponse(data)

#hrm-office-Shift end



# select 2 javascript remote serching
# plsql

#----------------------------hrm-Degree-start------------------------------
class hrm_employee_education_degree_view(LoginRequiredMixin,TemplateView):
    template_name='hrm/hrm-degree-info-view.html'
    def get(self,request):
        form=EducationDegreeForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Education Degree"

        return render(request,self.template_name,context)


@transaction.atomic
def hrm_employee_education_degree_info_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')

    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method=='POST':
        form=EducationDegreeForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form_obj=form.save(commit=False)
                    degree_id=fn_get_degree_id()
                    form_obj.app_user_id=app_user_id
                    form_obj.degree_id=degree_id
                    form_obj.save()
                    data['form_is_valid']=True
                    data['degree_id']=degree_id
                    data['success_message']="degree create successfully"
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)


@transaction.atomic
def hrm_employee_education_degree_edit(request,id):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    instance_data=get_object_or_404(Education_Degree,degree_id=id)
    template_name='hrm/hrm-degree-edit.html'
    data=dict()
    if request.method == "POST":
        form = EducationDegreeForm(request.POST,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    form_obj=form.save(commit=False)
                    form_obj.save()
                    data['success_message']="update successfully"
                    data['form_is_valid']=True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
    else:
        form=EducationDegreeForm(instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['id']=id
        context['title']="Education Degree"

        data["html_form"]=render_to_string(
            template_name,context,request=request
        )
    return JsonResponse(data)
#X-X-X-X-X-X-X-X-X-X-X-X-------hrm-Degree-end-------X-X-X-X-X-X-X-X-X-X-X-X


# -----------------Hrm - Designation start--------------------- 
class hrm_designation_create_view(TemplateView):
    template_name="hrm/hrm-designation-create.html"

    def get(self,request):
        if not request.user.is_authenticated:
            return render (request,'appauth/appauth-login.html')
        form=EmployeeDesignationForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Designation"

        return render(request,self.template_name,context)


@transaction.atomic
def hrm_designation_info_insert(request):
    if not request.user.is_authenticated:
        return render (request,'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method == 'POST':
        form = EmployeeDesignationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post=form.save(commit=False)
                    designation_id=fn_get_designation_id()
                    post.app_user_id=app_user_id
                    post.desig_id=designation_id
                    post.save()
                    data['form_is_valid']=True
                    data['success_message']="Designation create successfully"
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.errors.as_json()

    return JsonResponse(data)

@transaction.atomic
def hrm_designation_info_edit(request,id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html') 
    instance_data = get_object_or_404(Employee_Designation, desig_id=id)
    template_name = 'hrm/hrm-desigtion-edit.html'
    data = dict()
    if request.method == 'POST':
        form = EmployeeDesignationForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj = form.save(commit=False)
                    obj.save()
                    data['success_message'] = 'Updated Successfully!'
                    data['error_message'] = ''
                    data['form_is_valid'] = True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = EmployeeDesignationForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        context['title']="Designation"

        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

# -----------------Hrm - Designation end-------------------------


#----------------------------hrm-employee type-view-start------------------------------
class hrm_employee_type_info_view(LoginRequiredMixin,TemplateView):
    template_name="hrm/hrm-employee-type-create.html"
    def get(self,request):
        form=EmplyeeTypeForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Employee Type"

        return render(request,self.template_name,context)

@transaction.atomic
def hrm_employee_type_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method=='POST':
        form=EmplyeeTypeForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post=form.save(commit=False)
                    emptype_id=fn_get_employee_type_id()
                    data['emptype_id']=emptype_id
                    post.app_user_id=app_user_id
                    post.emptype_id=emptype_id
                    post.save()
                    data['form_is_valid']=True
                    data['success_message']="employee Type create successfuly"
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.error.as_json()
    return JsonResponse(data)

@transaction.atomic
def hrm_employee_type(request,id):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')

    instance_data=get_object_or_404(Employment_Type,emptype_id=id)
    template_name='hrm/hrm-employee-type-edit.html'
    data=dict()
    if request.method=='POST':
        form=EmplyeeTypeForm(request.POST,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    form_obj=form.save(commit=False)
                    form_obj.save()
                    data['success_message']="update successfully"
                    data['error_message']=''
                    data['form_is_valid']=True

                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                return JsonResponse(data)

        else:
            data['form_is_valid']=False
            data['error_message']=form.errors.as_json()
            return JsonResponse(data)
    else:
        form=EmplyeeTypeForm(instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['id']=id
        context['title']="Employee Type"

        data['html_form']=render_to_string(
            template_name,context,request=request
        )
    return JsonResponse(data)


#X-X-X-X-X-X-X-X-X-X-X-X------hrm-employee type - view-end-------X-X-X-X-X-X-X-X-X-X-X-X


#----------------------------hrm-salary scale type-view-start------------------------------
class hrm_employee_salary_scale_info_view(LoginRequiredMixin,TemplateView):
    template_name="hrm/hrm-salary-scale-type-create.html"
    def get(self,request):
        form=SalaryScaleForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Salary Scale Type"

        return render(request,self.template_name,context)

@transaction.atomic
def hrm_employee_salary_scale_info_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method=='POST':
        form=SalaryScaleForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post=form.save(commit=False)
                    salscale_id=fn_get_salscale_id()
                    data['id']=salscale_id
                    post.app_user_id=app_user_id
                    post.salscale_id=salscale_id
                    post.save()
                    data['form_is_valid']=True
                    data['success_message']="salary scale type create successfuly"
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.error.as_json()
    return JsonResponse(data)

@transaction.atomic
def hrm_employee_salary_scale_info_edit(request,id):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')

    instance_data=get_object_or_404(Salary_Scale,salscale_id=id)
    template_name='hrm/hrm-salary-scale-edit.html'
    data=dict()
    if request.method=='POST':
        form=SalaryScaleForm(request.POST,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    form_obj=form.save(commit=False)
                    form_obj.save()
                    data['success_message']="update successfully"
                    data['error_message']=''
                    data['form_is_valid']=True

                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                return JsonResponse(data)

        else:
            data['form_is_valid']=False
            data['error_message']=form.errors.as_json()
            return JsonResponse(data)
    else:
        form=SalaryScaleForm(instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['id']=id
        context['title']="Salary Scale Type"

        data['html_form']=render_to_string(
            template_name,context,request=request
        )
    return JsonResponse(data)


#X-X-X-X-X-X-X-X-X-X-X-X------hrm-salary scale type - view-end-------X-X-X-X-X-X-X-X-X-X-X-X


#----------------------------hrm-view-start------------------------------
class hrm_salary_Scale_details(LoginRequiredMixin,TemplateView):
    template_name="hrm/hrm-salary-scale-detail.html"
    def get(self,request):
        form=SalaryScaleDetailsForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Salary Scale"

        return render(request,self.template_name,context)
@transaction.atomic
def hrm_salary_Scale_details_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method=='POST':
        form=SalaryScaleDetailsForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post=form.save(commit=False)
                    salsdtlcale_id=fn_get_salsdtlcale_id()
                    data['id']=salsdtlcale_id
                    post.salsdtlcale_id=salsdtlcale_id
                    post.app_user_id=app_user_id
                    post.save()
                    data['form_is_valid']=True
                    data['success_message']="salary scale details add successfully"
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

@transaction.atomic
def hrm_salary_scale_details_edit(request,id):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    instance_data=get_object_or_404(Salary_Scale_Details,salsdtlcale_id=id)
    print(instance_data)
    template_name='hrm/hrm-salary-scale-details-edit.html'
    data=dict()
    if request.method == "POST":
        form=SalaryScaleDetailsForm(request.POST,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj= form.save(commit=False)
                    obj.save()
                    data['success_message']="updated successfully!"
                    data['error_message']=''
                    data['form_is_valid']=True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid']=False
            data['error_message']=form.errors.as_json()
            return JsonResponse(data)

    else:
        form=SalaryScaleDetailsForm(instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['id']=id
        context['title']="Salary Scale Type"

        data['html_form']=render_to_string(
            template_name,context,request=request
        )

    return JsonResponse(data)

#X-X-X-X-X-X-X-X-X-X-X-X------hrm-view-end-------X-X-X-X-X-X-X-X-X-X-X-X

#----------------------------hrm-salary bonus-start------------------------------
class hrm_salary_bonus_create_view(LoginRequiredMixin,TemplateView):
    template_name='hrm/hrm-salary-bonus.html'
    def get(self,request):
        form=SalaryBonusDetailsForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Salary Bonus"

        return render (request,self.template_name,context)

@transaction.atomic
def hrm_salary_bonus_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method=='POST':
        form=SalaryBonusDetailsForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post=form.save(commit=False)
                    bonus_id=fn_get_salsbonus_id()
                    data['id']=bonus_id
                    post.bonus_id=bonus_id
                    post.app_user_id=app_user_id
                    post.save()
                    data['form_is_valid']=True
                    data['error_message']=''
                    data['success_message']="salary bonus create successfully"
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

@transaction.atomic
def hrm_salary_bonus_details_edit(request,id):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    instance_data=get_object_or_404(Salary_Scale_Bonous,bonus_id=id)
    print(instance_data)
    template_name='hrm/hrm-salary-bonus-edit.html'
    data=dict()
    if request.method == "POST":
        form=SalaryBonusDetailsForm(request.POST,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj= form.save(commit=False)
                    obj.save()
                    data['success_message']="updated successfully!"
                    data['error_message']=''
                    data['form_is_valid']=True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid']=False
            data['error_message']=form.errors.as_json()
            return JsonResponse(data)

    else:
        form=SalaryBonusDetailsForm(instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['id']=id
        context['title']="Salary Bonus"

        data['html_form']=render_to_string(
            template_name,context,request=request
        )

    return JsonResponse(data)

#X-X-X-X-X-X-X-X-X-X-X-X------hrm-salary bonus-end-------X-X-X-X-X-X-X-X-X-X-X-X

#----------------------------hrm-Extra Alownce-start------------------------------
class hrm_extra_allownce_create_view(LoginRequiredMixin,TemplateView):
    template_name='hrm/hrm-extra-allownce.html'
    def get(self,request):
        form=ExtraAllowanceDetailsForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Extra Allowance "

        return render (request,self.template_name,context)

@transaction.atomic
def hrm_extra_allownce_create_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method=='POST':
        form=ExtraAllowanceDetailsForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    allowance_id=fn_get_alownce_id()
                    post=form.save(commit=False)
                    data['id']=allowance_id
                    post.allowance_id=allowance_id
                    post.app_user_id=app_user_id
                    post.save()
                    data['form_is_valid']=True
                    data['success_message']="extra allownce create successfully"
                    data['error_message']=''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

@transaction.atomic
def hrm_extra_allownce_edit(request,id):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    instance_data=get_object_or_404(Extra_Allowance,allowance_id=id)
    print(instance_data)
    template_name='hrm/hrm-extra-allownce-edit.html'
    data=dict()
    if request.method == "POST":
        form=ExtraAllowanceDetailsForm(request.POST,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj= form.save(commit=False)
                    obj.save()
                    data['success_message']="updated successfully!"
                    data['error_message']=''
                    data['form_is_valid']=True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid']=False
            data['error_message']=form.errors.as_json()
            return JsonResponse(data)

    else:
        form=ExtraAllowanceDetailsForm(instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['id']=id
        context['title']="Extra Allowance "
        
        data['html_form']=render_to_string(
            template_name,context,request=request
        )

    return JsonResponse(data)
#X-X-X-X-X-X-X-X-X-X-X-X------hrm-Extra Alownce-end-------X-X-X-X-X-X-X-X-X-X-X-X


#----------------------------hrm-bank Info-start------------------------------
class hrm_bank_info_create_view(LoginRequiredMixin,TemplateView):
    template_name='hrm/hrm-bank-info.html'
    def get(self,request):
        form=BankInfoDetailsForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Bank Information"

        return render (request,self.template_name,context)

@transaction.atomic
def hrm_bank_info_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method=='POST':
        form=BankInfoDetailsForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    bank_id=fn_get_bank_id()
                    post=form.save(commit=False)
                    data['id']=bank_id
                    post.bank_id=bank_id
                    post.app_user_id=app_user_id
                    post.save()
                    data['form_is_valid']=True
                    data['success_message']="Bank info create successfully"
                    data['error_message']=''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

@transaction.atomic
def hrm_bank_info_edit(request,id):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    instance_data=get_object_or_404(Bank_Info,bank_id=id)
    print(instance_data)
    template_name='hrm/hrm-bank-info-edit.html'
    data=dict()
    if request.method == "POST":
        form=BankInfoDetailsForm(request.POST,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj= form.save(commit=False)
                    obj.save()
                    data['success_message']="updated successfully!"
                    data['error_message']=''
                    data['form_is_valid']=True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid']=False
            data['error_message']=form.errors.as_json()
            return JsonResponse(data)

    else:
        form=BankInfoDetailsForm(instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['id']=id
        context['title']="Bank "

        data['html_form']=render_to_string(
            template_name,context,request=request
        )

    return JsonResponse(data)




#X-X-X-X-X-X-X-X-X-X-X-X------hrm-Bnak info-end-------X-X-X-X-X-X-X-X-X-X-X-X


#----------------------------hrm-employee Info-start------------------------------
class hrm_employee_info_create_view(LoginRequiredMixin,TemplateView):
    template_name='hrm/hrm-employee-info.html'
    def get(self,request):
        form=EmployeeDetailsForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Employee Info Form "

        return render (request,self.template_name,context)

@transaction.atomic
def hrm_employee_info_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method=='POST':
        form=EmployeeDetailsForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    employee_id=fn_get_employee_id()
                    post=form.save(commit=False)
                    data['id']=employee_id
                    post.employee_id=employee_id
                    post.app_user_id=app_user_id
                    post.save()
                    data['form_is_valid']=True
                    data['success_message']="Employee create successfully"
                    data['error_message']=''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

@transaction.atomic
def hrm_employee_info_edit(request,id):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    instance_data=get_object_or_404(Employee_Details,employee_id=id)
    print(instance_data)
    template_name='hrm/hrm-employee-info-edit.html'
    data=dict()
    if request.method == "POST":
        form=EmployeeDetailsForm(request.POST,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj= form.save(commit=False)
                    obj.save()
                    data['success_message']="updated successfully!"
                    data['error_message']=''
                    data['form_is_valid']=True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid']=False
            data['error_message']=form.errors.as_json()
            return JsonResponse(data)

    else:
        form=EmployeeDetailsForm(instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['id']=id
        context['title']="Employee Info Form "

        data['html_form']=render_to_string(
            template_name,context,request=request
        )

    return JsonResponse(data)




#X-X-X-X-X-X-X-X-X-X-X-X------hrm-employee info-end-------X-X-X-X-X-X-X-X-X-X-X-X

#----------------------------hrm-employee experiance Info-start------------------------------
class hrm_employee_experiance_info_create_view(LoginRequiredMixin,TemplateView):
    template_name='hrm/hrm-employee-experiance-info.html'
    def get(self,request):
        form=EmployeeExperinceInfoForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Employee Experiance "

        return render (request,self.template_name,context)

@transaction.atomic
def hrm_employee_experiance_info_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method=='POST':
        form=EmployeeExperinceInfoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post=form.save(commit=False)
                    post.app_user_id=app_user_id
                    post.save()
                    data['form_is_valid']=True
                    data['success_message']="Experiance create successfully"
                    data['error_message']=''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

@transaction.atomic
def hrm_employee_experiance_info_edit(request,id):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    instance_data=get_object_or_404(Employee_Experience,id=id)
    print(instance_data)
    template_name='hrm/hrm-employee-experiance-info-edit.html'
    data=dict()
    if request.method == "POST":
        form=EmployeeExperinceInfoForm(request.POST,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj= form.save(commit=False)
                    obj.save()
                    data['success_message']="updated successfully!"
                    data['error_message']=''
                    data['form_is_valid']=True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid']=False
            data['error_message']=form.errors.as_json()
            return JsonResponse(data)

    else:
        form=EmployeeExperinceInfoForm(instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['id']=id
        context['title']="Employee Experiance "

        data['html_form']=render_to_string(
            template_name,context,request=request
        )

    return JsonResponse(data)




#X-X-X-X-X-X-X-X-X-X-X-X------hrm-employee-experiance info-end-------X-X-X-X-X-X-X-X-X-X-X-X

#----------------------------hrm-employee Nomene Info-start------------------------------
class hrm_employee_nominee_info_create_view(LoginRequiredMixin,TemplateView):
    template_name='hrm/hrm-employee-nominee-info.html'
    def get(self,request):
        form=EmployeeNomineeForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Employee Nominee "

        return render (request,self.template_name,context)

@transaction.atomic
def hrm_employee_nominee_info_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method=='POST':
        form=EmployeeNomineeForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post=form.save(commit=False)
                    post.app_user_id=app_user_id
                    post.save()
                    data['form_is_valid']=True
                    data['success_message']="Nomenee create successfully"
                    data['error_message']=''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

@transaction.atomic
def hrm_employee_nominee_info_edit(request,id):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    instance_data=get_object_or_404(Employee_Nominee,id=id)
    template_name='hrm/hrm-employee-nominee-info-edit.html'
    data=dict()
    if request.method == "POST":
        form=EmployeeNomineeForm(request.POST,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj= form.save(commit=False)
                    obj.save()
                    data['success_message']="updated successfully!"
                    data['error_message']=''
                    data['form_is_valid']=True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid']=False
            data['error_message']=form.errors.as_json()
            return JsonResponse(data)

    else:
        form=EmployeeNomineeForm(instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['title']="Employee Nominee "
        data['html_form']=render_to_string(
            template_name,context,request=request
        )
        
    return JsonResponse(data)
#X-X-X-X-X-X-X-X-X-X-X-X------hrm-employee-nomene info-end-------X-X-X-X-X-X-X-X-X-X-X-X


#----------------------------hrm-document type-start------------------------------
class hrm_document_type_create_view(LoginRequiredMixin,TemplateView):
    template_name='hrm/hrm-document-type-info.html'
    def get(self,request):
        form=EmployeeDocumentTypeForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Document Type "

        return render (request,self.template_name,context)

@transaction.atomic
def hrm_document_type_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method=='POST':
        form=EmployeeDocumentTypeForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post=form.save(commit=False)
                    document_type_id=fn_get_document_id()
                    post.document_type_id=document_type_id
                    post.app_user_id=app_user_id
                    post.save()
                    data['form_is_valid']=True
                    data['success_message']="document type create successfully"
                    data['error_message']=''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

@transaction.atomic
def hrm_document_type_edit(request,id):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    instance_data=get_object_or_404(Employee_Document_Type,document_type_id=id)
    print(instance_data)
    template_name='hrm/hrm-document-type-edit.html'
    data=dict()
    if request.method == "POST":
        form=EmployeeDocumentTypeForm(request.POST,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj= form.save(commit=False)
                    obj.save()
                    data['success_message']="updated successfully!"
                    data['error_message']=''
                    data['form_is_valid']=True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid']=False
            data['error_message']=form.errors.as_json()
            return JsonResponse(data)

    else:
        form=EmployeeDocumentTypeForm(instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['id']=id
        context['title']="Document Type "

        data['html_form']=render_to_string(
            template_name,context,request=request
        )

    return JsonResponse(data)
#X-X-X-X-X-X-X-X-X-X-X-X------hrm-document type-end-------X-X-X-X-X-X-X-X-X-X-X-X


#----------------------------hrm-employee document Info-start------------------------------
class hrm_employee_document_info_create_view(LoginRequiredMixin,TemplateView):
    template_name='hrm/hrm-employee-document-info.html'
    def get(self,request):
        form=EmployeeDocumentForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Employee Document "

        return render (request,self.template_name,context)

@transaction.atomic
def hrm_employee_document_info_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method=='POST':
        form=EmployeeDocumentForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post=form.save(commit=False)
                    file_obj=request.GET.get('file')
                    post.document_location=file_obj
                    print(file_obj)
                    post.app_user_id=app_user_id
                    post.save()
                    data['form_is_valid']=True
                    data['success_message']="document insert successfully"
                    data['error_message']=''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

@transaction.atomic
def hrm_employee_document_info_edit(request,id):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    instance_data=get_object_or_404(Employee_Document,id=id)
    print(instance_data)
    template_name='hrm/hrm-employee-document-info-edit.html'
    data=dict()
    if request.method == "POST":
        form=EmployeeDocumentForm(request.POST,request.FILES,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj= form.save(commit=False)
                    obj.save()
                    data['success_message']="updated successfully!"
                    data['error_message']=''
                    data['form_is_valid']=True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid']=False
            data['error_message']=form.errors.as_json()
            return JsonResponse(data)

    else:
        form=EmployeeDocumentForm(request.POST,request.FILES,instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['id']=id
        context['title']="Employee Document "

        data['html_form']=render_to_string(
            template_name,context,request=request
        )

    return JsonResponse(data)

#X-X-X-X-X-X-X-X-X-X-X-X------hrm-employee-document info-end-------X-X-X-X-X-X-X-X-X-X-X-X



#----------------------------hrm-leave-info-start------------------------------
class hrm_employee_leave_info_create_view(LoginRequiredMixin,TemplateView):
    template_name='hrm/hrm-emp-leave-info.html'
    def get(self,request):
        form=LeaveInfoForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Employee Leave "

        return render (request,self.template_name,context)

@transaction.atomic
def hrm_employee_leave_info_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method=='POST':
        form=LeaveInfoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post=form.save(commit=False)
                    leave_id=fn_get_leave_id()
                    post.leave_id=leave_id
                    post.app_user_id=app_user_id
                    post.save()
                    data['id']=leave_id
                    data['form_is_valid']=True
                    data['success_message']="Leave info create successfully"
                    data['error_message']=''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

@transaction.atomic
def hrm_employee_leave_info_edit(request,id):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    instance_data=get_object_or_404(Leave_Info,leave_id=id)
    print(instance_data)
    template_name='hrm/hrm-emp-leave-edit.html'
    data=dict()
    if request.method == "POST":
        form=LeaveInfoForm(request.POST,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj= form.save(commit=False)
                    obj.save()
                    data['success_message']="updated successfully!"
                    data['error_message']=''
                    data['form_is_valid']=True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid']=False
            data['error_message']=form.errors.as_json()
            return JsonResponse(data)

    else:
        form=LeaveInfoForm(instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['id']=id
        context['title']="Employee Leave "

        data['html_form']=render_to_string(
            template_name,context,request=request
        )

    return JsonResponse(data)
#X-X-X-X-X-X-X-X-X-X-X-X------hrm-leave-info-end-------X-X-X-X-X-X-X-X-X-X-X-X
#----------------------------hrm-leave-application-start------------------------------
class hrm_employee_leave_application_create_view(LoginRequiredMixin,TemplateView):
    template_name='hrm/hrm-emp-leave-application.html'
    def get(self,request):
        form=LeaveApplicationForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Employee Leave Application "

        return render (request,self.template_name,context)

@transaction.atomic
def hrm_employee_leave_application_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method=='POST':
        form=LeaveApplicationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post=form.save(commit=False)
                    post.app_user_id=app_user_id
                    post.save()
                    data['form_is_valid']=True
                    data['success_message']="Leave info create successfully"
                    data['error_message']=''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

@transaction.atomic
def hrm_employee_leave_application_edit(request,id):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    instance_data=get_object_or_404(Leave_Application,id=id)
    print(instance_data)
    template_name='hrm/hrm-emp-leave-application-edit.html'
    data=dict()
    if request.method == "POST":
        form=LeaveApplicationForm(request.POST,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj= form.save(commit=False)
                    obj.save()
                    data['success_message']="updated successfully!"
                    data['error_message']=''
                    data['form_is_valid']=True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid']=False
            data['error_message']=form.errors.as_json()
            return JsonResponse(data)

    else:
        form=LeaveApplicationForm(instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['id']=id
        context['title']="Employee Leave Application "

        data['html_form']=render_to_string(
            template_name,context,request=request
        )

    return JsonResponse(data)
#X-X-X-X-X-X-X-X-X-X-X-X------hrm-leave-application-end-------X-X-X-X-X-X-X-X-X-X-X-X

#----------------------------hrm-employee-traning-info-start------------------------------
class hrm_employee_training_info_create_view(LoginRequiredMixin,TemplateView):
    template_name='hrm/hrm-emp-Training-info.html'
    def get(self,request):
        form=EmployeeTrainingForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Employee  Tranining "

        return render (request,self.template_name,context)

@transaction.atomic
def hrm_employee_training_info_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method=='POST':
        form=EmployeeTrainingForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post=form.save(commit=False)
                    post.app_user_id=app_user_id
                    post.save()
                    data['form_is_valid']=True
                    data['success_message']="Traning info create successfully"
                    data['error_message']=''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

@transaction.atomic
def hrm_employee_training_info_edit(request,id):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    instance_data=get_object_or_404(Employee_Training,id=id)
    print(instance_data)
    template_name='hrm/hrm-emp-Training-edit.html'
    data=dict()
    if request.method == "POST":
        form=EmployeeTrainingForm(request.POST,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj= form.save(commit=False)
                    obj.save()
                    data['success_message']="updated successfully!"
                    data['error_message']=''
                    data['form_is_valid']=True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid']=False
            data['error_message']=form.errors.as_json()
            return JsonResponse(data)

    else:
        form=EmployeeTrainingForm(instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['id']=id
        context['title']="Employee  Tranining "

        data['html_form']=render_to_string(
            template_name,context,request=request
        )

    return JsonResponse(data)
#X-X-X-X-X-X-X-X-X-X-X-X------hrm-traning-info-end-------X-X-X-X-X-X-X-X-X-X-X-X

#----------------------------hrm-pay-bill-info-start------------------------------
class hrm_pay_bill_info_create_view(LoginRequiredMixin,TemplateView):
    template_name='hrm/hrm-pay-bill-info.html'
    def get(self,request):
        form=PayBillForm()
        context=get_global_data(request)
        context['form']=form
        context['title']="Bill info "
        return render (request,self.template_name,context)

@transaction.atomic
def hrm_pay_bill_info_insert(request):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid']=False
    app_user_id=request.session['app_user_id']
    if request.method=='POST':
        form=PayBillForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post=form.save(commit=False)
                    post.app_user_id=app_user_id
                    bill_id=fn_get_bill_id()
                    post.bill_id=bill_id
                    post.save()
                    data['form_is_valid']=True
                    data['success_message']="Traning info create successfully"
                    data['error_message']=''
                    return JsonResponse(data)

            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)

        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

@transaction.atomic
def hrm_pay_bill_info_edit(request,id):
    if not request.user.is_authenticated:
        return render(request,'appauth/appauth-login.html')
    instance_data=get_object_or_404(Pay_Bill,bill_id=id)
    print(instance_data)
    template_name='hrm/hrm-paybill-edit.html'
    data=dict()
    if request.method == "POST":
        form=PayBillForm(request.POST,instance=instance_data)
        data['form_error']=form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj= form.save(commit=False)
                    obj.save()
                    data['success_message']="updated successfully!"
                    data['error_message']=''
                    data['form_is_valid']=True
                    return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['form_is_valid']=False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid']=False
            data['error_message']=form.errors.as_json()
            return JsonResponse(data)

    else:
        form=PayBillForm(instance=instance_data)
        context=get_global_data(request)
        context['form']=form
        context['id']=id
        
        context['title']="Bill info "

        data['html_form']=render_to_string(
            template_name,context,request=request
        )

    return JsonResponse(data)
#X-X-X-X-X-X-X-X-X-X-X-X------hrm-traning-info-end-------X-X-X-X-X-X-X-X-X-X-X-X

#------Advance salary payment----------------------

class hrm_advsalary_view(TemplateView):
    template_name = 'hrm/hrm-advance-salary-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = AdvanceSalary()
        # args = {'form': form}
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def hrm_advsalary_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = AdvanceSalary(request.POST)
                if form.is_valid():
                    try:
                        with transaction.atomic():
                            app_user_id = request.session["app_user_id"]
                            #branch_code = request.session["branch_code"]
                            post = form.save(commit=False)
                            post.app_user_id = app_user_id
                            post.save()
                            data['form_is_valid'] = True
                            data['success_message'] = 'Save Successfully!'
                    except Exception as e:
                        data['form_is_valid'] = False
                        if len(str(data['error_message'])) > 0:
                            return JsonResponse(data)
                        data['error_message'] = str(e)
                        logger.error("Error on line {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(e).__name__, str(e)))
                        return JsonResponse(data)
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


def hrm_advsalary_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    try:
        with transaction.atomic():

            instance_data = get_object_or_404(Advance_Salary, employee_id=id)
            template_name = 'hrm/hrm-advance-salary-edit.html'
            context = {}
            data = dict()

            if request.method == 'POST':
                form = AdvanceSalary(request.POST, instance=instance_data)
                data['form_error'] = form.errors.as_json()
                if form.is_valid():

                    obj = form.save(commit=False)
                    obj.save()
                    context = get_global_data(request)
                    context['success_message'] = ''
                    context['error_message'] = ''
                    data['form_is_valid'] = True
                else:
                    data['form_is_valid'] = False
            else:
                form = AdvanceSalary(instance=instance_data)
                context = get_global_data(request)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)
#-----Allowance Payment ----------------

class hrm_allowancepay_view(TemplateView):
    template_name = 'hrm/hrm-allowancepay-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = AllowancePayment()  
        args = {'form': form}
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def hrm_allowancepay_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = AllowancePayment(request.POST)
                if form.is_valid():
                    try:
                        with transaction.atomic():
                            app_user_id = request.session["app_user_id"]
                            #branch_code = request.session["branch_code"]
                            post = form.save(commit=False)
                            post.app_user_id = app_user_id
                            post.save()
                            data['form_is_valid'] = True
                            data['success_message'] = 'Save Successfully!'
                    except Exception as e:
                        data['form_is_valid'] = False
                        if len(str(data['error_message'])) > 0:
                            return JsonResponse(data)
                        data['error_message'] = str(e)
                        logger.error("Error on line {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(e).__name__, str(e)))
                        return JsonResponse(data)
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


def hrm_allowancepay_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    try:
        with transaction.atomic():

            instance_data = get_object_or_404(Allowance_Payment, employee_id=id)
            template_name = 'hrm/hrm-allowancepay-edit.html'
            context = {}
            data = dict()

            if request.method == 'POST':
                form = AllowancePayment(request.POST, instance=instance_data)
                data['form_error'] = form.errors.as_json()
                if form.is_valid():

                    obj = form.save(commit=False)
                    obj.save()
                    context = get_global_data(request)
                    context['success_message'] = ''
                    context['error_message'] = ''
                    data['form_is_valid'] = True
                else:
                    data['form_is_valid'] = False
            else:
                form = AllowancePayment(instance=instance_data)
                context = get_global_data(request)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)

#------Deductions salary payment----------------------
class hrm_deduct_salary_view(TemplateView):
    template_name = 'hrm/hrm-deduct-salary-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = OthersDeduction()
        args = {'form': form}
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def hrm_deduct_salary_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = OthersDeduction(request.POST)
                if form.is_valid():
                    try:
                        with transaction.atomic():
                            app_user_id = request.session["app_user_id"]
                            #branch_code = request.session["branch_code"]
                            post = form.save(commit=False)
                            post.app_user_id = app_user_id
                            post.save()
                            data['form_is_valid'] = True
                            data['success_message'] = 'Save Successfully!'
                    except Exception as e:
                        data['form_is_valid'] = False
                        if len(str(data['error_message'])) > 0:
                            return JsonResponse(data)
                        data['error_message'] = str(e)
                        logger.error("Error on line {} \nType: {} \nError:{}".format(
                            sys.exc_info()[-1], type(e).__name__, str(e)))
                        return JsonResponse(data)
                else:
                    data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


def hrm_deduct_salary_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    try:
        with transaction.atomic():

            instance_data = get_object_or_404(Others_Deduction, employee_id=id)
            template_name = 'hrm/hrm-deduct-salary-edit.html'
            context = {}
            data = dict()

            if request.method == 'POST':
                form = OthersDeduction(request.POST, instance=instance_data)
                data['form_error'] = form.errors.as_json()
                if form.is_valid():

                    obj = form.save(commit=False)
                    obj.save()
                    context = get_global_data(request)
                    context['success_message'] = ''
                    context['error_message'] = ''
                    data['form_is_valid'] = True
                else:
                    data['form_is_valid'] = False
            else:
                form = AdvanceSalary(instance=instance_data)
                context = get_global_data(request)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


#------------report---------------------------------------------
class hrm_salary_processing(TemplateView):
    template_name = 'hrm_report/hrm-salary-processing.html'
   
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)

        forms = CommonReportForm(
            initial={'branch_code': branch_code})
        context = get_global_data(request)
        context['forms'] = forms
        return render(request, self.template_name, context)

def hrm_choice_department(request):
    list_data = Department_Info.objects.filter().values(
        'department_id', 'department_name').order_by('department_name')
    return render(request, 'hrm_report/hrm-choice-department.html', {'list_data': list_data})



class hrm_salary_sheet_view(TemplateView):
    template_name = 'hrm/hrm-salary-sheet-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        
        form = Salary_sheet_Model_Form()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


@transaction.atomic
def hrm_salary_sheet_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''
   

    if request.method == 'POST':
        form = Salary_sheet_Model_Form(request.POST)
        if form.is_valid():
            try:
                form.save(commit=False)
                dept_id = form.cleaned_data["dept_id"]
                month_year = form.cleaned_data["month_year"]
                branch_code = form.cleaned_data["branch_code"]
                app_user_id=request.session["app_user_id"]
                print(dept_id+" "+month_year+" "+branch_code+" "+app_user_id)
                try:
                    with transaction.atomic():
                        cursor = connection.cursor()
                        cursor.callproc("fn_hrm_salary_processing", [branch_code, dept_id,month_year,app_user_id])
                        row = cursor.fetchone()
                        if row[0] != 'S':
                            data['error_message'] = row[1]
                            raise Exception("database error: "+row[1])
                        data['form_is_valid'] = True
                        data['success_message'] = " salary processing successfull "
                        
                        return JsonResponse(data)
                except Exception as e:
                    data['form_is_valid'] = False
                    data['error_message'] = "database error: "+ str(e)
                    logger.error("Error on line {} \nType: {} \nError:{}".format(
                        sys.exc_info()[-1], type(e).__name__, str(e)))
                    return JsonResponse(data)
            except Exception as e:
                data['error_message'] = "Form error: "+str(e)
                data['form_is_valid'] = False
                return JsonResponse(data)

        else:
            data['error_message'] ="form2 error: "+ form.errors.as_json()
    return JsonResponse(data)


    ############### Holiday Type ##########################

class hrm_holiday_type_view(TemplateView):
    template_name = 'hrm/hrm-holiday-type-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Holyday_Type_Form()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def hrm_holiday_Type_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = Holyday_Type_Form(request.POST)
        if form.is_valid():
            holiday_type_id = fn_get_holiday_type_id()
            post = form.save(commit=False)
            post.app_user_id = request.session["app_user_id"]
            post.holiday_type_id = holiday_type_id
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Section Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)

def hrm_holiday_Type_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    
    instance_data = get_object_or_404(Holyday_Type, holiday_type_id=id)
    template_name = 'hrm/hrm-holiday-type-edit.html'
    data = dict()

    if request.method == 'POST':
        form = Holyday_Type_Form(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():

            obj = form.save(commit=False)
            obj.save()
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return JsonResponse(data)
    else:
        form = Holyday_Type_Form(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)



   

###################### holiday info ########################
class hrm_Holyday_Info_view(TemplateView):
    template_name = 'hrm/hrm-Holyday-Info-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Holyday_Info_Form()  
        args = {'form': form}
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def hrm_Holyday_Info_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = Holyday_Info_Form(request.POST)
        if form.is_valid():
           
            post = form.save(commit=False)
            holiday_sl_nos = fn_get_holiday_sl_no()
            post.app_user_id = request.session["app_user_id"]
            post.holiday_sl_no = holiday_sl_nos
            post.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Section Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def hrm_Holyday_Info_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    try:
        with transaction.atomic():

            instance_data = get_object_or_404(Holyday_Info, holiday_sl_no=id)
            template_name = 'hrm/hrm-Holyday-Info-edit.html'
            context = {}
            data = dict()

            if request.method == 'POST':
                form = Holyday_Info_Form(request.POST, instance=instance_data)
                data['form_error'] = form.errors.as_json()
                if form.is_valid():

                    obj = form.save(commit=False)
                    obj.save()
                    context = get_global_data(request)
                    context['success_message'] = ''
                    context['error_message'] = ''
                    data['form_is_valid'] = True
                else:
                    data['form_is_valid'] = False
            else:
                form = Holyday_Info_Form(instance=instance_data)
                context = get_global_data(request)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)
######################## employee holiday #################
class hrm_Employee_Holyday_view(TemplateView):
    template_name = 'hrm/hrm-Employee-Holyday-createlist.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Employee_Holyday_Form()  
        args = {'form': form}
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def hrm_Employee_Holyday_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False

    if request.method == 'POST':
        form = Employee_Holyday_Form(request.POST)
        if form.is_valid():
           
            post = form.save(commit=False)
            holiday_sl_no = fn_get_holiday_sl_no1()
            post.app_user_id = request.session["app_user_id"]
            post.holiday_sl_no = holiday_sl_no
            post.save()
            data['id'] = holiday_sl_no
            data['form_is_valid'] = True
            data['success_message'] = 'Section Added Successfully!'
        else:
            data['error_message'] = form.errors.as_json()
    return JsonResponse(data)


def hrm_Employee_Holyday_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    data = dict()
    try:
        with transaction.atomic():

            instance_data = get_object_or_404(Employee_Holyday, holiday_sl_no=id)
            template_name = 'hrm/hrm-employee-holiday-edit.html'
            context = {}
            data = dict()

            if request.method == 'POST':
                form = Employee_Holyday_Form(request.POST, instance=instance_data)
                data['form_error'] = form.errors.as_json()
                if form.is_valid():

                    obj = form.save(commit=False)
                    obj.save()
                    context = get_global_data(request)
                    context['success_message'] = ''
                    context['error_message'] = ''
                    data['form_is_valid'] = True
                else:
                    data['form_is_valid'] = False
            else:
                form = Employee_Holyday_Form(instance=instance_data)
                context = get_global_data(request)
                context['form'] = form
                context['id'] = id
                data['html_form'] = render_to_string(
                    template_name, context, request=request)
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)

