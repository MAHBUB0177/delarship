$(function () {
    $('#btnSearch').click(function () {
        ProductList();
    });
})

$(document).ready(function () {
    $('#id_group_id').select2();
    $('#id_brand_id').select2();
    $('#id_product_name').select2();
    refresh_branch_list('');
    refresh_group_list();
    refresh_brand_list();
});

$(window).on('load', function () {
    var global_branch_code = document.getElementById('id_global_branch_code').value;
    $('#id_branch_code').val(global_branch_code);
});

function ProductList(){
    var product_id = document.getElementById('id_product_name').value;
    var group_id = document.getElementById('id_group_id').value;
    var brand_id = document.getElementById('id_brand_id').value;
    var product_model = document.getElementById('id_product_model').value;
    var product_bar_code = document.getElementById('id_product_bar_code').value;
    var search_url = "/sales-products-api/?product_id=" + product_id + "&product_model=" + product_model 
    + "&product_bar_code=" + product_bar_code+ "&group_id=" + group_id+ "&brand_id=" + brand_id;
    
    $.ajax({
        url: search_url,
        dataType: 'json',
        success: function (data) {
           let html=""
           data.forEach(p => {
               html+='<tr>\
               <td><input type="checkbox" class="form-control product_id" value="'+p.product_id+'"></td>\
               <td>'+p.product_name+'</td>\
               <td>'+p.product_group.group_name+'</td>\
               <td>'+p.brand_id.brand_name+'</td>\
               <td></td>\
               <td>'+p.product_sales_price+'</td>\
               <td>'+p.product_bar_code+'</td>\
               <td><input type="number" min="0" id="qty_'+p.product_id+'" value="0" class="form-control"></td>\
               </tr>'
           });
           $('#table_barcode tbody tr').remove()
           $('#table_barcode').find('tbody').append(html);

        }
      })

}

function checkAll(all){
    let product_ids= document.querySelectorAll('.product_id')
    product_ids.forEach(element => {
        element.checked = all.checked
    });
}

function submit_form(){
    let product_ids= document.querySelectorAll('.product_id')
    let selete_product=[]
    let potion = $('input[name="choice"]:checked').val();
    product_ids.forEach(element => {
        if(element.checked){
            let qty=$('#qty_'+element.value).val()
            let data={product_id:element.value,qty: Number(qty)}
            selete_product.push(JSON.stringify(data))
        }
    });
    let dataString={
        product:selete_product,
        potion:potion
    }
    $('#page_loading').modal('show');
    $.ajax({
        url: '/sales-products-barcode',
        type:'POST',
        data:dataString,
        dataType: 'json',
        success: function (data) {
            if(data.success_message){
                    // location.href='/sales-products-barcode-pdf';
                generate_pdf()
            }
        }
      })
}

function generate_pdf(){
    $.ajax({
        url:'/sales-products-barcode-pdf-gen',
        type:'get',
        dataType: 'json',
        success: function (data) {
            var pdf = new jsPDF('p', 'pt', 'a4');
            // console.log(data)
                let x=0
                let y=15
                let counter=1
            data.barcode_list.forEach(barcode => {
                for (let index = 1; index <= barcode.print_qty; index++) {
                    
                    var img = new Image();
                    let imgSource ='/media/'+barcode.barcode_image
                    img.src=imgSource
                    pdf.addImage(img, 'PNG', x*84,y,80,100);
                    if(counter%7 == 0){
                        x=0
                        y+=102
                        pdf.line(x,y-2,595,y-2)
                    }else{
                        x++
                    }
                    if(counter%56 == 0){
                        pdf.addPage('a4','p')
                        x=0
                        y=15
                    }
                    counter++
                }
            });
            pdf.save(Date.now()+'.pdf')
            $('#page_loading').modal('hide');
        }
      })
}
