

let myPromise = new Promise(function(myResolve, myReject) {
    // "Producing Code" (May take some time)
    
      myResolve(); // when successful
      myReject();  // when error
    });
    
    // "Consuming Code" (Must wait for a fulfilled Promise)
    myPromise.then(
      function(value) { /* code if successful */ },
      function(error) { /* code if some error */ }
    );
    function print_div_data(divName) {
                var promise = new Promise(function (resolve,reject) {
                var divContents = document.getElementById(divName).innerHTML;
                // var title = document.getElementById('print_title').value;
                var host="http://"+window.location.host+"/static/assets/stylesheets/report-page-a4-portrait.css" 
                var pos_css="http://"+window.location.host+"/static/assets/stylesheets/pos-print.css" 
                var a = window.open('', '', 'height=720, width=1024');
                a.document.write('<html><head>');
                // a.document.write('<title>'+title+'</title>');
                a.document.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">');
                a.document.write('<link rel="stylesheet" href='+host+'>');
                a.document.write('<link rel="stylesheet" href='+pos_css+'>');
                a.document.write('</head><body>');
                a.document.write(divContents);
                a.document.write('</body></html>');
                a.document.close();
                if(a.document){
                  resolve(a)
                }else{
                  reject(("It is a failure lode print window."));
                }
              // setTimeout(() => {
                //   a.print();
                // }, 500);
    
                });
                return promise;
                
            }
    function print_div(){
      print_div_data('receipt-data').then(x=>{
        setTimeout(() => {
         x.print()
        }, 500);
        x.onafterprint = x.close;  
      }).catch(err=> {
      alert("Error: " + err);
    })
    }
    
    // var document_width=document.getElementById('receipt-data').offsetWidth
    // var document_height = document.getElementById('receipt-data').offsetHeight
    // var save_pdf_btn= document.getElementById('save-pdf-button')
    // if (document_width>794){
    //   save_pdf_btn.style.display='none'
    // }else{
    //   save_pdf_btn.style.display='inline-block'
    // }
    // if (document_height>1123){
    //   save_pdf_btn.style.display='none'
    // }else{
    //   save_pdf_btn.style.display='inline-block'
    // }
    
    //HTML to PDF 
  // function generatePDF() {
  //   var width_value = document.getElementById('receipt-data').offsetWidth
  //   var height_value = document.getElementById('receipt-data').offsetHeight
  //   var html_data = document.getElementById('receipt-data').innerHTML
  //   var data = document.getElementById('receipt-data')

  //   if(width_value >794){
  //     ore='landscape'
  //     font_size=8
  //   }else{
  //     ore='portrait'
  //     font_size=11
  //   }
  //   var opt = {
  //       margin:       10,
  //       filename:     Date.now(),
  //       image:        { type: 'jpeg', quality: .94 },
  //       jsPDF:        { unit: 'pt', format: 'a4', orientation:ore,getFontSize:font_size }
  //     };
  //   html2pdf().set(opt).from(html_data).save();
  //   data.style.fontSize='1em'
  //   data.style.width=width_value
  // }

  // Quick and simple export target #table_id into a csv
function download_table_as_csv(table_id, separator = ',') {
  
  
  // Select rows from table_id
  var rows = document.querySelectorAll('table#' + table_id + ' tr');
  // Construct csv
  var csv = [];
  for (var i = 0; i < rows.length; i++) {
      var row = [], cols = rows[i].querySelectorAll('td, th');
      for (var j = 0; j < cols.length; j++) {
          // Clean innertext to remove multiple spaces and jumpline (break csv)
          var data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ')
          // Escape double-quote with double-double-quote (see https://stackoverflow.com/questions/17808511/properly-escape-a-double-quote-in-csv)
          data = data.replace(/"/g, '""');
          // Push escaped string
          row.push('"' + data + '"');
      }
      csv.push(row.join(separator));
  }
  var csv_string=""
  setTimeout(() => {
    csv_string += csv.join('\n');
  
  // Download it
  let time_stame=Date.now()
  var filename = String(new Date().toLocaleString())+ '-' + String(Math.floor(Math.random() * 100)) + '.csv';
  var link = document.createElement('a');
  link.style.display = 'none';
  link.setAttribute('target', '_blank');
  link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv_string));
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  }, 1500);
  
}

function print_div_test(){
  let data=document.getElementById('receipt-data')
  data.style.fontSize='9px';
  window.print()
}