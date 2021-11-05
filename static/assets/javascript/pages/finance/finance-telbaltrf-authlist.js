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
                var org_teller_id = document.getElementById('id_org_teller_id').value;
                var auth_pending = document.getElementById('id_auth_pending').value;
                var transaction_date = document.getElementById('id_transaction_date').value;
                var from_date = document.getElementById('id_from_date').value;
                var upto_date = document.getElementById('id_upto_date').value;

                var search_url = "/apifinance-telbaltrf-api/?org_teller_id="
                    + org_teller_id + "&auth_pending=" + auth_pending + "&transaction_date=" + transaction_date
                    + "&from_date=" + from_date + "&upto_date=" + upto_date;
                console.log(search_url)
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
                        { data: 'transaction_date' },
                        { data: 'tran_debit_credit' },
                        { data: 'tran_amount' },
                        { data: 'cancel_amount' },
                        { data: 'available_balance' },
                        { data: 'app_user_id' },
                        { data: 'app_data_time' },
                        { data: 'auth_by' },
                        { data: 'auth_on' },
                        { data: 'cancel_by' },
                        { data: 'cancel_on' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-info btn-sm">Accept</button>' + '&nbsp;&nbsp' +
                                '<button type="button" class="btn btn-danger btn-sm">Reject</button>'
                        }
                    ]
                });
            }
        }]);

        return fn_data_table;
    }();

$(function () {
    $('#btnSearchStockMst').click(function () {
        var org_teller_id = document.getElementById('id_org_teller_id').value;

        if (org_teller_id === "") {
            alert("Please Enter Requesting Teller ID!")
        } else {
            new fn_data_table();
        }
    });
})


$("#id_branch_code").on("change", function () {
    refresh_user_list();
});

$(document).ready(function () {
    $("#id_org_teller_id").select2();
    refresh_user_list();
    refresh_branch_list();
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});

function refresh_user_list() {
    var branch_code = document.getElementById('id_branch_code').value;
    var url = '/appauth-choice-appuserlist';
    $.ajax({
        url: url,
        data: {
            'branch_code': branch_code
        },
        success: function (data) {
            $("#id_org_teller_id").html(data);
        }
    });
    return false;
}
$(function () {
    var id = 0
    $('#dt-table-list').on('click', 'button', function () {

        try {
            var table_row = table_data.row(this).data();
            id = table_row['id']
            var cancel_by = table_row['cancel_by']
        }
        catch (e) {
            var table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['id']
            var cancel_by = table_row['cancel_by']
        }

        var class_name = $(this).attr('class');

        if (class_name == 'btn btn-danger btn-sm') {
            if (cancel_by != null) {
                alert('This Transaction already Canceled!')
            } else {
                reject_transaction(id);
            }
        }
        if (class_name == 'btn btn-info btn-sm') {
            accept_transaction(id);
        }
    })

    function accept_transaction(id) {
        $('#page_loading').modal('show');
        $.ajax({
            url: "/finance-telbaltrf-accept/" + id,
            type: "POST",
            success: function (data) {
                if (data.form_is_valid) {
                    $('#page_loading').modal('hide');
                    table_data.ajax.reload();
                    alert(data.success_message);
                } else {
                    $('#page_loading').modal('hide');
                    alert(data.error_message)
                    table_data.ajax.reload();
                }
            }
        })
    }

    function reject_transaction(id) {
        if (confirm('Are you sure you want to cancel this transaction?') == true) {
            $('#page_loading').modal('show');
            $.ajax({
                url: "/finance-telbaltrf-reject/" + id,
                type: "POST",
                success: function (data) {
                    if (data.form_is_valid) {
                        $('#page_loading').modal('hide');
                        alert(data.success_message);
                        table_data.ajax.reload();
                    } else {
                        $('#page_loading').modal('hide');
                        alert(data.error_message)
                        table_data.ajax.reload();
                    }
                }
            })
        }
    }

})