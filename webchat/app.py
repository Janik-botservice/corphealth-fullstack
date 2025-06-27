from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://orange-plant-063661303.6.azurestaticapps.net"}})

antworten = {
    "passwort vergessen": "Kein Problem! Du kannst dein Passwort ganz einfach über diesen Link zurücksetzen: https://example.com/passwort-zuruecksetzen",
    "id vergessen": "Das lässt sich klären. Bitte wende dich mit deiner E-Mail-Adresse direkt an unseren Support.",
    "registrierung nicht möglich": "Bitte überprüfe, ob alle Pflichtfelder korrekt ausgefüllt sind. Bei weiteren Problemen melde dich gern bei uns.",
    "terminbuchung nicht möglich": "Stelle sicher, dass du eingeloggt bist. Wenn es trotzdem nicht klappt, helfen wir dir gern weiter.",
    "terminbestätigung nicht erhalten": "Bitte schau auch in deinem Spam-Ordner nach. Manchmal landen unsere Mails dort.",
    "wann erhalte ich meinen bericht": "Dein Gesundheitsbericht ist in der Regel ca. 7 Tage nach deinem Check-up verfügbar.",
    "fragen zum bericht": "Bei Unklarheiten helfen wir dir gerne weiter. Du kannst auch einen Rückruf durch unser Team anfordern.",
    "2-faktor-authentifizierung einrichten": "Hier findest du eine einfache Schritt-für-Schritt-Anleitung zur Einrichtung: https://example.com/2fa",
    "support-ticket erstellen": "Nutze bitte unser Support-Portal, um ein Ticket zu eröffnen: https://example.com/support",
    "checkup 1": "Der Checkup 1 ist ein Basis-Check mit den wichtigsten Untersuchungen. Weitere Infos findest du hier: https://example.com/checkup1",
    "checkup 2": "Checkup 2 enthält zusätzlich eine Blutuntersuchung und ein EKG. Ideal für eine umfassendere Analyse.",
    "checkup 3": "Der Premium-Checkup mit ausführlicher ärztlicher Beratung. Für alle, die mehr wissen möchten.",
    "teilnehmer-id & problem eingeben": "Bitte teile mir deine Teilnehmer-ID sowie eine kurze Beschreibung deines Anliegens mit, damit wir dir schnell helfen können."
}

@app.route("/api/messages", methods=["POST"])
def receive_message():
    data = request.get_json()
    text = data.get("text", "").strip().lower()
    antwort = antworten.get(text, f"👀 Ich habe verstanden: '{text}'. Ein Mensch hilft dir bald weiter.")
    return jsonify({"reply": antwort})

@app.route("/api/messages", methods=["OPTIONS"])
def handle_options():
    response = app.make_default_options_response()
    headers = response.headers

    headers["Access-Control-Allow-Origin"] = "https://orange-plant-063661303.6.azurestaticapps.net"
    headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

