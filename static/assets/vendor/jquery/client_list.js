$(function () {
	$('#btnLaunch').click(function () {
		$('#ClientModel').modal('show');
	});
});

$(document).ready(function () {
	$("#SearchClient").on("keyup", function () {
		var value = $(this).val().toLowerCase();
		$("#ClientTable tr").filter(function () {
			$(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
		});
	});
});