const checkCredentials = () => {
    // package data in a JSON object
    // var data_d = {'email': 'owner@email.com', 'password': 'password'}
    var data_d = {
        'email': document.getElementById('email_input').value,
        'password': document.getElementById('password_input').value
    };

    // SEND DATA TO SERVER VIA jQuery.ajax({})
    jQuery.ajax({
        url: "/processregister", data: data_d, type: "POST", success: function (returned_data) {
            if (returned_data['success'] === 0) {
                alert(`Register failed. ${returned_data?.['error']}. Please try again.`);
            } else {
                alert(`Register succeeded. Redirecting to login page.`);
                window.location.href = "/login";
            }
        }
    });
}

