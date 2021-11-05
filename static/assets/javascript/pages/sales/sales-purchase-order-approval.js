"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var table_data

var DataTablesResponsiveDemo =
    function () {
        function DataTablesResponsiveDemo() {
            _classCallCheck(this, DataTablesResponsiveDemo);

            this.init();
        }

        _createClass(DataTablesResponsiveDemo, [{
            key: "init",
            value: function init() {
                this.table = this.table();
            }
        }, {
            key: "table",
            value: function table() {
                table_data = $('#dt-purchase-approval').DataTable({
                    "processing": true,
                    "ajax": {
                        "url": "/purchase-master-api/",
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
                        { data: 'purchase_ord_no' },
                        { data: 'voucher_number' },
                        { data: 'purchase_date' },
                        { data: 'total_pur_qnty' },
                        { data: 'g_total_price' },
                        { data: 'comments' },
                       
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-info btn-sm">Approve</button>' + '&nbsp;&nbsp' +
                                '<button type="button" class="btn btn-danger btn-sm">Reject</button>'
                        }
                    ]
                });
            }
        }]);

        return DataTablesResponsiveDemo;
    }();

$(document).on('theme:init', function () {
    new DataTablesResponsiveDemo();
});

$(function () {
    var id = 0
    $('#dt-purchase-approval').on('click', 'button', function () {

        try {
            var table_row = table_data.row(this).data();
            id = table_row['id']
            var purchase_ord_no = table_row['purchase_ord_no']
            var purchase_date = table_row['purchase_date']
        }
        catch (e) {
            var table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['id']
            var purchase_ord_no = table_row['purchase_ord_no']
            var purchase_date = table_row['purchase_date']
        }

        var class_name = $(this).attr('class');

        if (class_name == 'btn btn-info btn-sm') {
            show_stock_payment_model(id)
        }
        if (class_name == 'btn btn-danger btn-sm') {
            reject_stock(id)
        }
        if (class_name == 'btn btn-secondary btn-sm') {
            view_stock_details(purchase_ord_no, purchase_date)
        }
    })

    function view_stock_details(stock_id, stock_date) {
        var url = "/sales-stock-search/" + stock_id + "/" + stock_date
        $(location).attr('href', url);
    }

    function reject_stock(stock_pk) {
        if (confirm('Are you sure you want to reject this stock?') == true) {
            $('#page_loading').modal('show');
            $.ajax({
                url: "/sales-purchase-order-reject/" + stock_pk,
                type: "POST",
                success: function (data) {
                    $('#page_loading').modal('hide');
                    table_data.ajax.reload();
                }
            })
        }
    }

    function show_stock_payment_model(stock_pk) {
       
        $('#page_loading').modal('show');
        $.ajax({
            url: '/sales-purchase-order-payment/' + stock_pk,
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $('#page_loading').modal('hide');
                $('#stock_edit').modal('show');
            },
            success: function (data) {
                console.log("ok")
                $('#page_loading').modal('hide');
                $('#stock_edit .modal-content').html(data.html_form);
            }
        })
    }

})
