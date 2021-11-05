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
                table_data = $('#dt-table-list').DataTable({
                    "processing": true,
                    "ajax": {
                        "url": "/sales-purchase-order-tempapi/",
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
                        { data: 'product_id' },
                        { data: 'origin' },
                        { data: 'pur_qnty' },
                        { data: 'total_price' },
                        
                        {
                            "data": null,
                            "defaultContent":
                                '<button type="button" class="btn btn-danger show-form-update"> <span class="glyphicon glyphicon-pencil"></span>Remove</button>'
                        }
                    ]
                });
            }
        }]);

        return fn_data_table;
    }();

var id = 0

$(document).on('theme:init', function () {
    new fn_data_table();
});


$("#id_product_id").on("change paste keyup", function () {
    get_product_name()
});

$("#id_product_bar_code").on("change paste keyup", function (e) {
    get_product_info_barcode()
    var key = e.which;
    if (key == 13) // the enter key code
    {
        var product_name = document.getElementById('id_product_id').value;
        if (product_name === '') {
            alert('Please Enter Product Information')
        } else {
            post_tran_table_data();
        }
    }
});

function get_product_name() {
    var product_id = document.getElementById('id_product_id').value;
    $.ajax({
        url: "/sales-product-info/" + product_id,
        type: 'GET',
        success: function (data) {
            if (data.form_is_valid) {
                $('#id_product_name').val(data.product_name);
                $('#id_product_bar_code').val(data.product_bar_code);
                $('#id_pur_qnty').val(1);
                $('#id_product_model').val(data.product_model);
                $('#id_unit_price').val(data.product_purces_price);
                $('#id_total_price').val(data.product_purces_price);
            } else {
                $('#id_product_name').val('Invalid Product');
            }
        }
    })
    return false;
}

function get_product_info_barcode() {
    var product_bar_code = document.getElementById('id_product_bar_code').value;
    $.ajax({
        url: "/sales-product-info-barcode/" + product_bar_code,
        type: 'GET',
        success: function (data) {
            if (data.form_is_valid) {
                $('#id_product_name').val(data.product_name);
                $('#div_id_product_id').val(data.product_id);
                $('#id_pur_qnty').val(1);
                $('#id_product_model').val(data.product_model);
                $('#id_unit_price').val(data.product_purces_price);
                $('#id_total_price').val(data.product_purces_price);
            } else {
                $('#id_product_name').val('Invalid Product');
            }
        }
    })
    return false;
}


$("#id_total_price").on("change paste keyup", function () {
    var quantity = document.getElementById('id_pur_qnty').value;
    var dtl_total_price = document.getElementById('id_total_price').value;
    var purces_rate = Math.round((dtl_total_price / quantity) * 100) / 100;
    $('#id_unit_price').val(purces_rate);
});



$("#id_pur_qnty").on("change paste keyup", function () {
    var quantity = document.getElementById('id_pur_qnty').value;
    var purces_rate = document.getElementById('id_unit_price').value;
    var dtl_total_price = Math.round((purces_rate * quantity) * 100) / 100;
    $('#id_total_price').val(dtl_total_price);
});

$("#id_unit_price").on("change paste keyup", function () {
    var quantity = document.getElementById('id_pur_qnty').value;
    var purces_rate = document.getElementById('id_unit_price').value;
    var dtl_total_price = Math.round((purces_rate * quantity) * 100) / 100;
    $('#id_total_price').val(dtl_total_price);
});


$(document).ready(function () {
    refresh_branch_list('');
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});

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
        if (class_name == 'btn btn-warning show-form-update') {
            show_edit_product_data(id)
        }

        if (class_name == 'btn btn-danger show-form-update') {
            if (confirm('Are you sure you want to remove this item?') == true) {
                stock_details_delete(id)
            }
        }

    })

    function show_edit_product_data(id) {
        $.ajax({
            url: '/sales-details-edit/' + id,
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $('#product_edit').modal('show');
            },
            success: function (data) {
                $('#product_edit .modal-content').html(data.html_form);
            }
        })
    }

    function stock_details_delete(id) {
        $.ajax({
            url: '/sales-prordertemp-delete/' + id,
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $('#id_total_pur_qnty').val(data.total_quantity);
                    $('#id_g_total_price').val(data.total_price);
                    table_data.ajax.reload();
                } else {
                    table_data.ajax.reload();
                }
            }
        })
        return false;
    }

});

$(function () {
    $('#btnAddItem').click(function () {
        post_tran_table_data();

    });
});

$(function () {
    $('#btn_stock_sumbit').click(function () {
        post_stock_master_data();

    });
});

function post_tran_table_data() {
    var data_string = $("#purchase_master_form").serialize();
    var data_url = $("#purchase_master_form").attr('data-url');
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                document.getElementById("purchase_master_form").reset();
                $('#id_total_pur_qnty').val(data.total_quantity);
                $('#id_g_total_price').val(data.total_price);
                table_data.ajax.reload();
                $('#page_loading').modal('hide');
                $('#id_product_name').val('');
                $('#id_product_id').val('');
                $('#id_pur_qnty').val(1);
                var product_id_span = document.getElementById("select2-id_product_id-container");
                product_id_span.textContent = "Select Product";
            } else {
                alert(data.error_message);
                table_data.ajax.reload();
                $('#page_loading').modal('hide');
            }
        }
    })
    return false;
}

function post_stock_master_data() {
    var data_string = $("#purchase_master_post").serialize();
    var data_url = $("#purchase_master_post").attr('data-url');
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                alert(data.message);
                document.getElementById("purchase_master_post").reset();
                document.getElementById("purchase_master_form").reset();
                table_data.ajax.reload();
                $('#page_loading').modal('hide');
                var global_branch_code = document.getElementById('id_global_branch_code').value;
                $('#id_branch_code').val(global_branch_code);
            } else {
                alert(data.error_message);
                table_data.ajax.reload();
                $('#page_loading').modal('hide');
            }
        }
    })
    return false;
}
