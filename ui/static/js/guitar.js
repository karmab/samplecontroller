function guitarcreate() {
    $("#wheel").show();
    var name = $("#name").val();
    var brand = $("#brand").val();
    data = {'name': name, 'brand': brand};
    $.ajax({
         type: "POST",
          url: '/guitaradd',
          data: data,
          success: function(data) {
              $("#wheel").hide();
              $("#result").html("<div class='alert alert-success alert-dismissable'>Guitar added!</div>");
              if (data.result == 'success') {
                $("body").overhang({message: "Guitar "+name+" Created!!!", type: "success", duration: 5});
              } else {
                $("body").overhang({message: "Guitar "+name+" Failed to Create Because "+data.reason, type: "error", closeConfirm: true});
              };
          }
    });
}
