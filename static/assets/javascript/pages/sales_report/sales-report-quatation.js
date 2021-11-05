$(function () {
	$('#btnSubmit').click(function () {
		save_and_show_report();
	});
});

function save_and_show_report() {
        console.log("test")
	var data_url = $("#report_data").attr('data-url');
	var report_data = {
		
		'p_quotation_id':$("#id_quotation_id").val()
	};
	var report_url = $('#report_url').val();
	report_data = JSON.stringify(report_data);
	$('#page_loading').modal('show');
	$.ajax({
		url: data_url,
		data: {
			'report_name': $('#report_name').val(),
                        'report_data':report_data
		
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


