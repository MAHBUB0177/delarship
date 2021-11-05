$(function () {
    $('#btnSubmit').click(function () {
        save_and_show_report();
    });
});

function save_and_show_report() {
    var data_url = $("#report_data").attr('data-url');
    var report_data = {
        'p_branch_code': $('#id_branch_code').val(), 'p_account_number': $('#id_account_number').val(),
        'p_from_date': $('#id_from_date').val(), 'p_upto_date': $('#id_upto_date').val()
    };
    var report_url = $('#report_url').val();
    report_data = JSON.stringify(report_data);
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: {
            'report_name': $('#report_name').val(),
            "report_data": report_data
        },
        cache: "false",
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                var account_number = document.getElementById("select2-id_account_number-container");
                account_number.textContent = "Select Customer";
                $('#page_loading').modal('hide');
                window.open(data.report_urls + "/" + report_url, "_blank");
            }
            else {
                $('#page_loading').modal('hide');
                alert(data.error_message);
            }
        }
    })
    return false;
}


let w_tran_screen = 'CLIENT_ACCOUNT';
let w_transaction_type = '';
let w_account_type = '';

$(document).ready(function () {
    refresh_branch_list('');
    var account_number = document.getElementById("select2-id_account_number-container");
    account_number.textContent = "Select Customer";
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});