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
        var search_url = "/apifinance-querytable-api/";
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
            { data: 'chr_column1' },
            { data: 'dat_column1' },
            { data: 'chr_column2' },
            { data: 'dec_column1' },
            { data: 'dec_column2' },
            { data: 'dec_column3' },
          ]
        });
      }
    }]);

    return fn_data_table;
  }();

$(function () {
  $('#btnSearchStockMst').click(function () {
    var account_number = document.getElementById('id_account_number').value;
    if (account_number === "") {
      alert("Invalid Account Number!")
    } else {
      finance_account_statement();
    }
  });
})

$(document).ready(function () {
  refresh_accounttype_list();
  var account_number = document.getElementById("select2-id_account_number-container");
  account_number.textContent = "--Select Account--";
  refresh_branch_list('');
  const global_branch_code = document.getElementById('id_global_branch_code').value;
  $('#id_branch_code').val(global_branch_code);
});


let w_account_type = '';
let w_tran_screen = '';
let w_transaction_type = '';

function refresh_accounttype_list() {
  var products_type = '';
  var url = '/finance-choice-accounttype';
  $.ajax({
    url: url,
    data: {
      'products_type': products_type
    },
    success: function (data) {
      $("#id_products_type").html(data);
    }
  });
  return false;
}

function refresh_branch_list(branch_code) {
  var url = '/finance-choice-branchlist';
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


$("#id_products_type").on("change paste keyup", function () {
  const account_type = document.getElementById('id_products_type').value;
  w_account_type = account_type;
  var account_number = document.getElementById("select2-id_account_number-container");
  account_number.textContent = "--Select Account--";
  $('#id_account_title').val('');
  $('#id_account_balance').val(0);
  $('#id_account_number').val('');
});

$("#id_account_number").on("change paste keyup", function () {
  get_account_balance();
});

function get_account_balance() {
  var account_number = document.getElementById('id_account_number').value;
  $.ajax({
    url: "/finance-account-byacnumber/" + account_number,
    type: 'GET',
    success: function (data) {
      if (data.form_is_valid) {
        $('#id_account_balance').val(data.account_balance);
      } else {
        $('#id_account_balance').val('');
      }
    }
  })
  return false;
}



function finance_account_statement() {
  var products_type = document.getElementById('id_products_type').value;
  var account_number = document.getElementById('id_account_number').value;
  var from_date = document.getElementById('id_from_date').value;
  var upto_date = document.getElementById('id_upto_date').value;
  $.ajax({
    url: "/finance-accounts-statement/" + account_number + "/" + from_date + "/" + upto_date,
    type: 'GET',
    success: function (data) {
      if (data.form_is_valid) {
        new fn_data_table();
      } else {
        alert(data.error_message);
      }
    }
  })
  return false;
}

$(function () {
  $('#btnSubmit').click(function () {
    var account_number = document.getElementById('id_account_number').value;
    if (account_number === "") {
      alert("Invalid Account Number!")
    } else {
      finance_account_statement();
      save_and_show_report();
    }
  });
});

function save_and_show_report() {
  const data_url = "appauth-report-submit/";
  let report_data = {
    'p_from_date': $('#id_from_date').val(), 'p_upto_date': $('#id_upto_date').val(),
    'p_account_number': $('#id_account_number').val(),
    'p_account_balance': $('#id_account_balance').val()
  };
  report_data = JSON.stringify(report_data);
  $.ajax({
    url: data_url,
    data: {
      'report_name': 'finance_account_statements',
      "report_data": report_data
    },
    cache: "false",
    type: 'POST',
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        window.open(data.report_urls + '/finance-report-account-statement-print-view', "_blank");
      }
      else {
        alert(data.error_message)
      }
    }
  })
  return false;
}