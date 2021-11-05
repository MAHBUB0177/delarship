from django.urls  import path

from .views import *
from apifinance.views import Search_Accounts_ApiView, Search_Accounts_Name_ApiView

urlpatterns = [
    path('apisales-accounts-search/',  Search_Accounts_ApiView.as_view(), name='apisales-accounts-search'),
    path('apisales-accountsname-search/',  Search_Accounts_Name_ApiView.as_view(), name='apisales-accountsname-search'),
    path('ecom-user-cart/',  User_Chart_ApiView.as_view(), name='ecom-user-cart'),
    path('ecom-order-api/', Ecom_Order_Master_ApiView.as_view(), name='ecom-order-api'), 
    path('stock-master-api/', StockMasterAuthQAPIView.as_view(), name='stock-master-api'),
     path('purchase-master-api/', PurchaseMasterAuthQAPIView.as_view(), name='purchase-master-api'), 
    path('stock-details-api/', StockDetailsAPIView.as_view(), name='stock-details-api'), 
    path('stock-master-apisearch/', StockMasterAPIViewSearch.as_view(), name='stock-master-apisearch'),
    path('sales-products-api/', ProductsApiView.as_view(), name='sales-products-api'), 
    path('sales-details-api/', SalesDetailsTempApiView.as_view(), name='sales-details-api'),
    path('sales-invoice-api/', SalesInvoiceApiView.as_view(), name='sales-invoice-api'), 
    path('sales-invoice-detailsapi/', SalesInvoiceDetailsApiView.as_view(), name='sales-invoice-detailsapi'), 
    path('sales-clients-api/',  SalesClientsApiView.as_view(), name='sales-clients-api'), 
    path('sales-productprice-api/',  ProductPriceListApiView.as_view(), name='sales-productprice-api'),
    path('sales-productoffer-api/',  ProductOfferListApiView.as_view(), name='sales-productoffer-api'),
    path('sales-productpackage-api/',  ProductOfferPackageApiView.as_view(), name='sales-productpackage-api'),
    path('sales-clientsec-api/',  ClientSecurityApiView.as_view(), name='sales-clientsec-api'),
    path('sales-dashboard-api/',  ChartData.as_view(), name='sales-dashboard-api'),
    path('sales-order-api/', SalesOrderApiView.as_view(), name='sales-order-api'), 
    path('sales-order-detailsapi/', SalesOrderDetailsApiView.as_view(), name='sales-order-detailsapi'), 
    path('sales-dashboard-apidata/',  SalesDashboardData.as_view(), name='sales-dashboard-apidata'),
    path('sales-stockdetails-tempapi/',  StockDetailsTempApiView.as_view(), name='sales-stockdetails-tempapi'),
    path('sales-products-search/',  SearchProductListApiView.as_view(), name='sales-products-search'),
    path('sales-clients-search/',  SearchClientsListApiView.as_view(), name='sales-clients-search'),
    path('sales-productgroup-api/',  st_group_model_apiview.as_view(), name='sales-productgroup-api'),
    path('sales-productbrand-api/',  product_brand_model_apiview.as_view(), name='sales-productbrand-api'),
    path('sales-emisetup-api/',  Emi_Setup_Apiview.as_view(), name='sales-emisetup-api'),
    path('sales-emireceive-api/',  Emi_Receive_ApiView.as_view(), name='sales-emireceive-api'),
    path('sales-emihistory-api/',  Emi_History_ApiView.as_view(), name='sales-emihistory-api'),
    path('sales-showroom-api/',  showroom_model_apiview.as_view(), name='sales-showroom-api'),
    path('sales-supplier-api/',  SalesSupplierApiView.as_view(), name='sales-supplier-api'),
    path('sales-clientprofit-api/', Client_Profit_HistoryApiView.as_view(), name='sales-clientprofit-api'),

    path('sales-productunit-api/',  product_unit_model_apiview.as_view(), name='sales-productunit-api'),
    #####
    path('sales-purchase-order-tempapi/',  PurchaseDetailsTempApiView.as_view(), name='sales-purchase-order-tempapi'),
    path('sales-branch-transfer-api/',  BranchTransferApiView.as_view(), name='sales-branch-transfer-api'),
    path('sales-Quotation-api/', sales_quotation_apiview.as_view(), name='sales-Quotation-api'),
]