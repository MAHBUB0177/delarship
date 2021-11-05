$(function () {
	$('#btnSubmit').click(function () {
		save_and_show_report();
	});
});

function save_and_show_report() {
	var data_url = $("#report_data").attr('data-url');
	var report_data = {
		'p_branch_code': $('#id_branch_code').val(), 'p_from_date': $('#id_from_date').val(),
		'p_upto_date': $('#id_upto_date').val(), 'p_gl_code': $('#id_gl_code').val()
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
				alert(data.error_message);
				$('#page_loading').modal('hide');
			}
		}
	})
	return false;
}


$(document).ready(function () {
	$('#id_gl_code').select2();
	refresh_branch_list('');
	refresh_ledger_list();
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

function refresh_ledger_list() {
	var url = '/finance-choice-allledgerlist';
	$.ajax({
		url: url,
		success: function (data) {
			$("#id_gl_code").html(data);
		}
	});
	return false;
}
