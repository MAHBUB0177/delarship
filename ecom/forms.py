from django import forms
from crispy_forms.layout import Field
from django.forms import ModelForm, TextInput, Select, Textarea, IntegerField, ChoiceField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.widgets import HiddenInput
from django.utils.translation import ugettext_lazy as _
from tinymce.widgets import TinyMCE
from tinymce.models import HTMLField

from .models import *

YES_NO = (
    ('Y', 'Yes'),
    ('N', 'No')
)


class DateInput(forms.DateInput):
    input_type = 'date'


class ChoiceFieldNoValidation(ChoiceField):
    def validate(self, value):
        pass

class EcomProductForm(forms.ModelForm):
    product_id = ChoiceFieldNoValidation(label='Select Product', choices=[('', 'Select Product')], initial="")
    # product_description = forms.HTMLField(widget=TinyMCE(attrs={'rows':2,'class': 'form-control'}))
    def __init__(self, *args, **kwargs):
        super(EcomProductForm, self).__init__(*args, **kwargs)
        self.fields['product_id'].required = True

    class Meta:
        model = Ecom_Products
        fields =["product_id","category_id","sub_category_id","product_brand_id","product_model","product_group","product_price","discount_amount","product_old_price","product_description","product_feature","product_specification","product_keyword"]

        widgets = {
            'product_feature': Textarea(attrs={'rows':2, 'placeholder':'Reverse automatic braking, Built-in rechargeable battery'}),
            'product_specification': Textarea(attrs={'rows':2, 'placeholder':'{"Stroke":"4 Stroke","Piston displacement":"150 cc"}'}),
            'product_keyword': Textarea(attrs={'rows':2, 'placeholder':'Black, Read, Motor Cycle'}),
        }
        labels = {  
                    "product_id": _("Product Code"),
                    "category_id": _("Product Category"),
                    "sub_category_id": _("Product Sub Category"),
                    "product_brand_id": _("Product Brand"),
                    "product_description": _("Product Overview"),
                    "product_feature": _("Product Feature | separate by (,) comma "),
                    "product_keyword": _("Product Keyword/Tag | separate by (,) comma "),
                    "product_specification": _("Product Specification | Enter key value pairs list"),
                    # separate by comma

                }

class OrderSearchForm(forms.Form):
    order_number = forms.CharField(label="Order Number", widget=forms.TextInput(
    attrs={ 'id': 'id_order_number'}
    ),required=False)
    customer_phone = forms.CharField(label="Customer Phone", widget=forms.TextInput(
    attrs={'id': 'id_customer_phone'}
    ),required=False)
    executive_phone = forms.CharField(label="Executive Phone", widget=forms.TextInput(
    attrs={'id': 'id_executive_phone'}
    ),required=False)
    order_date = forms.DateField(label="Order Date",widget=DateInput(), required=True)
    from_date = forms.DateField(label="From Date",widget=DateInput(), required=True)
    upto_date = forms.DateField(label="Upto Date",widget=DateInput(), required=True)
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)

class EcomSliderFrom(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EcomSliderFrom, self).__init__(*args, **kwargs)
        # self.fields['product_id'].required = True

    class Meta:
        model = Ecom_Slider
        fields =["title","second_title","button_up_title","button_one_label","button_one_icon","button_one_url","button_two_label","button_two_icon","button_two_url","image","status"]

        widgets = {
            # 'product_description': Textarea(attrs={'rows':2, 'class':'tinyText'}),
        }
        labels = {  
                    # "product_id": _("Product Code")

                }


class PageModelForm(forms.ModelForm):

    class Meta:
        model = PageModel
        fields =["title","content","publish_status"]

class EcomProductCategoriesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EcomProductCategoriesForm, self).__init__(*args, **kwargs)
        self.fields['categories_id'].widget.attrs['readonly'] = True
    class Meta:
        model = Ecom_Product_Categories
        fields =["categories_id","categories_name","image_class_name","status"]

class EcomProductSubCategoriesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EcomProductSubCategoriesForm, self).__init__(*args, **kwargs)
        self.fields['subcategories_id'].widget.attrs['readonly'] = True
    class Meta:
        model = Ecom_Product_Sub_Categories
        fields =["categories_id","subcategories_id","subcategories_name","status"]