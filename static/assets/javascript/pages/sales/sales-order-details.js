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
        var order_number = document.getElementById('id_order_number').value;
        var search_url = "/sales-order-detailsapi/?order_number=" + order_number;
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
            { data: 'serial_no' },
            { data: 'product_id' },
            { data: 'product_price' },
            { data: 'quantity' },
            { data: 'total_price' },
            { data: 'discount_rate' },
            { data: 'discount_amount' },
            { data: 'status' },
            { data: 'comments' }
          ]
        });
      }
    }]);

    return fn_data_table;
  }();


$(document).ready(function () {
  var order_number = document.getElementById('id_order_number').value;
  if (order_number != "") {
    new fn_data_table();
  }
});

$('#btnSearch').click(function () {
  var order_number = document.getElementById('id_order_number').value;

  if (order_number === "") {
    alert("Please Enter Order Number.")
  } else {
    new fn_data_table();
  }
});
