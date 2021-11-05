from django.urls  import path

from .views import *

urlpatterns = [
    path('apifinance-ledger-api/', General_Ledger_ApiView.as_view(), name='apifinance-ledger-api'),
    path('apifinance-trantype-api/', Transaction_Type_ApiView.as_view(), name='apifinance-trantype-api'),
    path('apifinance-trantypeledger-api/', Ledger_Transaction_Type_ApiView.as_view(), name='apifinance-trantypeledger-api'),
    path('apifinance-cashnbankledger-api/', Cash_And_Bank_Ledger_ApiView.as_view(), name='apifinance-cashnbankledger-api'),
    path('apifinance-accounttype-api/', Account_Type_ApiView.as_view(), name='apifinance-accounttype-api'),
    path('apifinance-clienttype-api/', Client_Type_ApiView.as_view(), name='apifinance-clienttype-api'),
    path('apifinance-clientacmap-api/', Client_Account_Mapping_ApiView.as_view(), name='apifinance-clientacmap-api'),
    path('apifinance-trantable-api/', Transaction_Table_ApiView.as_view(), name='apifinance-trantable-api'), 
    path('apifinance-tranlist-api/', Transaction_Master_ApiView.as_view(), name='apifinance-tranlist-api'),
    path('apifinance-querytable-api/',  Finance_Query_Table_ApiView.as_view(), name='apifinance-querytable-api'),
    path('apifinance-accounts-search/',  Search_Accounts_ApiView.as_view(), name='apifinance-accounts-search'),
    path('apifinance-accountsname-search/',  Search_Accounts_Name_ApiView.as_view(), name='apifinance-accountsname-search'),
    path('apifinance-accounts-api/',  Accounts_Balance_ApiView.as_view(), name='apifinance-accounts-api'),
    path('apifinance-telbaltrf-api/',  Tran_Telbal_Details_ApiView.as_view(), name='apifinance-telbaltrf-api'),
    path('apifinance-depositreceive-api/',  Deposit_Receive_ApiView.as_view(), name='apifinance-depositreceive-api'),
    path('apifinance-depositpayment-api/',  Deposit_Payment_ApiView.as_view(), name='apifinance-depositpayment-api'),
    path('apifinance-depositclosing-api/',  Deposit_Closing_ApiView.as_view(), name='apifinance-depositclosing-api'),
    path('apifinance-deposittransfer-api/',  Deposit_Transfer_ApiView.as_view(), name='apifinance-deposittransfer-api'),
    path('apifinance-charges-api/',  Charges_ApiView.as_view(), name='apifinance-charges-api'),
]