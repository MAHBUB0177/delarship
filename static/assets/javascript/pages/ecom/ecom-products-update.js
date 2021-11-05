
// $('#btnUpdate').click(function () {
//   var data_string = $("#ecom-product-update").serialize();
//   console.log(data_string)
//   var data_url = $("#ecom-product-update").attr('data-url');
//   $('#page_loading').modal('show');
//   $.ajax({
//     url: data_url,
//     data: data_string,
//     type: 'POST',
//     dataType: 'json',
//     success: function (data) {
//       if (data.form_is_valid) {
//         $('#page_loading').modal('hide');
//         alert(data.success_message);
//       } else {
//         $('#page_loading').modal('hide');
//         alert(data.error_message);
//       }
//     }
//   })
// })

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
    aspectRatio: 16 / 9,
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
      var product_id = $('#id_product_id').val()
      $.ajax({
        type: "POST",
        dataType: "json",
        url: "/ecom-product-image-insert",
        data: { 'image': base64data, 'product_id': product_id },
        success: function (data) {
          console.log(data)
          $modal.modal('hide');
          document.getElementById('image_upload').value = ""
          // location.reload();
          var rowCount = $('#product_images tr').length;
          $("#product_images > tbody").append(
            "<tr><td>" + rowCount + "</td><td><img src='/media/" + data.new_image.image + "' style='height: 120px;'></td><td>" + data.new_image.image_serial + "</td><td><button class='btn btn-danger' id='" + data.new_image.id + "' onclick='image_delete_button(" + data.new_image.id + ")'>Delete</button>"
          );
        }
      });
    }
  });

})

function image_delete_button(id) {
  $('#image-delete').modal('show')
  $("#image-confrim").attr('data-id', id)
}
$("#image-confrim").click(function () {
  let id = $("#image-confrim").attr('data-id')
  delete_image(id)
})
function delete_image(id) {

  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/ecom-product-image-delete",
    data: { 'id': id },
    success: function (data) {
      $('#image-delete').modal('hide')
      var button = $('#' + id)
      var table_row = jQuery(button).closest('tr');
      table_row.remove();
      $('#product_images tbody tr').each(function (idx) {
        $(this).children(":eq(0)").html(idx + 1);
      });
    }
  });
}
tinymce.init({ selector: '.tinymce' });