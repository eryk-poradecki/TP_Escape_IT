var socket = new WebSocket('ws://127.0.0.1:8000/ws/socket-server/web'); // not sure if it's correct
var form = document.getElementById('tts-form');
var textInput = document.getElementById('tts-text');

form.addEventListener('submit', function (event) {
    event.preventDefault();
    var text = textInput.value;

    var message = {
        'type': 'help_response',
        'hint': text
    };

    socket.send(JSON.stringify(message));
});
