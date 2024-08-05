import os
from typing import Annotated
from fastapi import APIRouter, Depends, Request
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

# slack_appを定義した後でslack_eventsをインポートする
from slack_events import parrot_bot

@router.post("/slack/events")
async def slack_events(req: Request):
    return await handler.handle(req)
