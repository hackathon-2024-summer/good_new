import os
from typing import Annotated
from fastapi import APIRouter, status, Depends, Request
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from sqlalchemy.ext.asyncio import AsyncSession
from db_session import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Slack"])

DbDependency = Annotated[AsyncSession, Depends(get_db)]

# Slackアプリの設定
slack_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    # process_before_response=True,
    # request_verification_enabled=False,
    # ignoring_self_events_enabled=False  # self eventsの無視を無効にする
)
handler = SlackRequestHandler(slack_app)


# @slack_app.event("message")
# def handle_message_events(body, say):
#     message = body["event"]
#     say(message["text"]+" ですぞえ")

@slack_app.event("message")
def handle_message_events(body, say, logger):
    logger.debug(f"Received event: {body}")
    event = body["event"]
    channel_type = event.get("channel_type")
    logger.info(f"Message received in channel type: {channel_type}")
    
    if channel_type == "im":
        logger.info("Responding to DM")
        say(event["text"] + " だがや")
    else:
        logger.info("Responding to channel message")
        say(event["text"] + " ですぞえ")


@router.post("/slack/events")
async def slack_events(req: Request):
    return await handler.handle(req)
