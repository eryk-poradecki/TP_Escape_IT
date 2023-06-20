

let url = `ws://${window.location.host}/ws/socket-server/web`

const chatSocket = new WebSocket(url);

const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

chatSocket.onmessage = function(e){
    let data = JSON.parse(e.data)
    
    console.log(data)

    if (data.type === "help_request" || data.type === "custom_help_request" || data.type === "progress") {
        let div = document.createElement('div');
        div.setAttribute("class", "notification notification_not_resolved");

        let p = document.createElement('p');
        p.innerText = data.message + ". Click here to send help!";

        let pDate = document.createElement('p');
        let date = new Date()
        let minutesDisplay = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes();
        pDate.innerText = months[date.getMonth()] + " " + date.getDate() + ", " + date.getFullYear() + ", " + date.getHours() + ":" + minutesDisplay;

        div.addEventListener("click", function() {
            location.href = `/rooms/${data.room_id}`;
            fetch(`/notifications/resolve_notification/${data.notification_id}/`, {
                    method: "POST",                        
            });
        });

        div.appendChild(p);
        div.appendChild(pDate);

        notificationContainer.appendChild(div);
    }
    
}

let notificationContainer = null

window.onload = init



function init () {
    notificationContainer = document.getElementById('notifications-container')
}