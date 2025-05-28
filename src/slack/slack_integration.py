import os
import logging

from dotenv import load_dotenv
from fastapi import Request, APIRouter
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from src.eva.conversation_validation import handle_conversation_logic
from src.models.conversation import Conversation

load_dotenv()
slack_router = APIRouter()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

client = WebClient(token=SLACK_BOT_TOKEN)

BOT_ID = None
try:
    BOT_ID = client.api_call("auth.test")["user_id"]
    logging.info(f"Bot inicializado con ID: {BOT_ID}")
except Exception as e:
    logging.error(f"Error al obtener BOT_ID: {e}")


@slack_router.post("/slack/events")
async def handle_slack_event(req: Request):
    payload = await req.json()

    if "challenge" in payload:
        return {"challenge": payload["challenge"]}
    
    if "event" not in payload:
        return {"status": "ok"}
    
    event = payload.get("event", {})
    
    if "user" not in event:
        return {"status": "ok"}
    
    if event['user'] == BOT_ID:
        logging.info(f"Ignorando mensaje del propio bot: {event}")
        return {"status": "ok"}
    
    logging.info(f"Procesando mensaje de usuario: {event['user']}")
    
    if (event.get("type") == "app_mention" or 
        (event.get("type") == "message" and not event.get("thread_ts")) or
        (event.get("type") == "message" and event.get("thread_ts") and BOT_ID in event.get("text", ""))):
        channel = event["channel"]
        user = event["user"]
        text = event["text"]
        
        conversation_object = Conversation(conversation_id=channel, message=text)
        
        response_json = await handle_conversation_logic(conversation_object, user_id=user)
        
        if response_json and "response" in response_json and len(response_json.get("response", [])) > 3:
            try:
                response_text = response_json.get("response")[3].get("message", "No hay respuesta disponible")
                
                thread_ts = event.get("ts")
                
                client.chat_postMessage(
                    channel=channel, 
                    text=response_text,
                    thread_ts=thread_ts
                )
                
                logging.info(f"Mensaje enviado como hilo en el canal {channel}")
            except SlackApiError as e:
                logging.error(f"Error al enviar mensaje a Slack: {e.response['error']}")
        else:
            logging.warning(f"Formato de respuesta incorrecto: {response_json}")
            try:
                thread_ts = event.get("ts")
                
                client.chat_postMessage(
                    channel=channel, 
                    text="Lo siento, ocurrió un error al procesar tu mensaje.",
                    thread_ts=thread_ts
                )
            except SlackApiError as e:
                logging.error(f"Error al enviar mensaje de error a Slack: {e.response['error']}")
    
    return {"status": "ok"}
