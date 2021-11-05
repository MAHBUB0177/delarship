
var w_branch_code = 0;

$(document).ready(function () {
    $('#id_new_center_code').select2();
    var branch_code = document.getElementById('id_global_branch_code').value;
    w_branch_code = branch_code
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    w_branch_code = global_branch_code
    $('#id_branch_code').val(global_branch_code);
    refresh_branch_list('');
    refresh_transfer_center_list(w_branch_code);
});

$("#id_branch_code").on("change", function () {
    var branch_code = document.getElementById('id_branch_code').value;
    w_branch_code = branch_code;
    refresh_transfer_center_list(w_branch_code);
});

$(function () {
    $('#btnAddItem').click(function () {
        $(this).prop("disabled", true);
        if (post_tran_table_data()) {
            $(this).prop("disabled", false);
        }
    });
});

function refresh_transfer_center_list(branch_code) {
    var url = '/sales-choice-centerlist';
    $.ajax({
        url: url,
        data: {
            'branch_code': branch_code
        },
        success: function (data) {
            $("#id_new_center_code").html(data);
        }
    });
    return false;
}

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
                var new_center_code = document.getElementById("select2-id_new_center_code-container");
                new_center_code.textContent = "-----------------";
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
