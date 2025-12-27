function send() {

    let input = document.getElementById("msg");

    let msg = input.value.trim();

    let chat = document.getElementById("chat");



    if (msg === "") return;



    // USER MESSAGE

    let userDiv = document.createElement("div");

    userDiv.className = "user-msg";

    userDiv.innerHTML = "<b>You</b><br>" + msg;

    chat.appendChild(userDiv);

    chat.scrollTop = chat.scrollHeight;



    // TYPING INDICATOR

    let typingDiv = document.createElement("div");

    typingDiv.className = "bot-msg typing";

    typingDiv.innerText = "AI Agent is typing...";

    chat.appendChild(typingDiv);

    chat.scrollTop = chat.scrollHeight;



    fetch("/chat", {

        method: "POST",

        headers: {"Content-Type": "application/json"},

        body: JSON.stringify({ message: msg })

    })

    .then(res => res.json())

    .then(data => {

        chat.removeChild(typingDiv);



        let botDiv = document.createElement("div");

        botDiv.className = "bot-msg";

        botDiv.innerHTML = "<b>🤖 AI Agent</b><br>" + data.reply;

        chat.appendChild(botDiv);

        chat.scrollTop = chat.scrollHeight;

    });



    input.value = "";

}

document.getElementById("msg").addEventListener("keydown", function(e) {

    if (e.key === "Enter") {

        send();

    }

}
);