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
        table_data = $('#dt-table-list').DataTable({
          "processing": true,
          "ajax": {
            "url": "/delar-sr_target-api/",
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
            { data: 'product_id' },
            { data: 'total_quantity' },
            { data: 'unit_price' },
            { data: 'total_price' },
            {
              "data": null,
              "defaultContent":
                '<button type="button" class="btn btn-danger show-form-update"> <span class="glyphicon glyphicon-pencil"></span>Remove</button>'
            }
          ]
        });
      }
    }]);

    return fn_data_table;
  }();

var id = 0

$(document).on('theme:init', function () {
  new fn_data_table();
});




$("#id_product_bar_code").on("change paste keyup", function (e) {
  get_product_info_barcode()
  var key = e.which;
  if (key == 13) // the enter key code
  {
    var product_name = document.getElementById('id_product_name').value;
    if (product_name === '') {
      alert('Please Enter Product Information')
    } else {
      post_tran_table_data();
    }
  }
});

$("#id_product_id").on("change paste keyup", function () {
  get_product_name()
});
function get_product_name() {
  var product_id = document.getElementById('id_product_id').value;
  $.ajax({
    url: "/sales-product-info/" + product_id,
    type: 'GET',
    success: function (data) {
      if (data.form_is_valid) {

        $('#id_total_quantity').val(1);
        $('#id_unit_price').val(data.product_purces_price);
        $('#id_total_price').val(data.product_purces_price);
      }
    }
  })
  return false;
}

function get_product_info_barcode() {
  var product_bar_code = document.getElementById('id_product_bar_code').value;
  $.ajax({
    url: "/sales-product-info-barcode/" + product_bar_code,
    type: 'GET',
    success: function (data) {
      if (data.form_is_valid) {

        $('#id_total_quantity').val(1);

        $('#id_unit_price').val(data.product_purces_price);
        $('#id_total_price').val(data.product_purces_price);
      } else {
        $('#id_product_name').val('Invalid Product');
      }
    }
  })
  return false;
}

let w_tran_screen = 'QUICK_PURCHASE';
let w_transaction_type = '';
let w_account_type = '';
let w_branch_code = '';

$("#id_total_price").on("change paste keyup", function () {
  var quantity = document.getElementById('id_total_quantity').value;
  var dtl_total_price = document.getElementById('id_total_price').value;
  var purces_rate = Math.round((dtl_total_price / quantity) * 100) / 100;
  $('#id_unit_price').val(purces_rate);
});

$("#id_total_quantity").on("change paste keyup", function () {
  var quantity = document.getElementById('id_total_quantity').value;
  var purces_rate = document.getElementById('id_unit_price').value;
  var dtl_total_price = Math.round((purces_rate * quantity) * 100) / 100;
  $('#id_total_price').val(dtl_total_price);
});

$("#id_unit_price").on("change paste keyup", function () {
  var quantity = document.getElementById('id_total_quantity').value;
  var purces_rate = document.getElementById('id_unit_price').value;
  var dtl_total_price = Math.round((purces_rate * quantity) * 100) / 100;
  $('#id_total_price').val(dtl_total_price);
});

$("#id_total_pay").on("change paste keyup", function () {
  var total_due = (((document.getElementById('id_total_price').value) - (document.getElementById('id_total_pay').value)));
  var total_due_round = Math.round((total_due) * 100) / 100;
  if (total_due < 0) {
    $('#id_due_amount').val(0);
  } else {
    $('#id_due_amount').val(total_due_round);
  }
});


// $(document).ready(function () {
//  $("#id_account_number").select2();
//  var w_branch_code = document.getElementById('id_global_branch_code').value;
//  refresh_branch_list('');
//  account_list_refresh(w_account_type, w_tran_screen, w_transaction_type, w_branch_code);
//  transaction_cashnbanklist_list();
// });

$(window).on('load', function () {
  var global_branch_code = document.getElementById('id_global_branch_code').value;
  $('#id_branch_code').val(global_branch_code);
});

// function account_list_refresh(account_type, tran_screen, transaction_type, branch_code) {
//  var url = '/sales-choice-accountslist';
//  $.ajax({
//   url: url,
//   data: {
//    'account_type': account_type, 'tran_screen': tran_screen,
//    'transaction_type': transaction_type, 'branch_code': branch_code,
//   },
//   success: function (data) {
//    $("#id_account_number").html(data);
//   }
//  });
//  return false;
// }

// function transaction_cashnbanklist_list(branch_code) {
//  var url = '/finance-choice-cashnbanklist';
//  $.ajax({
//   url: url,
//   data: {
//    'branch_code': branch_code
//   },
//   success: function (data) {
//    $("#id_receipt_payment_ledger").html(data);
//   }
//  });
//  return false;
// }


$(function () {

  $('#dt-table-list').on('click', 'button', function () {

    try {
      var table_row = table_data.row(this).data();
      id = table_row['id']
    }
    catch (e) {
      var table_row = table_data.row($(this).parents('tr')).data();
      id = table_row['id']
    }

    var class_name = $(this).attr('class');
    if (class_name == 'btn btn-warning show-form-update') {
      show_edit_product_data(id)
    }

    if (class_name == 'btn btn-danger show-form-update') {
      if (confirm('Are you sure you want to remove this item?') == true) {
        stock_details_delete(id)
      }
    }

  })

  function show_edit_product_data(id) {
    $.ajax({
      url: '/sales-details-edit/' + id,
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $('#product_edit').modal('show');
      },
      success: function (data) {
        $('#product_edit .modal-content').html(data.html_form);
      }
    })
  }

  function stock_details_delete(id) {
    $.ajax({
      url: '/delar_sr_target-delate/' + id,
      type: 'POST',
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          //  $('#id_total_quantity').val(data.total_quantity);
          //  $('#id_total_price').val(data.total_price);
          table_data.ajax.reload();
        } else {
          table_data.ajax.reload();
        }
      }
    })
    return false;
  }

});

$(function () {
  $('#btnAddItem').click(function () {
    post_tran_table_data();

  });
});

$(function () {
  $('#btn_stock_sumbit').click(function () {
    post_stock_master_data();

  });
});

function post_tran_table_data() {
  var data_string = $("#stock_master_form").serialize();
  var data_url = $("#stock_master_form").attr('data-url');
  $('#page_loading').modal('show');
  $.ajax({
    url: data_url,
    data: data_string,
    type: 'POST',
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        document.getElementById("stock_master_form").reset();
        $('#id_total_quantity').val(data.total_quantity);
        $('#id_total_price').val(data.total_price);
        table_data.ajax.reload();
        $('#page_loading').modal('hide');
        $('#id_product_name').val('');
        $('#id_product_id').val('');
        $('#id_total_quantity').val(1);
        var product_id_span = document.getElementById("select2-id_product_id-container");
        product_id_span.textContent = "Select Product";
      } else {
        alert(data.error_message);
        table_data.ajax.reload();
        $('#page_loading').modal('hide');
      }
    }
  })
  return false;
}

function post_stock_master_data() {
  var data_string = $("#stock_master_post").serialize();
  var data_url = $("#stock_master_post").attr('data-url');
  $('#page_loading').modal('show');
  $.ajax({
    url: data_url,
    data: data_string,
    type: 'POST',
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        alert(data.message);
        document.getElementById("stock_master_post").reset();
        document.getElementById("stock_master_form").reset();
        table_data.ajax.reload();
        $('#page_loading').modal('hide');
        var global_branch_code = document.getElementById('id_global_branch_code').value;
        $('#id_branch_code').val(global_branch_code);
        var account_number = document.getElementById("select2-id_account_number-container");
        account_number.textContent = "-----------";
        $('#id_total_price').val(0.00);
      } else {
        alert(data.error_message);
        table_data.ajax.reload();
        $('#page_loading').modal('hide');
      }
    }
  })
  return false;
}

$(document).ready(function () {
  $("#id_employee_id").select2();
  $("#id_unit_id").select2();
  get_product_id();
  get_employee_name();
  get_unit_name();
})

function get_product_id() {
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
          value.product_id +
          '">' +
          value.product_name +
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


function get_unit_name() {
  $.ajax({
    url: "/sales-productunit-api/",
    type: "get",
    datatype: "json",
    success: function (data) {
      // console.log(data)
      data.forEach((value) => {
        document.getElementById("id_unit_id").innerHTML +=
          '<option value="' +
          value.unit_id +
          '" id="' +
          value.unit_name +
          '">' +
          value.unit_name +
          "</option>";
      });
    },
  });
}



$('#id_target_type').change(function () {
  let check = $('#id_target_type').val()

  if (check == "A") {
    document.getElementById("one").style.display = 'none';
  } else {
    document.getElementById("one").style.display = 'block';
  }
})

