import os
from fastapi import APIRouter, Request
from slack_bolt.async_app import AsyncApp
from slack_bolt.oauth.async_oauth_settings import AsyncOAuthSettings
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
import logging

from repository.slack_oauth import installation_store, oauth_state_store

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Slack"])


client_id, client_secret, signing_secret = (
    os.environ["SLACK_CLIENT_ID"],
    os.environ["SLACK_CLIENT_SECRET"],
    os.environ["SLACK_SIGNING_SECRET"],
)

# Slackアプリの設定（OAuth対応）
slack_app = AsyncApp(
    logger=logger,
    signing_secret=signing_secret,
    installation_store=installation_store,
    oauth_settings=AsyncOAuthSettings(
        client_id=client_id, client_secret=client_secret, state_store=oauth_state_store,
    ),
)

handler = AsyncSlackRequestHandler(slack_app)

# slack_appを定義した後でslack_eventsをインポートする
from slack_events import parrot_bot
from slack_events import show_modal_answer, handle_submit_answer

@router.post("/slack/events")
async def slack_events(req: Request):
    return await handler.handle(req)

@router.get("/slack/install")
async def install(req: Request):
    return await handler.handle(req)

@router.get("/slack/oauth_redirect")
async def oauth_redirect(req: Request):
    return await handler.handle(req)
