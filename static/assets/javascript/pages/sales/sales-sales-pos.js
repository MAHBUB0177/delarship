"use strict";
$(document).ready(function () {
    promise_return();
});

async function promise_return() {
    let cart_table = $("#cart_table");
    cart_table.html("");
    cart_table.hide();
    await post_data_to_model().then((data) => {
        fn_tr_of_chart(data);
    }).catch((err) => {
        console.log(err);
    });
}

async function promise_return2(e, ...param) {
    let cart_table = $("#cart_table");
    cart_table.html("");
    cart_table.hide();
    await post_data_to_model(e, ...param).then((data) => {
        fn_tr_of_chart(data);
    }).catch((err) => {
        console.log(err);
    });
}

function post_data_to_model(event, ...param) {
    let URL;
    let product_id;
    let data_string;

    if (event && param) {
        if (param == undefined) {
            product_id = event.getAttribute("data-product_id");
            URL = "/sales-postemp-update/" + product_id;
            //log("event+param")
        }
        else {
            product_id = event.getAttribute("data-product_id");
            URL = "/sales-postemp-update/" + product_id;
            data_string = {
                "quantity": param[0]
            };
            //log("only event");
        }
    }
    else {
        URL = "/sales-postemp-update";
       // log("no event");
    }
    return new Promise((resolve, reject) => {
        $.ajax({
            url: URL,
            data: data_string,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                resolve(data);
            },
            error: function (err) {
                console.log(err);

                reject(err);
            }
        });
    });
}


function fn_tr_of_chart(data) {
    let sales_details = data.sales_details;
    sales_details.forEach(element => {
        let total_price = 0.00;
        let element_literal = `<tr><td><a href="#">${element.product_name}</a></td>
                            <td class="align-middle text-center"> ${element.product_model} </td>
                            <td class="align-middle"><button onclick=btn_increase_quantity(this) data-product_id=${element.product_id} class="btn" style="background-color:#b8b8b8;">
							<i class="fas fa-plus"></i></button></td>
                            <td class="align-middle m-auto input_td"> <input type="text" onchange="refresh_quentity_update_on_manual(this)" class="align-middle text-center" data-product_id=${element.product_id}  value="${element.quantity}" style="width: 60px;"></td>
                            <td class="align-middle"><button class="btn" data-product_id=${element.product_id} onclick=btn_decrease_quantity(this) style="background-color:#b8b8b8;">
							<i class="fas fa-minus"></i></button></td>

                            <td class="align-middle text-center">${element.product_price} </td>
                            <td class="align-middle text-center">${element.total_price} </td>
                            <td class="align-middle text-center">${element.discount_amount} </td>
                            <td class="align-middle text-center">${element.discount_rate} </td>

                            <td class="align-middle text-right">
                            <a href="#" onclick="edit_btn_click(this)" data-product_id=${element.id}  class="btn btn-sm btn-icon btn-secondary"><i class="fa fa-pencil-alt"></i>
							<span class="sr-only">Edit</span></a> <a href="#"onclick="remove_btn_click(this)" data-product_id=${element.id}  class="btn btn-sm btn-icon btn-secondary">
							<i class="far fa-trash-alt"></i> <span class="sr-only">Remove</span></a>
                            </td>
							</tr>`;


        let cart_table = $("#cart_table");
        cart_table.append(element_literal).show('slow');
        cart_table.slideDown();
    });

}


function refresh_listof_product_infoby_group(e) {
    promise_return();
    nav_active_class_add(e);
    let group_id = e.getAttribute("data-group_id");
    let URL = "/sales-posproductby-group/" + group_id;
    fetch(URL, {
        method: "GET",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    })
        .then(response => {
            return response.json();
        })
        .then(function (html) {
            if (!html) {

                $(".group_product_list").append(`<h6>No data found</h6>`);
            }
            else {
                $(".group_product_list").html(" ");
                fn_li_group_by_product(html);
            }

        })
        .catch(function (err) {
            console.log('Failed to fetch page: ', err);
        });
}
function fn_li_group_by_product(data) {
    let product = data.list_products;
    product.forEach(element => {
        let li_element = `   <li id="id_list_of_products_bygrp" onclick=promise_return2(this) class="list-group-item list-group-item-action list-group-item-info" data-product_id=${element.product_id}>
        ${element.product_name}</li> `;
        $(".group_product_list").append(li_element);

    });

}

function nav_active_class_add(e) {
    let class_name = $(".nav-link");
    class_name.each((element) => {
        let class_list = class_name[element].classList;
        if (class_list.contains("active")) {
            class_list.remove("active");
        }
    });
    if (e.classList.contains("active")) {
        e.classList.remove("active");
    }
    else {
        e.classList.add("active");
    }
}

$("#id_product_id").on("change", function () {
    let myElm = document.createElement("li");
    myElm.setAttribute("data-product_id", this.value);
    promise_return2(myElm);
});

function StringToNumber(values) {
    var number_value = Number(values);
    return number_value;
}
let sub_increse_decrese_fn = function (event) {
    let product_id = event.getAttribute("data-product_id");
    let quantity_input = $(event).parent().siblings(".input_td").children();
    let current_quantity = quantity_input.val();
    let myElm = document.createElement("li");
    myElm.setAttribute("data-product_id", product_id);
    return { myElm, product_id, quantity_input, current_quantity };
}


function btn_increase_quantity(event) {
    let obj = sub_increse_decrese_fn(event);
    obj.quantity_input.val(StringToNumber(obj.current_quantity) + 1);
    let new_quantity = obj.quantity_input.val();
    setTimeout(function () {
        promise_return2(obj.myElm, new_quantity);
    }, 200);

}

function btn_decrease_quantity(event) {
    let obj = sub_increse_decrese_fn(event);
    obj.quantity_input.val(StringToNumber(obj.current_quantity) - 1);
    if (obj.current_quantity < 1) {
        obj.quantity_input.val("0");
    }
    let new_quantity = obj.quantity_input.val();
    setTimeout(function () {
        promise_return2(obj.myElm, new_quantity);
    }, 200);
}

function refresh_quentity_update_on_manual(event) {
    let obj = sub_increse_decrese_fn(event);
    let new_quantity = $(event).val();
    promise_return2(obj.myElm, new_quantity);

}


function remove_btn_click(event) {
    confirm("Are you sure delete this product")
    let product_id = event.getAttribute("data-product_id");
    product_in_cart_delete(product_id, promise_return);
}
function product_in_cart_delete(id, callback) {
    $.ajax({
        url: '/sales-details-delete/' + id,
        type: 'POST',
        dataType: 'json',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        success: function (data) {
            if (data.form_is_valid) {
                callback()
            } else {

            }
        }
    });
    return false;
}

function edit_btn_click(event) {
    let product_id = event.getAttribute("data-product_id");
    product_in_cart_edit(product_id, promise_return);
}
function product_in_cart_edit(id, callback) {
    $.ajax({
        url: '/sales-details-edit/' + id,
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
            $('#edit_model').modal('show');
        },
        success: function (data) {
            $('#edit_model .modal-content').html(data.html_form);
        }
    });
    callback()
    return false;
}