var table_data=""
function get_data(){
    table_data=$('#dt-invoice-list').DataTable( {
        "ajax":{ 
            "url":"/ecom-product-subcategory/",
            "dataSrc": ""
        },
        "columns": [
            { "data": "categories_id.categories_name" },
            { "data": "subcategories_id" },
            { "data": "subcategories_name" },
            { "data": "status" },
            { "data": null,
                "defaultContent":'<button class="btn btn-info show-form-update">Edit</button>'
            },
        ]
    } );
}

$('#btnSearch').click(function(){
    if(table_data==""){
        get_data()
    }else{
        table_data.ajax.reload()
    }
})
$('#btnInsert').click(function(){
    insert_data()
})

function insert_data(){
    var data_string = $("#New-create-data").serialize();
    var data_url = $("#New-create-data").attr('data-url');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.form_is_valid) {
                if(table_data){table_data.ajax.reload()}
                alert(data.succ_message);
            } else {
                alert(data.error_message);
            }
        }
    })
}

$('#dt-invoice-list').on('click', 'button', function () {

    try {
        var table_row = table_data.row(this).data();
        id = table_row['subcategories_id']
    }
    catch (e) {
        var table_row = table_data.row($(this).parents('tr')).data();
        id = table_row['subcategories_id']
    }

    var class_name = $(this).attr('class');
    if (class_name == 'btn btn-info show-form-update') {
        show_edit_product_data(id)
    }

})

function show_edit_product_data(id) {
    $.ajax({
        url: '/ecom-product-subcategory-edit/' + id,
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
