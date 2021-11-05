from django.urls  import path

from .views import *

urlpatterns = [
    path('apidelar-center-api/',  Center_ApiView.as_view(), name='apidelar-center-api'),
    path('delar-salesdetails-api/', DelarSalesDetailsTempApiView.as_view(), name='delar-salesdetails-api'),
    path('delar-invoice-api/', DelarSalesInvoiceApiView.as_view(), name='delar-invoice-api'), 
    path('delar-return-packet-api/', DelarSalesreturnpacketApiView.as_view(), name='delar-return-packet-api'), 

    path('delar-sr_target-api/', DelarSrDetailsTempApiView.as_view(), name='delar-sr_target-api'),
]