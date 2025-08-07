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
        if (response.success) {
          // Reset form
          $("#birthday_form")[0].reset();

          // Show success message
          $(".messages-container").html(`
            <div class="message success">
              <i class="message-icon fas fa-check-circle"></i>
              <div class="message-text">${response.message}</div>
            </div>
          `).show();

          // Hide after 5 seconds
          setTimeout(function () {
            $(".messages-container").fadeOut("slow", function () {
              $(this).empty().show(); // ✅ THIS WORKS
            });
          }, 5000);
        } else if (response.error) {
          $(".messages-container").html(`
            <div class="message error">
              <i class="message-icon fas fa-times-circle"></i>
              <div class="message-text">${response.error}</div>
            </div>
          `).show();
        }
      },
      error: function () {
        $(".messages-container").html(`
          <div class="message error">
            <i class="message-icon fas fa-times-circle"></i>
            <div class="message-text">Something went wrong. Try again.</div>
          </div>
        `).show();
      },
    });
  });
});
