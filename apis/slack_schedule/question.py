import random
import datetime
import jpholiday
from routers.slack import slack_app, logger


# Slack APIから全ユーザーを取得し、Botと削除済みユーザーを除外して返す
async def get_slack_users():
    data = await slack_app.client.users_list()

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
async def send_question_to_user(user, sent_messages):
    msg_block = [
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
    ]

    response_data = await slack_app.client.chat_postMessage(
        channel=user["id"], blocks=msg_block
    )

    # JSONレスポンスの取得とエラーチェック
    if not response_data.get("ok"):
        logger.error(f"Slack API error: {response_data.get('error')}")
        return "質問の送信に失敗しました"
    else:
        logger.info(f"質問を{user['name']}に送信しました")
        # JSONレスポンスから、質問送信先チャンネルとタイムスタンプを取得
        return response_data.get("channel"), response_data.get("ts")


# Good and New Botから質問を送信する関数
async def question(sent_messages):
    today = datetime.date.today()
    weekday = today.weekday()  # 0(月曜日)から6(日曜日)が取得できる

    if weekday >= 5 or jpholiday.is_holiday(today):
        logger.warning("土日祝日のため、質問を送信しません")
        return

    users = await get_random_users()
    if not users:
        logger.error("ユーザーが見つかりませんでした")
        return

    for user in users:
        channel_id, timestamp = await send_question_to_user(user, sent_messages)
        if channel_id and timestamp:
            # [sent_messages]辞書のkeyとして、SlackのユーザーIDを保存
            sent_messages[user["id"]] = {
                # [sent_messages]辞書のvalueとして、channel_idとtimestampを保存
                "channel_id": channel_id,
                "timestamp": timestamp,
            }
