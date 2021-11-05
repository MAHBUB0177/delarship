$(function () {
    $('#btnSubmit').click(function () {
        save_and_show_report();
    });
});

function save_and_show_report() {
    var data_url = $("#report_data").attr('data-url');
    var report_data = {
        'p_branch_code': $('#id_branch_code').val(), 'p_product_id': $('#id_product_id').val(),
        'p_from_date': $('#id_from_date').val(), 'p_upto_date': $('#id_upto_date').val(), 'p_brand_id': $('#id_brand_id').val(),
        'p_group_id': $('#id_group_id').val(), 'p_stock_available': $('#id_stock_available').val()
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

$(document).ready(function () {
    $('#id_group_id').select2();
    $('#id_brand_id').select2();
    refresh_branch_list('');
    refresh_group_list();
    refresh_brand_list();
    var product_id = document.getElementById("select2-id_product_id-container");
    product_id.textContent = "Select Product";
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});
