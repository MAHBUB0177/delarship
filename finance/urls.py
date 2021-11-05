from django.urls import path

##### For Image Upload
from django.conf import settings
from django.conf.urls.static import static

from .views import *
from .report_views import *
from delar.views import delar_choice_centerlist

urlpatterns = [
     path('finance-choice-centerlist/', delar_choice_centerlist, name='finance-choice-centerlist'),
     path('finance-ledger-create/', finance_ledger_view.as_view(), name ='finance-ledger-create' ),
     path('finance-ledger-insert', finance_ledger_insert , name='finance-ledger-insert'),
     path('finance-ledger-edit/<slug:id>', finance_ledger_edit, name='finance-ledger-edit'),
     path('finance-trantype-createlist/', finance_trantype_view.as_view(), name ='finance-trantype-createlist' ),
     path('finance-trantype-insert', finance_trantype_insert , name='finance-trantype-insert'),
     path('finance-trantype-edit/<slug:id>', finance_trantype_edit, name='finance-trantype-edit'),
     path('finance-trantypeledger-createlist/', finance_trantypeledger_view.as_view(), name ='finance-trantypeledger-createlist' ),
     path('finance-trantypeledger-insert', finance_trantypeledger_insert , name='finance-trantypeledger-insert'),
     path('finance-trantypeledger-edit/<slug:id>', finance_trantypeledger_edit, name='finance-trantypeledger-edit'),
     path('finance-cashnbankledger-createlist/', finance_cashnbankledger_view.as_view(), name ='finance-cashnbankledger-createlist' ),
     path('finance-cashnbankledger-insert', finance_cashnbankledger_insert , name='finance-cashnbankledger-insert'),
     path('finance-cashnbankledger-edit/<slug:id>', finance_cashnbankledger_edit, name='finance-cashnbankledger-edit'),
     path('finance-accounttype-createlist/', finance_accounttype_view.as_view(), name ='finance-accounttype-createlist' ),
     path('finance-accounttype-insert', finance_accounttype_insert , name='finance-accounttype-insert'),
     path('finance-accounttype-edit/<slug:id>', finance_accounttype_edit, name='finance-accounttype-edit'),
     path('finance-charges-createlist/', finance_charges_view.as_view(), name ='finance-charges-createlist' ),
     path('finance-charges-insert', finance_charges_insert , name='finance-charges-insert'),
     path('finance-charges-edit/<slug:id>', finance_charges_edit, name='finance-charges-edit'),
     path('finance-clienttype-createlist/', finance_clienttype_view.as_view(), name ='finance-clienttype-createlist' ),
     path('finance-clienttype-insert', finance_clienttype_insert , name='finance-clienttype-insert'),
     path('finance-clienttype-edit/<slug:id>', finance_clienttype_edit, name='finance-clienttype-edit'),
     path('finance-clientacmap-createlist/', finance_clientacmap_view.as_view(), name ='finance-clientacmap-createlist' ),
     path('finance-clientacmap-insert', finance_clientacmap_insert , name='finance-clientacmap-insert'),
     path('finance-clientacmap-edit/<slug:id>', finance_clientacmap_edit, name='finance-clientacmap-edit'),
     path('finance-ledger-transaction', finance_ledger_transaction.as_view(), name='finance-ledger-transaction'),
     path('finance-account-transaction', finance_account_transaction.as_view(), name='finance-account-transaction'),
     path('finance-transaction-post', finance_transaction_post, name='finance-transaction-post'),
     path('finance-depositreceive-createlist', finance_deposit_receive_view.as_view(), name='finance-depositreceive-createlist'),
     path('finance-depositreceive-insert', finance_deposit_receive_insert, name='finance-depositreceive-insert'),
     path('finance-depositreceive-cancel/<int:id>', finance_deposit_receive_cancel, name='finance-depositreceive-cancel'),
     path('finance-depositpayment-createlist', finance_deposit_payment_view.as_view(), name='finance-depositpayment-createlist'),
     path('finance-depositpayment-insert', finance_deposit_payment_insert, name='finance-depositpayment-insert'),
     path('finance-depositpayment-cancel/<int:id>', finance_deposit_payment_cancel, name='finance-depositpayment-cancel'),
     path('finance-deposittransfer-createlist', finance_deposit_transfer_view.as_view(), name='finance-deposittransfer-createlist'),
     path('finance-deposittransfer-insert', finance_deposit_transfer_insert, name='finance-deposittransfer-insert'),
     path('finance-deposittransfer-cancel/<int:id>', finance_deposit_transfer_cancel, name='finance-deposittransfer-cancel'),

     path('finance-depositclosing-createlist', finance_deposit_closing_view.as_view(), name='finance-depositclosing-createlist'),
     path('finance-depositclosing-insert', finance_deposit_closing_insert, name='finance-depositclosing-insert'),
     path('finance-depositclosing-cancel/<int:id>', finance_deposit_closing_cancel, name='finance-depositclosing-cancel'),
     path('finance-choice-trantype/', finance_transaction_typelist, name='finance-choice-trantype'),
     path('finance-choice-clienttype/', finance_client_typelist, name='finance-choice-clienttype'),
     path('finance-choice-trantypeledger/', finance_transaction_ledgerlist, name='finance-choice-trantypeledger'),
     path('finance-choice-allledgerlist/', finance_all_ledgerlist, name='finance-choice-allledgerlist'),
     path('finance-choice-branchlist/', finance_choice_branchlist, name='finance-choice-branchlist'),
     path('finance-choice-accounttype/', finance_account_typelist, name='finance-choice-accounttype'),
     path('finance-choice-cashnbanklist/', finance_choice_cashnbank_list, name='finance-choice-cashnbanklist'),
     path('finance-choice-accountslist', finance_choice_accountslist, name='finance-choice-accountslist'),
     path('finance-account-byacnumber/<slug:account_number>', finance_get_account_infobyacnumber, name='finance-account-byacnumber'),
     path('finance-account-clientbalance/<slug:client_id>', finance_get_client_account_balance, name='finance-account-clientbalance'),
     path('finance-transaction-list', finance_transaction_list.as_view(), name='finance-transaction-list'),
     path('finance-transaction-details-list', finance_transaction_details_list, name='finance-transaction-details-list'),
     path('finance-transaction-cancel/<int:id>', finance_tranbatch_cancel, name='finance-transaction-cancel'),
     path('finance-transaction-query', finance_transaction_query.as_view(), name='finance-transaction-query'),
     path('finance-transaction-query-submit', finance_transaction_details_query_submit, name='finance-transaction-query-submit'),
     path('finance-transaction-query-cancel/<int:id>', finance_transaction_query_cancel, name='finance-transaction-query-cancel'),
     path('finance-accounts-balance', finance_account_balance_query.as_view(), name='finance-accounts-balance'),
     path('finance-actran-details', finance_actran_details.as_view(), name='finance-actran-details'),
     path('finance-accounts-statement/<slug:account_number>/<slug:tran_from_date>/<slug:tran_upto_date>', finance_account_statement, name='finance-accounts-statement'),
     path('finance-telbaltrf-view', finance_telbaltrf_view.as_view(), name='finance-telbaltrf-view'),
     path('finance-telbaltrf-insert', finance_telbaltrf_insert , name='finance-telbaltrf-insert'),
     path('finance-telbaltrf-authlist', finance_telbaltrf_authlist.as_view(), name='finance-telbaltrf-authlist'),
     path('finance-telbaltrf-accept/<int:id>', finance_telbaltrf_accept, name='finance-telbaltrf-accept'),
     path('finance-telbaltrf-reject/<int:id>', finance_telbaltrf_reject, name='finance-telbaltrf-reject'),
     path('finance-report-account-statement-print-view', finance_report_accstmt_print_view.as_view(), name='finance-report-account-statement-print-view'),
     path('finance-report-account-balance', finance_account_balance_report.as_view(), name='finance-report-account-balance'),
     path('finance-report-account-balance-print-view', finance_report_accountbalance_print_view.as_view(), name='finance-report-account-balance-print-view'),
     path('finance-report-teller-balance', finance_report_tellerbalance.as_view(), name='finance-report-teller-balance'),
     path('finance-report-teller-balance-print-view', finance_report_tellerbalance_print_view.as_view(), name='finance-report-teller-balance-print-view'),
     path('finance-report-cashtrandetails', finance_report_cashtrandetails.as_view(), name='finance-report-cashtrandetails'),
     path('finance-report-cashtrandetails-print-view', finance_report_cashtrandetails_print_view.as_view(), name='finance-report-cashtrandetails-print-view'),
     path('finance-report-ledgerstatements', finance_report_ledgerstatements.as_view(), name='finance-report-ledgerstatements'),
     path('finance-report-ledgerstatements-print-view', finance_report_ledgerstatements_print_view.as_view(), name='finance-report-ledgerstatements-print-view'),
     path('finance-report-assetliabilities', finance_report_assetliabilities.as_view(), name='finance-report-assetliabilities'),
     path('finance-report-assetliabilities-print-view', finance_report_assetliabilities_print_view.as_view(), name='finance-report-assetliabilities-print-view'),
     path('finance-report-receiptpayment', finance_report_receiptpayment.as_view(), name='finance-report-receiptpayment'),
     path('finance-report-receiptpayment-print-view', finance_report_receiptpayment_print_view.as_view(), name='finance-report-receiptpayment-print-view'),

     path('finance-report-incomeexpenses', finance_report_incomeexpenses.as_view(), name='finance-report-incomeexpenses'),
     path('finance-report-incomeexpenses-print-view', finance_report_incomeexpenses_print_view.as_view(), name='finance-report-incomeexpenses-print-view'),
     path('finance-report-trialbalance', finance_report_trialbalance.as_view(), name='finance-report-trialbalance'),
     path('finance-report-trialbalance-print-view', finance_report_trialbalance_print_view.as_view(), name='finance-report-trialbalance-print-view'),
     path('finance-report-cashnbank', finance_report_cashnbank.as_view(), name='finance-report-cashnbank'),
     path('finance-report-cashnbank-print-view', finance_report_cashnbank_print_view.as_view(), name='finance-report-cashnbank-print-view'),
]

#### For Image Upload
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#managecollect  finance-choice-trantype 