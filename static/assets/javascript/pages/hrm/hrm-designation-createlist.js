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
                const desig_id = '';
                const search_url = "/apihrm-designation-api?desig_id=" + desig_id;
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
                        { data: 'desig_id' },
                        { data: 'desig_name' },
                        { data: 'attendance_bonus' },
                        { data: 'attendance_bonus_amt' },
                        { data: 'production_bonus' },
                        { data: 'production_bonus_amt' },
                        { data: 'ot_hour_allow' },
                        { data: 'ot_hour_rate' },
                        {data:'sales_comission'},
                        { data: 'stamp_ded_allow' },
                        { data: 'stamp_ded_amount' },
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
            id = table_row['desig_id']
        } catch (e) {
            const table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['desig_id']
        }

        const class_name = $(this).attr('class');
        if (class_name == 'btn btn-info btn-sm') {
            show_edit_form(id);
        }
    })

    function show_edit_form(id) {
        $.ajax({
            url: '/hrm-designation-info-edit/' + id,
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
                alert(data.success_message + " " + data.department_id);
            } else {
                $('#page_loading').modal('hide');
                alert(data.error_message);
            }
        }
    })
    return false;
}

$("#id_attendance_bonus").on("change", function() {
    const attendance_bonus_amt = document.getElementById('div_id_attendance_bonus_amt');
    const att_allow = document.getElementById('id_attendance_bonus');
    if (att_allow.checked) {
        attendance_bonus_amt.style.display = "block"
    } else {
        attendance_bonus_amt.style.display = "none"
    }
});

$("#id_production_bonus").on("change", function() {
    const production_bonus_amt = document.getElementById('div_id_production_bonus_amt');
    const prod_allow = document.getElementById('id_production_bonus');
    if (prod_allow.checked) {
        production_bonus_amt.style.display = "block"
    } else {
        production_bonus_amt.style.display = "none"
    }
});

$("#id_ot_hour_allow").on("change", function() {
    const v_ot_rate = document.getElementById('div_id_ot_hour_rate');
    const ot_allow = document.getElementById('id_ot_hour_allow');
    if (ot_allow.checked) {
        v_ot_rate.style.display = "block"
    } else {
        v_ot_rate.style.display = "none"
    }
});


$("#id_stamp_ded_allow").on("change", function() {
    const stamp_allow_amt = document.getElementById('div_id_stamp_ded_amount');
    const stamp_allow = document.getElementById('id_stamp_ded_allow');
    if (stamp_allow.checked) {
        stamp_allow_amt.style.display = "block"
    } else {
        stamp_allow_amt.style.display = "none"
    }
});