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

BOT_ID = None
try:
    bot_info = client.api_call("auth.test")
    BOT_ID = bot_info["user_id"]
    print(f"Bot inicializado con ID: {BOT_ID}")
except Exception as e:
    print(f"Error al obtener BOT_ID: {e}")
    
processed_events = {}


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
        
    event_id = payload.get("event_id") or payload.get("event_time") or time.time()
    event_ts = event.get("ts", "")
    unique_id = f"{event_id}-{event_ts}"
    
    if unique_id in processed_events:
        print(f"Evento ya procesado: {unique_id}")
        return {"status": "ok"}
    else:
        processed_events[unique_id] = True
        if len(processed_events) > 1000:
            processed_events.clear()
    
    if event['user'] == BOT_ID:
        return {"status": "ok"}
    

    if event.get("type") == "app_mention" or event.get("type") == "message":
        channel = event["channel"]
        user = event["user"]
        text = event["text"]
        
        
        conversation_object = Conversation(conversation_id=1, message=text)
        
        response_json = await handle_conversation_logic(conversation_object, user_id=user)



        try:
            thread_ts = event.get("ts")
            
            placeholder_response = client.chat_postMessage(
                channel=channel,
                text=":thinking_face: Estoy pensando....",
                thread_ts=thread_ts
            )

            
            try:
                reaction_response = client.reactions_add(
                    channel=channel,
                    timestamp=thread_ts,
                    name="thinking_face"
                )
                print(f"Reacción añadida correctamente: {reaction_response}")
            except SlackApiError as e:
                print(f"Error al añadir reacción: {e.response['error']}")
                
            time.sleep(3)
            
            response_text = response_json.get("response")[3].get("message")
            
            client.chat_update(
                channel=channel,
                ts=placeholder_response["ts"],  
                text=response_text
            )
            
            try:
                client.reactions_remove(
                    channel=channel,
                    timestamp=thread_ts,
                    name="thinking_face"
                )
                print("Reacción eliminada correctamente")
            except SlackApiError as e:
                print(f"Error al eliminar reacción: {e.response['error']}")
                
        except SlackApiError as e:
            print(f"Error: {e.response['error']}")

    return {"status": "ok"}
