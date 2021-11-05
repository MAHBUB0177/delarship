"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var table_data

// DataTables Demo
// =============================================================
var ProductList =
    /*#__PURE__*/
    function () {
        function ProductList() {
            _classCallCheck(this, ProductList);

            this.init();
        }

        _createClass(ProductList, [{
            key: "init",
            value: function init() {
                // event handlers
                this.table = this.table();
            }
        }, {
            key: "table",
            value: function table() {
                table_data = $('#dt-product-list').DataTable({
                    "processing": true,
                    "ajax": {
                        "url": "/sales-trantable-api/",
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
                        { data: 'batch_serial' },
                        { data: 'transaction_date' },
                        { data: 'tran_gl_code' },
                        { data: 'account_phone' },
                        { data: 'tran_debit_credit' },
                        { data: 'tran_type' },
                        { data: 'tran_amount' },
                        { data: 'transaction_naration' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-danger show-form-update"> <i class="fa fa-trash" aria-hidden="true"></i></button>'
                        }
                    ]
                });
            }
        }]);

        return ProductList;
    }();
/**
 * Keep in mind that your scripts may not always be executed after the theme is completely ready,
 * you might need to observe the `theme:load` event to make sure your scripts are executed after the theme is ready.
 */
var id = 0

$(document).on('theme:init', function () {
    new ProductList();
});


$(function () {

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

        if (class_name == 'btn btn-danger show-form-update') {
            if (confirm('Are you sure you want to remove this item?') == true) {
                delete_tran_table_data(id)
            }
        }

    })

    function delete_tran_table_data(id) {
        $('#page_loading').modal('show');
        $.ajax({
            url: '/sales-trantable-delete/' + id,
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $('#page_loading').modal('hide');
                    table_data.ajax.reload();
                } else {
                    $('#page_loading').modal('hide');
                    table_data.ajax.reload();
                }
            }
        })
        return false;
    }

});


$(document).ready(function () {
    transaction_type_list('TRANSFER_TRAN');
    refresh_branch_list('');
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_delar_id').val(global_branch_code);
});

function transaction_type_list(transaction_screen) {
    var url = '/sales-choice-trantype';
    $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request
        data: {
            'transaction_screen': transaction_screen       // add the id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the view function
            $("#id_tran_type").html(data);  // replace the values of the input with the data that came from the server
        }
    });
    return false;
}

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_delar_id').val(global_branch_code);
});

function refresh_branch_list(branch_code) {
    var url = 'sales-choice-branch';
    $.ajax({
        url: url,
        data: {
            'branch_code': branch_code
        },
        success: function (data) {
            $("#id_delar_id").html(data);
        }
    });
    return false;
}

$(function () {

    $(function () {
        $('#btnAddItem').click(function () {
            if ((document.getElementById('id_tran_amount').value) <= 0) {
                alert('Transaction amount can not be Zero or Negative!')
            } else {
                post_tran_table_data();
            }
        });
    });

    $(function () {
        $('#btn_stock_sumbit').click(function () {
            post_transfer_transaction();
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
                    alert(data.success_message);
                    document.getElementById("tran_table_data").reset();
                    $('#page_loading').modal('hide');
                } else {
                    $('#page_loading').modal('hide');
                    alert(data.error_message);

                }
            }
        })
        return true;
    }

    function post_transfer_transaction() {
        $('#page_loading').modal('show');
        $.ajax({
            url: '/sales-transfer-tranpost',
            data: '',
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $('#page_loading').modal('hide');
                    table_data.ajax.reload();
                    alert(data.message);
                } else {
                    $('#page_loading').modal('hide');
                    alert(data.error_message);
                    table_data.ajax.reload();
                }
            }
        })
        return false;
    }


    $("#id_tran_gl_code").on("change paste keyup", function () {
        var tran_gl_code = document.getElementById('id_tran_gl_code').value;
        console.log(tran_gl_code)
        if (tran_gl_code != '0') {
            get_gl_name();
        }
    });

    $("#id_phone_number").on("change paste keyup", function () {
        get_client_info();
    });

    $("#id_tran_debit_credit").on("change paste keyup", function () {
        get_client_info();
    });

    function get_gl_name() {
        var tran_gl_code = document.getElementById('id_tran_gl_code').value;
        $.ajax({
            url: "/sales-ledger-info/" + tran_gl_code,
            type: 'GET',
            success: function (data) {
                if (data.form_is_valid) {
                    console.log(data.gl_name);
                    $('#id_gl_name').val(data.gl_name);
                } else {
                    $('#id_gl_name').val('');
                }
            }
        })
        return false;
    }

    function get_client_info() {
        var client_id = document.getElementById('id_phone_number').value;
        var type_code = document.getElementById('id_tran_type').value;
        var tran_debit_credit = document.getElementById('id_tran_debit_credit').value;
        var tran_screen = 'TRANSFER_TRAN';
        $.ajax({
            url: "/sales-account-infotrantype/" + client_id + "/" + tran_screen + "/" + type_code,
            type: 'GET',
            success: function (data) {
                if (data.form_is_valid) {
                    if (tran_debit_credit == 'D') {
                        $('#id_customer_name').val(data.debit_account_title);
                        $('#id_current_balance').val(data.debit_account_banalce);
                        $('#id_account_number').val(data.debit_account_number);
                    } else {
                        $('#id_customer_name').val(data.account_title);
                        $('#id_current_balance').val(data.account_banalce);
                        $('#id_account_number').val(data.account_number);
                    }
                } else {
                    $('#id_customer_name').val('');
                    $('#id_current_balance').val('');
                    $('#id_account_number').val('');
                }
            }
        })
        return false;
    }

    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});

