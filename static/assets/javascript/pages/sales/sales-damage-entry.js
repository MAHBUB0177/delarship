let w_tran_screen = 'STOCK_PAYMENT';
let w_transaction_type = '';
let w_account_type = '';
let w_branch_code = '';
let w_product_rate = 0.0;

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
                alert(data.success_message);
                document.getElementById("tran_table_data").reset();
                $('#page_loading').modal('hide');
                var global_branch_code = document.getElementById('id_global_branch_code').value;
                $('#id_branch_code').val(global_branch_code);
            } else {
                $('#page_loading').modal('hide');
                alert(data.error_message);

            }
        }
    })
    return true;
}

$(document).ready(function () {
    refresh_branch_list('');
    var w_branch_code = document.getElementById('id_global_branch_code').value;
    account_list_refresh(w_account_type, w_tran_screen, w_transaction_type, w_branch_code);
    $('#id_supplier_account').select2();

});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});

function account_list_refresh(account_type, tran_screen, transaction_type, branch_code) {
    var url = '/sales-choice-accountslist';
    $.ajax({
        url: url,
        data: {
            'account_type': account_type, 'tran_screen': tran_screen,
            'transaction_type': transaction_type, 'branch_code': branch_code,
        },
        success: function (data) {
            $("#id_supplier_account").html(data);
        }
    });
    return false;
}

$("#id_branch_code").on("change", function () {
    var w_branch_code = document.getElementById('id_branch_code').value;
    account_list_refresh(w_account_type, w_tran_screen, w_transaction_type, w_branch_code)
});

$("#id_damage_quantity").on("change paste keyup", function () {
    var damage_quantity = document.getElementById('id_damage_quantity').value;
    $('#id_damage_amount').val(damage_quantity * w_product_rate);
});


$("#id_product_id").on("change", function () {
    get_product_rate();
});


function get_product_rate() {
    var product_id = document.getElementById('id_product_id').value;
    var branch_code = document.getElementById('id_branch_code').value;
    $.ajax({
        url: "sales-product-purchaserate",
        data: { "product_id": product_id, "branch_code": branch_code },
        type: 'GET',
        success: function (data) {
            if (data.form_is_valid) {
                w_product_rate = data.product_current_rate;
                $('#id_damage_quantity').val(1);
                $('#id_damage_amount').val(w_product_rate);
            } else {
                $('#id_damage_quantity').val(0);
            }
        }
    })
    return false;
}