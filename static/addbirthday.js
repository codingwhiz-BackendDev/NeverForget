$(document).ready(function () {
    $(document).on('submit', '#birthday_form', function (e) {
        e.preventDefault()
        $.ajax({ 
            type: 'POST',
            url: '/add_birthday',
            data: {
                community_user_name : $('community_user_name').val(),
                personName: $('#personName').val(),
                birthDate: $('#birthDate').val(),
                phoneNumber: $('#phoneNumber').val(),
                email: $('#email').val(),
                matric: $('#matric').val(),
                department: $('#department').val(),
                level: $('#level').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) { 

                //alert(response)

            },
            error: function (response) {
                //alert('an error occured')
            }
        }) 
        // modal =  document.getElementById('addBirthdayModal')
        // message = '{personName} successfully added'
        // modal.innerHTML= `
        //     <div class="messages-container"> 
        //         <div class="message {{ message.tags }}">
        //             <i class="message-icon fas fa- {{ message.tags }}"></i>
        //             <div class="message-text">{{ message }}</div>
        //             </div> 
        //         </div>`
        document.getElementById('personName').value = ''
        document.getElementById('birthDate').value = ''
        document.getElementById('phoneNumber').value = ''
        document.getElementById('email').value = ''
        document.getElementById('email').value = ''
        document.getElementById('matric').value = ''
        document.getElementById('department').value = ''
        document.getElementById('level').value = '' 
    })
})