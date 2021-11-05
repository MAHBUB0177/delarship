// $(function () {
// 	$('#btnSubmit').click(function () {
// 		post_edit_form_data();
// 	});
// });

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
//Image
function modal_cancle() {
  var selete_img = document.getElementById('image_upload').value = ""
  $('#modal').modal('hide')
}

var $modal = $('#modal');
var image = document.getElementById('image');
var cropper;

$("body").on("change", "#image_upload", function (e) {
  var files = e.target.files;
  var done = function (url) {
    image.src = url;
    $modal.modal('show');
  };
  var reader;
  var file;
  var url;
  if (files && files.length > 0) {
    file = files[0];
    if (URL) {
      done(URL.createObjectURL(file));
    } else if (FileReader) {
      reader = new FileReader();
      reader.onload = function (e) {
        done(reader.result);
      };
      reader.readAsDataURL(file);
    }
  }
});
$modal.on('shown.bs.modal', function () {
  cropper = new Cropper(image, {
    preview: '.preview',
    aspectRatio: 16 / 16,
  });

}).on('hidden.bs.modal', function () {
  cropper.destroy();
  cropper = null;
});


$("#crop").click(function () {
  canvas = cropper.getCroppedCanvas({
    width: 800,
    height: 800,
  });
  canvas.toBlob(function (blob) {
    url = URL.createObjectURL(blob);
    var reader = new FileReader();
    reader.readAsDataURL(blob);
    reader.onloadend = function () {
      var base64data = reader.result;
      var id = $('#slider_id').val();
      $.ajax({
        type: "POST",
        dataType: "json",
        url: "/ecom-slider-image-insert",
        data: { 'image': base64data, 'id': id },
        success: function (data) {
          console.log(data)
          $modal.modal('hide');
          document.getElementById('image_upload').value = ""
          $('.set_slider_image').attr('src', data.image)
          $('#edit_model').modal('hide');
          setTimeout(() => {
            $('#edit_model').modal('show');
          }, 500);
          // location.reload();

        }
      });
    }
  });

})
