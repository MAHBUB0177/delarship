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
                var charges_code = ""
                var search_url = "/apifinance-charges-api/?charges_code=" + charges_code
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
                        { data: 'charges_code' },
                        { data: 'charges_name' },
                        { data: 'actype_code' },
                        { data: 'charge_type' },
                        { data: 'charge_percentage' },
                        { data: 'charge_from_amount' },
                        { data: 'charge_upto_amount' },
                        { data: 'charge_amount' },
                        { data: 'account_opening_charge' },
                        { data: 'account_closing_charge' },
                        { data: 'member_admission_fee' },
                        { data: 'loan_application_fee' },
                        { data: 'loan_insurance_fee' },
                        { data: 'pass_book_fee' },
                        { data: 'penal_charge' },
                        { data: 'others_fee' },
                        { data: 'status' },
                        { data: 'effective_from_date' },
                        { data: 'effective_upto_date' },
                        { data: 'charges_ledger_code' },
                        { data: 'comments' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-info btn-sm">Edit</button>'
                        }
                    ]
                });
            }
        }]);

        return fn_data_table;
    }();

var id = 0

$(document).ready(function () {
    $('#id_charges_ledger_code').select2();
});

$('#btnSearch').click(function () {
    new fn_data_table();
})

$(function () {

    $('#dt-table-list').on('click', 'button', function () {

        try {
            var table_row = table_data.row(this).data();
            id = table_row['charges_code']
        }
        catch (e) {
            var table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['charges_code']
        }

        var class_name = $(this).attr('class');
        if (class_name == 'btn btn-info btn-sm') {
            show_edit_form(id);
        }

    })

    function show_edit_form(id) {
        $.ajax({
            url: '/finance-charges-edit/' + id,
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $('#edit_model').modal('show');
            },
            success: function (data) {
                $('#edit_model .modal-content').html(data.html_form);
            }
        })
    }

});

$(function () {

    $(function () {
        $('#btnAddItem').click(function () {
            post_tran_table_data();

        });
    });


    function post_tran_table_data() {
        var data_string = $("#tran_table_data").serialize();
        var data_url = $("#tran_table_data").attr('data-url');
        $('#page_loading').modal('show');
        $.ajax({
            url: data_url,
            data: data_string,
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    document.getElementById("tran_table_data").reset();
                    $('#page_loading').modal('hide');
                    alert(data.success_message);
                } else {
                    $('#page_loading').modal('hide');
                    alert(data.error_message);
                    table_data.ajax.reload();

                }
            }
        })
        return false;
    }

});
