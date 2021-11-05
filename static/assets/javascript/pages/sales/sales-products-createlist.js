"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var table_data
var ProductList =
    function () {
        function ProductList() {
            _classCallCheck(this, ProductList);

            this.init();
        }

        _createClass(ProductList, [{
            key: "init",
            value: function init() {
                this.table = this.table();
            }
        }, {
            key: "table",
            value: function table() {
                var product_name = document.getElementById('id_product_name').value;
                var group_id = document.getElementById('id_product_group').value;
                var brand_id = document.getElementById('id_brand_id').value;
                var product_model = document.getElementById('id_product_model').value;
                var product_bar_code = document.getElementById('id_product_bar_code').value;
                var search_url = "/sales-products-api/?product_name=" + product_name + "&product_model=" + product_model 
                + "&product_bar_code=" + product_bar_code+ "&group_id=" + group_id+ "&brand_id=" + brand_id;

                table_data = $('#dt-product-list').DataTable({
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
                        { data: 'product_model' },
                        { data: 'product_name' },
                        { data: 'product_bar_code' },
                        { data: 'product_purces_price' },
                        { data: 'product_sales_price' },
                        { data: 'product_tax_rate' },
                        { data: 'product_life_time' },
                        { data: 'product_status' },
                        { data: 'product_narration' },
                        { data: 'sales_discount_type' },
                        { data: 'sales_discount_percent' },
                        { data: 'sales_discount_maxamt' },
                        { data: 'sales_discount_minamt' },
                        { data: 'sales_discount_fromdt' },
                        { data: 'sales_discount_uptodt' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-warning show-form-update"> <span class="glyphicon glyphicon-pencil"></span> Edit</button>'
                        }
                    ]
                });
            }
        }]);

        return ProductList;
    }();

var id = 0

$(function () {
    $('#btnSearch').click(function () {
        new ProductList();
    });
})

$(function () {

    $('#dt-product-list').on('click', 'button', function () {

        try {
            var table_row = table_data.row(this).data();
            id = table_row['product_id']
        }
        catch (e) {
            var table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['product_id']
        }

        var class_name = $(this).attr('class');
        if (class_name == 'btn btn-warning show-form-update') {
            show_edit_product_data(id)
        }

    })

    function show_edit_product_data(id) {
        $.ajax({
            url: '/sales-products-edit/' + id,
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

})

$(document).ready(function () {
    $('#id_brand_id').select2();
    $('#id_product_group').select2();
});

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
                table_data.ajax.reload();
            } else {
                $('#page_loading').modal('hide');
                alert(data.error_message);
                table_data.ajax.reload();
            }
        }
    })
    return false;
}


