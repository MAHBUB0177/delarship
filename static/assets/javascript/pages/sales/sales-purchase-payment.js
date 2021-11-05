
$('#btnSubmit').click(function () {
    post_edit_product_data();
});

let w_tran_screen = 'STOCK_PAYMENT';
let w_transaction_type = '';
let w_account_type = '';
let w_branch_code = '';

function post_edit_product_data() {
    var data_string = $("#stock_edit_form").serialize();
    var data_url = $("#stock_edit_form").attr('data-url');
    $('#page_loading').modal('show');
    console.log('Test');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                $('#page_loading').modal('hide');
                alert('Authorization Completed!')
                $('#stock_edit').modal('hide');
                location.reload();
            } else {
                $('#page_loading').modal('hide');
                alert(data.error_message)
                location.reload();
            }
        }
    })
    return false;
}

$("#id_tran_type_code").on("change paste keyup", function () {
    var tran_type = document.getElementById('id_tran_type_code').value;
    w_transaction_type = tran_type;
    account_list_refresh(w_account_type, w_tran_screen, w_transaction_type, w_branch_code)
    var total_price = (document.getElementById('id_total_price').value);
    var discount_amount = (document.getElementById('id_discount_amount').value);
    var price_after_disc = total_price - discount_amount;
    var total_price_after_disc = Math.round((price_after_disc) * 100) / 100;
    $('#id_total_price_after_disc').val(total_price_after_disc);
    $('#id_due_amount').val(total_price_after_disc);
});

$("#id_discount_amount").on("change paste keyup", function () {
    var total_price = (document.getElementById('id_total_price').value);
    var discount_amount = (document.getElementById('id_discount_amount').value);
    var total_pay = (document.getElementById('id_total_pay').value);
    var price_after_disc = total_price - discount_amount;
    var total_price_after_disc = Math.round((price_after_disc) * 100) / 100;
    $('#id_total_price_after_disc').val(total_price_after_disc);
    $('#id_due_amount').val(total_price_after_disc - total_pay);
});

$("#id_total_pay").on("change paste keyup", function () {

    var total_due = (((document.getElementById('id_total_price_after_disc').value) - (document.getElementById('id_total_pay').value)));
    var total_due_round = Math.round((total_due) * 100) / 100;
    if (total_due < 0) {
        $('#id_due_amount').val(0);
    } else {
        $('#id_due_amount').val(total_due_round);
    }
});

$(document).ready(function () {
    $('#id_account_number').select2()
    transaction_type_list('STOCK_PAYMENT');
});

function transaction_type_list(transaction_screen) {
    var url = '/sales-choice-trantype';
    $.ajax({
        url: url,
        data: {
            'transaction_screen': transaction_screen
        },
        success: function (data) {
            $("#id_tran_type_code").html(data);
        }
    });
    return false;
}

function account_list_refresh(account_type, tran_screen, transaction_type, branch_code) {
    var url = '/sales-choice-accountslist';
    $.ajax({
        url: url,
        data: {
            'account_type': account_type, 'tran_screen': tran_screen,
            'transaction_type': transaction_type, 'branch_code': branch_code,
        },
        success: function (data) {
            $("#id_account_number").html(data);
        }
    });
    return false;
}
