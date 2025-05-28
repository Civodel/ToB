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

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("slack_integration")


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
        
    # Control de idempotencia - construir un ID único más robusto
    event_id = payload.get("event_id", "no-id")
    event_ts = event.get("ts", str(time.time()))
    event_channel = event.get("channel", "no-channel")
    event_user = event.get("user", "no-user")
    event_type = event.get("type", "no-type")
    event_text = event.get("text", "")[:20]  # Solo primeros 20 caracteres
    
    # Crear un identificador único que combine varios campos
    unique_id = f"{event_id}-{event_ts}-{event_channel}-{event_user}-{event_type}-{event_text}"
    
    logger.info(f"Evento recibido: {unique_id}")
    
    # Verificar si ya procesamos este evento
    if unique_id in processed_events:
        logger.warning(f"Evento duplicado detectado y omitido: {unique_id}")
        return {"status": "ok"}
    
    # Marcar como procesado
    processed_events[unique_id] = time.time()
    
    # Limpieza de cache - eliminar eventos antiguos (más de una hora)
    current_time = time.time()
    old_events = [k for k, v in processed_events.items() if current_time - v > 3600]
    for event_key in old_events:
        del processed_events[event_key]
        
    # Si el cache sigue creciendo demasiado, limpiarlo todo
    if len(processed_events) > 1000:
        logger.warning("Limpiando cache de eventos - demasiados eventos acumulados")
        processed_events.clear()
    
    # Ignorar mensajes del propio bot
    if event.get('user') == BOT_ID:
        logger.info(f"Ignorando mensaje del propio bot: {event.get('text', '')[:30]}")
        return {"status": "ok"}
    
    # Filtrar eventos que no son relevantes para nosotros
    if event.get("type") not in ["app_mention", "message"]:
        logger.info(f"Ignorando evento de tipo: {event.get('type')}")
        return {"status": "ok"}
        
    # Ignorar mensajes de subtipos que no queremos procesar (ediciones, eliminaciones, etc.)
    if event.get("subtype") in ["message_changed", "message_deleted", "bot_message"]:
        logger.info(f"Ignorando mensaje de subtipo: {event.get('subtype')}")
        return {"status": "ok"}
    
    logger.info(f"Procesando mensaje de usuario: {event.get('user')} - Texto: {event.get('text', '')[:30]}...")

    # Ya filtramos los tipos de eventos arriba, ahora procesamos
    channel = event.get("channel")
    user = event.get("user")
    text = event.get("text", "")

    logger.info(f"Canal: {channel} - Usuario: {user} - Mensaje: {text[:30]}")

    # Usar el ID del canal como ID de conversación para mantener contexto
    conversation_object = Conversation(conversation_id=1, message=text)

    # Pasar el user_id a la función de manejo de conversación
    response_json = await handle_conversation_logic(conversation_object, user_id=user)

    try:
        # Obtener el timestamp del mensaje original
        thread_ts = event.get("ts")

        # Verificar que tengamos una respuesta válida
        if response_json and "response" in response_json and len(response_json.get("response", [])) > 3:
            response_text = response_json.get("response")[3].get("message", "No hay respuesta disponible")
            
            # Enviar la respuesta como hilo al mensaje original
            logger.info(f"Enviando respuesta al canal {channel} como hilo al mensaje {thread_ts}")
            
            client.chat_postMessage(
                channel=channel,
                text=response_text,
                thread_ts=thread_ts
            )
        else:
            logger.error(f"Formato de respuesta incorrecto: {response_json}")
    except SlackApiError as e:
        print(f"Error: {e.response['error']}")

    return {"status": "ok"}
