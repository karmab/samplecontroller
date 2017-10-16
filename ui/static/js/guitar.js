function guitaradd() {
    var name = $("#name").val();
    var brand = $("#brand").val();
    data = {'name': name, 'brand': brand};
    $.ajax({
         type: "POST",
          url: '/guitaradd',
          data: data,
          success: function(data) {
              alert(data.result)
              if (data.result == 'success') {
                $(".result").replaceWith("<div class='alert alert-success alert-dismissable'>Guitar added!</div>");
              } else {
                $(".result").replaceWith("<div class='alert alert-error alert-dismissable'>Guitar not added</div>");
              };
          }
    });
    return ;
}
