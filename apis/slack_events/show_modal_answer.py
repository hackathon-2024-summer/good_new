import datetime
from routers.slack import slack_app, logger

# タイムゾーンの設定
JST = datetime.timezone(datetime.timedelta(hours=9))

# 回答モーダルの表示
@slack_app.action("click_button_answer")
async def show_modal_answer(ack, body, client):
    # アクションを確認したことを即時で応答
    await ack()

    today = datetime.datetime.now(JST).date()

    # 質問の送信日を取得
    value = body["actions"][0]["value"]
    sent_date = datetime.datetime.strptime(value, '%Y-%m-%d').date()

    # 質問の送信日が今日であれば、回答用のモーダルを作成
    if sent_date == today:
        modal_view = {
            "type": "modal",
            # ビューの識別子
            "callback_id": "modal_answer",
            "submit": {
                "type": "plain_text",
                "text": "送信",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "キャンセル",
                "emoji": True
            },
            "title": {
                "type": "plain_text",
                "text": "Good & New",
                "emoji": True
            },
            "blocks": [
                    {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "こんにちは！ :wave:\n\nあなたの、24時間以内に起きた「よかったこと」や「新しい発見」を教えて下さい :star2: ",
                        "emoji": True
                        }
                    },
                    {
                    "type": "input",
                    "block_id": "input_1",
                    "label": {
                        "type": "plain_text",
                        "text": "Your Good & New",
                        "emoji": True
                        },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "input_content",
                        "multiline": True
                        }
                    }
                ]
            }
        logger.info(f"質問日{value}：回答用のモーダルを作成")
    # 質問の送信日が今日でなければ、回答締め切りのモーダルを作成
    else:
        modal_view = {
            "type": "modal",
            # ビューの識別子
            "callback_id": "modal_expired",
            "close": {
                "type": "plain_text",
                "text": "戻る",
                "emoji": True
            },
            "title": {
                "type": "plain_text",
                "text": "Good & New",
                "emoji": True
            },
            "blocks": [
                    {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "この質問の回答受付は終了しました :wave:\n（回答期限：質問された当日中）\n\nまたの機会にお願いします！ :star2:",
                        "emoji": True
                        }
                    }
                ]
            }
        logger.info(f"質問日{value}：回答締め切りのモーダルを作成")

    # モーダルを表示
    response = await client.views_open(
        trigger_id=body["trigger_id"],
        view=modal_view
    )
    logger.info(f"質問日{value}：モーダルを送信しました")

    return response
