import os
import asyncio
from aiohttp import web
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    BotFrameworkAdapter,
    TurnContext
)
from botbuilder.schema import Activity
from dotenv import load_dotenv

load_dotenv()

from botbuilder.core.integration import aiohttp_error_middleware

# Antworten-Logik wie vorher
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

class EchoBot:
    async def on_turn(self, turn_context: TurnContext):
        if turn_context.activity.type == "message":
            user_text = turn_context.activity.text.strip().lower()
            antwort = antworten.get(user_text, f"👀 Ich habe verstanden: '{user_text}'. Ein Mensch hilft dir bald weiter.")
            await turn_context.send_activity(antwort)

# Adapter konfigurieren (Credential leer für lokalen Test)
SETTINGS = BotFrameworkAdapterSettings("", "")
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Error Handling
async def on_error(context: TurnContext, error: Exception):
    print(f"❌ Fehler im Bot: {error}")
    await context.send_activity("Es ist ein Fehler aufgetreten.")

ADAPTER.on_turn_error = on_error

BOT = EchoBot()

# Webserver starten
async def messages(req: web.Request) -> web.Response:
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return web.Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return web.json_response(data=response.body, status=response.status)
    return web.Response(status=200)

APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 8000))
        web.run_app(APP, host="0.0.0.0", port=port)
    except Exception as e:
        raise e
