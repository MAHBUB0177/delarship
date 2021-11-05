from django.db import models

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
    customer = models.CharField(max_length=15,blank=True)
    full_name = models.CharField(max_length=200,blank=True,null=True)
    mobile = models.CharField(max_length=15,blank=True,null=True)
    email = models.CharField(max_length=200,blank=True,null=True)
    address_1= models.CharField(max_length=300,blank=True,null=True)
    address_2= models.CharField(max_length=300,blank=True,null=True)
    distric_id= models.CharField(max_length=6,blank=True,null=True)
    upazilla_id= models.CharField(max_length=6,blank=True,null=True)
    zip_code= models.CharField(max_length=10,blank=True,null=True)
    use_count= models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        managed = False
        db_table = 'ecom_delivery_address'


class Ecom_Order_Master(models.Model):
    order_number = models.CharField(max_length=20, primary_key=True)
    delivery_address_id= models.ForeignKey(Ecom_Delivery_Address, on_delete=models.CASCADE, related_name='delivery_address_id', db_column='delivery_address_id', blank=True, null=True)
    delivery_charge = models.CharField(max_length=20,blank=True,null=True)
    order_date = models.DateTimeField()
    customer_id = models.IntegerField(blank=True,null=True)
    account_number = models.CharField(max_length=200,blank=True,null=True)
    customer_name = models.CharField(max_length=200,blank=True,null=True)
    customer_phone = models.CharField(max_length=20,blank=True,null=True)
    customer_address = models.CharField(max_length=500,blank=True,null=True)
    executive_phone = models.CharField(max_length=20,blank=True,null=True)
    coupon_code = models.CharField(max_length=20, blank=True,null=True)
    total_quantity = models.IntegerField(blank=True)
    returned_quantity = models.IntegerField(null=True, blank=True, default=0)
    bill_amount = models.DecimalField(max_digits=22,decimal_places=2,default=0.00, blank=True)
    discount_amount = models.DecimalField(max_digits=22,decimal_places=2,default=0.00, blank=True)
    payment_method = models.CharField(max_length=20,blank=True,null=True)
    pay_amount = models.DecimalField(max_digits=22,decimal_places=2,default=0.00, blank=True)
    due_amount = models.DecimalField(max_digits=22,decimal_places=2,default=0.00, blank=True)
    advance_pay = models.DecimalField(max_digits=22,decimal_places=2,default=0.00, blank=True)
    status =  models.CharField(max_length=2, choices=ORDER_STATUS, default='N',null=True, blank=True)
    order_comments = models.TextField(blank=True,null=True)
    latitude = models.DecimalField(max_digits=22, decimal_places=12, null=True, blank=True )
    longitude = models.DecimalField(max_digits=22, decimal_places=12, null=True, blank=True )
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'ecom_order_master'

