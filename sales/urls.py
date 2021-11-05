from django.urls import path

##### For Image Upload
from django.conf import settings
from django.conf.urls.static import static

from sales.views import *
from sales.report_views import *
from finance.views import finance_transaction_typelist, finance_choice_accountslist, finance_get_account_infobyacnumber, finance_client_typelist
from delar.views import delar_choice_centerlist
from appauth.views import appauth_choice_employeelist

urlpatterns = [
     path('sales-choice-trantype/', finance_transaction_typelist, name='sales-choice-trantype'),
     path('sales-choice-accountslist', finance_choice_accountslist, name='sales-choice-accountslist'),
     path('sales-choice-clientsproduct/', sales_choice_clientsproductlist, name='sales-choice-clientsproduct'),
     path('sales-choice-clienttype/', finance_client_typelist, name='sales-choice-clienttype'),
     path('sales-choice-centerlist/', delar_choice_centerlist, name='sales-choice-centerlist'),
     path('sales-choice-supplierlist/', sales_choice_supplierlist, name='sales-choice-supplierlist'),
     path('sales-choice-employeelist/', appauth_choice_employeelist, name='sales-choice-employeelist'),
     path('sales-choice-productgrouplist/', sales_choice_productgrouplist, name='sales-choice-productgrouplist'),
     path('sales-choice-productbrandlist/', sales_choice_productbrandlist, name='sales-choice-productbrandlist'),
     path('sales-account-byacnumber/<slug:account_number>', finance_get_account_infobyacnumber, name='sales-account-byacnumber'),
     path('sales-clients-createlist', sales_clients_view.as_view(), name ='sales-clients-createlist'),
     path('sales-clients-insert', sales_clients_insert, name='sales-clients-insert'),
     path('sales-clients-edit/<slug:id>', sales_clients_edit, name='sales-clients-edit'),
     path('sales-clients-list', sales_clientlist_view.as_view(), name='sales-clients-list'),
     path('sales-clientid-change', sales_clientid_change.as_view(), name ='sales-clientid-change'),
     path('sales-clientid-change-insert', sales_clientid_change_insert, name='sales-clientid-change-insert'),
     path('sales-client-closing', sales_clientclosing_view.as_view(), name ='sales-client-closing'),
     path('sales-client-closing-insert', sales_clientclosing_insert, name='sales-client-closing-insert'),
     path('sales-client-closing-remove', sales_clientclosing_remove, name='sales-client-closing-remove'),
     path('sales-image-upload', sales_image_upload.as_view(), name ='sales-image-upload'),
     path('sales-show-image/<slug:phone_number>', sales_show_image, name='sales-show-image'),
     path('sales-supplier-createlist', sales_supplier_view.as_view(), name='sales-supplier-createlist'),
     path('sales-supplier-insert', sales_supplier_insert, name='sales-supplier-insert'),
     path('sales-supplier-edit/<slug:id>', sales_supplier_edit, name='sales-supplier-edit'),
     path('sales-productgroup-createlist', sales_productgroup_view.as_view(), name='sales-productgroup-createlist'),
     path('sales-productgroup-insert', sales_productgroup_insert, name='sales-productgroup-insert'),
     path('sales-productgroup-edit/<slug:id>', sales_productgroup_edit, name='sales-productgroup-edit'),
     path('sales-productbrand-createlist', sales_productbrand_view.as_view(), name='sales-productbrand-createlist'),
     path('sales-productbrand-insert', sales_productbrand_insert, name='sales-productbrand-insert'),
     path('sales-productbrand-edit/<slug:id>', sales_productbrand_edit, name='sales-productbrand-edit'),

     path('sales-productunit-createlist', sales_productunit_view.as_view(), name='sales-productunit-createlist'),
     path('sales-productunit-insert', sales_productunit_insert, name='sales-productunit-insert'),
     path('sales-productunit-edit/<slug:id>', sales_productunit_edit, name='sales-productunit-edit'),

     path('sales-products-createlist', sales_products_view.as_view(), name='sales-products-createlist'),
     path('sales-products-insert', sales_products_insert, name='sales-products-insert'),
     path('sales-products-edit/<slug:id>', sales_products_edit, name='sales-products-edit'),
     path('sales-products-balance', sales_product_balance.as_view(), name='sales-products-balance'),
     path('sales-products-list', sales_product_list.as_view(), name='sales-products-list'),
     path('sales-product-price', sales_product_price, name='sales-product-price'),
     path('sales-product-purchaserate', sales_product_purchase_rate, name='sales-product-purchaserate'),
     path('sales-product-info/<slug:product_code>', get_product_info, name='sales-product-info'),
     path('sales-purchase-master', sales_purchase_view.as_view(), name='sales-purchase-master'),
     path('sales-quickpurchase-master', sales_quickpurchase_view.as_view(), name='sales-quickpurchase-master'),
     path('sales-purchase-dtlsinsert', sales_purchase_details_insert, name='sales-purchase-dtlsinsert'),
     path('sales-stocktemp-delete/<int:id>', sales_delete_temp_stock_data, name='sales-stocktemp-delete'),
     path('sales-purchase-post', sales_purchase_post, name='sales-purchase-post'),
     path('sales-quickpurchase-post', sales_quickpurchase_post, name='sales-quickpurchase-post'),
     path('sales-purchase-approval', sales_purchase_approval.as_view(), name='sales-purchase-approval'),
     path('sales-purchase-payment/<int:id>', sales_purchase_payment, name='sales-purchase-payment'),
     path('sales-purchase-reject/<int:id>', sales_purchase_reject, name='sales-purchase-reject'),
     path('sales-purchase-list', sales_purchase_list.as_view(), name='sales-purchase-list'),
     path('sales-purchase-details/<int:id>', sales_purchase_details, name='sales-purchase-details'),
     path('sales-purchase-return/<int:id>', sales_purchase_return, name='sales-purchase-return'),
     path('sales-purchase-cancel/<int:id>', sales_purchase_cancel, name='sales-purchase-cancel'),
     path('sales-purchase-returnproduct', sales_purchase_returnproduct.as_view(), name='sales-purchase-returnproduct'),
     path('sales-purchase-returnproduct-insert', sales_purchase_returnproduct_insert, name='sales-purchase-returnproduct-insert'),
     path('sales-purchasereturn-list', sales_purchasereturn_list.as_view(), name='sales-purchasereturn-list'),
     path('sales-purchasereturn-entrydetails', sales_purchasereturn_entrydetails, name='sales-purchasereturn-entrydetails'),
     path('sales-purchasereturn-cancel/<int:id>', sales_purchasereturn_cancel, name='sales-purchasereturn-cancel'),
     path('sales-damage-entry', sales_product_damage.as_view(), name='sales-damage-entry'),
     path('sales-damage-entry-insert', sales_product_damage_insert, name='sales-damage-entry-insert'),
     path('sales-damage-list', sales_damage_list.as_view(), name='sales-damage-list'),
     path('sales-damage-entrydetails', sales_damage_entrydetails, name='sales-damage-entrydetails'),
     path('sales-damage-cancel/<int:id>', sales_damage_cancel, name='sales-damage-cancel'),
     path('sales-sales-create', sales_sales_create_view.as_view(), name='sales-sales-create'),
     path('sales-details-entry', sales_details_entry, name='sales-details-entry'),
     path('sales-details-edit/<int:id>', sales_details_edit, name='sales-details-edit'),
     path('sales-details-delete/<int:id>', sales_details_delete, name='sales-details-delete'),
     path('sales-details-clear', sales_details_clear, name='sales-details-clear'),
     path('sales-invoice-post', sales_post_sales, name='sales-invoice-post'),
     path('sales-invoice-list', sales_invoice_list.as_view(), name='sales-invoice-list'),
     path('sales-invoice-details/<int:id>', sales_invoice_details, name='sales-invoice-details'),
     path('sales-invoice-return/<int:id>', sales_invoice_return, name='sales-invoice-return'),
     path('sales-invoice-cancel/<int:id>', sales_invoice_cancel, name='sales-invoice-cancel'),
     path('sales-invoicereturn-list', sales_invoicereturn_list.as_view(), name='sales-invoicereturn-list'),
     path('sales-invoicereturn-entrydetails', sales_invoicereturn_entrydetails, name='sales-invoicereturn-entrydetails'),
     path('sales-invoicereturn-cancel/<int:id>', sales_invoicereturn_cancel, name='sales-invoicereturn-cancel'),
     path('sales-sales-return', Sales_Return_View.as_view(), name='sales-sales-return'),
     path('sales-return-insert', sales_return_insert, name='sales-return-insert'),
     path('sales-quick-sales', sales_quick_sales_view.as_view(), name='sales-quick-sales'),
     path('sales-invoice-info/<slug:product_code>/<slug:invoice_number>', get_invoice_details, name='sales-invoice-info'),
     path('sales-emisetup-createlist', sales_emisetup_view.as_view(), name='sales-emisetup-createlist'),
     path('sales-emisetup-insert', sales_emisetup_insert, name='sales-emisetup-insert'),
     path('sales-emifees-fee', sales_emi_insurance_fee, name='sales-emifees-fee'),
     path('sales-emisetup-cancel/<int:id>', sales_emisetup_cancel, name='sales-emisetup-cancel'),
     path('sales-invoice-summary/<slug:invoice_number>', get_invoice_summary, name='sales-invoice-summary'),
     path('sales-choice-emiinvoice/', sales_choice_emiinvoicelist, name='sales-choice-emiinvoice'),
     path('sales-choice-emiinvoiceall/', sales_choice_emiinvoicelistall, name='sales-choice-emiinvoiceall'),
     path('sales-emi-details', sales_emi_details, name='sales-emi-details'),
     path('sales-emimat-date/<slug:emi_freq>/<slug:inst_number>/<slug:from_date>', sales_emi_maturity_date, name='sales-emimat-date'),
     path('sales-emimat-date/<slug:emi_freq>/<slug:inst_number>/', sales_emi_maturity_date_fromcbd, name='sales-emimat-date'),
     path('sales-emircv-view', sales_emircv_view.as_view(), name='sales-emircv-view'),
     path('sales-emircv-insert', sales_emircv_insert, name='sales-emircv-insert'),
     path('sales-emircv-edit/<int:id>', sales_emircv_edit, name='sales-emircv-edit'),
     path('sales-emircv-cancel/<int:id>', sales_emircv_cancel, name='sales-emircv-cancel'),
     path('sales-emihist-list', sales_emihist_list.as_view(), name='sales-emihist-list'),
     path('sales-order-create', sales_order_create_view.as_view(), name='sales-order-create'),
     path('sales-order-post', sales_post_order, name='sales-order-post'),
     path('sales-order-list', OrderListView.as_view(), name='sales-order-list'),
     path('sales-order-details/<int:id>', sales_order_details, name='sales-order-details'),
     path('sales-order-accept/<int:id>', sales_order_accept, name='sales-order-accept'),
     path('sales-order-cancel/<int:id>', sales_order_cancel, name='sales-order-cancel'),
     path('sales-order-details-update', sales_order_details_update, name='sales-order-details-update'),
     path('sales-order-clear', sales_details_clear, name='sales-order-clear'),
     path('sales-invoice-print-view', sales_invoice_html_report.as_view(), name='sales-invoice-print-view'),
     path('sales-report-stockinventory', sales_report_stockinventory.as_view(), name='sales-report-stockinventory'),
     path('sales-report-stockinventory-print-view', sales_report_stockinventory_print_view.as_view(), name='sales-report-stockinventory-print-view'),
     path('sales-report-daywisepurchase', sales_report_daywisepurchase.as_view(), name='sales-report-daywisepurchase'),
     path('sales-report-daywisepurchase-print-view', sales_report_daywisepurchase_print_view.as_view(), name='sales-report-daywisepurchase-print-view'),
     path('sales-report-daywise-purchasenreturn', sales_report_daywise_purchasenreturn.as_view(), name='sales-report-daywise-purchasenreturn'),
     path('sales-report-daywise-purchasenreturn-print-view', sales_report_daywise_purchasenreturn_print_view.as_view(), name='sales-report-daywise-purchasenreturn-print-view'),
     path('sales-report-daywise-purchasenreturnstmt', sales_report_daywise_purchasenreturnstmt.as_view(), name='sales-report-daywise-purchasenreturnstmt'),
     path('sales-report-daywise-purchasenreturnstmt-print-view', sales_report_purchasenreturnstmt_print_view.as_view(), name='sales-report-daywise-purchasenreturnstmt-print-view'),
     path('sales-report-invoice', sales_report_invoice.as_view(), name='sales-report-invoice'),
     path('sales-report-daywisesales', sales_report_daywisesales.as_view(), name='sales-report-daywisesales'),
     path('sales-report-daywisesales-print-view', sales_report_daywisesales_print_view.as_view(), name='sales-report-daywisesales-print-view'),
     path('sales-report-daywise-salesnreturn', sales_report_daywise_salesnreturn.as_view(), name='sales-report-daywise-salesnreturn'),
     path('sales-report-daywise-salesnreturn-print-view', sales_report_daywise_salesnreturn_print_view.as_view(), name='sales-report-daywise-salesnreturn-print-view'),
     path('sales-report-daywise-salesnreturnstmt', sales_report_daywise_salesnreturnstmt.as_view(), name='sales-report-daywise-salesnreturnstmt'),
     path('sales-report-daywise-salesnreturnstmt-print-view', sales_report_daywise_salesnreturnstmt_print_view.as_view(), name='sales-report-daywise-salesnreturnstmt-print-view'),
     path('sales-report-profitnloss', sales_report_profitnloss.as_view(), name='sales-report-profitnloss'),
     path('sales-report-profitnloss-print-view', sales_report_profitnloss_print_view.as_view(), name='sales-report-profitnloss-print-view'),
     path('sales-report-salesdetails', sales_report_salesdetails.as_view(), name='sales-report-salesdetails'),
     path('sales-report-salesdetails-print-view', sales_report_salesdetails_print_view.as_view(), name='sales-report-salesdetails-print-view'),
     path('sales-report-centersalesdetails', sales_report_centersalesdetails.as_view(), name='sales-report-centersalesdetails'),
     path('sales-report-centersalesdetails-print-view', sales_report_centersalesdetails_print_view.as_view(), name='sales-report-centersalesdetails-print-view'),
     path('sales-report-emidetails', sales_report_emidetails.as_view(), name='sales-report-emidetails'),
     path('sales-report-emidetails-print-view', sales_report_emidetails_print_view.as_view(), name='sales-report-emidetails-print-view'),



  
     ################
     path('sales-purchase-order-view', sales_purchase_order_view.as_view(), name='sales-purchase-order-view'),
     path('sales-purchase-order-details-insert', sales_purchase_order_details_insert, name='sales-purchase-order-details-insert'),
     path('sales-prordertemp-delete/<int:id>', sales_delete_temp_prorder_data, name='sales-prordertemp-delete'),
     path('sales-purchase-order-post', sales_purchase_order_post, name='sales-purchase-order-post'),
     path('sales-purchase-order-approval', sales_purchase_order_approval.as_view(), name='sales-purchase-order-approval'),
     path('sales-purchase-order-payment/<int:id>', sales_purchase_order_payment, name='sales-purchase-order-payment'),
     path('sales-purchase-order-reject/<int:id>', sales_purchase_order_reject, name='sales-purchase-order-reject'),
     


     path('sales-branch-transfer-view', sales_branch_transfer_view.as_view(), name='sales-branch-transfer-view'),
     path('sales-branch-transfer-insert', sales_branch_transfer_insert, name='sales-branch-transfer-insert'),
     path('sales-branch-transfer-edit/<int:id>', sales_branch_transfer_edit, name='sales-branch-transfer-edit'),

     path('sales-invoice-return-allocate-list', sales_invoice_return_allocate_list.as_view(), name='sales-invoice-return-allocate-list'),
     path('sales-invoice-return-allocatedetails', sales_invoice_return_allocate_details, name='sales-invoice-return-allocatedetails'),
     path('sales_invoice_allocate_details_return', sales_invoice_allocate_details_return, name='sales_invoice_allocate_details_return'),
     ##########report#####
     
     path('sales-report-packet-return', sales_report_packet_return.as_view(), name='sales-report-packet-return'),
     path('sales-report-packet-return-print-view', sales_report_packet_return_print_view.as_view(), name='sales-report-packet-return-print-view'),

     path('sales-details-report', sales_details_report.as_view(), name='sales-details-report'),
     path('sales-details-report-print-view', sales_details_report_print_view.as_view(), name='sales-details-report-print-view'),

     path('sales-allocate-quantity-report', sales_allocate_report.as_view(), name='sales-allocate-quantity-report'),
     path('sales-allocate-quantity-report-print-view', sales_allocate_report_print_view.as_view(), name='sales-allocate-quantity-report-print-view'),

     path('sales-order-report', sales_order_invoice.as_view(), name='sales-order-report'),
     path('sales-order-report-print-view', sales_order_invoice_html_report.as_view(), name='sales-order-report-print-view'),
     #Barcode
     path('sales-products-barcode', sales_product_barcode, name='sales-products-barcode'),
     # path('sales-products-barcode-html', sales_product_barcode_html, name='sales-products-barcode-html'),
     # path('sales-products-barcode-pdf', sales_product_barcode_pdf, name='sales-products-barcode-pdf'),
     path('sales-products-barcode-pdf-gen', sales_product_barcode_pdf_gen, name='sales-products-barcode-pdf-gen'),
     path('sales-pos-sales', sales_sales_pos_view.as_view(), name='sales-pos-sales'),
     path('sales-posproductby-group/<slug:id>', sales_pos_productslist_bygroup, name='sales-posproductby-group'),
     path('sales-postemp-update/<slug:id>', sales_pos_temp_update, name='sales-postemp-update'),
     path('sales-postemp-update', sales_pos_temp_update, name='sales-postemp-update'),

     path('sales-quatation-master-view', sales_quation_master_view.as_view(), name='sales-quatation-master-view'),
     path('sales-quatation-master-insert', sales_quation_master_insert, name='sales-quatation-master-insert'),
     path('sales-quatation-dtl-insert', sales_quation_dtl_insert, name='sales-quatation-dtl-insert'),


     #########report#########
     path('sales-quatation_report', sales_report_quatation_view.as_view(), name='sales-quatation_report'),
     path('sales-quation-print-view', sales_report_quatation_print_view.as_view(), name='sales-quation-print-view'),

]
#### For Image Upload  
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    