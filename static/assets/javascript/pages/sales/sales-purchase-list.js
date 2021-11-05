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
                var stock_id = document.getElementById('id_stock_id').value;
                var from_date = document.getElementById('id_from_date').value;
                var upto_date = document.getElementById('id_upto_date').value;
                var supplier_phone = document.getElementById('id_supplier_phone').value;
                var branch_code = document.getElementById('id_branch_code').value;

                var search_url = "/stock-master-apisearch/?stock_id=" + stock_id + "&branch_code=" + branch_code + "&supplier_phone=" + supplier_phone + "&from_date=" + from_date + "&upto_date=" + upto_date;
                table_data = $('#dt-stock-mst').DataTable({
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
                        { data: 'stock_id' },
                        { data: 'voucher_number' },
                        { data: 'supplier_id' },
                        { data: 'stock_date' },
                        { data: 'total_quantity' },
                        { data: 'total_price' },
                        { data: 'status' },
                        { data: 'comments' },
                        { data: 'app_user_id' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-info btn-sm">Return</button>' + '&nbsp;&nbsp' +
                                '<button type="button" class="btn btn-danger btn-sm">Cancel</button>' + '&nbsp;&nbsp' +
                                '<button type="button" class="btn btn-secondary btn-sm">Dtl</button>'
                        }
                    ]
                });
            }
        }]);

        return stock_mst_details;
    }();

$(function () {
    $('#btnSearchStockMst').click(function () {
        var stock_id = document.getElementById('id_stock_id').value;
        var from_date = document.getElementById('id_from_date').value;
        var upto_date = document.getElementById('id_upto_date').value;
        var supplier_phone = document.getElementById('id_supplier_phone').value;
        if (stock_id === "" & upto_date === "" & from_date === "" & supplier_phone === "") {
            alert("Please enter at least one value.")
        } else {
            new stock_mst_details();
        }
    });
})


$(document).ready(function () {
    refresh_branch_list('');
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});

var id = 0
$('#dt-stock-mst').on('click', 'button', function () {

    try {
        var table_row = table_data.row(this).data();
        id = table_row['id']
        var stock_id = table_row['stock_id']
        var stock_date = table_row['stock_date']
        var stock_status = table_row['status']
    }
    catch (e) {
        var table_row = table_data.row($(this).parents('tr')).data();
        id = table_row['id']
        var stock_id = table_row['stock_id']
        var stock_date = table_row['stock_date']
        var stock_status = table_row['status']
    }

    var class_name = $(this).attr('class');
    console.log(class_name);

    if (class_name == 'btn btn-info btn-sm') {
        if (stock_status == 'C') {
            alert('This Stock already Canceled!')
        } else {
            return_stock(id);
        }
    }
    if (class_name == 'btn btn-danger btn-sm') {
        if (stock_status == 'C') {
            alert('This Stock already Canceled!')
        } else {
            cancel_stock(id);
        }
    }
    if (class_name == 'btn btn-secondary btn-sm') {
        view_stock_details(id)
    }
})

function return_stock(stock_pk) {
    if (confirm('Are you sure you want to return this purchase?') == true) {
        $('#page_loading').modal('show');
        $.ajax({
            url: "/sales-purchase-return/" + stock_pk,
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

function view_stock_details(id) {
    var url = "sales-purchase-details/"+id;
    $.ajax({
        url: url,
        type: "GET",
        data: {
            'id': id
        },
        success: function (data) {
            $('#view_details').modal('show');
            $("#data_table_details").html(data);
        }
    });
    return false;
}


function cancel_stock(stock_pk) {
    if (confirm('Are you sure you want to cancel this purchase?') == true) {
        $('#page_loading').modal('show');
        $.ajax({
            url: "/sales-purchase-cancel/" + stock_pk,
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
