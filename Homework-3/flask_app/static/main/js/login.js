const checkCredentials = () => {
    // package data in a JSON object
    // var data_d = {'email': 'owner@email.com', 'password': 'password'}
    var data_d = {
        'email': document.getElementById('email_input').value,
        'password': document.getElementById('password_input').value
    };

    // SEND DATA TO SERVER VIA jQuery.ajax({})
    jQuery.ajax({
        url: "/processlogin", data: data_d, type: "POST", success: function (returned_data) {

            returned_data = JSON.parse(returned_data);
            if (returned_data['success'] === 0) {
                alert('Login failed. Please try again.');
                // document.getElementById('login_error').innerHTML = returned_data['msg'];
                // document.getElementById('login_error').style.display = 'block';
                document.getElementById('login_attempts').innerHTML = 'Login Failed. Attempts: ' + returned_data['login_attempt'];
            } else {

                window.location.href = "/home";
            }
        }
    });
}