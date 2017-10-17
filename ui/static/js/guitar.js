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
                $('.top-right').notify({message: { text: "Guitar "+name+" Created!!!" }, type: 'success', fadeOut: { delay: 5000 }}).show();
              } else {
                $('.top-right').notify({message: { text: "Pool "+name+" Failed to Create Because "+data.reason }, type: 'danger', fadeOut: { delay: 5000 }}).show();
              };
          }
    });
}
