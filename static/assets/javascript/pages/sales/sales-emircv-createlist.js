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
                var account_number = document.getElementById('id_account_number').value;
                var emi_reference_no = document.getElementById('id_emi_reference_no').value;
                var search_url = "/sales-emireceive-api/?account_number=" + account_number + "&emi_reference_no=" + emi_reference_no;   //change
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
                        { data: 'account_number' },
                        { data: 'emi_reference_no' },
                        { data: 'receive_date' },
                        { data: 'entry_day_sl' },
                        { data: 'receive_amount' },
                        { data: 'receive_document_number' },
                        {
                            "data": null,
                            "defaultContent": '<button type="button" class="btn btn-info btn-sm">Edit</button>' + '&nbsp;&nbsp' +
                                '<button type="button" class="btn btn-danger btn-sm">Cancel</button>'

                        }
                    ]
                });
            }
        }]);

        return fn_data_table;
    }();

var id = 0
let w_tran_screen = 'EMI_RECEIVE';
let w_transaction_type = '';
let w_account_type = '';

$(function () {
    $('#btnSearch').click(function () {
        var account_number = document.getElementById('id_account_number').value;
        if (account_number === "") {
            alert("Please Select Customer");
        } else {
            new fn_data_table();
        }
    });
})


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
            show_edit_form(id);
        }
        if (class_name == 'btn btn-danger btn-sm') {
            cancel_transaction(id);
        }
    })

    function show_edit_form(id) {
        $.ajax({
            url: '/sales-emircv-edit/' + id, //change
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

    function cancel_transaction(id) {
        if (confirm('Are you sure you want to cancel this Transaction?') == true) {
            $('#page_loading').modal('show');
            $.ajax({
                url: "/sales-emircv-cancel/" + id,
                type: "POST",
                success: function (data) {
                    if (data.form_is_valid) {
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
        }
    }

    $("#id_account_number").on("change paste keyup", function () {
        refresh_emiinvoice_list();
    });

    function refresh_emiinvoice_list() {
        var account_number = document.getElementById('id_account_number').value;
        var url = 'sales-choice-emiinvoice';
        $.ajax({
            url: url,
            data: {
                'account_number': account_number
            },
            success: function (data) {
                $("#id_emi_reference_no").html(data);
            }
        });
        return false;
    }

    $("#id_emi_reference_no").on("change paste keyup", function () {
        get_emi_amount();
    });

    function get_emi_amount() {
        var emi_reference_no = document.getElementById('id_emi_reference_no').value;
        var account_number = document.getElementById('id_account_number').value;
        $.ajax({
            url: "sales-emi-details",
            data: {
                'account_number': account_number,
                'emi_reference_no': emi_reference_no
            },
            type: 'GET',
            success: function (data) {
                if (data.form_is_valid) {
                    $('#id_receive_amount').val(data.installment_amount);
                    $('#id_number_of_installment').val(data.number_of_installment);
                    $('#id_total_emi_amount').val(data.total_emi_amount);
                    $('#id_total_emi_payment').val(data.total_emi_payment);
                    $('#id_total_emi_due').val(data.total_emi_due);
                    $('#id_paid_installment_number').val(data.paid_installment_number);
                } else {
                    $('#id_receive_amount').val('');
                    $('#id_number_of_installment').val('');
                    $('#id_total_emi_amount').val('');
                    $('#id_total_emi_payment').val('');
                    $('#id_total_emi_due').val('');
                    $('#id_paid_installment_number').val('');
                }
            }
        })
        return false;
    }

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
                    var account_number = document.getElementById("select2-id_account_number-container");
                    account_number.textContent = "-----------------";
                    var global_branch_code = document.getElementById('id_global_branch_code').value;
                    $('#id_branch_code').val(global_branch_code);
                } else {
                    $('#page_loading').modal('hide');
                    alert(data.error_message);
                }
            }
        })
        return false;
    }

});