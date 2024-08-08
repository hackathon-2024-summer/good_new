import os
from typing import Annotated
from fastapi import APIRouter, Depends, Request
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from sqlalchemy.ext.asyncio import AsyncSession
from db_session import get_db
import logging

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Slack"])

DbDependency = Annotated[AsyncSession, Depends(get_db)]

# Slackアプリの設定
slack_app = AsyncApp(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    # process_before_response=True,
    # request_verification_enabled=False,
    # ignoring_self_events_enabled=False  # self eventsの無視を無効にする
)
handler = AsyncSlackRequestHandler(slack_app)

# slack_appを定義した後でslack_eventsをインポートする
from slack_events import parrot_bot
from slack_events import show_modal_answer, handle_submit_answer

@router.post("/slack/events")
async def slack_events(req: Request):
    return await handler.handle(req)
