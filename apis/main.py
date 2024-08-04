import os
from fastapi import FastAPI, Request, Response
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from contextlib import asynccontextmanager
from slack_sdk.signature import SignatureVerifier
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# スケジューラの設定
scheduler = None

# Slack clientの初期化
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

slack_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    # process_before_response=True,
    # request_verification_enabled=False,
    # ignoring_self_events_enabled=False  # self eventsの無視を無効にする
)
handler = SlackRequestHandler(slack_app)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_task, trigger=IntervalTrigger(minutes=60))
    scheduler.start()
    logger.info("Scheduler started")

    yield

    if scheduler:
        scheduler.shutdown()
        logger.info("Scheduler shut down")


app = FastAPI(lifespan=lifespan)


# チャンネルにメッセージに送信する関数
def send_message_to_channel(channel_id: str, message: str):
    try:
        response = client.chat_postMessage(channel=channel_id, text=message)
        logger.info(f"Message sent: {response['ts']}")
    except SlackApiError as e:
        logger.error(f"Error sending message: {e}")


def send_dm_to_user(user_id: str, message: str):
    try:
        response = client.chat_postMessage(channel=user_id, text=message)
        logger.info(f"DM sent: {response['ts']}")
    except SlackApiError as e:
        logger.error(f"Error sending DM: {e}")


# スケジュールされたタスク
def scheduled_task():
    # チャンネルにメッセージを送信
    send_message_to_channel("C07EFMQBMB6", "定期的なチャンネルメッセージですぞえ")

    # 特定のユーザーにDMを送信
    send_dm_to_user("U07E21NGPA7", "定期的なDMだがや")

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

@app.post("/slack/events")
async def slack_events(req: Request):
    return await handler.handle(req)

@app.get("/")
def read_root():
    return {"Hello": "Scheduled Slack Bot World"}

