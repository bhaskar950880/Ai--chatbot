function send() {
    let input = document.getElementById("msg");
    let msg = input.value.trim();
    let chat = document.getElementById("chat");

    if (msg === "") return;

    // 1. USER MESSAGE: Screen par user ka message dikhana
    let userDiv = document.createElement("div");
    userDiv.className = "user-msg";
    userDiv.innerHTML = "<b>You</b><br>" + msg;
    chat.appendChild(userDiv);
    chat.scrollTop = chat.scrollHeight;

    // 2. TYPING INDICATOR: Bot soch raha hai...
    let typingDiv = document.createElement("div");
    typingDiv.className = "bot-msg typing";
    typingDiv.innerText = "AI Agent is typing...";
    chat.appendChild(typingDiv);
    chat.scrollTop = chat.scrollHeight;

    // 3. FETCH: Server se data mangwana
    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: msg })
    })
    .then(res => res.json())
    .then(data => {
        // Typing indicator hatana
        chat.removeChild(typingDiv);

        // 4. BOT MESSAGE: Markdown parsing ke saath
        let botDiv = document.createElement("div");
        botDiv.className = "bot-msg";
        
        // YAHAN BADLAV HAI: 
        // marked.parse(data.reply) use karne se paragraphs aur points sahi ho jayenge
        botDiv.innerHTML = "<b>🤖 AI Agent</b><br>" + marked.parse(data.reply);
        
        chat.appendChild(botDiv);
        chat.scrollTop = chat.scrollHeight;
    })
    .catch(error => {
        console.error("Error:", error);
        chat.removeChild(typingDiv);
    });

    // Input field khali karna
    input.value = "";
}

// Enter Key support
document.getElementById("msg").addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
        send();
    }
});