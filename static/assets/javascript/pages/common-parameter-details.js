function refresh_branch_list(branch_code) {
    var url = '/appauth-choice-branchlist';
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


function refresh_center_list(branch_code) {
    var url = '/sales-choice-centerlist';
    $.ajax({
        url: url,
        data: {
            'branch_code': branch_code
        },
        success: function (data) {
            $("#id_center_code").html(data);
        }
    });
    return false;
}

function refresh_employee_list(branch_code) {
    var url = '/sales-choice-employeelist';
    $.ajax({
        url: url,
        data: {
            'branch_code': branch_code
        },
        success: function (data) {
            $("#id_employee_id").html(data);
        }
    });
    return false;
}

function refresh_appuser_list(branch_code) {
    var url = '/appauth-choice-appuserlist';
    $.ajax({
        url: url,
        data: {
            'branch_code': branch_code
        },
        success: function (data) {
            $("#id_app_user_id").html(data);
        }
    });
    return false;
}

function refresh_group_list() {
    var url = '/sales-choice-productgrouplist';
    $.ajax({
        url: url,
        success: function (data) {
            $("#id_group_id").html(data);
        }
    });
    return false;
}

function refresh_brand_list() {
    var url = '/sales-choice-productbrandlist';
    $.ajax({
        url: url,
        success: function (data) {
            $("#id_brand_id").html(data);
        }
    });
    return false;
}
