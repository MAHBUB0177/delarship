$(document).ready(function () {
    transaction_type_list('LEDCASH_TRAN');
    refresh_ledger_list('LEDCASH_TRAN');
    $('#id_tran_screen').val('LEDCASH_TRAN');
    refresh_branch_list('');
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
    $('#id_tran_gl_code').select2();
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});

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

function refresh_ledger_list(tran_type_id) {
    var url = '/finance-choice-trantypeledger';
    $.ajax({
        url: url,
        data: {
            'tran_type_id': tran_type_id
        },
        success: function (data) {
            $("#id_tran_gl_code").html(data);
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


$("#id_tran_type").on("change paste keyup", function () {
    const tran_type = document.getElementById('id_tran_type').value;
    refresh_ledger_list(tran_type);
});


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
                alert(data.success_message);
                var tran_gl_code = document.getElementById("select2-id_tran_gl_code-container");
                tran_gl_code.textContent = "----------";
                $('#tran_gl_code').val('');
                var global_branch_code = document.getElementById('id_global_branch_code').value;
                $('#id_branch_code').val(global_branch_code);
            } else {
                $('#page_loading').modal('hide');
                alert(data.error_message);
            }
        }
    })
    return false;
}

$("#id_phone_number").on("change paste keyup", function () {
    get_client_info();
});