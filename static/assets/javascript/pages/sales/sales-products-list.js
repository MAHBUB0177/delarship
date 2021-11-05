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
                var group_id = document.getElementById('id_group_id').value;
                var brand_id = document.getElementById('id_brand_id').value;
                var product_model = document.getElementById('id_product_model').value;
                var product_bar_code = document.getElementById('id_product_bar_code').value;
                var search_url = "/sales-products-api/?product_name=" + product_name + "&product_model=" + product_model 
                + "&product_bar_code=" + product_bar_code+ "&group_id=" + group_id+ "&brand_id=" + brand_id;

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
                        { data: 'product_name' },
                        { data: 'product_model' },
                        { data: 'product_available_stock' },
                        { data: 'product_sales_price' },
                        { data: 'emi_sales_price' },
                        { data: 'whole_sales_price' },
                        { data: 'sales_discount_type' },
                        { data: 'sales_discount_percent' },
                        { data: 'sales_discount_maxamt' },
                        { data: 'sales_discount_minamt' },
                        { data: 'sales_discount_fromdt' },
                        { data: 'sales_discount_uptodt' }
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

$(document).ready(function () {
    $('#id_group_id').select2();
    $('#id_brand_id').select2();
    refresh_branch_list('');
    refresh_group_list();
    refresh_brand_list();
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});