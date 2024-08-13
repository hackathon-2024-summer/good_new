import os
from fastapi import APIRouter, Request
from slack_bolt.async_app import AsyncApp
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
import logging

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Slack"])

# OAuth設定
oauth_settings = OAuthSettings(
    client_id=os.environ.get("SLACK_CLIENT_ID"),
    client_secret=os.environ.get("SLACK_CLIENT_SECRET"),

    scopes=["channels:read", "channels:manage", "groups:read", "users:read", "chat:write"],
    installation_store={ 
        "store": lambda installation: store_installation(installation),
        "fetch": lambda query: fetch_installation(query),
        # "store_org_installation": lambda installation: store_org_installation(installation),
        # "fetch_org_installation": lambda query: fetch_org_installation(query),
    },
)

# Bolt for PythonのApp初期化
slack_app = AsyncApp(
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    oauth_settings=oauth_settings
)


# # Slackアプリの設定
# slack_app = AsyncApp(
#     token=os.environ.get("SLACK_BOT_TOKEN"),
#     signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
#     # process_before_response=True,
#     # request_verification_enabled=False,
#     # ignoring_self_events_enabled=False  # self eventsの無視を無効にする
# )

handler = AsyncSlackRequestHandler(slack_app)

# slack_appを定義した後でslack_eventsをインポートする
from slack_events import parrot_bot
from slack_events import show_modal_answer, handle_submit_answer

@router.post("/slack/events")
async def slack_events(req: Request):
    return await handler.handle(req)
