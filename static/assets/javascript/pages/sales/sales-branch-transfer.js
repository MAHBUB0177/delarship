"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var table_data
var ProductList =
    function () {
        function ProductList() {
            _classCallCheck(this, ProductList);

            this.init();
        }

        _createClass(ProductList, [{
            key: "init",
            value: function init() {
                this.table = this.table();
            }
        }, {
            key: "table",
            value: function table() {
                const search_url = "/sales-branch-transfer-api/";
                table_data = $('#dt-table-list').DataTable({
                    "processing": true,
                    destroy: true,
                    "ajax": {
                        "url":search_url ,
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
                      { data: 'from_branch_code' },
                      { data: 'to_branch_code' },
                      { data: 'product_id' },
                      { data: 'stock_quantity' },
                      { data: 'trf_quantity' },
                      
                      {
                       "data": null,
                       "defaultContent": '<button type="button" class="btn btn-info btn-sm">Edit</button>' + '&nbsp;&nbsp' +
                           '<button type="button" class="btn btn-danger btn-sm">Cancel</button>' 
                   }
                    ]
                });
            }
        }]);

        return ProductList;
    }();

var id = 0

$(function () {
    $('#btnSearch').click(function () {
        new ProductList();
    });
})

$(function() {

  $('#dt-table-list').on('click', 'button', function() {

      try {
          var table_row = table_data.row(this).data();
          id = table_row['id']
      } catch (e) {
          var table_row = table_data.row($(this).parents('tr')).data();
          id = table_row['id']
      }

      var class_name = $(this).attr('class');
      if (class_name == 'btn btn-info btn-sm') {
        show_edit_product_data(id);
        
      }

  })

    function show_edit_product_data(id) {
        $.ajax({
            url: '/sales-branch-transfer-edit/' + id,
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $('#edit_model').modal('show');
            },
            success: function (data) {
                $('#edit_model .modal-content').html(data.html_form);
            }
        })
    }

})

$(document).ready(function () {
    $('#id_from_branch_code').select2();
    $('#id_to_branch_code').select2();
    
   
    $("#id_trf_quantity").on("change", function (){
        equation()
        console.log("click");
    })
    let equation=()=>{
        
        let trf_quantity=document.getElementById("id_trf_quantity").value;
        let av_stock=document.getElementById("id_stock_quantity").value;
        let count=(av_stock-trf_quantity);
        $("#id_stock_quantity").val(count);
    }       
    

});




$(window).on('load', function () {
  var global_branch_code = document.getElementById('id_global_branch_code').value;
  $('#id_branch_code').val(global_branch_code);
});

$(function () {
    $('#btnAddRecord').click(function () {
        post_tran_table_data();
       

    });
});

function post_tran_table_data() {
 console.log("test")
    var data_string = $("#tran_table_data").serialize();
    var data_url = $("#tran_table_data").attr('data-url');
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                document.getElementById("tran_table_data").reset();
                $('#page_loading').modal('hide');
                alert(data.success_message);
                // table_data.ajax.reload();
            } else {
                $('#page_loading').modal('hide');
                alert(data.error_message);
                // table_data.ajax.reload();
            }
        }
    })
    return false;
}






$("#id_product_id").on("change paste keyup", function (){
    var product_id = document.getElementById('id_product_id').value;
    $.ajax({
       
        url: "/sales-products-api/?product_id=" + product_id + "",
        type:'get',
        success:function(data){
            if(data){
                const avl_stock=data[0].product_available_stock;
                $("#id_stock_quantity").val(avl_stock)
                
                }
            console.log(data)
        }

    }) 
})