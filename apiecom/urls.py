from django.urls  import path

from .views import *
from apifinance.views import Search_Accounts_ApiView

urlpatterns = [
    path('ecom-product-category/',  Ecom_Product_Category_ApiView.as_view(), name='ecom-product-category'),
    path('ecom-product-subcategory/',  Ecom_Product_Subcategory_ApiView.as_view(), name='ecom-product-subcategory'),
    path('ecom-user-cart/',  User_Chart_ApiView.as_view(), name='ecom-user-cart'),
    path('ecom-order-api/', Ecom_Order_Master_ApiView.as_view(), name='ecom-order-api'), 
    path('ecom-slider-api/', Ecom_Slider_ApiView.as_view(), name='ecom-slider-api'), 
]