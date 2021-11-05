var w_branch_code = 0;

$(document).ready(function () {
    $('#id_new_center_code').select2();
    var branch_code = document.getElementById('id_global_branch_code').value;
    w_branch_code = branch_code
});

$(window).on('load', function () {
    refresh_branch_list('');
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    w_branch_code = global_branch_code
    $('#id_branch_code').val(global_branch_code);
});

$("#id_branch_code").on("change", function () {
    var branch_code = document.getElementById('id_branch_code').value;
    w_branch_code = branch_code;
});


$("#id_client_id").on("change", function () {
    get_clients_balance();
});

function get_clients_balance() {
    var client_id = document.getElementById('id_client_id').value;
    $.ajax({
        url: "/finance-account-clientbalance/" + client_id,
        type: 'GET',
        success: function (data) {
            if (data.form_is_valid) {
                $('#id_balance_message').val(data.message);
            } else {
                $('#id_balance_message').val('');
            }
        }
    })
    return false;
}

$(function () {
    $('#btnAddItem').click(function () {
        if (confirm('Are you sure you want to close this Customer?') == true) {
            if (confirm('Please Confirm Again!') == true) {
                post_tran_table_data();
            }
        }
    });
});

$(function () {
    $('#btnReomveClient').click(function () {
        if (confirm('Are you sure you want to remove this Customer?') == true) {
            if (confirm('Please Confirm Again!') == true) {
                post_client_reomve_data();
            }
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
                alert(data.success_message);
                document.getElementById("tran_table_data").reset();
                $('#page_loading').modal('hide');
                var client_id = document.getElementById("select2-id_client_id-container");
                client_id.textContent = "-----------------";
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

function post_client_reomve_data() {
    var data_string = $("#tran_table_data").serialize();
    var data_url = 'sales-client-closing-remove';
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
                var client_id = document.getElementById("select2-id_client_id-container");
                client_id.textContent = "-----------------";
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
