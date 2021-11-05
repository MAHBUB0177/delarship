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
                var center_referred_by = document.getElementById('id_center_referred_by').value;
                var center_name = document.getElementById('id_center_name').value;
                var branch_code = document.getElementById('id_branch_code').value;
                var center_region_id = document.getElementById('id_center_region_id').value;
                var center_employee_id = document.getElementById('id_center_employee_id').value;
                var center_day = document.getElementById('id_center_day').value;

                var search_url = "/apidelar-center-api/?center_referred_by=" + center_referred_by
                    + "&center_name=" + center_name + "&branch_code=" + branch_code + "&center_region_id=" + center_region_id
                    + "&center_employee_id=" + center_employee_id + "&center_day=" + center_day;
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
                        { data: 'branch_code' },
                        { data: 'branch_center_code' },
                        { data: 'center_name' },
                        { data: 'center_referred_by' },
                        { data: 'center_address' },
                        { data: 'center_region_id' },
                        { data: 'center_open_date' },
                        { data: 'center_employee_id' },
                        { data: 'center_phone_number' },
                        { data: 'center_day' },
                        { data: 'center_status' },
                        { data: 'center_close_by' },
                        { data: 'center_closure_date' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-info btn-sm">Edit</button>'
                        }
                    ]
                });
            }
        }]);

        return fn_data_table;
    }();

var id = 0


$(document).ready(function () {
    refresh_branch_list('');
    $('#id_center_region_id').select2();
    $('#id_center_employee_id').select2();
});

$(function () {
    $('#btnSearch').click(function () {

        var branch_code = document.getElementById('id_branch_code').value;

        if (branch_code === "") {
            alert("Please Select Branch Name!")
        } else {
            new fn_data_table();
        }
    });
})

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});

$(function () {

    $('#dt-table-list').on('click', 'button', function () {

        try {
            var table_row = table_data.row(this).data();
            id = table_row['center_code']
        }
        catch (e) {
            var table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['center_code']
        }

        var class_name = $(this).attr('class');
        if (class_name == 'btn btn-info btn-sm') {
            show_edit_form(id);
        }

    })

    function show_edit_form(id) {
        $.ajax({
            url: '/delar-center-edit/' + id,
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

});

$(function () {

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
                    document.getElementById("tran_table_data").reset();
                    $('#page_loading').modal('hide');
                    alert(data.success_message);
                    var center_region_id = document.getElementById("select2-id_center_region_id-container");
                    center_region_id.textContent = "----------";
                    var center_admin_id = document.getElementById("select2-id_center_admin_id-container");
                    center_admin_id.textContent = "----------";
                    var center_employee_id = document.getElementById("select2-id_center_employee_id-container");
                    center_employee_id.textContent = "----------";
                    var global_branch_code = document.getElementById('id_global_branch_code').value;
                    $('#id_branch_code').val(global_branch_code);
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