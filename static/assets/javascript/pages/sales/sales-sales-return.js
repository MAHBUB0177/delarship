let w_tran_screen = 'CLIENT_ACCOUNT';
let w_transaction_type = '';
let w_account_type = '';

$(function () {
    $('#btnAddItem').click(function () {
        post_tran_table_data();

    });
});

function post_tran_table_data() {
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
                $('#page_loading').modal('hide');
                alert(data.success_message);
                document.getElementById("tran_table_data").reset();
                var client_name = document.getElementById("select2-id_client_id-container");
                client_name.textContent = "--Select Customer--";
                var product_name = document.getElementById("select2-id_product_id-container");
                product_name.textContent = "--Select Product--";
                var global_branch_code = document.getElementById('id_global_branch_code').value;
                $('#id_branch_code').val(global_branch_code);
            } else {
                alert(data.error_message);
                $('#page_loading').modal('hide');
            }
        }
    })
    return false;
}

$("#id_sales_invoice").on("change paste keyup", function () {
    get_invoice_details();
    // product_return_validation()
});

$("#id_returned_quantity").on("change paste keyup", function () {
    var total_bill_amount = Number(document.getElementById('id_total_bill_amount').value);
    var total_quantity = Number(document.getElementById('id_total_quantity').value);
    var returned_quantity = Number(document.getElementById('id_returned_quantity').value);
    var return_amount = (total_bill_amount / total_quantity) * returned_quantity;
    $('#id_return_amount').val(return_amount);
});

$("#id_product_id").on("change paste keyup", function () {
    refresh_invoice_list();
});

function refresh_invoice_list() {
    var client_id = document.getElementById('id_client_id').value;
    var product_id = document.getElementById('id_product_id').value;
    var url = 'sales-choice-clientsproduct';
    $.ajax({
        url: url,
        data: {
            'client_id': client_id, 'product_id': product_id
        },
        success: function (data) {
            $("#id_sales_invoice").html(data);
        }
    });
    return false;
}

function get_invoice_details() {
    var sales_invoice = document.getElementById('id_sales_invoice').value;
    var product_id = document.getElementById('id_product_id').value;
    $.ajax({
        url: "/sales-invoice-info/" + product_id + "/" + sales_invoice,
        type: 'GET',
        success: function (data) {
            if (data.form_is_valid) {
                $('#id_total_quantity').val(data.total_quantity);
                $('#id_total_bill_amount').val(data.sales_price);
            } else {
                $('#id_total_quantity').val(data.total_quantity);
                $('#id_total_bill_amount').val(data.sales_price);
            }
        }
    })
    return false;
}

$("#id_account_number").on("change paste keyup", function () {
    get_client_info();
});

function get_client_info() {
    var account_number = document.getElementById('id_account_number').value;
    $.ajax({
        url: "/sales-account-byacnumber/" + account_number,
        type: 'GET',
        success: function (data) {
            if (data.form_is_valid) {
                $('#id_client_id').val(data.client_id);
            } else {
                $('#id_client_id').val('');
            }
        }
    })
    return false;
}
$(document).ready(function(){
    myresult()

});

function myresult() {
    console.log('test')
    let total_quantity=document.getElementById("id_total_quantity").value;
    let quantity=document.getElementById("id_returned_quantity").val;

    let result=total_quantity-quantity;
    $('#id_total_quantity').val(result);

    // document.getElementById('id_total_quantity').value(result);
}