    var socket;
    $(document).ready(function () {

        socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
        socket.on('connect', function () {
            socket.emit('joined', {});
        });

        socket.on('status', function (data) {
            let tag = document.createElement("p");
            let text = document.createTextNode(data.msg);
            let element = document.getElementById("chat");
            tag.appendChild(text);
            tag.style.cssText = data.style;
            element.appendChild(tag);
            $('#chat').scrollTop($('#chat')[0].scrollHeight);

        });

        socket.on('message', function(data) {
            let tag = document.createElement("p");
            let text = document.createTextNode(data.msg);
            let element = document.getElementById("chat");



            tag.appendChild(text);
            tag.style.cssText = data.style;
            element.appendChild(tag);
            $('#chat').scrollTop($('#chat')[0].scrollHeight);

        });

        $('#message_input').keypress(function (e) {
            if (e.which === 13) {
                let message = $(this).val();
                socket.emit('send-message', {msg: message});
                $(this).val('');
            }
        });

        $('#leave').click(function (e) {
            // e.preventDefault();
            socket.emit('left', {});
        });

    });