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
        var return_invoice = document.getElementById('id_return_invoice_number').value;
        var invoice_from_date = document.getElementById('id_invoice_from_date').value;
        var invoice_upto_date = document.getElementById('id_invoice_upto_date').value;
        var product_id = document.getElementById('id_product_id').value;
        var branch_code = document.getElementById('id_branch_code').value;
        var search_url = "/delar-return-packet-api/?return_invoice=" + return_invoice + "&branch_code=" + branch_code
          + "&invoice_from_date=" + invoice_from_date + "&invoice_upto_date=" + invoice_upto_date +"&product_id="+product_id;
        console.log(search_url)
        table_data = $('#dt-invoice-return-list').DataTable({
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
            { data: 'return_invoice' },
            { data: 'return_date' },
            { data: 'product_id' },
            { data: 'receive_quantity' },
            {data:'receive_value'},
            { data: 'status' },
            {
              "data": null,
              "defaultContent": '<button type="button" class="btn btn-danger btn-sm">Cancel</button>' + '&nbsp;&nbsp' +
                '<button type="button" class="btn btn-secondary btn-sm">Dtl</button>'
            }
          ]
        });
      }
    }]);

    return fn_data_table;
  }();

$(function () {
  $('#btnSearchStockMst').click(function () {
    console.log("ok")
    var return_invoice = document.getElementById('id_return_invoice_number').value;
    var invoice_from_date = document.getElementById('id_invoice_from_date').value;
    var invoice_upto_date = document.getElementById('id_invoice_upto_date').value;
    var product_id = document.getElementById('id_product_id').value;

    if  (return_invoice === "" & invoice_from_date === "" & product_id === "" & invoice_upto_date === "") {
      alert("Please enter at least one value.")
    } else {
      new fn_data_table();
    }
  });
})

$(document).ready(function () {
 get_product_name();
  $('#id_product_id').select2();
  get_employee_name();
  $('#id_employee_id').select2();
  refresh_branch_list('');
  var branch_code = document.getElementById('id_global_branch_code').value;
  refresh_employee_list(branch_code);
});

$(window).on('load', function () {
  var global_branch_code = document.getElementById('id_global_branch_code').value;
  $('#id_branch_code').val(global_branch_code);
});

$("#id_branch_code").on("change", function () {
  var branch_code = document.getElementById('id_branch_code').value;
  refresh_employee_list(branch_code);
});

$(function () {

  $(function () {
    var id = 0
    $('#dt-invoice-return-list').on('click', 'button', function () {

      try {
        var table_row = table_data.row(this).data();
        id = table_row['id']
        var return_invoice = table_row['return_invoice']
        var return_date = table_row['return_date']
        var invoice_status = table_row['status']
      }
      catch (e) {
        var table_row = table_data.row($(this).parents('tr')).data();
        id = table_row['id']
        var return_invoice = table_row['return_invoice']
        var return_date = table_row['return_date']
        var invoice_status = table_row['status']
      }

      var class_name = $(this).attr('class');

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
    })

    

    function view_invoice_details(id) {
      var url = "delar-invoice-return-details/" + id;
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
      if (confirm('Are you sure you want to cancel this Transaction?') == true) {
        $('#page_loading').modal('show');
        $.ajax({
          url: "/delar-invoice-return-cancel/" + id,
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




function get_product_name() {
  $.ajax({
      url: "/sales-products-api/",
      type: "get",
      datatype: "json",
      success: function (data) {
          data.forEach((value) => {
              document.getElementById("id_product_id").innerHTML +=
                  '<option value="' +
                  value.product_id +
                  '" id="' +
                  value.product_name +
                  '">' +
                  value.product_name +
                  "</option>";
          });
      },
  });
}


function get_client_name() {
  $.ajax({
    url: "/sales-clients-api/",
    type: "get",
    datatype: "json",
    success: function (data) {
      // console.log(data)
      data.forEach((value) => {
        document.getElementById("id_client_id").innerHTML +=
          '<option value="' +
          value.client_id +
          '" id="' +
          value.client_name +
          '">' +
          value.client_name +
          "</option>";
      });
    },
  });
}


function get_employee_name() {
  $.ajax({
    url: "/apiauth-employee-api/",
    type: "get",
    datatype: "json",
    success: function (data) {
      // console.log(data)
      data.forEach((value) => {
        document.getElementById("id_employee_id").innerHTML +=
          '<option value="' +
          value.employee_id +
          '" id="' +
          value.employee_name +
          '">' +
          value.employee_name +
          "</option>";
      });
    },
  });
}
