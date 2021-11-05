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
                table_data = $('#dt-product-list').DataTable({
                    "processing": true,
                    "ajax": {
                        "url": "/delar-salesdetails-api/",
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
                        { data: 'product_price' },
                        { data: 'quantity' },
                        { data: 'total_price' },
                        { data: 'discount_rate' },
                        { data: 'discount_amount' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-warning show-form-update"> <span class="glyphicon glyphicon-pencil"></span> Edit</button>' + '&nbsp;&nbsp' +
                                '<button type="button" class="btn btn-danger show-form-update"> <span class="glyphicon glyphicon-pencil"></span>Rem</button>'
                        }
                    ]
                });
            }
        }]);

        return ProductList;
    }();

var id = 0
var total_discount_amount = 0;
var total_bill_amount = 0;
var total_quantity = 0;
var total_product_price = 0;
var due_amount = 0;
var advance_pay = 0;
var account_balance = 0;
var credit_limit = 0;
var update_account_balance = 0;
var discount_type = '';
var total_discount_amount = 0;
var product_discount_amount = 0;
var total_price = 0;

var zero_value = parseFloat(0)
let w_tran_screen = 'SALES_ENTRY';
let w_transaction_type = '';
let w_account_type = '';


$(document).on('theme:init', function () {
    new ProductList();
    //new getLocation();
    var currency = "-$4,400.50XYZ6";
    var number = Number(currency.replace(/[^0-9.-]+/g, ""));
    console.log(Math.round(number * 100) / 100);
    $.ajax({
        url: '/delar-salesdetails-entry',
        data: '',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            total_quantity = data.total_quantity;
            document.getElementById("id_total_quantity").innerHTML = total_quantity;
            total_discount_amount = data.total_discount
            document.getElementById("id_total_discount_amount").innerHTML = numberWithCommas(total_discount_amount);
            total_bill_amount = data.total_price;
            document.getElementById("id_total_bill_amount").innerHTML = numberWithCommas(total_bill_amount);
            total_product_price = (data.total_price - data.total_discount);
            document.getElementById("id_total_product_price").innerHTML = numberWithCommas(total_product_price);
            document.getElementById("id_customer_balance").innerHTML = numberWithCommas(0.00);
        }
    })
});

function getLocation() {
    if (navigator.geolocation) {
        // Call getCurrentPosition with success and failure callbacks
        navigator.geolocation.getCurrentPosition(SavePosition);
    }
    else {
        alert("Sorry, your browser does not support geolocation services.");
    }
}

function SavePosition(position) {
    $("#id_longitude").val(position.coords.longitude);
    $("#id_latitude").val(position.coords.latitude);
}

function numberWithCommas(number) {
    var parts = number.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}

function StringToNumber(values) {
    var number_value = Number(values);
    return number_value;
}

function roundNumber(values) {
    var output_data = (Math.round(values * 100) / 100);
    return output_data;
}

$("#id_product_id").on("change paste keyup", function (e) {
    var product_id = document.getElementById('id_product_id').value;
    get_product_name(product_id);
    var key = e.which;
    if (key == 13) // the enter key code
    {
        post_sales_details_data();
    }
});

$("#id_product_bar_code").on("change paste keyup", function (e) {
    var product_bar_code = document.getElementById('id_product_bar_code').value;
    get_product_name(product_bar_code);
    var key = e.which;
    if (key == 13) // the enter key code
    post_sales_details_data();
});

function get_product_name(product_id) {
    var branch_code = document.getElementById('id_branch_code').value;
    $.ajax({
        url: "sales-product-price",
        data: { "product_id": product_id, "branch_code": branch_code, "account_number": '', "tran_type_code": '' },
        type: 'GET',
        success: function (data) {
            if (data.form_is_valid) {
                $('#id_product_name').val(data.product_name);
                $('#id_product_price').val(data.product_price);
                $('#id_discount_rate').val(data.discount_percent);
                $('#id_discount_amount').val(data.discount_amount);
                $('#id_stock_available').val(data.stock_available);
                $('#id_product_model').val(data.product_model);
                product_discount_amount = data.discount_amount;
                $('#id_total_price').val(data.product_price);
                discount_type = data.discount_type;
                $('#id_quantity').val(1);
            } else {
                $('#id_product_price').val(0);
                $('#id_discount_rate').val(0);
                $('#id_discount_amount').val(0);
                $('#id_quantity').val(0);
            }
        }
    })
    return false;
}

$("#id_quantity").on("change paste keyup", function (e) {
    total_price = Number(document.getElementById('id_quantity').value) * Number(document.getElementById('id_product_price').value);
    $('#id_total_price').val(total_price);
    if (discount_type === 'F') {
        total_discount_amount = (Number(product_discount_amount) * Number(document.getElementById('id_quantity').value));
    } else {
        total_discount_amount = (Number(document.getElementById('id_total_price').value) * Number(document.getElementById('id_discount_rate').value)) / 100;
    }
    $('#id_discount_amount').val(total_discount_amount);

    var key = e.which;
    if (key == 13) // the enter key code
    {
        post_sales_details_data();
    }
});

$("#id_discount_rate").on("change paste keyup", function () {
    total_discount_amount = ((document.getElementById('id_total_price').value) * (document.getElementById('id_discount_rate').value)) / 100;
    $('#id_discount_amount').val(total_discount_amount);
});

$("#id_product_price").on("change paste keyup", function () {

    total_price = Number(document.getElementById('id_quantity').value) * Number(document.getElementById('id_product_price').value);
    $('#id_total_price').val(total_price);

    if (discount_type === 'F') {
        total_discount_amount = (Number(product_discount_amount) * Number(document.getElementById('id_quantity').value));
    } else {
        total_discount_amount = (Number(document.getElementById('id_total_price').value) * Number(document.getElementById('id_discount_rate').value)) / 100;
    }
    $('#id_discount_amount').val(total_discount_amount);

});

$("#id_total_discount_rate").on("change paste keyup", function () {
    discount_amount = (document.getElementById('id_total_bill_amount').value) * ((document.getElementById('id_total_discount_rate').value) / 100);
    bill_amount = (document.getElementById('id_total_bill_amount').value) - discount_amount;
    $("#id_total_discount_amount").val(discount_amount);
    $("#id_bill_amount").val(bill_amount);

    due_amount = (document.getElementById('id_bill_amount').value) - (document.getElementById('id_pay_amount').value);
    if (due_amount >= 0) {
        $("#id_due_amount").val(due_amount);
        $("#id_advance_pay").val(0);
    } else {
        advance_pay = (document.getElementById('id_pay_amount').value) - (document.getElementById('id_bill_amount').value);
        $("#id_advance_pay").val(advance_pay);
        $("#id_due_amount").val(0);
    }
});

$('#dt-product-list').on('click', 'button', function () {

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
            sales_details_delete(id)
        }
    }

})

function show_edit_product_data(id) {
    $.ajax({
        url: '/delar-salesdetails-edit/' + id,
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

function sales_details_delete(id) {
    $.ajax({
        url: '/delar-salesdetails-delete/' + id,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                total_quantity = data.total_quantity;
                document.getElementById("id_total_quantity").innerHTML = total_quantity;
                total_discount_amount = data.total_discount
                document.getElementById("id_total_discount_amount").innerHTML = numberWithCommas(total_discount_amount);
                total_bill_amount = data.total_price;
                document.getElementById("id_total_bill_amount").innerHTML = numberWithCommas(total_bill_amount);
                total_product_price = ((data.total_price - data.total_discount));
                document.getElementById("id_total_product_price").innerHTML = numberWithCommas(total_product_price);
                table_data.ajax.reload();
            } else {
                table_data.ajax.reload();
            }
        }
    })
    return false;
}

function post_sales_details_data() {
    var data_string = $("#sales_details_form").serialize();
    var data_url = $("#sales_details_form").attr('data-url');
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                $('#page_loading').modal('hide');
                total_quantity = data.total_quantity;
                document.getElementById("id_total_quantity").innerHTML = total_quantity;
                total_discount_amount = Number(data.total_discount);
                document.getElementById("id_total_discount_amount").innerHTML = numberWithCommas(total_discount_amount);
                total_bill_amount = Number(data.total_price);
                document.getElementById("id_total_bill_amount").innerHTML = numberWithCommas(total_bill_amount);
                total_product_price = ((Number(data.total_price) - Number(data.total_discount)));
                document.getElementById("id_total_product_price").innerHTML = numberWithCommas(total_product_price);
                document.getElementById("sales_details_form").reset();
                var product_id_span = document.getElementById("select2-id_product_id-container");
                product_id_span.textContent = "Select Product";
                $('#id_product_id').val('');
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

$(document).ready(function () {
    $('#id_employee_id').select2();
    transaction_type_list('SALES_ENTRY');
    refresh_branch_list('');
    var branch_code = document.getElementById('id_global_branch_code').value;
    refresh_center_list(branch_code);
    refresh_employee_list(branch_code)
});

$("#id_branch_code").on("change", function () {
    var branch_code = document.getElementById('id_branch_code').value;
    refresh_center_list(branch_code);
    refresh_employee_list(branch_code)
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});

function transaction_type_list(transaction_screen) {
    var url = '/sales-choice-trantype';
    $.ajax({
        url: url,
        data: {
            'transaction_screen': transaction_screen
        },
        success: function (data) {
            $("#id_type_code").html(data);
        }
    });
    return false;
}

$(function () {

    $(function () {
        $('#btnAddItem').click(function () {
            post_sales_details_data();
            fn_calculate_payment();
        });
    });

    $(function () {
        $('#btnSubmitOrder').click(function () {
            post_sales_master_data();
        });
    });

    $(function () {
        $('#btnClearItem').click(function () {
            if (confirm('Are you sure you want to Clear Your Chart?') == true) {
                clear_chart_item();
                document.getElementById("sales_details_form").reset();
                $("#select2-id_product_id-container").trigger("chosen:updated");
            }
        });
    });

    function post_sales_master_data() {
        var data_string = $("#sales_master_form").serialize();
        var data_url = $("#sales_master_form").attr('data-url');
        $('#page_loading').modal('show');
        $.ajax({
            url: data_url,
            data: data_string,
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $('#page_loading').modal('hide');
                    document.getElementById("sales_master_form").reset();
                    total_quantity = 0;
                    document.getElementById("id_total_quantity").innerHTML = total_quantity;
                    total_discount_amount = 0.00;
                    document.getElementById("id_total_discount_amount").innerHTML = numberWithCommas(total_discount_amount);
                    total_bill_amount = 0.00;
                    document.getElementById("id_total_bill_amount").innerHTML = numberWithCommas(total_bill_amount);
                    total_product_price = 0.00;
                    document.getElementById("id_total_product_price").innerHTML = numberWithCommas(total_product_price);
                    table_data.ajax.reload();
                    var global_branch_code = document.getElementById('id_global_branch_code').value;
                    $('#id_branch_code').val(global_branch_code);
                    alert(data.success_message);
                } else {
                    $('#page_loading').modal('hide');
                    alert(data.error_message)
                    table_data.ajax.reload();
                }
            },
            error: function (data) {
                alert(data.error_message);
            }
        });
    }

    function clear_chart_item() {
        var data_url = '/delar-salesdetails-clear';
        $.ajax({
            url: data_url,
            data: '',
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    var total_quantity = 0;
                    document.getElementById("id_total_quantity").innerHTML = total_quantity;
                    total_discount_amount = 0.00;
                    document.getElementById("id_total_discount_amount").innerHTML = numberWithCommas(total_discount_amount);
                    total_bill_amount = 0.00;
                    document.getElementById("id_total_bill_amount").innerHTML = numberWithCommas(total_bill_amount);
                    total_product_price = 0.00;
                    document.getElementById("id_total_product_price").innerHTML = numberWithCommas(total_product_price);
                    table_data.ajax.reload();
                } else {
                    var total_quantity = 0;
                    document.getElementById("id_total_quantity").innerHTML = total_quantity;
                    total_discount_amount = 0.00;
                    document.getElementById("id_total_discount_amount").innerHTML = numberWithCommas(total_discount_amount);
                    total_bill_amount = 0.00;
                    document.getElementById("id_total_bill_amount").innerHTML = numberWithCommas(total_bill_amount);
                    total_product_price = 0.00;
                    document.getElementById("id_total_product_price").innerHTML = numberWithCommas(total_product_price);
                    table_data.ajax.reload();
                }
            }
        })
        return false;
    }

});