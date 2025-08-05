$(document).ready(function () {
  $(document).on("submit", "#birthday_form", function (e) {
    e.preventDefault();

    var formData = new FormData(this);
    var communityUserName = $("#admin-data").data("username"); 

    $.ajax({
      type: "POST",
      url: "/profile/" + communityUserName + "/",
      data: formData,
      processData: false,
      contentType: false,
      headers: {
        "X-Requested-With": "XMLHttpRequest",  
      },
      success: function (response) {
        console.log(response);
        if (response.success) {
          //alert(response.message);
          $("#birthday_form")[0].reset();
        }
      },
      error: function (response) {
        console.error("An error occurred:", response);
      },
    });
  });
});
