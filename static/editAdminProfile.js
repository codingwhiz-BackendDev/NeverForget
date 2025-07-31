$(document).ready(function () {
    $('#editProfileForm').on('submit', function (e) {
        e.preventDefault();
        var formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: '/editAdminProfile',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) { 
                closeModal('editProfileModal');
                location.reload();
            },
            error: function (xhr) {
                console.error(xhr.responseText); 
            }
        });
    });
});
