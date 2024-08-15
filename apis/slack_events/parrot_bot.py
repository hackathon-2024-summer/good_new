from routers.slack import slack_app, logger


# オウム返しBOT
# DMへのメッセージに対してはGood&Newを尋ねるように変更（テスト用）
@slack_app.event("message")
async def handle_message_events(body, say, logger):
    logger.debug(f"Received event: {body}")
    event = body["event"]
    channel_type = event.get("channel_type")
    logger.info(f"Message received in channel type: {channel_type}")
    
    if channel_type == "im":
        logger.info("Responding to DM")
        await say(
            blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "あなたのGood & Newな事を教えて下さい :eyes:"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text":"回答する"},
                    "value": "2024-08-14",
                    "action_id": "click_button_answer"
                }
            }
        ],
        text="あなたのGood & Newな事を教えて下さい :eyes:"
        )
    else:
        logger.info("Responding to channel message")
        await say(event["text"] + " ですぞえ")