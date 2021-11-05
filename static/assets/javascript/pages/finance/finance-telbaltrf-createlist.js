
$('#btnAddRecord').click(function () {
    post_tran_table_data();
});

function post_tran_table_data() {
    const data_string = $("#tran_table_data").serialize();
    const data_url = $("#tran_table_data").attr('data-url');
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                $('#page_loading').modal('hide');
                document.getElementById("tran_table_data").reset();
                alert(data.success_message);
                var res_teller = document.getElementById("select2-id_res_teller_id-container");
                res_teller.textContent = "----------";
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

$("#id_branch_code").on("change", function () {
    refresh_user_list();
});

$(document).ready(function () {
    $("#id_res_teller_id").select2();
    refresh_user_list();
    refresh_branch_list();
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});

function refresh_user_list() {
    var branch_code = document.getElementById('id_branch_code').value;
    var url = '/appauth-choice-appuserlist';
    $.ajax({
        url: url,
        data: {
            'branch_code': branch_code
        },
        success: function (data) {
            $("#id_res_teller_id").html(data);
        }
    });
    return false;
}
