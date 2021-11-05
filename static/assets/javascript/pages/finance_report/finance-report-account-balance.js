$(function () {
	$('#btnSubmit').click(function () {
		save_and_show_report();
	});
});

function save_and_show_report() {
	var data_url = $("#report_data").attr('data-url');
	var report_data = { 'p_branch_code': $('#id_branch_code').val(), 'p_account_type': $('#id_products_type').val(), 
	'p_zero_balance': $('#id_zero_balance').val(),'p_account_number': $('#id_account_number').val(),
	'p_center_code': $('#id_center_code').val() };
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
				alert(data.error_message)
			}
		}
	})
	return false;
}

$(document).ready(function () {
	refresh_accounttype_list();
});

function refresh_accounttype_list() {
	var products_type = '';
	var url = 'finance-choice-accounttype';
	$.ajax({
		url: url,
		data: {
			'products_type': products_type
		},
		success: function (data) {
			$("#id_products_type").html(data);
		}
	});
	return false;
}

let w_account_type = '';
let w_tran_screen = '';
let w_transaction_type = '';

$(document).ready(function () {
	$("#id_center_code").select2();
	refresh_branch_list('');
	var global_branch_code = document.getElementById('id_global_branch_code').value;
	refresh_center_list(global_branch_code);
});

$(window).on('load', function () {
	var global_branch_code = document.getElementById('id_global_branch_code').value;
	$('#id_branch_code').val(global_branch_code);
});


$("#id_branch_code").on("change", function () {
	var branch_code = document.getElementById('id_branch_code').value;
	refresh_center_list(branch_code);
});

$("#id_products_type").on("change paste keyup", function () {
	const account_type = document.getElementById('id_products_type').value;
	w_account_type = account_type;
	const account_number = document.getElementById("select2-id_account_number-container");
	account_number.textContent = "--Select Account--";
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

function refresh_center_list(branch_code) {
	var url = '/finance-choice-centerlist';
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
