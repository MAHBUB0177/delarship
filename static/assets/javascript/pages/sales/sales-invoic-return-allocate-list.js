"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var table_data
var edit_stock_id

var stock_mst_details =
    function () {
        function stock_mst_details() {
            _classCallCheck(this, stock_mst_details);

            this.init();
        }

        _createClass(stock_mst_details, [{
            key: "init",
            value: function init() {
                this.table = this.table();
            }
        }, {
            key: "table",
            value: function table() {
                var invoice_from_date = document.getElementById('id_invoice_from_date').value;
                var invoice_upto_date = document.getElementById('id_invoice_upto_date').value;
                var branch_code = document.getElementById('id_branch_code').value;
                var employee_id = document.getElementById('id_employee_id').value;
                var product_id = document.getElementById('id_product_id').value;

                var search_url = "/sales-invoice-return-allocatedetails";
                
                table_data = $('#dt-invoice-stock-mst').DataTable({
                    "processing": true,
                    destroy: true,
                    "ajax": {
                        "url": search_url,
                        "type": "GET",
                        "dataSrc": "data",
                        "data": {
                            'invoice_from_date': invoice_from_date, 'invoice_upto_date': invoice_upto_date, 'branch_code': branch_code,
                            'employee_id': employee_id,'product_id':product_id,
                        }
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
                        { data: 'product_name' },
                        { data: 'employee_name' },
                        { data: 'product_total_stock' },
                        { data: 'product_total_sales' },
                        { data: 'total_stock_return' },
                        { data: 'product_available_stock' },
                        
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-danger btn-sm">Return</button>'
                        }
                    ]
                });
            }
        }]);

        return stock_mst_details;
    }();

    
    

$(function () {
    $('#btnSearchStockMst').click(function () {
        var invoice_from_date = document.getElementById('id_invoice_from_date').value;
        var invoice_upto_date = document.getElementById('id_invoice_upto_date').value;
        if (invoice_upto_date === "" & invoice_from_date === "") {
            alert("Please enter at least one value.")
        } else {
            new stock_mst_details();
        }
    });
})

let w_branch_code = 0;

$(document).ready(function () {
    refresh_branch_list('');
    get_product_name()
    get_client_name()
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    w_branch_code = global_branch_code;
    $('#id_branch_code').val(global_branch_code);
});

$("#id_branch_code").on("change", function () {
    var branch_code = document.getElementById('id_branch_code').value;
    w_branch_code = branch_code;
});
var product_id=0
var id = 0
var employee_id=0
var product_available_stock=0
var product_total_sales=0
var total_stock_return=0
var product_total_stock=0
$('#dt-invoice-stock-mst').on('click', 'button', function () {

    try {
        var table_row = table_data.row(this).data();
        product_id = table_row['product_id']
        employee_id = table_row['employee_id']
        product_total_stock = table_row['product_total_stock']
        product_total_sales = table_row['product_total_sales']
        total_stock_return = table_row['total_stock_return']
        product_available_stock=table_row['product_available_stock']



        // id = table_row['id']
    }
    catch (e) {
        var table_row = table_data.row($(this).parents('tr')).data();
        
        product_id = table_row['product_id']
        employee_id = table_row['employee_id']
        product_total_stock = table_row['product_total_stock']
        product_total_sales = table_row['product_total_sales']
        total_stock_return = table_row['total_stock_return']
        product_available_stock=table_row['product_available_stock']
    }

    var class_name = $(this).attr('class');
    console.log(class_name);

    if (class_name == 'btn btn-danger btn-sm') {
        cancel_damage(id,product_id,employee_id,product_total_stock,product_total_sales,total_stock_return,product_available_stock);
    }
    $('.btn-danger').on('click', 'button', function () {
        console.log('click')
    })
})



function cancel_damage(id,product_id,employee_id,product_total_stock,product_total_sales,total_stock_return,product_available_stock) {
   
    let data_s={"product_id":product_id,"employee_id":employee_id,"product_total_stock":product_total_stock,"product_total_sales":product_total_sales,"total_stock_return":total_stock_return,"product_available_stock":product_available_stock }
    console.log(data_s)
    if (confirm('Are you sure you want to cancel this transaction?') == true) {
        $('#page_loading').modal('show');
        $.ajax({
            url: "sales_invoice_allocate_details_return" ,
            type: "POST",
            data:data_s,
            success: function (data) {
                if (data.form_is_valid) {
                    $('#page_loading').modal('hide');
                    alert(data.success_message);
                } else {
                    $('#page_loading').modal('hide');
                    alert(data.error_message);
                }
                table_data.ajax.reload();
            }
        })
    }
}


function get_product_name(){
   
 $.ajax({
     url: '/sales-products-api/',
     type: 'get',
     datatype: 'json',
     success: function (data) {
      
      data.forEach((value)=>{
          document.getElementById("id_product_id").innerHTML += '<option value="' + value.product_id + '"  id="' + value.product_name + '">' + value.product_name+ '</option>';
       
       })
     
     }
 })
}


function get_client_name(){
 $.ajax({
     url: '/apiauth-employee-api/',
     type: 'get',
     datatype: 'json',
     success: function (data) {
      // console.log(data)
      data.forEach((value)=>{
          document.getElementById("id_employee_id").innerHTML += '<option value="' + value.employee_id + '" id="' + value.employee_id + '">' + value.employee_name+ '</option>';

       })
     
     }
 })
}