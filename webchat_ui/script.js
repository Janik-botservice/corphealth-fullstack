const submenuContainer = document.getElementById("submenu-container");
const chatBox = document.getElementById("chat-box");

// URL zeigt auf den Azure Bot App-Service (angepasst)
const API_URL = "https://corphealth-webchat.azurewebsites.net/api/messages";

function clearSubmenu() {
    submenuContainer.innerHTML = '';
    submenuContainer.style.display = 'none';
}

function clearChat() {
    chatBox.innerHTML = '';
}

function showOptions(options) {
    submenuContainer.innerHTML = '';
    submenuContainer.style.display = 'block';
    options.forEach(option => {
        const button = document.createElement("button");
        button.classList.add("clickable");
        button.textContent = option;
        button.onclick = () => {
            clearChat();
            appendMessage("user", option);
            sendToBot(option);
        };
        submenuContainer.appendChild(button);
    });
}

function selectMenu(menu, button) {
    document.querySelectorAll('.menu button').forEach(btn => btn.classList.remove('selected'));
    button.classList.add('selected');
    clearSubmenu();
    clearChat();

    switch (menu) {
        case 'login_registration':
            showOptions(["Passwort vergessen", "ID vergessen", "Registrierung nicht möglich"]);
            break;
        case 'terminbuchung':
            showOptions(["Terminbuchung nicht möglich", "Terminbestätigung nicht erhalten"]);
            break;
        case 'gesundheitsbericht':
            showOptions(["Wann erhalte ich meinen Bericht?", "Fragen zum Bericht"]);
            break;
        case 'it_probleme':
            showOptions(["2-Faktor-Authentifizierung einrichten", "Support-Ticket erstellen"]);
            break;
        case 'angebote_infomaterial':
            showOptions(["Checkup 1", "Checkup 2", "Checkup 3"]);
            break;
        case 'weitere_fragen':
            showOptions(["Teilnehmer-ID & Problem eingeben"]);
            break;
    }
}

function appendMessage(sender, text) {
    const msg = document.createElement("div");
    msg.className = sender === "user" ? "user-message" : "bot-message";
    msg.textContent = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById("user-input");
    const text = input.value.trim();
    if (!text) return;
    appendMessage("user", text);
    sendToBot(text);
    input.value = "";
}

function sendToBot(message) {
    fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            type: "message",
            from: { id: "user1", name: "User" },
            text: message
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data && data.text) {
            appendMessage("bot", data.text);
        }
    })
    .catch(err => {
        console.error("Fehler beim Senden:", err);
        appendMessage("bot", "❌ Fehler beim Senden an den Bot.");
    });
}

window.onload = () => {
    appendMessage("bot", "👋 Hallo, ich bin Corpi, dein digitaler Support-Assistent. Wähle einfach oben ein Thema aus, und ich helfe dir so gut ich kann!");
};
