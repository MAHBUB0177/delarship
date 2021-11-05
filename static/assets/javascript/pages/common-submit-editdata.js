$(function () {
	$('#btnSubmit').click(function () {
		post_edit_form_data();
	});
});

function post_edit_form_data() {
	const data_string = $("#edit_form").serialize();
	const data_url = $("#edit_form").attr('data-url');
	console.log("Test");
	$('#page_loading').modal('show');
	$.ajax({
		url: data_url,
		data: data_string,
		type: 'POST',
		dataType: 'json',
		success: function (data) {
			
			if (data.form_is_valid) {
				$('#page_loading').modal('hide');
				$('#edit_model').modal('hide');
				table_data.ajax.reload();
			} else {
				$('#page_loading').modal('hide');
				alert(data.error_message);
				table_data.ajax.reload();
			}
		}
	})
	return false;
}