from django.urls import path

##### For Image Upload
from django.conf import settings
from django.conf.urls.static import static

from sales.views import *
from sales.report_views import *
from finance.views import finance_transaction_typelist, finance_choice_accountslist, finance_get_account_infobyacnumber
from .views import *

urlpatterns = [
     path('ecom-order-list/', ecom_orderlist_view.as_view(), name='ecom-order-list'),
     path('ecom-order-details/<slug:order_number>', ecom_order_details, name='ecom-order-details'),
     path('ecom-order-accept/<slug:order_number>', ecom_order_accept, name='ecom-order-accept'),
     path('ecom-order-details-update', ecom_order_details_update, name='ecom-order-details-update'),
     #Ecom Product Category
     path('ecom-product-categories-createlist', ecom_product_cat_view.as_view(), name='ecom-product-categories-createlist'),
     path('ecom-product-categories-insert', ecom_product_cat_insert, name='ecom-product-categories-insert'),
     path('ecom-product-category-edit/<slug:id>', ecom_product_cat_edit, name='ecom-product-category-edit'),

     #Ecom Product Sub Category
     path('ecom-product-subcategories-createlist', ecom_product_subcat_view.as_view(), name='ecom-product-subcategories-createlist'),
     path('ecom-product-subcategories-insert', ecom_product_subcat_insert, name='ecom-product-subcategories-insert'),
     path('ecom-product-subcategory-edit/<slug:id>', ecom_product_subcat_edit, name='ecom-product-subcategory-edit'),

     #Ecom Products
     path('ecom-product-createlist', ecom_product_view.as_view(), name='ecom-product-createlist'),
     path('ecom-products-list', ecom_products_list, name='ecom-products-list'),
     path('ecom-product-add', ecom_product_add, name='ecom-product-add'),
     path('ecom-product-vieworedit/<slug:id>', ecom_product_vieworedit.as_view(), name='ecom-product-vieworedit'),
     path('ecom-product-edit', ecom_product_edit, name='ecom-product-edit'),
     path('ecom-product-image-insert', ecom_product_image_insert, name='ecom-product-image-insert'),
     path('ecom-product-image-delete', ecom_product_image_delete, name='ecom-product-image-delete'),
     #Slider
     path('ecom-slider-createlist', ecom_slider_view.as_view(), name='ecom-slider-createlist'),
     path('ecom-slider-create', ecom_slider_create, name='ecom-slider-create'),
     path('ecom-slider-edit/<slug:id>', ecom_slider_edit, name='ecom-slider-edit'),
     path('ecom-slider-image-insert', ecom_slider_image_insert, name='ecom-slider-image-insert'),
     
     path('ecom-page-create', PageCreateView.as_view(), name='ecom-page-create'),
     path('ecom-page-list', ecom_page_list.as_view(), name='ecom-page-list'),
     path('ecom-edit-page/<slug:id>', ecom_edit_page, name='ecom-edit-page'),

]
#### For Image Upload
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    