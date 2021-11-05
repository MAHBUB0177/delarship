from django.urls import path

##### For Image Upload
from django.conf import settings
from django.conf.urls.static import static

from .views import *
from .report_views import *
from finance.views import finance_transaction_typelist, finance_choice_accountslist, finance_get_account_infobyacnumber, finance_client_typelist
from appauth.views import appauth_choice_employeelist

urlpatterns = [
     path('delar-center-createlist', delar_center_view.as_view(), name='delar-center-createlist'),
     path('delar-center-insert', delar_center_insert, name='delar-center-insert'),
     path('delar-center-edit/<slug:id>', delar_center_edit, name='delar-center-edit'),
     path('delar-choice-centerlist', delar_choice_centerlist, name='delar-choice-centerlist'),
     path('delar-clientcenter-transfer', delar_clientcenter_transfer.as_view(), name='delar-clientcenter-transfer'),
     path('delar-clientcenter-transfer-insert', delar_clientcenter_transfer_insert, name='delar-clientcenter-transfer-insert'),
     path('delar-sales-create', delar_sales_create_view.as_view(), name='delar-sales-create'),
     path('delar-salesdetails-entry', delar_details_entry, name='delar-salesdetails-entry'),
     path('delar-salesdetails-edit/<int:id>', delar_details_edit, name='delar-salesdetails-edit'),
     path('delar-salesdetails-delete/<int:id>', delar_details_delete, name='delar-salesdetails-delete'),
     path('delar-salesdetails-clear', delar_details_clear, name='delar-salesdetails-clear'),
     path('delar-invoice-post', delar_post_sales, name='delar-invoice-post'),
     path('delar-invoice-list', delar_invoice_list.as_view(), name='delar-invoice-list'),
     path('delar-invoice-details/<int:id>', delar_invoice_details, name='delar-invoice-details'),
     path('delar-invoice-cancel/<int:id>', delar_invoice_cancel, name='delar-invoice-cancel'),


     ###
     path('delar_sales_return_packet_view', delar_sales_return_packet_view.as_view(), name='delar_sales_return_packet_view'),
     path('delar_sales_return_packet_insert', delar_sales_return_packet_insert, name='delar_sales_return_packet_insert'),
     path('delar_sales_packet_return_edit/<slug:id>', delar_sales_packet_return_edit, name='delar_sales_packet_return_edit'),
     # path('delar-product-info/<slug:product_id>', get_product_information, name='delar-product-info'),
     path('delar-invoice-return-list', delar_packet_return_invoice_list.as_view(), name='delar-invoice-return-list'),
     path('delar-invoice-return-details/<int:id>', delar_invoice_return_details, name='delar-invoice-return-details'),
     path('delar-invoice-return-cancel/<int:id>', delar_invoice_return_cancel, name='delar-invoice-return-cancel'),
    
     

     path('delar-sr-target',delar_sales_sr.as_view(),name='delar-sr-target'),
     path('delar_sr_purchase_details_insert',sales_sr_purchase_details_insert,name='delar_sr_purchase_details_insert'),
     path('delar_sr_target-post',delar_sr_target_post,name='delar_sr_target-post'),
     path('delar_sr_target-delate/<int:id>',delar_delete_temp_stock_data,name='delar_sr_target-delate'),
    

     
    


     #############
     
]
#### For Image Upload  
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    