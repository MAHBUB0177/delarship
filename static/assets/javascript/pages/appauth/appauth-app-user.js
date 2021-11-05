$(document).ready(function () {
    refresh_branch_list('');
    $('#id_employee_id').select2();
    $('#id_branch_code').select2();
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});