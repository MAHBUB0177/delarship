$(function () {
	$('#btnSubmit').click(function () {
		save_and_show_report();
	});
});

function save_and_show_report() {
	var data_url = $("#report_data").attr('data-url');
	var report_data = {
		'p_branch_code': $('#id_branch_code').val(), 'p_product_id': $('#id_product_id').val(),
		'p_employee_id': $('#id_employee_id').val(), 'p_order_date': $('#id_order_date').val()
		
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
	$("#id_employee_id").select2()
	get_employee_name();
   
    refresh_branch_list('');
    
    var product_id = document.getElementById("select2-id_product_id-container");
    product_id.textContent = "Select Product";
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});



function get_employee_name() {
	$.ajax({
	    url: "apiauth-employee-api",
	    type: "get",
	    datatype: "json",
	    success: function (data) {
		console.log(data)
		data.forEach((value) => {
		    document.getElementById("id_employee_id").innerHTML +=
			'<option value="' +
			value.employee_id +
			'" id="' +
			value.employee_name +
			'">' +
			value.employee_name +
			"</option>";
		});
	    },
	});
      }