"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var table_data
var edit_stock_id

// DataTables Demo
// =============================================================
var fn_data_table =
  /*#__PURE__*/
  function () {
    function fn_data_table() {
      _classCallCheck(this, fn_data_table);

      this.init();
    }

    _createClass(fn_data_table, [{
      key: "init",
      value: function init() {
        // event handlers
        this.table = this.table();
      }
    }, {
      key: "table",
      value: function table() {
        var invoice_number = document.getElementById('id_invoice_number').value;
        var invoice_from_date = document.getElementById('id_invoice_from_date').value;
        var invoice_upto_date = document.getElementById('id_invoice_upto_date').value;
        var customer_phone = document.getElementById('id_customer_phone').value;
        var employee_id = document.getElementById('id_employee_id').value;
        var branch_code = document.getElementById('id_branch_code').value;
        var center_code = document.getElementById('id_center_code').value;
        var search_url = "/sales-invoice-api/?invoice_number=" + invoice_number + "&branch_code=" + branch_code
          + "&invoice_from_date=" + invoice_from_date + "&invoice_upto_date=" + invoice_upto_date + "&customer_phone="
          + customer_phone + "&employee_id=" + employee_id + "&center_code=" + center_code;
        console.log(search_url)
        table_data = $('#dt-invoice-list').DataTable({
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
            { data: 'branch_code' },
            { data: 'invoice_number' },
            { data: 'invoice_date' },
            { data: 'customer_name' },
            { data: 'customer_phone' },
            { data: 'employee_id' },
            { data: 'total_quantity' },
            { data: 'bill_amount' },
            { data: 'pay_amount' },
            { data: 'advance_pay' },
            { data: 'total_discount_amount' },
            { data: 'status' },
            { data: 'invoice_comments' },
            {
              "data": null,
              "defaultContent": '<button type="button" class="btn btn-info btn-sm">Return</button>' + '&nbsp;&nbsp' +
                '<button type="button" class="btn btn-danger btn-sm">Cancel</button>' + '&nbsp;&nbsp' +
                '<button type="button" class="btn btn-secondary btn-sm">Dtl</button>' + '&nbsp;&nbsp' +
                '<button type="button" class="btn btn-success btn-sm">Print Invoice</button>'
            }
          ]
        });
      }
    }]);

    return fn_data_table;
  }();

$(function () {
  $('#btnSearchStockMst').click(function () {
    var invoice_number = document.getElementById('id_invoice_number').value;
    var invoice_from_date = document.getElementById('id_invoice_from_date').value;
    var invoice_upto_date = document.getElementById('id_invoice_upto_date').value;
    var customer_phone = document.getElementById('id_customer_phone').value;
    var employee_id = document.getElementById('id_employee_id').value;

    if (invoice_number === "" & customer_phone === "" & invoice_from_date === "" & employee_id === "" & invoice_upto_date === "") {
      alert("Please enter at least one value.")
    } else {
      new fn_data_table();
    }
  });
})


$(document).ready(function () {
  $('#id_center_code').select2();
  refresh_branch_list('');
  var branch_code = document.getElementById('id_global_branch_code').value;
  refresh_center_list(branch_code);
});

$(window).on('load', function () {
  var global_branch_code = document.getElementById('id_global_branch_code').value;
  $('#id_branch_code').val(global_branch_code);
});

$("#id_branch_code").on("change", function () {
  var branch_code = document.getElementById('id_branch_code').value;
  refresh_center_list(branch_code);
});

$(function () {


  $(function () {
    var id = 0
    $('#dt-invoice-list').on('click', 'button', function () {

      try {
        var table_row = table_data.row(this).data();
        id = table_row['id']
        var invoice_number = table_row['invoice_number']
        var invoice_date = table_row['invoice_date']
        var invoice_status = table_row['status']
      }
      catch (e) {
        var table_row = table_data.row($(this).parents('tr')).data();
        id = table_row['id']
        var invoice_number = table_row['invoice_number']
        var invoice_date = table_row['invoice_date']
        var invoice_status = table_row['status']
      }

      var class_name = $(this).attr('class');

      if (class_name == 'btn btn-info btn-sm') {
        if (invoice_status == 'C') {
          alert('This Invoice already Canceled!')
        } else {
          invoice_return(id);
        }
      }
      if (class_name == 'btn btn-danger btn-sm') {
        if (invoice_status == 'C') {
          alert('This Invoice already Canceled!')
        } else {
          invoice_cancel(id);
        }
      }
      if (class_name == 'btn btn-secondary btn-sm') {
        view_invoice_details(id);
      }
      if (class_name == 'btn btn-success btn-sm') {
        save_and_show_report(invoice_number);
      }
    })

    function invoice_return(id) {
      if (confirm('Are you sure you want to return this invoice?') == true) {
        $('#page_loading').modal('show');
        $.ajax({
          url: "/sales-invoice-return/" + id,
          type: "POST",
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
    }

    function save_and_show_report(p_invoice_number) {
      console.log("test")
      var data_url = 'appauth-report-submit/';
      var report_name = 'sales_invoice';
      var report_data = { 'p_invoice_number': p_invoice_number };
      report_data = JSON.stringify(report_data);
      console.log(report_data)
      $.ajax({
        url: data_url,
        data: {
          'report_name': report_name,
          "report_data": report_data
        },
        cache: "false",
        type: 'POST',
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            window.open(data.report_urls + '/sales-invoice-print-view', "_blank");
          }
          else {
            alert(data.error_message)
          }
        }
      })
      return false;
    }

    function view_invoice_details(id) {
      var url = "sales-invoice-details/" + id;
      $.ajax({
        url: url,
        type: "GET",
        data: {
          'id': id
        },
        success: function (data) {
          $('#view_details').modal('show');
          $("#data_table_details").html(data);
        }
      });
      return false;
    }

    function invoice_cancel(id) {
      if (confirm('Are you sure you want to cancel this Invoice?') == true) {
        $('#page_loading').modal('show');
        $.ajax({
          url: "/sales-invoice-cancel/" + id,
          type: "POST",
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
    }
  })

});
