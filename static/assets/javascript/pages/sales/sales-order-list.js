"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var table_data
var edit_stock_id

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
        var order_number = document.getElementById('id_order_number').value;
        var from_date = document.getElementById('id_from_date').value;
        var upto_date = document.getElementById('id_upto_date').value;
        var customer_phone = document.getElementById('id_customer_phone').value;
        var executive_phone = document.getElementById('id_executive_phone').value;
        var order_status = document.getElementById('id_order_status').value;

        var search_url = "/sales-order-api/?order_number=" + order_number + "&from_date=" + 
        from_date + "&upto_date=" + upto_date + "&customer_phone=" + customer_phone + 
        "&executive_phone=" + executive_phone+"&order_status=" + order_status;
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
            { data: 'order_number' },
            { data: 'order_date' },
            { data: 'customer_name' },
            { data: 'customer_phone' },
            { data: 'executive_phone' },
            { data: 'total_quantity' },
            { data: 'bill_amount' },
            { data: 'pay_amount' },
            { data: 'advance_pay' },
            { data: 'total_discount_amount' },
            { data: 'status' },
            { data: 'order_comments' },
            {
              "data": null,
              "defaultContent": '<button type="button" class="btn btn-info btn-sm">Accept</button>' + '&nbsp;&nbsp' +
                '<button type="button" class="btn btn-danger btn-sm">Cancel</button>' + '&nbsp;&nbsp' +
                '<button type="button" class="btn btn-secondary btn-sm">Dtl</button>' +  '&nbsp;&nbsp' +
                '<button type="button" class="btn btn-success btn-sm">Print Invoice</button>'
            }

            
          ]
        });
      }
    }]);

    return fn_data_table;
  }();

$(function () {
  $('#btnSearch').click(function () {
    var order_number = document.getElementById('id_order_number').value;
    var from_date = document.getElementById('id_from_date').value;
    var upto_date = document.getElementById('id_upto_date').value;
    var customer_phone = document.getElementById('id_customer_phone').value;
    var executive_phone = document.getElementById('id_executive_phone').value;

    if (order_number === "" & from_date === "" & upto_date === "" & customer_phone === "" & executive_phone === "") {
      alert("Please enter at least one value.")
    } else {
      new fn_data_table();
    }
  });
})

$(function () {
  var id = 0
  $('#dt-invoice-list').on('click', 'button', function () {

    try {
      var table_row = table_data.row(this).data();
      id = table_row['id']
      var order_number = table_row['order_number']
      var order_date = table_row['order_date']
      var order_status = table_row['status']
    }
    catch (e) {
      var table_row = table_data.row($(this).parents('tr')).data();
      id = table_row['id']
      var order_number = table_row['order_number']
      var order_date = table_row['order_date']
      var order_status = table_row['status']
    }

    var class_name = $(this).attr('class');
    console.log(class_name);

    if (class_name == 'btn btn-info btn-sm') {
      order_accept(id);
    }
    if (class_name == 'btn btn-danger btn-sm') {
      if (order_status == 'C') {
        alert('This Order already Canceled!')
      } else {
        order_cancel(id);
      }
    }
   
    if (class_name == 'btn btn-secondary btn-sm') {
      $('#id_detail_order_number').val(order_number);
      view_order_details(id);
    }
    if (class_name == 'btn btn-success btn-sm') {
      save_and_show_report(order_number);
    }
  })


  function save_and_show_report(p_order_number) {
    console.log("test")
    var data_url = 'appauth-report-submit/';
    var report_name = 'sales_order_invoice';
    var report_data = { 'p_order_number': p_order_number };
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
          window.open(data.report_urls + '/sales-order-report-print-view', "_blank");
        }
        else {
          alert(data.error_message)
        }
      }
    })
    return false;
  }

  function order_accept(id) {
    $('#page_loading').modal('show');
    $.ajax({
      url: "/sales-order-accept/" + id,
      type: "POST",
      success: function (data) {
        if (data.form_is_valid) {
          $('#page_loading').modal('hide');
          table_data.ajax.reload();
          alert(data.success_message);
        } else {
          $('#page_loading').modal('hide');
          alert(data.error_message)
          table_data.ajax.reload();
        }
      }
    })
  }

  function view_order_details(id) {
    var url = "sales-order-details/" + id;
    $.ajax({
      url: url,
      data: {
        'id': id
      },
      success: function (data) {
        $('#view_details').modal('show');
        $("#data_table_sheet").html(data);
        calculfac();
      }
    });
    return false;
  }

  function order_cancel(id) {
    if (confirm('Are you sure you want to cancel this order?') == true) {
      $.ajax({
        url: "/sales-order-cancel/" + id,
        type: "POST",
        success: function (data) {
          table_data.ajax.reload();
        }
      })
    }
  }

})