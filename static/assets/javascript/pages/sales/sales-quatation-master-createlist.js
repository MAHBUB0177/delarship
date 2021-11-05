"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
        var descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true;
        if ("value" in descriptor) descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
    }
}

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
                        "url": "/sales-Quotation-api/",
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
                        { data: 'quantity' },
                        { data: 'unit' },
                        { data: 'unit_price' },
                        { data: 'total_price' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-danger show-form-update">Print</button>'
                        }
                    ]
                });
            }
        }]);

        return fn_data_table;
    }();


    $("#btnSearch").on('click',function(){
        new fn_data_table();
    })
var id = 0

// $(document).on('theme:init', function () {
//     new fn_data_table();
// });

$(document).ready(function () {
    refresh_branch_list('');
    
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});


$('#dt-table-list').on('click', 'button', function () {

    try {
        var table_row = table_data.row(this).data();
        id = table_row['id']
        var quotation_id=table_row['quotation_id']
    } catch (e) {
        var table_row = table_data.row($(this).parents('tr')).data();
        id = table_row['id']
        var quotation_id=table_row['quotation_id']
    }

    var class_name = $(this).attr('class');
    
    if (class_name == 'btn btn-danger show-form-update') {
        save_and_show_report(quotation_id);
      }

})

function save_and_show_report(p_quotation_id) {
    console.log("report function")
    var data_url = 'appauth-report-submit/';
    var report_name = 'sales_quatation_list';
    var report_data = { 'p_quotation_id': p_quotation_id };
    report_data = JSON.stringify(report_data);
    console.log(report_data)
    $.ajax({
      url: data_url,
      data: {
        'report_name':report_name,
        'report_data':report_data
      },
      type: 'POST',
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
            $('#page_loading').modal('hide');
			window.open(data.report_urls + "/sales-quation-print-view", "_blank");
        
        }
        else {
          alert(data.error_message)
        }
      }
    })
    return false;
  }





$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});


$(function () {
    $('#btn_param_sumbit').click(function () {
        post_tran_table_data();
    });
});

function post_tran_table_data() {
    console.log("test")
    var data_string = $("#id_master_forms").serialize();
    var data_url = $("#id_master_forms").attr('data-url');
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                
                alert(data.success_message);
                document.getElementById("id_master_forms").reset();
                $('#page_loading').modal('hide');
                table_data.ajax.reload();
            } else {
                $('#page_loading').modal('hide');
                alert(data.error_message);
                table_data.ajax.reload();
            }
        }
    })
    return false;
}



$(function () {
    $('#btnAddItem').click(function () {
        
        post_tran_table_details_data();
        fn_data_table();


});


    function post_tran_table_details_data() {
        console.log("ok")
        var data_string = $("#details_forms").serialize();
        var data_url = $("#details_forms").attr('data-url');
        $('#page_loading').modal('show');
        $.ajax({
            url: data_url,
            data: data_string,
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    alert(data.success_message);
                    document.getElementById("details_forms").reset();
                    $('#page_loading').modal('hide');
                    $('#id_product_id2').val(data.product_id);
                    $('#id_quotation_id').val(data.quotation_id);
                    console.log(data.quotation_id)
                    table_data.ajax.reload();
                } else {
                    $('#page_loading').modal('hide');
                    table_data.ajax.reload();
                    alert(data.error_message);
                }
            }
        })
        return false;
    }

   

$(document).ready(function(){
       $("#id_supplier_id").select2();
       $("#id_product_id").select2();
       $("#id_unit").select2();

        get_supplier_name();
        get_product_name();
        get_product_unit_name();
})
    function get_supplier_name() {
        $.ajax({
            url: "sales-supplier-api",
            type: "get",
            datatype: "json",
            success: function (data) {
               
                data.forEach((value) => {
                    document.getElementById("id_supplier_id").innerHTML +=
                        '<option value="' +
                        value.supp_id +
                        '" id="' +
                        value.supp_id +
                        '">' +
                        value.supp_name +
                        "</option>";
                });
            },
        });
    }


    function get_product_name() {
        $.ajax({
            url: "sales-products-api",
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



function get_product_unit_name() {
        $.ajax({
            url: "sales-productunit-api",
            type: "get",
            datatype: "json",
            success: function (data) {
                console.log(data)
                data.forEach((value) => {
                    document.getElementById("id_unit").innerHTML +=
                        '<option value="' +
                        value.unit_id +
                        '" id="' +
                        value.unit_id +
                        '">' +
                        value.unit_name +
                        "</option>";
                });
            },
        });
    }



    $("#id_product_id").on("change paste keyup", function (){
        get_product_price()
    })
    
    function get_product_price() {
            var product_id = document.getElementById('id_product_id').value;
            $.ajax({
                url: "/sales-product-info/" + product_id,
                type: 'GET',
                success: function (data) {
                    console.log(data)
                    if (data.form_is_valid) {
                        
                        $('#id_quantity').val(1);
                        $('#id_unit_price').val(data.product_purces_price);
                        $('#id_total_price').val(data.product_purces_price);
                    } else {
                        $('#id_product_name').val('Invalid Product');
                    }
                }
            })
            return false;
        }




$("#id_quantity").on("change paste keyup", function () {
    var quantity = document.getElementById('id_quantity').value;
    var purces_rate = document.getElementById('id_unit_price').value;
    var dtl_total_price = Math.round((purces_rate * quantity) * 100) / 100;
    $('#id_total_price').val(dtl_total_price);
});

$("#id_total_price").on("change paste keyup", function () {
    var quantity = document.getElementById('id_quantity').value;
    var dtl_total_price = document.getElementById('id_total_price').value;
    var purces_rate = Math.round((dtl_total_price / quantity) * 100) / 100;
    $('#id_unit_price').val(purces_rate);
});

$("#id_unit_price").on("change paste keyup", function () {
    var quantity = document.getElementById('id_quantity').value;
    var purces_rate = document.getElementById('id_unit_price').value;
    var dtl_total_price = Math.round((purces_rate * quantity) * 100) / 100;
    $('#id_total_price').val(dtl_total_price);
});


});




