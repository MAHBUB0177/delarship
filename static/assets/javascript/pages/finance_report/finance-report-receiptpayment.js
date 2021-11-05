$(function () {
	$('#btnSubmit').click(function () {
		save_and_show_report();
	});
});

function save_and_show_report() {
	var data_url = $("#report_data").attr('data-url');
	var report_data = { 'p_branch_code': $('#id_branch_code').val(), 'p_ason_date': $('#id_ason_date').val() };
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
				alert(data.error_message);
				$('#page_loading').modal('hide');
			}
		}
	})
	return false;
}


$(document).ready(function () {
	refresh_branch_list('');
});

$(window).on('load', function () {
	var global_branch_code = document.getElementById('id_global_branch_code').value;
	$('#id_branch_code').val(global_branch_code);
});

function refresh_branch_list(branch_code) {
	var url = '/finance-choice-branchlist';
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
