from datetime import date
import jpholiday
from routers.slack import logger
from slack_apis.conversations import get_target_slack_channel
from utils.date import format_date_slash
from slack_apis.chat import slack_post_message
from utils.slack_oauth import installation_store
from repository.contents import Contents


async def delivery():
    today = date.today()
    weekday = today.weekday()  # 0(月曜日)から6(日曜日)が取得できる

    if weekday >= 5 or jpholiday.is_holiday(today):
        logger.warning("土日祝日のため、メッセージを送信しません")
        return

    # アプリをインストールしている全てのワークスペース情報を取得
    installations = await installation_store.async_find_all()

    for installation in installations:
        # 各インストールに対してBOTトークンとteam_idを取得
        token = installation.bot_token
        team_id = installation.team_id

        contents = await Contents.delivery(team_id)
        channel = await get_target_slack_channel(channel_name="雑談", token=token)
        channel_id = channel.get('id')

        if not len(contents):
            response_data = await slack_post_message(
                token=token, channel=channel_id, text="みなさんのGood & Newをお待ちしています！")
            if not response_data.get("ok"):
                logger.error(f"Slack API error: {response_data.get('error')}")
                return "メッセージの送信に失敗しました"
            
            else:
                logger.info("messageをPOSTしました")
                return

        
        for content in contents:
            user_id = content[2]
            msg_block = [
                {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<@{user_id}> さんから {format_date_slash(content[3])} のGood & Newが届きました :star2:"
                    }
                },
                {
                "type": "divider"
                },
                {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": content[1]
                    }
                }
            ]
            
            try:
                response = await slack_post_message(token=token, channel=channel_id, blocks=msg_block)
                logger.debug(f"GoodAndNewをポストしました {channel_id}: {response}")
            except Exception as e:
                logger.error(f"error {channel_id}: {e}")
        
        
        content_ids = [content[0] for content in contents]
        await Contents.updateDelivery(content_ids)
       

