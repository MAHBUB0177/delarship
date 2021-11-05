

tinymce.init({ 
  selector: '.tinymce',
  plugins: 'table link autoresize fullscreen image code imagetools lists insertdatetime',
  menubar: 'file edit insert format table',
  toolbar: 'undo redo | styleselect | bold italic underline | forecolor backcolor | alignleft aligncenter alignright alignjustify | outdent indent numlist bullist table image link insertdatetime code fullscreen',
  images_upload_url: 'filebrowser/',
  file_picker_types: 'image',
  automatic_uploads: false
});