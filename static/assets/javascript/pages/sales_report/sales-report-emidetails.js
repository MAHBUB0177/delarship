$(function () {
    $('#btnSubmit').click(function () {
        save_and_show_report();
    });
});

function save_and_show_report() {
    var data_url = $("#report_data").attr('data-url');
    var report_data = {
        'p_branch_code': $('#id_branch_code').val(), 'p_account_number': $('#id_account_number').val(),
        'p_emi_reference_no': $('#id_emi_reference_no').val(), 'p_ason_date': $('#id_ason_date').val(),
        'p_center_code': $('#id_center_code').val(),'p_emi_reporting_type': $('#id_emi_reporting_type').val() 
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

let w_tran_screen = 'EMI_RECEIVE';
let w_transaction_type = '';
let w_account_type = '';

$(document).ready(function () {
    $('#id_center_code').select2();
    refresh_branch_list('');
    var branch_code = document.getElementById('id_global_branch_code').value;
    refresh_center_list(branch_code);
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});

$("#id_branch_code").on("change", function () {
    var branch_code = document.getElementById('id_branch_code').value;
    refresh_center_list(branch_code);
});

$("#id_account_number").on("change paste keyup", function () {
    refresh_emiinvoice_list();
});

function refresh_emiinvoice_list() {
    var account_number = document.getElementById('id_account_number').value;
    var url = 'sales-choice-emiinvoice';
    $.ajax({
        url: url,
        data: {
            'account_number': account_number
        },
        success: function (data) {
            $("#id_emi_reference_no").html(data);
        }
    });
    return false;
}