"use strict";

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) {
    for (let i = 0; i < props.length; i++) {
        let descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true;
        if ("value" in descriptor) descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
    }
}

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

let table_data

const fn_data_table =
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
        }, {
            key: "table",
            value: function table() {
                const employee_id = '';
                const search_url = "/apihrm-employee-api?employee_id=" + employee_id;
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
                        { data: 'employee_father_name' },
                        { data: 'employee_mother_name' },
                        { data: 'employee_blood_group' },
                        { data: 'employee_sex' },
                        { data: 'employee_religion' },
                        { data: 'employee_marital_status' },
                        { data: 'employee_national_id' },
                        { data: 'country_id' },

                        { data: 'division_id' },
                        { data: 'district_id' },
                        { data: 'upozila_id' },
                        { data: 'employee_present_address' },
                        { data: 'employee_permanent_address' },
                        { data: 'employee_phone_own' },
                        { data: 'employee_phone_office' },

                        { data: 'employee_phone_home' },
                        { data: 'passport_no' },
                        { data: 'driving_licence' },
                        { data: 'employee_tin' },
                        { data: 'email_personal' },
                        { data: 'employee_joining_date' },

                        { data: 'employee_date_of_birth' },
                        { data: 'employee_status' },
                        { data: 'eme_contact_name' },

                        { data: 'eme_contact_relation' },
                        { data: 'eme_contact_phone' },

                        { data: 'eme_contact_address' },
                        { data: 'office_id' },

                        { data: 'emptype_id' },
                        { data: 'salscale' },
                        { data: 'salary_gross' },

                        { data: 'designation_id' },
                        { data: 'email_official' },
                        { data: 'reporting_to' },

                        { data: 'current_shift' },
                        { data: 'office_location' },
                        { data: 'card_number' },

                        { data: 'salary_bank' },
                        { data: 'salary_bank_ac' },
                        { data: 'contract_start_date' },
                        { data: 'contract_exp_date' },

                        { data: 'last_inc_date' },
                        { data: 'next_inc_date' },
                        { data: 'service_end_date' },

                        { data: 'last_transfer_date' },
                        { data: 'next_transfer_date' },
                        { data: 'job_confirm_date' },

                        { data: 'pf_confirm_date' },
                        { data: 'gf_confirm_date' },
                        { data: 'wf_confirm_date' },

                        // { data: 'last_promotion_date' },







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

    function() {

        new fn_data_table();
    }

);

$(function() {

    $('#dt-table-list').on('click', 'button', function() {

        try {
            const table_row = table_data.row(this).data();
            id = table_row['employee_id']
        } catch (e) {
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
            url: '/hrm-employee-info-edit/' + id,
            type: 'get',
            dataType: 'json',
            beforeSend: function() {
                $('#edit_model').modal('show');
            },
            success: function(data) {
                $('#edit_model .modal-content').html(data.html_form);
            }
        })
    }

});

$('#btnAddRecord').click(function() {
    post_tran_table_data();
});

function post_tran_table_data() {
    const data_string = $("#tran_table_data").serialize();
    const data_url = $("#tran_table_data").attr('data-url');
    $('#page_loading').modal('show');
    $.ajax({
        url: data_url,
        data: data_string,
        type: 'POST',
        dataType: 'json',
        success: function(data) {
            if (data.form_is_valid) {
                $('#page_loading').modal('hide');
                document.getElementById("tran_table_data").reset();
                table_data.ajax.reload();
                alert(data.success_message + " " + data.id);
            } else {
                $('#page_loading').modal('hide');
                alert(data.error_message);
            }
        }
    })
    return false;
}