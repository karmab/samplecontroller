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
                $.notify("Guitar "+name+" Created!!!", "success");
              } else {
                $.notify("Pool "+name+" Failed to Create Because "+data.reason, "danger");
              };
          }
    });
}
