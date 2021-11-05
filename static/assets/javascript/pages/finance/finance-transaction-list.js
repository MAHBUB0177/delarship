"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var table_data
var edit_stock_id

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
        var from_batch_number = document.getElementById('id_from_batch_number').value;
        var upto_batch_number = document.getElementById('id_upto_batch_number').value;
        var tran_from_date = document.getElementById('id_tran_from_date').value;
        var tran_upto_date = document.getElementById('id_tran_upto_date').value;
        var branch_code = document.getElementById('id_branch_code').value;

        var search_url = "/apifinance-tranlist-api/?from_batch_number="
          + from_batch_number + "&upto_batch_number=" + upto_batch_number + "&tran_from_date=" + tran_from_date
          + "&tran_upto_date=" + tran_upto_date + "&branch_code=" + branch_code;
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
            { data: 'batch_number' },
            { data: 'tran_date' },
            { data: 'total_debit_amount' },
            { data: 'transaction_narration' },
            { data: 'app_user_id' },
            { data: 'auth_by' },
            { data: 'cancel_by' },
            {
              "data": null,
              "defaultContent": '<button type="button" class="btn btn-secondary btn-sm">Dtl</button>'
            }
          ]
        });
      }
    }]);

    return fn_data_table;
  }();

$(function () {
  $('#btnSearchStockMst').click(function () {
    var tran_from_date = document.getElementById('id_tran_from_date').value;
    var tran_upto_date = document.getElementById('id_tran_upto_date').value;

    var branch_code = document.getElementById('id_branch_code').value;

    if (tran_upto_date === "" && tran_from_date === "" && branch_code === "") {
      alert("Please Select Transaction Date and Branch!")
    } else {
      new fn_data_table();
    }
  });
})

$(document).ready(function () {
  refresh_branch_list('');
  var global_branch_code = document.getElementById('id_global_branch_code').value;
  $('#id_branch_code').val(global_branch_code);
});

$(window).on('load', function () {
  var global_branch_code = document.getElementById('id_global_branch_code').value;
  $('#id_branch_code').val(global_branch_code);
});

function refresh_branch_list(branch_code) {
  var url = 'finance-choice-branchlist';
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

$(function () {
  var id = 0
  $('#dt-table-list').on('click', 'button', function () {

    try {
      var table_row = table_data.row(this).data();
      id = table_row['id']
      var cancel_by = table_row['cancel_by']
      var tran_date = table_row['tran_date']
      var batch_number = table_row['batch_number']
      var branch_code = table_row['branch_code']
    }
    catch (e) {
      var table_row = table_data.row($(this).parents('tr')).data();
      id = table_row['id']
      var cancel_by = table_row['cancel_by']
      var tran_date = table_row['tran_date']
      var batch_number = table_row['batch_number']
      var branch_code = table_row['branch_code']
    }

    var class_name = $(this).attr('class');
    console.log(class_name);

    if (class_name == 'btn btn-danger btn-sm') {
      if (cancel_by != null) {
        alert('This Batch already Canceled!')
      } else {
        batch_cancel(id);
      }
    }
    if (class_name == 'btn btn-secondary btn-sm') {
      view_transaction_details(id, batch_number, tran_date, branch_code);
    }
  })

  function view_transaction_details(id, batch_number, tran_date, branch_code) {
    var url = "finance-transaction-details-list";
    $.ajax({
      url: url,
      type: "GET",
      data: {
        'id': id, 'batch_number': batch_number, 'transaction_date': tran_date, 'branch_code': branch_code
      },
      success: function (data) {
        $('#view_details').modal('show');
        $("#data_table_details").html(data);
      }
    });
    return false;
  }

  function batch_cancel(id) {
    if (confirm('Are you sure you want to cancel this batch?') == true) {
      $('#page_loading').modal('show');
      $.ajax({
        url: "/finance-transaction-cancel/" + id,
        type: "POST",
        success: function (data) {
          if (data.form_is_valid) {
            $('#page_loading').modal('hide');
            alert(data.message);
            table_data.ajax.reload();
          } else {
            $('#page_loading').modal('hide');
            alert(data.error_message)
            table_data.ajax.reload();
          }
        }
      })
    }
  }

})