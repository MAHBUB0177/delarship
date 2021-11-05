"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var table_data
var app_user_name
var id

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
        var app_user_id = document.getElementById('id_app_user_id').value;
        var employee_id = document.getElementById('id_employee_id').value;

        var search_url = "/apiauth-applicationuser-api/?app_user_id=" + app_user_id + "&employee_id=" + employee_id;
        console.log(search_url)
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
            { data: 'employee_id' },
            { data: 'employee_name' },
            { data: 'app_user_id' },
            { data: 'reset_user_password' },
            { data: 'is_active' },
            {
              "data": null,
              "defaultContent": '<button type="button" class="btn btn-warning show-form-update"> <span class="glyphicon glyphicon-pencil"></span> Reset Password</button>' + '&nbsp;&nbsp' + '<button type="button" class="btn btn-info show-form-update"> <span class="glyphicon glyphicon-pencil"></span> Update Limit </button>'
            }
          ]
        });
      }
    }]);

    return fn_data_table;
  }();

$(document).ready(function () {
  $('#id_employee_id').select2();
});

$(function () {

  $(function () {
    $('#btnSearchStockMst').click(function () {
      new fn_data_table();
    });
  })

  $(function () {
    $('#dt-table-list').on('click', 'button', function () {

      try {
        var table_row = table_data.row(this).data();
        var id = table_row['app_user_id'];
        var django_user_id = table_row['django_user_id'];
      }
      catch (e) {
        var table_row = table_data.row($(this).parents('tr')).data();
        var id = table_row['app_user_id'];
        var django_user_id = table_row['django_user_id'];
      }

      var class_name = $(this).attr('class');
      if (class_name == 'btn btn-warning show-form-update') {
        if (confirm('Are you sure you want to reset password?') == true) {
          reset_user_password(id);
        }
      }

      var class_name = $(this).attr('class');
      if (class_name == 'btn btn-info show-form-update') {
        show_edit_form(django_user_id);
      }

    })

    function show_edit_form(django_user_id) {
      $('#page_loading').modal('show');
      $.ajax({
        url: '/appauth-appuser-update/' + django_user_id,
        type: 'GET',
        dataType: 'json',
        beforeSend: function () {
          $('#page_loading').modal('hide');
          $('#edit_model').modal('show');
        },
        success: function (data) {
          $('#page_loading').modal('hide');
          $('#edit_model .modal-content').html(data.html_form);
        }
      })
    }

    function reset_user_password(id) {
      $('#page_loading').modal('show');
      $.ajax({
        url: 'appauth-reset-userspassword',
        data: {
          'app_user_id': id
        },
        type: 'POST',
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            $('#page_loading').modal('hide');
            alert(data.success_message);
            table_data.ajax.reload();
          } else {
            $('#page_loading').modal('hide');
            alert(data.error_message);
            table_data.ajax.reload();
          }
        }
      })
    }

  })

});