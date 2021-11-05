"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var table_data
var edit_stock_id

var stock_mst_details =

    function () {
        function stock_mst_details() {
            _classCallCheck(this, stock_mst_details);

            this.init();
        }

        _createClass(stock_mst_details, [{
            key: "init",
            value: function init() {
                this.table = this.table();
            }
        }, {
            key: "table",
            value: function table() {
                var from_date = document.getElementById('id_from_date').value;
                var upto_date = document.getElementById('id_upto_date').value;
                var branch_code = document.getElementById('id_branch_code').value;
                var client_id = document.getElementById('id_client_id').value;

                var search_url = "/sales-invoicereturn-entrydetails";
                table_data = $('#dt-stock-mst').DataTable({
                    "processing": true,
                    destroy: true,
                    "ajax": {
                        "url": search_url,
                        "type": "GET",
                        "dataSrc": "data",
                        "data": {
                            'from_date': from_date, 'upto_date': upto_date, 'branch_code': branch_code,
                            'client_id': client_id,
                        }
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
                        { data: 'center_name' },
                        { data: 'product_name' },
                        { data: 'client_name' },
                        { data: 'return_date' },
                        { data: 'returned_quantity' },
                        { data: 'return_amount' },
                        { data: 'return_reason' },
                        { data: 'app_user_id' },
                        { data: 'cancel_by' },
                        { data: 'cancel_on' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-danger btn-sm">Cancel</button>'
                        }
                    ]
                });
            }
        }]);

        return stock_mst_details;
    }();

$(function () {
    $('#btnSearchStockMst').click(function () {
     
        var from_date = document.getElementById('id_from_date').value;
        var upto_date = document.getElementById('id_upto_date').value;
        if (upto_date === "" & from_date === "") {
            alert("Please enter at least one value.")
        } else {
            new stock_mst_details();
        }
    });
})

let w_branch_code = 0;

$(document).ready(function () {
    refresh_branch_list('');
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    w_branch_code = global_branch_code;
    $('#id_branch_code').val(global_branch_code);
});

$("#id_branch_code").on("change", function () {
    var branch_code = document.getElementById('id_branch_code').value;
    w_branch_code = branch_code;
});

var id = 0
$('#dt-stock-mst').on('click', 'button', function () {

    try {
        var table_row = table_data.row(this).data();
        id = table_row['id']
    }
    catch (e) {
        var table_row = table_data.row($(this).parents('tr')).data();
        id = table_row['id']
    }

    var class_name = $(this).attr('class');
    console.log(class_name);

    if (class_name == 'btn btn-danger btn-sm') {
        cancel_damage(id);
    }
})

function cancel_damage(id) {
    if (confirm('Are you sure you want to cancel this transaction?') == true) {
        $('#page_loading').modal('show');
        $.ajax({
            url: "/sales-invoicereturn-cancel/" + id,
            type: "POST",
            success: function (data) {
                if (data.form_is_valid) {
                    $('#page_loading').modal('hide');
                    alert(data.success_message);
                } else {
                    $('#page_loading').modal('hide');
                    alert(data.error_message);
                }
                table_data.ajax.reload();
            }
        })
    }
}