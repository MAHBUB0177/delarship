$(function () {
	$('#btnSubmit').click(function () {
		save_and_show_report();
	});
});

function save_and_show_report() {
	var data_url = $("#report_data").attr('data-url');
	var report_data = { 'p_employee_id': $('#id_employee_id').val(), 'p_from_date': $('#id_from_date').val(), 'p_upto_date': $('#id_upto_date').val() };
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
				window.open(data.report_urls, "_blank");
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
	refresh_employee_list();
});


function refresh_employee_list() {
	var employee_id = '';
	var url = 'appauth-choice-employeelist';
	$.ajax({
		url: url,
		data: {
			'employee_id': employee_id
		},
		success: function (data) {
			$("#id_employee_id").html(data);
		}
	});
	return false;
}
