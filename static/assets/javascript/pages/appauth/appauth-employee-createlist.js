"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (let i = 0; i < props.length; i++) { let descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

let table_data

const fn_data_table =
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
                const employee_name = document.getElementById('id_employee_name').value;
                const search_url = "/apiauth-employee-api/?employee_name=" + employee_name;
                table_data = $('#dt-table-list').DataTable({
                    "processing": true,
                    destroy: true,
                    "ajax": {
                        "url": search_url,
                        "type": "GET",
                        "dataSrc": ""
                    },
                    responsive: true,
                    dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>\n <'table-responsive'tr>\n        <'row align-items-center'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 d-flex justify-content-end'p>>",
                    language: {
                        paginate: {
                            previous: '<i class="fa fa-lg fa-angle-left"></i>',
                            next: '<i class="fa fa-lg fa-angle-right"></i>'
                        }
                    },
                    columns: [
                        { data: 'employee_id' },
                        { data: 'employee_name' },
                        {data:'desig_id'},
                        {data:'department_id'},
                        { data: 'branch_code' },
                        { data: 'employee_sex' },
                        { data: 'father_name' },
                        { data: 'mother_name' },
                        { data: 'joining_date' },
                        { data: 'present_address' },
                        { data: 'permanent_address' },
                        { data: 'birth_date' },
                        { data: 'nid_number' },
                        { data: 'employee_religion' },
                        { data: 'blood_group' },
                        { data: 'employee_education' },
                        { data: 'marital_status' },
                        { data: 'mobile_num' },
                        { data: 'alternate_phone' },
                        
                        { data: 'is_active' },
                        { data: 'basic_salary' },
                        { data: 'house_rent' },
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

let id = 0

$('#btnSearch').click(

    function () {
        const branch_code = document.getElementById('id_branch_code').value;
        new fn_data_table();
    }

);

$(function () {

    $('#dt-table-list').on('click', 'button', function () {

        try {
            const table_row = table_data.row(this).data();
            id = table_row['employee_id']
        }

        catch (e) {
            const table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['employee_id']
        }

        const class_name = $(this).attr('class');
        if (class_name == 'btn btn-info btn-sm') {
            show_edit_form(id);
        }
    })

    function show_edit_form(id) {
        $.ajax({
            url: '/appauth-employee-edit/' + id,
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

$('#btnAddRecord').click(function () {
    post_tran_table_data();
    
});


function post_tran_table_data() {
    console.log("test")
    const data_string = $("#tran_table_data").serialize();
    const data_url = $("#tran_table_data").attr('data_url');
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            console.log(data)
            if (data.form_is_valid) {
				document.getElementById("tran_table_data").reset();
                $('#page_loading').modal('hide');
                alert(data.success_message);
                // var global_branch_code = document.getElementById('id_global_branch_code').value;
                // $('#id_branch_code').val(global_branch_code);
            } else {
                $('#page_loading').modal('hide');
                alert(data.error_message);
            }
        }
    })
    return false;
}


$(document).ready(function () {
    // $('#id_branch_code').select2();
    $('#id_employee_religion').select2();
    $('#id_blood_group').select2();
    $('#id_employee_education').select2();
    $('#id_employee_sex').select2();
    $('#id_desig_id').select2();
    $("#id_department_id").select2();
    get_designation_name();
    get_department_name();
});

$("#id_present_address").on("change paste keyup", function () {
    $('#id_permanent_address').val(document.getElementById('id_present_address').value);
});

////////////
function get_designation_name() {
    $.ajax({
        url: "apihrm-designation-api",
        type: "get",
        datatype: "json",
        success: function (data) {
            console.log(data)
            data.forEach((value) => {
                document.getElementById("id_desig_id").innerHTML +=
                    '<option value="' +
                    value.desig_id +
                    '" id="' +
                    value.desig_name +
                    '">' +
                    value.desig_name +
                    "</option>";
            });
        },
    });
}



///////////
function get_department_name() {
    $.ajax({
        url: "apiauth-department-api",
        type: "get",
        datatype: "json",
        success: function (data) {
            console.log(data)
            data.forEach((value) => {
                document.getElementById("id_department_id").innerHTML +=
                    '<option value="' +
                    value.department_id +
                    '" id="' +
                    value.department_name +
                    '">' +
                    value.department_name +
                    "</option>";
            });
        },
    });
}
