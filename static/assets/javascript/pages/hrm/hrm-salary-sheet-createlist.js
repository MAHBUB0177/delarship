$(document).ready(function () {
  $("#id_dept_id").select2();
  $("#id_month_year").select2();
   monthYear()

   refresh_branch_list('');
   var branch_code = document.getElementById('id_global_branch_code').value;
   get_department_name();
  
 });

$(function () {
   $('#btnAddItem').click(function () {
    
     
       post_tran_table_data();
       
       

   });
});


function post_tran_table_data() {
   var data_string = $("#tran_table_data").serialize();
   var data_url = $("#tran_table_data").attr('data-url');
   $.ajax({
       url: data_url,
       data: data_string,
       type: 'POST',
       dataType: 'json',
       success: function (data) {
         if(data.form_is_valid){
          alert(" salary processing successful")
         }
         
         console.log(data);
       },
       error:(err)=>{
         console.log(err);
       }

   })
   return false;
}



function get_department_name() {
  $.ajax({
      url: "apiauth-department-api",
      type: "get",
      datatype: "json",
      success: function (data) {
          console.log(data)
          data.forEach((value) => {
              document.getElementById("id_dept_id").innerHTML +=
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


function monthYear(){
  const months = ["JAN-","FEB-","MAR-","APR-","MAY-","JUN-","JUL-","AUG-","SEP-","OCT-","NOV-","DEC-"];
  for(i=0;i<months.length;i++){
    let month=months[i]
    let result=month.concat(new Date().getFullYear());
    document.getElementById("id_month_year").innerHTML +=
                  '<option value="' +
                  result +
                  '">' +
                  result +
                  "</option>";
  }
}



