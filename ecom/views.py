from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import FieldDoesNotExist
from django.core import serializers
from random import randint
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.db import connection, transaction
from django.template.loader import render_to_string
from django.db.models import Count, Sum, Avg, Subquery, Q, F
import logging
import sys
logger = logging.getLogger(__name__)
from decimal import Decimal
from datetime import date, datetime, timedelta
import time
import base64
from django.core.files.base import ContentFile
from .utils import *
from .validations import *
from .myException import *
from .models import *
from appauth.models import Employees
from .forms import *
from appauth.views import get_global_data, fn_get_employee_by_app_user_id
from finance.utils import fn_open_account_transaction_screen, fn_get_transaction_account_type, fn_get_account_info_byactype, fn_create_account, fn_get_accountinfo_byacnumber, fn_get_transaction_gl
from finance.validations import fn_val_account_number
from django.views.generic import CreateView, DetailView

class ecom_orderlist_view(TemplateView):
    template_name = 'ecom/ecom-order-list.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = OrderSearchForm(initial={'from_date': cbd, 'upto_date': cbd})
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

def ecom_order_details(request, order_number):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    order = Ecom_Order_Master.objects.get(order_number=order_number)
    delivery_man=Employees.objects.filter(employee_designation="DG0005")
    rows = Order_Details.objects.raw('''select o.id, o.order_number, p.product_name, p.product_id, o.order_quantity,
    o.product_price, o.total_price, o.discount_rate, o.discount_amount, (o.total_price-o.discount_amount) as sales_amount 
    from ecom_order_details o INNER JOIN ecom_products p 
    on o.product_id=p.product_id and order_number='''+"'"+order_number+"'")
    context = get_global_data(request)
    context['delivery_man'] = delivery_man
    context['data'] = rows
    context['order'] = order
    return render(request, 'ecom/ecom-order-details.html', context)

@transaction.atomic
def ecom_order_accept(request, order_number):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = {}
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            order = Ecom_Order_Master.objects.get(order_number=order_number)
            branch_code = request.session["branch_code"]
            order_number = order.order_number
            account_number = order.account_number
            discount_amount = order.discount_amount
            bill_amount = (order.bill_amount + Decimal(order.delivery_charge))-Decimal(order.discount_amount)
            app_user_id = request.session["app_user_id"]
            cbd = get_business_date(branch_code, app_user_id)
            delivery_man=request.POST.get('delivery_man')
            employee_id = delivery_man
            # employee_id = fn_get_employee_by_app_user_id(app_user_id)

            app_param = Application_Settings.objects.get()
            tran_type_code = app_param.quick_payment_type
            tran_screen = 'SALES_ENTRY'

            credit_gl_code, debit_gl_code = fn_get_transaction_gl(
                p_transaction_screen=tran_screen, p_tran_type_code=tran_type_code)

            if credit_gl_code is None and debit_gl_code is None:
                data['error_message'] = 'Sales Configuration Ledger Not Exist!\nPlease Contact with your Admin.'
                return JsonResponse(data)

            invoice_number = fn_generate_invoice_number(branch_code)
            cursor = connection.cursor()
            cursor.callproc("fn_sales_online_order_accept", [branch_code, app_user_id, order_number, invoice_number, cbd, employee_id,
                                                             bill_amount, discount_amount,  tran_type_code, credit_gl_code, debit_gl_code, order_number])

            row = cursor.fetchone()

            if row[0] != 'S':
                data['error_message'] = row[1]
                raise Exception(row[1])

            message = "Order Accepted Successfully with Invoice Number : " + invoice_number

            data['success_message'] = message
            data['form_is_valid'] = True

            data['form_is_valid'] = True
            data['success_message'] = message
    except Exception as e:
        data['error_message'] = str(e)
    return JsonResponse(data)


def ecom_order_details_update(request):
    try:
        data = dict()
        data_string = request.POST.getlist('data_string')
        data_dict = json.loads(data_string[0])
        for row in data_dict:
            try:
                product_id = row['product_id']
                order_number = row['order_number']
                quantity = row['quantity']
                unit_price = row['unit_price']
                total_price = row['total_price']
                discount_rate = row['discount_rate']
                discount_amount = row['discount_amount']
                sales_amount = row['sales_amount']
                try:
                    update_row = Order_Details.objects.get(
                        product_id=product_id, order_number=order_number)
                    update_row.quantity = quantity
                    update_row.product_price = unit_price
                    update_row.total_price = total_price
                    update_row.discount_rate = discount_rate
                    update_row.discount_amount = discount_amount
                    update_row.save()
                except Order_Details.DoesNotExist:
                    pass
            except Exception as e:
                data['error_message'] = 'Error for Updating Product ' + \
                    str(product_id)+' ' + str(e)
                data['form_is_valid'] = False
                return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        data['form_is_valid'] = False
        return JsonResponse(data)

    data['form_is_valid'] = True
    data['success_message'] = 'Save Successfully!'
    return JsonResponse(data)


class ecom_product_view(TemplateView):
    template_name = 'ecom/ecom-product-list.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = EcomProductForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)


def ecom_products_list(request):
    product_id = request.GET.get('product_id', None)
    product_model = request.GET.get('product_model', None)
    product_group = request.GET.get('product_group', None)

    products = Ecom_Products.objects.all()
    if(product_id):
        products = Ecom_Products.objects.filter(product_id=product_id)
    if(product_model):
        products = Ecom_Products.objects.filter(product_model=product_model)
    if(product_group):
        products = Ecom_Products.objects.filter(product_group=product_group)

    product_list = serializers.serialize("json", products)
    return HttpResponse(product_list)


@transaction.atomic
def ecom_product_add(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = EcomProductForm(request.POST)
                if form.is_valid():
                    try:
                        with transaction.atomic():
                            product = products.objects.get(
                                pk=form.cleaned_data['product_id'])
                            app_user_id = request.session["app_user_id"]
                            post = form.save(commit=False)
                            post.product_name = product.product_name
                            post.app_user_id = app_user_id
                            post.save()

                            data['form_is_valid'] = True
                            data['success_message'] = 'Product Added Successfull'
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

class ecom_product_vieworedit(TemplateView):
    template_name = 'ecom/ecom-product-view.html'

    def get(self, request, id):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        product = Ecom_Products.objects.get(pk=id)
        images = Product_Images.objects.filter(product_id=id)

        form = EcomProductForm(instance=product)
        context = get_global_data(request)
        context['form'] = form
        context['product'] = product
        context['images'] = images
        return render(request, self.template_name, context)


def ecom_product_edit(request):
    data = dict()
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')

    instance_data = get_object_or_404(
        Ecom_Products, product_id=request.POST.get('product_id'))
    data['success_message'] = ''
    data['error_message'] = ''
    if request.method == 'POST':
        form = EcomProductForm(
            request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        app_user_id = request.session["app_user_id"]
        if form.is_valid():
            obj = form.save(commit=False)
            obj.app_user_id = app_user_id
            obj.save()
            data['form_is_valid'] = True
            data['success_message'] = 'Product Updated'
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
        return redirect('/ecom-product-vieworedit/'+request.POST.get('product_id'))
        # return JsonResponse(data)
    else:
        return redirect('/ecom-product-vieworedit/'+request.POST.get('product_id'))
        # return JsonResponse(data)


def ecom_product_image_insert(request):
    data = dict()
    product_id = request.POST.get('product_id')
    prod_inst = Ecom_Products.objects.get(product_id=product_id)
    app_user_id = request.session["app_user_id"]
    img_inst = Product_Images(product_id=prod_inst,
                              image_serial=1, app_user_id=app_user_id)
    img_inst.image = base64_to_image(
        request.POST.get('image'), prod_inst.product_name)
    img_inst.image_serial = Product_Images.objects.filter(
        product_id=product_id).count()+1
    img_inst.save()
    data['new_image'] = Product_Images.objects.filter(
        product_id=product_id).values().order_by('-id')[0]
    return JsonResponse(data)


def ecom_product_image_delete(request):
    data = dict()
    id = request.POST.get('id')
    Product_Images.objects.get(id=id).delete()
    data['success_message'] = 'This image removed.'
    return JsonResponse(data)


# ecom_slider_view
class ecom_slider_view(TemplateView):
    template_name = 'ecom/ecom-slider-list.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = EcomSliderFrom()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

@transaction.atomic
def ecom_slider_create(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ''
    try:
        with transaction.atomic():
            if request.method == 'POST':
                form = EcomSliderFrom(request.POST)
                if form.is_valid():
                    try:
                        with transaction.atomic():
                            app_user_id = request.session["app_user_id"]
                            post = form.save(commit=False)
                            post.app_user_id = app_user_id
                            post.save()
                            data['form_is_valid'] = True
                            # data['success_message'] = product.product_name
                            data['success_message'] = 'Slider create Successfull'
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

def ecom_slider_edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
        
    instance_data = get_object_or_404(Ecom_Slider, id=id)
    template_name = 'ecom/ecom-slider-edit.html'
    app_user_id = request.session["app_user_id"]
    data = dict()

    if request.method == 'POST':
        form = EcomSliderFrom(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.app_user_id=app_user_id
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
        form = EcomSliderFrom(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        if instance_data.image:
            context['image'] = instance_data.image.url
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

def ecom_slider_image_insert(request):
    data = dict()
    id = request.POST.get('id')
    slider_inst = Ecom_Slider.objects.get(pk=id)
    app_user_id = request.session["app_user_id"]
    slider_inst.app_user_id=app_user_id
    if slider_inst.image:
        slider_inst.image.delete(save=False)
    slider_inst.image = base64_to_image_slider(request.POST.get('image'), slider_inst.title)
    slider_inst.app_user_id=app_user_id
    slider_inst.save()
    data['image'] = Ecom_Slider.objects.filter(pk=id)[0].image.url
    return JsonResponse(data)

# ecom_slider_view

class PageCreateView(TemplateView):
    template_name = 'ecom/ecom-create-page.html'
    
    def get(self, request):
        form = PageModelForm()
        context = dict()
        context['form'] = form
        return render(request, self.template_name, context)
    def post(self, request):
        data=dict()
        app_user_id = request.session["app_user_id"]
        forms =  PageModelForm(request.POST)
        if forms.is_valid():
            obj = forms.save(commit=False)
            obj.app_user_id=app_user_id
            obj.save()
            print(obj.pk)
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            return redirect('/ecom-edit-page/'+str(obj.pk))
            # return JsonResponse(data)
        # return render(request, self.template_name, context)
        else:
            data['form_is_valid'] = False
            data['error_message'] = forms.errors.as_json()
            return JsonResponse(data)
            # return redirect('/ecom-page-create/')

class ecom_page_list(TemplateView):
    template_name = 'ecom/ecom-page-list.html'
    def get(self, request):
        context = dict()
        pages=PageModel.objects.filter(publish_status=1)
        context['pages'] = pages
        return render(request, self.template_name, context)

def ecom_edit_page(request,id):
    template_name = 'ecom/ecom-edit-page.html'
    page=get_object_or_404(PageModel, pk=id)
    form = PageModelForm(instance=page)
    context = dict()
    data=dict()
    context['form'] = form
    context['id'] = id
    if request.method == 'POST':
        app_user_id = request.session["app_user_id"]
        form = PageModelForm(request.POST,instance=page)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.app_user_id=app_user_id
            obj.save()
            data['success_message'] = 'Updated Successfully!'
            data['error_message'] = ''
            data['form_is_valid'] = True
            # return JsonResponse(data)
            return redirect('/ecom-edit-page/'+id)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            # return JsonResponse(data)
    return render(request, template_name, context)

class ecom_product_cat_view(TemplateView):
    template_name = 'ecom/ecom-product-categories.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = EcomProductCategoriesForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

@transaction.atomic
def ecom_product_cat_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid'] = False
    if request.method=='POST':
        form = EcomProductCategoriesForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    app_user_id = request.session["app_user_id"]
                    categories_name = form.cleaned_data['categories_name']

                    if fn_val_check_ecom_category_exist(categories_name):
                        data['error_message'] = 'This Category Name Already Exist!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    post = form.save(commit=False)
                    post.categories_id=fn_generate_category_id(100)
                    post.app_user_id = app_user_id
                    post.save()
                    data['form_is_valid'] = True
                    data['succ_message'] = "Save Successfully"
            except Exception as e:
                data['form_is_valid'] = False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

def ecom_product_cat_edit(request,id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
        
    instance_data = get_object_or_404(Ecom_Product_Categories, categories_id=id)
    template_name = 'ecom/ecom-product-category-edit.html'
    data = dict()

    if request.method == 'POST':
        form = EcomProductCategoriesForm(request.POST, instance=instance_data)
        app_user_id = request.session["app_user_id"]
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.app_user_id=app_user_id
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
        form = EcomProductCategoriesForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)

# Product Sub Categories

class ecom_product_subcat_view(TemplateView):
    template_name = 'ecom/ecom-product-subcategories.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        app_user_id = request.session["app_user_id"]
        branch_code = request.session["branch_code"]
        cbd = get_business_date(branch_code, app_user_id)
        form = EcomProductSubCategoriesForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)

@transaction.atomic
def ecom_product_subcat_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data=dict()
    data['form_is_valid'] = False
    if request.method=='POST':
        form = EcomProductSubCategoriesForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    app_user_id = request.session["app_user_id"]
                    subcategories_name = form.cleaned_data['subcategories_name']

                    if fn_val_check_ecom_subcategory_exist(subcategories_name):
                        data['error_message'] = 'This Sub Category Name Already Exist!'
                        data['form_is_valid'] = False
                        return JsonResponse(data)

                    post = form.save(commit=False)
                    post.subcategories_id=fn_generate_subcategory_id(100)
                    post.app_user_id = app_user_id
                    post.save()
                    data['form_is_valid'] = True
                    data['succ_message'] = "Save Successfully"
            except Exception as e:
                data['form_is_valid'] = False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)

def ecom_product_subcat_edit(request,id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
        
    instance_data = get_object_or_404(Ecom_Product_Sub_Categories, subcategories_id=id)
    template_name = 'ecom/ecom-product-subcategory-edit.html'
    data = dict()

    if request.method == 'POST':
        form = EcomProductSubCategoriesForm(request.POST, instance=instance_data)
        app_user_id = request.session["app_user_id"]
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.app_user_id=app_user_id
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
        form = EcomProductSubCategoriesForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request)
    return JsonResponse(data)