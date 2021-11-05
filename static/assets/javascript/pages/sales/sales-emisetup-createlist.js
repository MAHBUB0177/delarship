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
                var client_id = document.getElementById('id_client_id').value;
                var emi_reference_no = document.getElementById('id_emi_reference_no').value;
                var search_url = "/sales-emisetup-api/?emi_reference_no=" + emi_reference_no + "&client_id=" + client_id;
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
                        { data: 'emi_reference_no' },
                        { data: 'emi_inst_frequency' },
                        { data: 'emi_inst_repay_from_date' },
                        { data: 'reference_due_amount' },
                        { data: 'emi_rate' },
                        { data: 'emi_profit_amount' },
                        { data: 'total_emi_amount' },
                        { data: 'number_of_installment' },
                        { data: 'emi_inst_amount' },
                        { data: 'installment_tot_repay_amt' },
                        { data: 'installment_exp_date' },
                        { data: 'emi_cancel_by' },
                        { data: 'emi_cancel_on' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-info btn-sm">Cancel</button>'
                        }
                    ]
                });
            }
        }]);

        return fn_data_table;
    }();

var id = 0

$(function () {
    $('#btnSearch').click(function () {
        var emi_reference_no = document.getElementById('id_emi_reference_no').value;
        var client_id = document.getElementById('id_client_id').value;
        if (emi_reference_no === "" && client_id === "") {
            alert("Please Enter Invoice Number!");
        } else {
            new fn_data_table();
        }
    });
})

$("#id_emi_reference_no").on("change paste keyup", function () {
    get_invoice_details();
    $('#id_emi_rate').val(0.00);
    $('#id_emi_profit_amount').val(0.00);
    $('#id_number_of_installment').val(1);
});

function get_invoice_details() {
    var emi_reference_no = document.getElementById('id_emi_reference_no').value;
    $.ajax({
        url: "/sales-invoice-summary/" + emi_reference_no,
        type: 'GET',
        success: function (data) {
            if (data.form_is_valid) {
                $('#id_emi_inst_repay_from_date').val(data.sales_date);
                $('#id_emi_reference_amount').val(data.bill_amount);
                $('#id_reference_due_amount').val(data.due_amount);
                $('#id_emi_inst_amount').val(data.due_amount);
                $('#id_client_id').val(data.client_id);
                $('#id_total_emi_amount').val(data.due_amount);
                $('#id_emi_reference_date').val(data.sales_date);
            } else {
                $('#id_emi_inst_repay_from_date').val('');
                $('#id_emi_reference_amount').val(0.00);
                $('#id_reference_due_amount').val(0.00);
                $('#id_emi_inst_amount').val(0.00);
                $('#id_total_emi_amount').val(0.00);
                $('#id_emi_reference_date').val('');
            }
        }
    })
    return false;
}

$("#id_emi_rate").on("change paste keyup", function () {
    calculate_emi_amount();
    emi_set();
});

$("#id_emi_inst_frequency").on("change paste keyup", function () {
    $('#id_emi_inst_repay_from_date').val('');
    set_emi_mat_date();
});

$("#id_number_of_installment").on("change paste keyup", function () {
    emi_set();
});

$("#id_emi_down_amount").on("change paste keyup", function () {
    calculate_emi_amount();
    emi_set();
});

$("#id_emi_inst_repay_from_date").on("change", function () {
    set_emi_mat_date();
});

$("#id_emi_ins_rate").on("change paste keyup", function () {
    calculate_emi_amount();
});


function calculate_emi_amount() {
    var invoice_due_amount = Number(document.getElementById('id_reference_due_amount').value);
    var total_invoice_amount = Number(document.getElementById('id_emi_reference_amount').value);
    var emi_ins_rate = Number(document.getElementById('id_emi_ins_rate').value);
    var emi_rate = document.getElementById('id_emi_rate').value;
    var emi_down_amount = Number(document.getElementById('id_emi_down_amount').value);
    var emi_prfit_amount = Math.round((invoice_due_amount * (emi_rate / 100)));
    var total_emi_amount = Math.round(emi_prfit_amount + invoice_due_amount - emi_down_amount);
    $('#id_emi_profit_amount').val(emi_prfit_amount);
    $('#id_total_emi_amount').val(total_emi_amount);
    $('#id_emi_ins_fee_amount').val(Math.round((emi_prfit_amount + invoice_due_amount) * (emi_ins_rate / 100)));
}

function emi_set() {
    set_emi_mat_date();
    var num_of_installment = document.getElementById('id_number_of_installment').value;
    var total_emi_amount = document.getElementById('id_total_emi_amount').value;
    var instrepay_repay_amt = Number(total_emi_amount) / Number(num_of_installment);
    $('#id_emi_inst_amount').val(Math.round(instrepay_repay_amt));
}

function set_emi_mat_date() {
    var emi_freq = document.getElementById('id_emi_inst_frequency').value;
    var num_of_installment = document.getElementById('id_number_of_installment').value;
    var repay_from_date = document.getElementById('id_emi_inst_repay_from_date').value;
    var total_amount = Number(document.getElementById('id_total_emi_amount').value);
    set_emi_emifees_fee(total_amount);
    $.ajax({
        url: "/sales-emimat-date/" + emi_freq + "/" + num_of_installment + "/" + repay_from_date,
        type: 'GET',
        success: function (data) {
            if (data.form_is_valid) {
                $('#id_installment_exp_date').val(data.maturity_date);
                $('#id_emi_inst_repay_from_date').val(data.first_inst_date);
            } else {
                $('#id_installment_exp_date').val('');
                $('#id_emi_inst_repay_from_date').val('');
            }
        }
    })
    return false;
}

function set_emi_emifees_fee(emi_amount) {
    $.ajax({
        url: "/sales-emifees-fee",
        type: 'GET',
        data: {
            'transaction_amount': emi_amount,
        },
        success: function (data) {
            if (data.form_is_valid) {
                $('#id_emi_fee_amount').val(data.charge_amount);
            } else {
                $('#id_emi_fee_amount').val(0);
            }
        }
    })
    return false;
}

$(function () {

    $('#dt-table-list').on('click', 'button', function () {

        try {
            var table_row = table_data.row(this).data();
            id = table_row['id']
        }
        catch (e) {
            var table_row = table_data.row($(this).parents('tr')).data();
            id = table_row['id']
        }

        var class_name = $(this).attr('class');
        if (class_name == 'btn btn-info btn-sm') {
            cancel_emi_setup(id);
        }

    })

    function cancel_emi_setup(id) {
        if (confirm('Are you sure you want to cancel this EMI?') == true) {
            $.ajax({
                url: "/sales-emisetup-cancel/" + id,
                type: "POST",
                success: function (data) {
                    if (data.form_is_valid) {
                        alert(data.success_message);
                        table_data.ajax.reload();
                    } else {
                        alert(data.error_message)
                        table_data.ajax.reload();
                    }
                }
            })
        }
    }

});

var total_amount = 0;

$("#id_total_emi_amount").on("change paste keyup", function () {
    total_amount = (Number(document.getElementById('id_total_emi_amount').value) * Number(document.getElementById('id_number_of_installment').value));
    $('#id_instrepay_tot_repay_amt').val(total_amount);
    set_emi_emifees_fee(total_amount);
});

$("#id_number_of_installment").on("change paste keyup", function () {
    total_amount = (Number(document.getElementById('id_total_emi_amount').value) * Number(document.getElementById('id_number_of_installment').value));
    $('#id_instrepay_tot_repay_amt').val(total_amount);
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

