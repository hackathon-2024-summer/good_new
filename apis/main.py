from fastapi import FastAPI
from routers import slack, develop
import logging
import requests
import os
import random

app = FastAPI()

app.include_router(slack.router)
app.include_router(develop.router)

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")


# feature/001 ユーザー一覧を取得するAPI
@app.get("/users")
def get_slack_users():
    url = "https://slack.com/api/users.list"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return "Slack usersの取得に失敗しました"

    data = response.json()

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

    # 十分なユーザー情報が含まれているか確認
    if len(real_users) < 5:
        logger.warning(
            "設定したランダム抽出数に満たないため、ユーザー全員を対象とします"
        )
        return real_users

    # ランダムに5人抽出
    users = random.sample(real_users, 5)
    logger.debug(f"ランダム5人抽出: {users}")

    return users


# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
