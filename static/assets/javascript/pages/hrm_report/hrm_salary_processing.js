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
    function() {
        function fn_data_table() {
            _classCallCheck(this, fn_data_table);

            this.init();
        }

        _createClass(fn_data_table, [{
            key: "init",
            value: function init() {
                this.table = this.table();
            }
        }, ]);

        return fn_data_table;
    }();

var id = 0

$(function() {
    $('#btnSearch').click(function() {
        new fn_data_table();
    });
})

$(function() {

    $('#dt-table-list').on('click', 'button', function() {

        try {
            var table_row = table_data.row(this).data();
            id = table_row['unit_id']
        } catch (e) {
            var table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['unit_id']
        }

        var class_name = $(this).attr('class');
        if (class_name == 'btn btn-info btn-sm') {
            show_edit_form(id);
        }

    })

});

$(function() {

    $(function() {
        $('#btnAddItem').click(function() {
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
            success: function(data) {
                if (data.form_is_valid) {
                    document.getElementById("tran_table_data").reset();
                    $('#page_loading').modal('hide');
                    alert(data.success_message);
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

});


$(document).ready(function() {
    refresh_branch_list('');
    refresh_materials_list('');
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});

$(window).on('load', function() {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});

function refresh_materials_list(material_id) {
    var url = '/fngoods-choice-materials';
    $.ajax({
        url: url, // set the url of the request
        data: {
            'material_id': material_id // add the id to the GET parameters
        },
        success: function(data) { // `data` is the return of the view function
            $("#id_material_id").html(data); // replace the values of the input with the data that came from the server
        }
    });
    return false;
}

function refresh_branch_list(branch_code) {
    var url = 'appauth-choice-branchlist';
    $.ajax({ // initialize an AJAX request
        url: url, // set the url of the request
        data: {
            'branch_code': branch_code // add the id to the GET parameters
        },
        success: function(data) { // `data` is the return of the view function
            $("#id_branch_code").html(data); // replace the values of the input with the data that came from the server
        }
    });
    return false;
}