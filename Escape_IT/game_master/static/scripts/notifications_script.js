
console.log("chuj")

let url = `ws://${window.location.host}/ws/socket-server/web`

const chatSocket = new WebSocket(url);

chatSocket.onmessage = function(e){
    let data = JSON.parse(e.data)
    
    console.log(data)

    if (data.type == 'help_request') {
        console.log("help request")

        // Tworzenie elementu ktory bedzie wrzucony do listy notyfikacji
        // TODO: Dopasowac do elementu i klass z css
        var p = document.createElement('p');
        p.setAttribute("class", "notification");
        p.innerText = data.message;
        notificationContainer.appendChild(p);
    }
}

let notificationContainer = null

window.onload = init



function init () {
    notificationContainer = document.getElementById('notifications-container')
}