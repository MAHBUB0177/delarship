"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var table_data
var edit_stock_id

var fn_data_table =
    function () {
        function fn_data_table() {
            _classCallCheck(this, fn_data_table);

            this.init();
        }

        _createClass(fn_data_table, [{
            key: "init",
            value: function init() {
                this.table = this.table();
            }
        }, {
            key: "table",
            value: function table() {
                var products_type = document.getElementById('id_products_type').value;
                var account_number = document.getElementById('id_account_number').value;
                var phone_number = document.getElementById('id_phone_number').value;
                var branch_code = document.getElementById('id_branch_code').value;
                var search_url = "/apifinance-accounts-api/?account_number=" + account_number + "&products_type=" + products_type + "&branch_code=" + branch_code + "&phone_number=" + phone_number;
                table_data = $('#dt-table-list').DataTable({
                    "processing": true,
                    destroy: true,
                    "ajax": {
                        "url": search_url,
                        "type": "GET",
                        "dataSrc": ""
                    },
                    responsive: true,
                    dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>\n        <'table-responsive'tr>\n        <'row align-items-center'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 d-flex justify-content-end'p>>",
                    language: {
                        paginate: {
                            previous: '<i class="fa fa-lg fa-angle-left"></i>',
                            next: '<i class="fa fa-lg fa-angle-right"></i>'
                        }
                    },
                    columns: [
                        { data: 'branch_code' },
                        { data: 'phone_number' },
                        { data: 'client_id' },
                        { data: 'account_type' },
                        { data: 'account_number' },
                        { data: 'account_title' },
                        { data: 'account_address' },
                        { data: 'total_credit_amount' },
                        { data: 'total_debit_amount' },
                        { data: 'account_balance' },
                        { data: 'credit_limit' },
                        { data: 'is_account_active' },
                        { data: 'account_closing_date' }
                    ]
                });
            }
        }]);

        return fn_data_table;
    }();

$(function () {
    $('#btnSearchStockMst').click(function () {
        new fn_data_table();
    });
})

let w_account_type = '';
let w_tran_screen = '';
let w_transaction_type = '';


$("#id_products_type").on("change paste keyup", function () {
    var tran_type = document.getElementById('id_products_type').value;
    w_account_type = tran_type;
    var account_number = document.getElementById("select2-id_account_number-container");
    account_number.textContent = "--Select Account--";
    $('#id_account_number').val('');
});

$(document).ready(function () {
    refresh_accounttype_list();
    var account_number = document.getElementById("select2-id_account_number-container");
    account_number.textContent = "--Select Account--";
    refresh_branch_list('');
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});


$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});


function refresh_accounttype_list() {
    var products_type = '';
    var url = 'finance-choice-accounttype';
    $.ajax({
        url: url,
        data: {
            'products_type': products_type
        },
        success: function (data) {
            $("#id_products_type").html(data);
        }
    });
    return false;
}

function refresh_branch_list(branch_code) {
    var url = '/finance-choice-branchlist';
    $.ajax({
        url: url,
        data: {
            'branch_code': branch_code
        },
        success: function (data) {
            $("#id_branch_code").html(data);
        }
    });
    return false;
}
