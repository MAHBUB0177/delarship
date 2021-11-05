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
                var search_url = "/apifinance-depositreceive-api/?account_number=" + account_number;
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
                        { data: 'client_id' },
                        { data: 'deposit_date' },
                        { data: 'deposit_amount' },
                        { data: 'deposit_doc_num' },
                        { data: 'cancel_by' },
                        { data: 'cancel_on' },
                        { data: 'narration' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-danger btn-sm">Cancel</button>'
                        }
                    ]
                });
            }
        }]);

        return fn_data_table;
    }();

var id = 0

let w_tran_screen = 'DEP_RECEIVE';
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
            alert("Please Customer Name");
        } else {
            new fn_data_table();
        }
    });
})

$("#id_account_number").on("change", function () {
    get_client_info();
});

function get_client_info() {
    var account_number = document.getElementById('id_account_number').value;
    $.ajax({
        url: "/finance-account-byacnumber/" + account_number,
        type: 'GET',
        success: function (data) {
            if (data.form_is_valid) {
                $('#id_account_balance').val(data.account_balance);
            } else {
                $('#id_account_balance').val('');
            }
        }
    })
    return false;
}

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

function cancel_transaction(id) {
    if (confirm('Are you sure you want to cancel this Transaction?') == true) {
        $('#page_loading').modal('show');
        $.ajax({
            url: "/finance-depositreceive-cancel/" + id,
            type: "POST",
            success: function (data) {
                if (data.form_is_valid) {
                    $('#page_loading').modal('hide');
                    alert(data.success_message);
                    table_data.ajax.reload();
                } else {
                    $('#page_loading').modal('hide');
                    alert(data.error_message);
                    table_data.ajax.reload();
                }
            }
        })
    }
}

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
                var account_number = document.getElementById("select2-id_account_number-container");
                account_number.textContent = "-----------------";
                var global_branch_code = document.getElementById('id_global_branch_code').value;
                $('#id_branch_code').val(global_branch_code);
            } else {
                $('#page_loading').modal('hide');
                alert(data.error_message);
            }
        }
    })
    return false;
}
