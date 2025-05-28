import logging
import os
import time

from dotenv import load_dotenv
from fastapi import Request, APIRouter
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from src.eva.conversation_validation import handle_conversation_logic
from src.models.conversation import Conversation

load_dotenv()
slack_router = APIRouter()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")  # xoxb-...
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")  # xapp-...

client = WebClient(token=SLACK_BOT_TOKEN)

# Obtener BOT_ID una sola vez al iniciar la aplicación
BOT_ID = None
try:
    bot_info = client.api_call("auth.test")
    BOT_ID = bot_info["user_id"]
    print(f"Bot inicializado con ID: {BOT_ID}")
except Exception as e:
    print(f"Error al obtener BOT_ID: {e}")
    
# Cache para evitar procesar eventos duplicados
processed_events = {}


@slack_router.post("/slack/events")
async def handle_slack_event(req: Request):
    payload = await req.json()

    # Verificación de URL de Slack
    if "challenge" in payload:
        return {"challenge": payload["challenge"]}
    
    # Verificar que sea un evento válido
    if "event" not in payload:
        return {"status": "ok"}
    
    event = payload.get("event", {})
    
    # Verificar que el evento tenga user_id
    if "user" not in event:
        return {"status": "ok"}
        
    # Control de idempotencia - evitar procesar el mismo evento varias veces
    event_id = payload.get("event_id") or payload.get("event_time") or time.time()
    event_ts = event.get("ts", "")
    unique_id = f"{event_id}-{event_ts}"
    
    if unique_id in processed_events:
        print(f"Evento ya procesado: {unique_id}")
        return {"status": "ok"}
    else:
        processed_events[unique_id] = True
        # Limitar tamaño del cache
        if len(processed_events) > 1000:
            # Eliminar elementos antiguos
            processed_events.clear()
    
    # Ignorar mensajes del propio bot
    if event['user'] == BOT_ID:
        return {"status": "ok"}
    
    print("Procesando mensaje de usuario: " + event['user'])



    # Solo procesar eventos de tipo mensaje o menciones
    if event.get("type") == "app_mention" or event.get("type") == "message":
        channel = event["channel"]
        user = event["user"]
        text = event["text"]
        logging.info(f"Procesando mensaje: {channel}")
        
        
        # Usar el ID del canal como ID de conversación para mantener contexto
        conversation_object = Conversation(conversation_id=1, message=text)
        
        # Pasar el user_id a la función de conversación
        response_json = await handle_conversation_logic(conversation_object, user_id=user)


        try:
            # Obtener el timestamp del mensaje original
            thread_ts = event.get("ts")
            
            # Enviar la respuesta como hilo al mensaje original
            client.chat_postMessage(
                channel=channel,
                text=response_json.get("response")[3].get("message"),
                thread_ts=thread_ts  # Este parámetro hace que sea un hilo
            )
        except SlackApiError as e:
            print(f"Error: {e.response['error']}")

    return {"status": "ok"}
