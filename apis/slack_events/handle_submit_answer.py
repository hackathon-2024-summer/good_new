from routers.slack import slack_app
from repository.contents import Contents


# 送信された回答をDBに保存
@slack_app.view("modal_answer")
async def handle_submit_answer(ack, body, client, view, logger):
    team_id = body["team"]["id"]
    user_id = body["user"]["id"]
    content = view["state"]["values"]["input_1"]["input_content"]["value"]
    logger.info(f"accept team_id: {team_id}, user_id: {user_id}, content: {content}")

    # 入力値を検証
    errors = {}
    if content is None:
        errors["input_1"] = "この項目は必須です"
    if len(errors) > 0:
        await ack(response_action="errors", errors=errors)
        return
    
    # リクエストの確認を行い、モーダルを閉じる
    await ack()
    
    # ユーザーに送信するメッセージ
    msg = ""

    # データを保存
    try:
        await Contents.add(team_id = team_id, user_id = user_id, content = content)
        logger.info(f"Successfully saved to database: {content}")
        msg = "回答を受け付けました :tada: ありがとうございます！"

    except Exception as e:
        logger.exception(f"Failed to save a answer {e}") 
        msg = "回答の保存に失敗しました :cry:"

    # ユーザーにメッセージを送信
    try:
        # slack側からのイベント処理をする時は、slackAPIを直接使用する（イベントが発生したBOTの情報が必要なため）
        await client.chat_postMessage(channel=user_id, text=msg)

    except Exception as e:
        logger.exception(f"Failed to post a message {e}") 

