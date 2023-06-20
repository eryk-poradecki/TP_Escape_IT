let socket = null;
let form = null;
let textInput = null;

window.onload = init

function init() {
    socket = new WebSocket('ws://127.0.0.1:8000/ws/socket-server/web');
    form = document.getElementById('tts-form');
    textInput = document.getElementById('tts-text');

    form.addEventListener('submit', function (event) {
    event.preventDefault();
    var text = textInput.value;

    var message = {
        'type': 'help_response',
        'hint': text
    };

    socket.send(JSON.stringify(message));
});
}
