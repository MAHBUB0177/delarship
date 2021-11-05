from django.db import models
from django.db import models
from tinymce.models import HTMLField
from django.conf import settings
import os
from django.urls import reverse


STATUS_LIST = (
    ('A', 'Active'),
    ('I', 'Inactive')
)
ORDER_STATUS = (
    ('N', 'New'),
    ('A', 'Approved'),
    ('D', 'Delivered')
)


class User_Chart(models.Model):
    product_id = models.CharField(max_length=20, null=False, blank=True)
    product_name = models.CharField(max_length=200)
    product_model = models.CharField(max_length=200, blank=True, null=True)
    product_group = models.CharField(max_length=200, blank=True, null=True)
    product_quantity = models.IntegerField(blank=True, null=True)
    product_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    discount_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    product_old_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    total_bill_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    product_photo1 = models.ImageField(
        upload_to='product_image/', blank=True, null=True)
    product_description = models.CharField(
        max_length=500, blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'ecom_user_chart'


class Ecom_Delivery_Address(models.Model):
    customer = models.CharField(max_length=15, blank=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    address_1 = models.CharField(max_length=300, blank=True, null=True)
    address_2 = models.CharField(max_length=300, blank=True, null=True)
    distric_id = models.CharField(max_length=6, blank=True, null=True)
    upazilla_id = models.CharField(max_length=6, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    use_count = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        managed = False
        db_table = 'ecom_delivery_address'


class Ecom_Order_Master(models.Model):
    order_number = models.CharField(max_length=20, primary_key=True)
    delivery_address_id = models.ForeignKey(Ecom_Delivery_Address, on_delete=models.CASCADE,
                                            related_name='delivery_address_id', db_column='delivery_address_id', blank=True, null=True)
    delivery_charge = models.CharField(max_length=20, blank=True, null=True)
    order_date = models.DateTimeField()
    customer_id = models.CharField(max_length=20, blank=True, null=True)
    account_number = models.CharField(max_length=200, blank=True, null=True)
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    customer_address = models.CharField(max_length=500, blank=True, null=True)
    executive_phone = models.CharField(max_length=20, blank=True, null=True)
    coupon_code = models.CharField(max_length=20, blank=True, null=True)
    total_quantity = models.IntegerField(blank=True)
    returned_quantity = models.IntegerField(null=True, blank=True, default=0)
    bill_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    discount_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    payment_method = models.CharField(max_length=20, blank=True, null=True)
    pay_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    due_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    advance_pay = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True)
    status = models.CharField(
        max_length=2, choices=ORDER_STATUS, default='N', null=True, blank=True)
    order_comments = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=22, decimal_places=12, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=22, decimal_places=12, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'ecom_order_master'


class Ecom_Product_Categories(models.Model):
    categories_id = models.CharField(
        max_length=20,  blank=True, primary_key=True)
    categories_name = models.CharField(max_length=200, null=False)
    image_class_name = models.CharField(max_length=200, null=False)
    status = models.CharField(max_length=5, null=True,
                              choices=STATUS_LIST, default='A', blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.categories_name

    class Meta:
        managed = False
        db_table = 'ecom_product_categories'


class Ecom_Product_Sub_Categories(models.Model):
    categories_id = models.ForeignKey(Ecom_Product_Categories, on_delete=models.PROTECT,
                                      related_name='sub_categories_id', db_column='categories_id', blank=True, null=True)
    subcategories_id = models.CharField(
        max_length=20,  blank=True, primary_key=True)
    subcategories_name = models.CharField(max_length=200, null=False)
    status = models.CharField(max_length=5, null=True,
                              choices=STATUS_LIST, default='A', blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subcategories_name

    class Meta:
        managed = False
        db_table = 'ecom_product_sub_categories'


class Products_Brand(models.Model):
    brand_id = models.CharField(max_length=20, blank=True, primary_key=True)
    brand_name = models.CharField(max_length=200, null=False)
    is_active = models.BooleanField(blank=True, default=True)
    is_deleted = models.BooleanField(blank=True, default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.brand_id+" "+self.brand_name

    class Meta:
        managed = False
        db_table = 'sales_products_brand'


class Ecom_Products(models.Model):
    product_id = models.CharField(
        max_length=20, null=False, blank=True, primary_key=True)
    category_id = models.ForeignKey(Ecom_Product_Categories, on_delete=models.PROTECT,
                                    related_name='product_category', db_column='category_id')
    sub_category_id = models.ForeignKey(Ecom_Product_Sub_Categories, on_delete=models.PROTECT,
                                        related_name='sub_product_category', db_column='sub_category_id')
    product_brand_id = models.ForeignKey(
        Products_Brand, on_delete=models.PROTECT, related_name='product_brand', db_column='product_brand_id')
    product_name = models.CharField(max_length=200)
    product_model = models.CharField(max_length=200, blank=True, null=True)
    product_group = models.CharField(max_length=200, blank=True, null=True)
    product_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    discount_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    product_old_price = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00, blank=True, null=True)
    product_description = HTMLField(blank=True, null=True)
    product_feature = models.CharField(max_length=500, blank=True, null=True)
    #product_specification=models.JSONField(blank=True, null=True)
    product_specification = models.CharField(
        max_length=1000, blank=True, null=True)
    product_keyword = models.CharField(max_length=400, blank=True, null=True)
    product_viewcount = models.IntegerField(blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'ecom_products'


class Product_Images(models.Model):
    product_id = models.ForeignKey(
        Ecom_Products, on_delete=models.PROTECT, related_name='product_images', db_column='product_id')
    image = models.ImageField(
        upload_to='product_image/', blank=True, null=True)
    image_serial = models.IntegerField(default=1)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
        super(Product_Images, self).delete(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'ecom_product_images'


class Ecom_Slider(models.Model):
    title = models.CharField(max_length=100)
    second_title = models.CharField(max_length=200, null=True, blank=True)
    button_up_title = models.CharField(max_length=80, null=True, blank=True)
    button_one_label = models.CharField(max_length=50, null=True, blank=True)
    button_one_icon = models.CharField(max_length=300, null=True, blank=True)
    button_one_url = models.CharField(max_length=300, null=True, blank=True)
    button_two_label = models.CharField(max_length=50, null=True, blank=True)
    button_two_icon = models.CharField(max_length=300, null=True, blank=True)
    button_two_url = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField(
        upload_to='product_image/', blank=True, null=True)
    status = models.IntegerField(default=1)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
        super(Ecom_Slider, self).delete(*args, **kwargs)
    class Meta:
        managed = False
        db_table = 'ecom_ecom_slider'

class PageModel(models.Model):
    title = models.CharField(max_length=50)
    content = HTMLField(verbose_name='HTML Content')
    publish_status = models.IntegerField(default=1, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        managed = False
        db_table = 'ecom_ecom_pagemodel'

