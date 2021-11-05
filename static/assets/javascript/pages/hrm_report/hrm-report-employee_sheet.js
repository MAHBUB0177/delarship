$(function() {
   $('#btnSubmit').click(function() {
       save_and_show_report();
   });
});

function save_and_show_report() {
   var data_url = $("#report_data").attr('data-url');
   var report_data = { 'p_employee_id': $('#id_employee_id').val(), 'p_from_date': $('#p_from_date').val(), 'p_upto_date': $('#p_upto_date').val() };
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
          console.log("man")
           if (data.form_is_valid) {

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
   refresh_employee_list('');
   // refresh_department_list('');
   // var global_branch_code = document.getElementById('id_global_branch_code').value;
   // $('#id_branch_code').val(global_branch_code);
});

// $(window).on('load', function() {
//    var global_branch_code = document.getElementById('id_global_branch_code').value;
//    $('#id_branch_code').val(global_branch_code);
// });

// function refresh_employee_list(employee_id) {
//    var url = '/hrm-choice-department';
//    $.ajax({
//        url: url,
//        data: {
//            'department_id': department_id
//        },
//        success: function(data) {
//            $("#id_dept_id").html(data);
//        }
//    });
//    return false;
// }

// function refresh_branch_list(branch_code) {
//    var url = 'appauth-choice-branchlist';
//    $.ajax({ // initialize an AJAX request
//        url: url, // set the url of the request
//        data: {
//            'branch_code': branch_code // add the id to the GET parameters
//        },
//        success: function(data) { // `data` is the return of the view function
//            $("#id_branch_code").html(data); // replace the values of the input with the data that came from the server
//        }
//    });
//    return false;
// }


// function _classCallCheck(instance, Constructor) {
//    if (!(instance instanceof Constructor)) {
//        throw new TypeError("Cannot call a class as a function");
//    }
// }

// function _defineProperties(target, props) {
//    for (var i = 0; i < props.length; i++) {
//        var descriptor = props[i];
//        descriptor.enumerable = descriptor.enumerable || false;
//        descriptor.configurable = true;
//        if ("value" in descriptor) descriptor.writable = true;
//        Object.defineProperty(target, descriptor.key, descriptor);
//    }
// }