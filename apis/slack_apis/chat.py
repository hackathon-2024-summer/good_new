from routers.slack import slack_app, logger

# post message https://api.slack.com/methods/chat.postMessage

async def slack_post_message(
        token: str = None,
        channel: str = None,
        text: str = None,
        blocks: list = None
):
    response_data = await slack_app.client.chat_postMessage(
        token=token, channel=channel, text=text, blocks=blocks
        )
    return response_data