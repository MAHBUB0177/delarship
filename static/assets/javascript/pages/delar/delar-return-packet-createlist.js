"use strict";

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _defineProperties(target, props) {
  for (var i = 0; i < props.length; i++) {
    var descriptor = props[i];
    descriptor.enumerable = descriptor.enumerable || false;
    descriptor.configurable = true;
    if ("value" in descriptor) descriptor.writable = true;
    Object.defineProperty(target, descriptor.key, descriptor);
  }
}

function _createClass(Constructor, protoProps, staticProps) {
  if (protoProps) _defineProperties(Constructor.prototype, protoProps);
  if (staticProps) _defineProperties(Constructor, staticProps);
  return Constructor;
}

var table_data;
var ProductList = (function () {
  function ProductList() {
    _classCallCheck(this, ProductList);

    this.init();
  }

  _createClass(ProductList, [
    {
      key: "init",
      value: function init() {
        this.table = this.table();
      },
    },
    {
      key: "table",
      value: function table() {
        const search_url = "/delar-return-packet-api/";
        table_data = $("#dt-table-list").DataTable({
          processing: true,
          destroy: true,
          ajax: {
            url: search_url,
            type: "GET",
            dataSrc: "",
          },
          responsive: true,
          dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>\n        <'table-responsive'tr>\n        <'row align-items-center'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 d-flex justify-content-end'p>>",
          language: {
            paginate: {
              previous: '<i class="fa fa-lg fa-angle-left"></i>',
              next: '<i class="fa fa-lg fa-angle-right"></i>',
            },
          },
          columns: [
            { data: "branch_code" },
            { data: "client_id" },
            { data: "product_id" },
            { data: "receive_quantity" },
            { data: "receive_value" },
            { data: "return_invoice" },
            { data: "status" },

            {
              data: "product_id",
              render: function (data) {
                return `<button data_product_id=${data}  type="button" class="btn btn-info btn-sm">Edit</button>`;
              },
            },
          ],
        });
      },
    },
  ]);

  return ProductList;
})();

var id = 0;

$(function () {
  $("#btnSearch").click(function () {
    new ProductList();
  });
});

$(function () {
  $("#dt-table-list").on("click", "button", function () {
    try {
      var table_row = table_data.row(this).data();
      id = table_row["id"];
    } catch (e) {
      var table_row = table_data.row($(this).parents("tr")).data();
      id = table_row["id"];
    }

    var class_name = $(this).attr("class");
    if (class_name == "btn btn-info btn-sm") {
      show_edit_product_data(id);
    }
  });

  function show_edit_product_data(id) {
    $.ajax({
      url: "/delar_sales_packet_return_edit/" + id,
      type: "get",
      dataType: "json",
      beforeSend: function () {
        $("#edit_model").modal("show");
      },
      success: function (data) {
        $("#edit_model .modal-content").html(data.html_form);
      },
    });
  }
});

$(document).ready(function () {
  $("#id_product_id").select2();
  $("#id_client_id").select2();
  $("#id_employee_id").select2();
  get_product_name();
  get_client_name();
  get_employee_name();
});
$(document).ready(function () {
  refresh_branch_list("");
});

$(window).on("load", function () {
  var global_branch_code = document.getElementById(
    "id_global_branch_code"
  ).value;
  $("#id_branch_code").val(global_branch_code);
});

$(function () {
  $("#btnAddItem").click(function () {
    post_tran_table_data();
  });
});

function post_tran_table_data() {
  var data_string = $("#tran_table_data").serialize();
  var data_url = $("#tran_table_data").attr("data-url");
  $("#page_loading").modal("show");
  $.ajax({
    url: data_url,
    data: data_string,
    type: "POST",
    dataType: "json",
    success: function (data) {
      if (data.form_is_valid) {
        document.getElementById("tran_table_data").reset();
        $("#page_loading").modal("hide");
        alert(data.success_message);
        // table_data.ajax.reload();
      } else {
        $("#page_loading").modal("hide");
        alert(data.error_message);
        // table_data.ajax.reload();
      }
    },
  });
  return false;
}

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





$("#id_product_id").on("change paste keyup", function () {
  $("#id_receive_value").val("");
  $("#id_receive_quantity").val("");
  var product_id = document.getElementById("id_product_id").value;
  console.log("PRODUCT ID", product_id);
  $.ajax({
    
    url: "/sales-products-api/?product_id=" + product_id + "",
    type: "get",
    success: function (data) {
      if (data) {
        console.log(data);
        $("#id_receive_quantity").on("change paste keyup", function () {
          var quantity = document.getElementById("id_receive_quantity").value;

          const price = data[0].product_purces_price;
          console.log(price);
          var dtl_total_price = Math.round(price * quantity * 100) / 100;
          $("#id_receive_value").val(dtl_total_price);
        });
      }
      console.log("serch data", data);
    },
  });
});
