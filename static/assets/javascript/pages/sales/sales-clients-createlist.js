"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var table_data

var fn_data_table =
  function () {
    function fn_data_table() {
      _classCallCheck(this, fn_data_table);

      this.init();
    }

    _createClass(fn_data_table, [{
      key: "init",
      value: function init() {
        this.table = this.table();
      }
    }, {
      key: "table",
      value: function table() {
        var client_phone = document.getElementById('id_client_phone').value;
        var client_name = document.getElementById('id_client_name').value;
        var search_url = "/sales-clients-api/?client_phone=" + client_phone + "&client_name=" + client_name;
        table_data = $('#dt-table-list').DataTable({
          "processing": true,
          destroy: true,
          "ajax": {
            "url": search_url,
            "type": "GET",
            "dataSrc": ""
          },
          responsive: true,
          dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>\n        <'table-responsive'tr>\n        <'row align-items-center'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 d-flex justify-content-end'p>>",
          language: {
            paginate: {
              previous: '<i class="fa fa-lg fa-angle-left"></i>',
              next: '<i class="fa fa-lg fa-angle-right"></i>'
            }
          },
          columns: [
            { data: 'client_id' },
            { data: 'client_name' },
            { data: 'client_type' },
            { data: 'client_father_name' },
            { data: 'client_mother_name' },
            { data: 'client_blood_group' },
            { data: 'client_sex' },
            { data: 'client_religion' },
            { data: 'client_marital_status' },
            { data: 'client_national_id' },
            { data: 'client_present_address' },
            { data: 'client_permanent_address' },
            { data: 'client_phone' },
            { data: 'client_joining_date' },
            { data: 'client_date_of_birth' },
            {
              "data": null,
              "defaultContent": '<button type="button" class="btn btn-info btn-sm">Edit</button>'
            }
          ]
        });
      }
    }]);

    return fn_data_table;
  }();

var id = 0


$(document).ready(function () {
  $('#id_center_code').select2();
  refresh_branch_list('');
  refresh_clienttype_list('CLIENT_ENTRY');
  var branch_code = document.getElementById('id_global_branch_code').value;
  refresh_center_list(branch_code);
});

$("#id_branch_code").on("change", function () {
  var branch_code = document.getElementById('id_branch_code').value;
  refresh_center_list(branch_code);
});

$(window).on('load', function () {
  var global_branch_code = document.getElementById('id_global_branch_code').value;
  $('#id_branch_code').val(global_branch_code);
});

function refresh_clienttype_list(transaction_screen) {
  var url = '/sales-choice-clienttype';
  $.ajax({
      url: url,
      data: {
          'transaction_screen': transaction_screen
      },
      success: function (data) {
          $("#id_client_type").html(data);
      }
  });
  return false;
}


$(function () {
  $('#btnSearch').click(function () {

    var client_phone = document.getElementById('id_client_phone').value;
    var client_name = document.getElementById('id_client_name').value;

    if (client_phone === "" & client_name === "") {
      alert("Please Enter Phone Number or Client Name!")
    } else {
      new fn_data_table();
    }
  });
})

$(window).on('load', function () {
  var global_branch_code = document.getElementById('id_global_branch_code').value;
  $('#id_branch_code').val(global_branch_code);
});

$("#id_client_present_address").on("change paste keyup", function () {
  $('#id_client_permanent_address').val(document.getElementById('id_client_present_address').value);
});

$(function () {

  $('#dt-table-list').on('click', 'button', function () {

    try {
      var table_row = table_data.row(this).data();
      id = table_row['client_id']
    }
    catch (e) {
      var table_row = table_data.row($(this).parents('tr')).data();
      id = table_row['client_id']
    }

    var class_name = $(this).attr('class');
    if (class_name == 'btn btn-info btn-sm') {
      show_edit_form(id);
    }

  })

  function show_edit_form(id) {
    $.ajax({
      url: '/sales-clients-edit/' + id,
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $('#edit_model').modal('show');
      },
      success: function (data) {
        $('#edit_model .modal-content').html(data.html_form);
      }
    })
  }

});

$(function () {

  $(function () {
    $('#btnAddItem').click(function () {
      post_tran_table_data();

    });
  });


  function post_tran_table_data() {
    var data_string = $("#tran_table_data").serialize();
    var data_url = $("#tran_table_data").attr('data-url');
    $('#page_loading').modal('show');
    $.ajax({
      url: data_url,
      data: data_string,
      type: 'POST',
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          document.getElementById("tran_table_data").reset();
          $('#page_loading').modal('hide');
          alert(data.success_message);
          var center_code = document.getElementById("select2-id_center_code-container");
          center_code.textContent = "----------";
          var global_branch_code = document.getElementById('id_global_branch_code').value;
          $('#id_branch_code').val(global_branch_code);
        } else {
          $('#page_loading').modal('hide');
          alert(data.error_message);
        }
      }
    })
    return false;
  }

});