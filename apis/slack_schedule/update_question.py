from routers.slack import slack_app, logger


# 14:00のchat_postMessageからchannel,tsを取得-->blocksを上書き処理
async def update_question_to_user(sent_messages):
    update_msg_block = [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "本日の回答を締め切りました:sleeping: ",
            },
        }
    ]

    # [sent_messages]辞書から、chat_updateメソッドに渡すchannel_idとtimestampを取り出す
    for user_id, msg_info in sent_messages.items():
        try:
            await slack_app.client.chat_update(
                channel=msg_info["channel_id"],
                ts=msg_info["timestamp"],
                blocks=update_msg_block,
            )
            logger.info(f"質問の回答を締め切りました")
        except Exception as e:
            logger.error(f"質問を締め切ることができませんでした：{e}")

    sent_messages.clear()
