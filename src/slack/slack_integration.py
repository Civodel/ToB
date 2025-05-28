import os

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


@slack_router.post("/slack/events")
async def handle_slack_event(req: Request):
    payload = await req.json()

    if "challenge" in payload:
        return {"challenge": payload["challenge"]}
    
    

    event = payload.get("event", {})
    BOT_ID = client.api_call("auth.test")["user_id"]

    if event['user'] == BOT_ID:
        return {"status": "ok"}

    if event.get("type") == "app_mention" or event.get("type") == "message":
        channel = event["channel"]
        user = event["user"]
        text = event["text"]

        conversation_object = Conversation(conversation_id=1, message=text)

        response_json = await handle_conversation_logic(conversation_object)


        try:
            client.chat_postMessage(channel=channel, text=response_json.get("response")[3].get("message"))
        except SlackApiError as e:
            print(f"Error: {e.response['error']}")

    return {"status": "ok"}
