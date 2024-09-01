import random
import datetime
import jpholiday
from routers.slack import logger
from slack_apis.users import get_slack_users
from slack_apis.chat import slack_post_message
from repository.slack_oauth import installation_store


# タイムゾーンの設定
JST = datetime.timezone(datetime.timedelta(hours=9))

# get_slack_usersを利用して、ランダムに5人のユーザーを取得する
async def get_random_users(token):
    real_users = await get_slack_users(token)

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
async def send_question_to_user(token, user):
    # 送信日をカスタムフィールドとしてvalueに格納
    sent_date = str(datetime.datetime.now(JST).date())

    msg_block = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "こんにちは！ :wave:\n\nあなたの、24時間以内に起きた「よかったこと」や「新しい発見」を教えて下さい :star2: （回答期限：本日中）",
            },
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": "回答する"},
                "value": sent_date,
                "action_id": "click_button_answer",
            },
        }
    ]

    response_data = await slack_post_message(token=token, channel=user["id"], blocks=msg_block)
    
    # JSONレスポンスの取得とエラーチェック
    if not response_data.get("ok"):
        logger.error(f"Slack API error: {response_data.get('error')}")
        return "質問の送信に失敗しました"
    else:
        logger.info(f"{sent_date}：質問を{user['name']}に送信しました")


# Good and New Botから質問を送信する関数
async def question():

    # アプリをインストールしている全てのワークスペース情報を取得
    installations = await installation_store.async_find_all()

    for installation in installations:
        # 各インストールに対してボットトークンを取得
        token = installation.bot_token
        users = await get_random_users(token)
        if not users:
            logger.error("ユーザーが見つかりませんでした")
            return

        for user in users:
            await send_question_to_user(token, user)


