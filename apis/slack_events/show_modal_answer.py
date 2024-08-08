from routers.slack import slack_app, logger


# 回答モーダルの表示
@slack_app.action("click_button_answer")
async def show_modal_answer(ack, body, client):
    # アクションを確認したことを即時で応答
    await ack()
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
                    "text": ":wave: こんにちは！\n\nあなたの、24時間以内に起きた「よかったこと」や「新しい発見」を教えて下さい :star2: ",
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
    # モーダルを表示
    response = await client.views_open(
        trigger_id=body["trigger_id"],
        view=modal_view
    )
    
    return response
