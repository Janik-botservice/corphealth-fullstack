
const submenuContainer = document.getElementById("submenu-container");

function clearSubmenu() {
    submenuContainer.innerHTML = '';
    submenuContainer.style.display = 'none';
}

function showOptions(options) {
    submenuContainer.innerHTML = '';
    submenuContainer.style.display = 'block';
    options.forEach(option => {
        const button = document.createElement("button");
        button.classList.add("clickable");
        button.textContent = option;
        button.onclick = () => sendToBot(option);
        submenuContainer.appendChild(button);
    });
}

function selectMenu(menu, button) {
    document.querySelectorAll('.menu button').forEach(btn => btn.classList.remove('selected'));
    button.classList.add('selected');
    clearSubmenu();

    switch (menu) {
        case 'login_registration':
            showOptions(["Passwort vergessen", "ID vergessen", "Registrierung nicht möglich"]);
            break;
        case 'terminbuchung':
            showOptions(["Terminbuchung nicht möglich", "Terminbestätigung nicht erhalten"]);
            break;
        case 'gesundheitsbericht':
            showOptions(["Wann erhalte ich meinen Bericht", "Fragen zum Bericht"]);
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

function sendToBot(message) {
    window.WebChat.postMessage({
        type: 'message',
        text: message
    });
}

window.WebChat.renderWebChat({
    directLine: window.WebChat.createDirectLine({
        secret: 'VAVWKQSl27XKOH8JbBcf4BnxC1ZdkNhS3dmzrZfmXdXXUfPbwiAXJQQJ99BCAC5RqLJAArohAAABAZBS1Vch.CVTlgZqlinYHwiOF88EHXEm8Y885rrQMq599iENWtsHj5uKNzTdaJQQJ99BCAC5RqLJAArohAAABAZBS2eV8'
    }),
    userID: 'user1',
    username: 'Nutzer',
    locale: 'de-DE'
}, document.getElementById('webchat'));
