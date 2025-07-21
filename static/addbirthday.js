$(document).ready(function () {
    $(document).on('submit', '#birthday_form', function (e) {
        e.preventDefault();

        var formData = new FormData(this);

        $.ajax({ 
            type: 'POST',
            url: '/add_birthday',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) { 
                console.log(response);
                // You can add a success message here, maybe clear the form
                $('#birthday_form')[0].reset();
            },
            error: function (response) {
                console.error('An error occurred:', response);
                // You can show an error message to the user
            }
        });
    });
});