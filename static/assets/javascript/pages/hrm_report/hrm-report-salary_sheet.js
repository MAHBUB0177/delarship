$(function() {
    $('#btnSubmit').click(function() {
        save_and_show_report();
    });
});

function save_and_show_report() {
    var data_url = $("#report_data").attr('data-url');
    var report_data = { 'p_branch_code': $('#id_branch_code').val(), 'p_dept_id': $('#id_dept_id').val(), 'p_month_year': $('#id_month_year').val() };
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
        success: function(data) {
            if (data.form_is_valid) {
                console.log(data)

                $('#page_loading').modal('hide');
                window.open(data.report_urls + "/" + report_url, "_blank");
            } else {
                $('#page_loading').modal('hide');
                alert(data.error_message);
            }
        }
    })
    return false;
}


$(document).ready(function() {
    refresh_branch_list('');
    refresh_department_list('');
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
    monthYear();
});

$(window).on('load', function() {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});

function refresh_department_list(department_id) {
    var url = '/hrm-choice-department';
    $.ajax({
        url: url,
        data: {
            'department_id': department_id
        },
        success: function(data) {
            $("#id_dept_id").html(data);
        }
    });
    return false;
}

function refresh_branch_list(branch_code) {
    var url = 'appauth-choice-branchlist';
    $.ajax({ // initialize an AJAX request
        url: url, // set the url of the request
        data: {
            'branch_code': branch_code // add the id to the GET parameters
        },
        success: function(data) { // `data` is the return of the view function
            $("#id_branch_code").html(data); // replace the values of the input with the data that came from the server
        }
    });
    return false;
}


function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
        throw new TypeError("Cannot call a class as a function");
    }
}

function _defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
        var descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true;
        if ("value" in descriptor) descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
    }
}




function monthYear(){
    const months = ["JAN-","FEB-","MAR-","APR-","MAY-","JUN-","JUL-","AUG-","SEP-","OCT-","NOV-","DEC-"];
    for(i=0;i<months.length;i++){
      let month=months[i]
      let result=month.concat(new Date().getFullYear());
      document.getElementById("id_month_year").innerHTML +=
                    '<option value="' +
                    result +
                    '">' +
                    result +
                    "</option>";
    }
  }