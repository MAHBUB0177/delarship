"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var table_data

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
                var account_number = document.getElementById('id_account_number').value;
                var emi_reference_no = document.getElementById('id_emi_reference_no').value;
                var from_date = document.getElementById('id_from_date').value;
                var upto_date = document.getElementById('id_upto_date').value;
                var branch_code = document.getElementById('id_branch_code').value;
                var search_url = "/sales-emihistory-api/?account_number=" + account_number + "&emi_reference_no=" + emi_reference_no
                    + "&from_date=" + from_date + "&upto_date=" + upto_date + "&branch_code=" + branch_code;   //change
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
                        { data: 'account_number' },
                        { data: 'emi_reference_no' },
                        { data: 'emi_rate' },
                        { data: 'emi_inst_amount' },
                        { data: 'inst_receive_date' },
                        { data: 'inst_receive_amount' },
                        { data: 'total_installment_due' },
                        { data: 'total_installment_payment' },
                        { data: 'total_installment_overdue' },
                        { data: 'total_installment_advance' },
                        { data: 'total_emi_outstanding' },
                        { data: 'emi_principal_outstanding' },
                        { data: 'emi_profit_outstanding' },
                        { data: 'emi_total_payment' },
                        { data: 'emi_principal_payment' },
                        { data: 'emi_profit_payment' },
                        { data: 'total_advance_recover' },
                        { data: 'principal_advance_recover' },
                        { data: 'profit_advance_recover' },
                        { data: 'total_due_recover' },
                        { data: 'principal_due_recover' },
                        { data: 'profit_due_recover' },
                        { data: 'emi_total_overdue' },
                        { data: 'emi_principal_overdue' },
                        { data: 'emi_profit_overdue' },
                    ]
                });
            }
        }]);

        return fn_data_table;
    }();

var id = 0
let w_tran_screen = 'EMI_RECEIVE';
let w_transaction_type = '';
let w_account_type = '';

$(document).ready(function () {
    refresh_branch_list('');
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});


$(function () {
    $('#btnSearch').click(function () {
        var account_number = document.getElementById('id_account_number').value;
        if (account_number === "") {
            alert("Please Select Customer");
        } else {
            new fn_data_table();
        }
    });
})


$(function () {

    $('#dt-table-list').on('click', 'button', function () {

        try {
            var table_row = table_data.row(this).data();
            id = table_row['id']
        }
        catch (e) {
            var table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['id']
        }

        var class_name = $(this).attr('class');
        if (class_name == 'btn btn-info btn-sm') {
            show_edit_form(id);
        }
        if (class_name == 'btn btn-danger btn-sm') {
            cancel_transaction(id);
        }
    })

    $("#id_account_number").on("change paste keyup", function () {
        refresh_emiinvoice_list();
    });

    function refresh_emiinvoice_list() {
        var account_number = document.getElementById('id_account_number').value;
        var url = 'sales-choice-emiinvoice';
        $.ajax({
            url: url,
            data: {
                'account_number': account_number
            },
            success: function (data) {
                $("#id_emi_reference_no").html(data);
            }
        });
        return false;
    }

});