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
            { data: 'int_column1' },
            { data: 'dat_column1' },
            { data: 'chr_column1' },
            { data: 'chr_column2' },
            { data: 'chr_column3' },
            { data: 'chr_column4' },
            { data: 'chr_column5' },
            { data: 'dec_column1' },
            { data: 'dec_column2' },
            { data: 'chr_column6' },
            { data: 'chr_column7' },
            { data: 'chr_column8' },
            { data: 'dat_column2' },
            { data: 'chr_column9' },
            { data: 'dat_column3' },
            {
              "data": null,
              "defaultContent": '<button type="button" class="btn btn-danger btn-sm">Calcel</button>' + '&nbsp;&nbsp' +
                '<button type="button" class="btn btn-secondary btn-sm">Dtl</button>'
            }
          ]
        });
      }
    }]);

    return fn_data_table;
  }();

let w_account_type = '';
let w_tran_screen = '';
let w_transaction_type = '';

$("#id_products_type").on("change paste keyup", function () {
  const account_type = document.getElementById('id_products_type').value;
  w_account_type = account_type;
  const account_number = document.getElementById("select2-id_account_number-container");
  account_number.textContent = "--Select Account--";
});


$(function () {

  var id = 0

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

      try {
        var table_row = table_data.row(this).data();
        id = table_row['id']
        var tran_date = table_row['dat_column1']
        var batch_number = table_row['int_column2']
        var branch_code = table_row['int_column1']
      }
      catch (e) {
        var table_row = table_data.row($(this).parents('tr')).data();
        id = table_row['id']
        var tran_date = table_row['dat_column1']
        var batch_number = table_row['int_column2']
        var branch_code = table_row['int_column1']
      }


      var class_name = $(this).attr('class');

      if (class_name == 'btn btn-danger btn-sm') {
        if (confirm('Are you sure you want to cancel this transaction?') == true) {
          cancel_transaction_batch(id)
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


    function cancel_transaction_batch(id) {
      $('#page_loading').modal('show');
      $.ajax({
        url: '/finance-transaction-query-cancel/' + id,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            $('#page_loading').modal('hide');
            table_data.ajax.reload();
            alert(data.success_message);
          } else {
            $('#page_loading').modal('hide');
            table_data.ajax.reload();
            alert(data.error_message);
          }
        }
      })
      return false;
    }
  });

  $(document).ready(function () {
    const account_number = document.getElementById("select2-id_account_number-container");
    account_number.textContent = "--Select Account--";
    refresh_branch_list('');
    const global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
    refresh_accounttype_list();
    refresh_ledger_list('');
    $('#id_tran_ledger_code').select2();
  });

  $(window).on('load', function () {
    const global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
  });

  $(function () {
    $('#btn_search_tran').click(function () {
      let tran_from_date = document.getElementById('id_tran_from_date').value;
      let tran_upto_date = document.getElementById('id_tran_upto_date').value;
      let branch_code = document.getElementById('id_branch_code').value;
      let account_number = document.getElementById('id_account_number').value;
      let tran_ledger_code = document.getElementById('id_tran_ledger_code').value;
      if (tran_from_date === "" & tran_upto_date === "" & branch_code === "" & account_number === "" & tran_ledger_code === "") {
        alert("Invalid Query Information!")
      } else {
        search_transaction_details();
        new fn_data_table();
      }
    });
  })

  function search_transaction_details() {
    let tran_from_date = document.getElementById('id_tran_from_date').value;
    let tran_upto_date = document.getElementById('id_tran_upto_date').value;
    let branch_code = document.getElementById('id_branch_code').value;
    let account_number = document.getElementById('id_account_number').value;
    let tran_ledger_code = document.getElementById('id_tran_ledger_code').value;
    if (account_number === "") {
      account_number = '0';
    }
    if (tran_ledger_code === "") {
      tran_ledger_code = '0';
    }
    if (branch_code === "") {
      branch_code = '0';
    }
    $.ajax({
      url: "/finance-transaction-query-submit",
      type: 'GET',
      data: {
        'tran_from_date': tran_from_date,
        'tran_upto_date': tran_upto_date,
        'branch_code': branch_code,
        'account_number': account_number,
        'tran_ledger_code': tran_ledger_code
      },
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

  function refresh_ledger_list(transaction_screen) {
    var url = '/finance-choice-allledgerlist';
    $.ajax({
      url: url,
      data: {
        'transaction_screen': transaction_screen
      },
      success: function (data) {
        $("#id_tran_ledger_code").html(data);
      }
    });
    return false;
  }

});