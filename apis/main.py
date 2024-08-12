from fastapi import FastAPI
from routers import slack, develop
import logging
# import requests
import os
import random
from contextlib import asynccontextmanager
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# import asyncio
import datetime
import jpholiday
import aiohttp


# from slack_events import show_modal_answer

# app = FastAPI()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")

# executors = {"default": ThreadPoolExecutor(20), "processpool": ProcessPoolExecutor(5)} # 非同期処理の時はThreadPoolExecutorを選択するとエラー
job_defaults = {"coalesce": False, "max_instances": 3, "misfire_grace_time": 3600}


@asynccontextmanager
async def lifespan(app: FastAPI):
    global scheduler
    # 非同期処理のためBackgroundSchedulerから変更
    scheduler = AsyncIOScheduler(job_defaults=job_defaults)
    scheduler.add_job(question, "cron", hour=16, minute=8)
    # scheduler.add_job(question, "interval", minutes=1)
    scheduler.start()
    logger.info("Scheduler started")

    yield

    if scheduler:
        scheduler.shutdown()
        logger.info("Scheduler shut down")


app = FastAPI(lifespan=lifespan)
app.include_router(slack.router)
app.include_router(develop.router)


# # 非同期関数実行のための動機関数
# def run_question_job():
#     asyncio.run(question())


# Slack APIから全ユーザーを取得し、Botと削除済みユーザーを除外して返す
# @app.get("/users")
async def get_slack_users():
    url = "https://slack.com/api/users.list"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                logger.error("Slack usersの取得に失敗しました")
                return []

            data = await response.json()

    # APIレスポンス全体を出力
    logger.debug(f"Slack API response: {data}")

    # レスポンスの中身をチェック
    if not data.get("ok"):
        logger.error(f"Slack API error: {data.get('error')}")
        return "Slack usersの取得に失敗しました"

    # ボットユーザーと削除済みユーザーを除外
    members = data.get("members", [])
    real_users = [
        user for user in members if not user.get("is_bot") and not (user.get("deleted"))
    ]

    return real_users


# get_slack_usersを利用して、ランダムに5人のユーザーを取得する
async def get_random_users():
    real_users = await get_slack_users()

    # 十分なユーザー情報が含まれているか確認
    if len(real_users) < 5:
        logger.warning(
            "設定したランダム抽出数に満たないため、ユーザー全員を対象とします"
        )
        return real_users

    # ランダムに5人を抽出
    random_users = random.sample(real_users, 5)

    return random_users


# Slack APIからユーザーに質問を送信する関数
async def send_question_to_user(user):
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    payload = {
        # channelの値としてユーザーIDを渡すと、そのユーザーのApp Homeチャンネルに投稿する
        "channel": user["id"],
        # Block Kit Builderで作ったものを貼り付け
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "こんにちは！ :wave:\n\nあなたの、24時間以内に起きた「よかったこと」や「新しい発見」を教えて下さい :star2:",
                },
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "回答する"},
                    "value": "click_me_123",
                    "action_id": "click_button_answer",
                },
            }
        ],
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            response_data = await response.json()

    # JSONレスポンスの取得とエラーチェック
    if not response_data.get("ok"):
        logger.error(f"Slack API error: {response_data.get('error')}")
        return "質問の送信に失敗しました"
    else:
        logger.info(f"質問を{user['name']}に送信しました")


# Good and New Botから質問を送信する関数
async def question():
    today = datetime.date.today()
    weekday = today.weekday()  # 0(月曜日)から6(日曜日)が取得できる

    # if weekday >= 5 or jpholiday.is_holiday(today):
    #     logger.warning("土日祝日のため、質問を送信しません")
    #     return

    users = await get_random_users()
    if not users:
        logger.error("ユーザーが見つかりませんでした")
        return

    for user in users:
        await send_question_to_user(user)


# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
