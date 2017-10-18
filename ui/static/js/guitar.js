function guitarcreate() {
    var name = $("#name").val();
    var brand = $("#brand").val();
    data = {'name': name, 'brand': brand};
    $.ajax({
         type: "POST",
          url: '/guitaradd',
          dataType: 'json',
          data: data,
          success: function(data) {
               if (data.result == 'success') {
                $("body").overhang({message: "Guitar "+name+" Created!!!", type: "success"});
               } else {
                $("body").overhang({message: "Guitar "+name+" Failed to Create Because "+data.reason, type: "error", closeConfirm: true});
               };
          }
    });
}

function guitardelete(name) {
    data = {'name': name};
    $.ajax({
         type: "POST",
          url: '/guitardelete',
          data: data,
          dataType: 'json',
          success: function(data) {
              if (data.result == 'success') {
                $("body").overhang({message: "Guitar "+name+" Deleted!!!", type: "success"});
                guitarlist();
              } else {
                $("body").overhang({message: "Guitar "+name+" Failed to Delete Because "+data.reason, type: "error", closeConfirm: true});
              };
          }
    });
}

function guitarlist() {
    $.ajax({
         type: "GET",
          url: '/guitarlist',
          //dataType: 'json',
          success: function(data) {
          $('#guitars').html(data);
          }
    });
}
