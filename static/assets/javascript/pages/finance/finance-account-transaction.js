$(document).ready(function () {
    transaction_type_list('CASH_TRANSACTION');
    $('#id_tran_screen').val('CASH_TRANSACTION');
    var account_number = document.getElementById("select2-id_account_number-container");
    account_number.textContent = "--Select Account--";
    refresh_branch_list('');
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
    $('#id_tran_gl_code').select2();
    transaction_cashnbanklist_list(global_branch_code);
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});

$("#id_branch_code").on("change paste keyup", function () {
    var branch_code = document.getElementById('id_branch_code').value;
    transaction_cashnbanklist_list(branch_code);
});

let w_tran_screen = 'CASH_TRANSACTION';
let w_transaction_type = '';
let w_account_type = '';

function transaction_type_list(transaction_screen) {
    var url = '/finance-choice-trantype';
    $.ajax({
        url: url,
        data: {
            'transaction_screen': transaction_screen
        },
        success: function (data) {
            $("#id_tran_type").html(data);
        }
    });
    return false;
}

function transaction_cashnbanklist_list(branch_code) {
    var url = '/finance-choice-cashnbanklist';
    $.ajax({
        url: url,
        data: {
            'branch_code': branch_code
        },
        success: function (data) {
            $("#id_receipt_payment_ledger").html(data);
        }
    });
    return false;
}

function refresh_branch_list(branch_code) {
    var url = 'finance-choice-branchlist';
    $.ajax({
        url: url,
        data: {
            'branch_code': branch_code
        },
        success: function (data) {
            $("#id_branch_code").html(data);
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
                    var account_number = document.getElementById("select2-id_account_number-container");
                    account_number.textContent = "--Select Account--";
                    $('#id_account_number').val('');
                    var global_branch_code = document.getElementById('id_global_branch_code').value;
                    $('#id_branch_code').val(global_branch_code);
                    alert(data.success_message);
                } else {
                    $('#page_loading').modal('hide');
                    alert(data.error_message);
                }
            }
        })
        return false;
    }

    $("#id_tran_gl_code").on("change paste keyup", function () {
        var tran_gl_code = document.getElementById('id_tran_gl_code').value;
        if (tran_gl_code != '0') {
            get_gl_name();
        }
    });

    $("#id_account_number").on("change paste keyup", function () {
        get_client_info();
    });

    $("#id_tran_type").on("change paste keyup", function () {
        var tran_type = document.getElementById('id_tran_type').value;
        w_transaction_type = tran_type;
        var account_number = document.getElementById("select2-id_account_number-container");
        account_number.textContent = "--Select Account--";
        $('#id_current_balance').val('');
        $('#id_account_number').val('');
    });

    function get_client_info() {
        var account_number = document.getElementById('id_account_number').value;
        $.ajax({
            url: "/finance-account-byacnumber/" + account_number,
            type: 'GET',
            success: function (data) {
                if (data.form_is_valid) {
                    $('#id_current_balance').val(data.account_balance);
                } else {
                    $('#id_current_balance').val('');
                }
            }
        })
        return false;
    }

});