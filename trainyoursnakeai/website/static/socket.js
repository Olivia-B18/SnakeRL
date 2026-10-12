const socket = io({ autoConnect: false });

document.getElementById("join-btn").addEventListener("click", function () {
    let username = document.getElementById("username").value;
    socket.connect();

    document.cre

    socket.on("connect", function () {
        socket.emit("user_join", username);
    })
})


document.getElementById("btn-train").addEventListener("click", function () {
    socket.emit("train");
})

socket.on("snake_data", function (data) {
    let ul = document.getElementById("ul-snake-data");
    let li = document.createElement("li")
    li.appendChild(document.createTextNode(data["data"]["snake"][0]["x"]));
    ul.appendChild(li)
    ul.scrollTop = ul.scrollHeight;
})
