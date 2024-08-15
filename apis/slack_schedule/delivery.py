from datetime import date
import jpholiday
from routers.slack import slack_app, logger
from slack_schedule.question import get_slack_users
from repository.contents import Contents

async def get_slack_channel():
    data = await slack_app.client.conversations_list()
    
    # APIレスポンス全体を出力
    logger.debug(f"Slack API response: {data}")

    # レスポンスの中身をチェック
    if not data.get("ok"):
        logger.error(f"Slack API error: {data.get('error')}")
        return "Slack channelsの取得に失敗しました"
    
    channels = data.get('channels',[])

    # 既に雑談チャンネルがある場合は雑談チャンネルを返す
    target_channel = None
    for channel in channels:
        if channel.get('name') == "雑談":
            target_channel = channel
            break
    
    if target_channel:
        return target_channel
    
    # 雑談チャンネルがない場合はチャンネルを作成する
    created_channel = await create_slack_channle()
    return created_channel


async def create_slack_channle():
    data = await slack_app.client.conversations_create(
        name="雑談",  # チャンネル名
        is_private=False  # パブリックチャンネルにする場合はFalse
    )

    # APIレスポンス全体を出力
    logger.debug(f"Slack API response: {data}")

    # レスポンスの中身をチェック
    if not data.get("ok"):
        logger.error(f"Slack API error: {data.get('error')}")
        return "Slack channelの作成に失敗しました"
    
    # userを作成したチャンネルに招待する
    users = await get_slack_users()
    user_ids = [user.get('id') for user in users]
 
    # 100名ずつしか追加できないようなので分割する
    list_size = 100
    user_list =  [user_ids[i:i + list_size] for i in range(0, len(user_ids), list_size)]

    # チャンネルIDを取得
    channel_id = data.get("channel").get("id")
    if not channel_id:
        logger.error("Slack channel IDの取得に失敗しました")
        return "Slack channel IDの取得に失敗しました"
    
    for user_id_list in user_list:
        data = await slack_app.client.conversations_invite(
            channel=channel_id,
            users=",".join(user_id_list)
        )

        # 招待のレスポンスをログに出力
        logger.debug(f"Invite API response: {data}")
        
        if not data.get("ok"):
            logger.error(f"Failed to invite users: {data.get('error')}")
            return f"ユーザーの招待に失敗しました: {data.get('error')}"
        
    logger.debug("channelの作成とユーザーの招待が完了しました")

    return data.get("channel")

async def delivery():
    today = date.today()
    weekday = today.weekday()  # 0(月曜日)から6(日曜日)が取得できる

    if weekday >= 5 or jpholiday.is_holiday(today):
        logger.warning("土日祝日のため、メッセージを送信しません")
        return


    contents = await Contents.delivery()
    channel = await get_slack_channel()
    channel_id = channel.get('id')

    if not len(contents):
        response_data = await slack_app.client.chat_postMessage(channel=channel_id, text="みなさんのGoodAndNewをお待ちしています！")
        if not response_data.get("ok"):
            logger.error(f"Slack API error: {response_data.get('error')}")
            return "メッセージの送信に失敗しました"
        
        else:
            logger.info("messageをPOSTしました")
            return

    
    for content in contents:
        user_id = content[2]
        message = f"<@{user_id}> さんの{format_date_slash(content[3])}のGoodAndNew！\n {content[1]}"
        
        try:
            response = await slack_app.client.chat_postMessage(
                channel=channel_id,  # 雑談チャンネルにメッセージを送る
                text=message
            )
            logger.debug(f"GoodAndNewをポストしました {channel_id}: {response}")
        except Exception as e:
            logger.error(f"error {channel_id}: {e}")
    
    
    content_ids = [content[0] for content in contents]
    await Contents.updateDelivery(content_ids)
       

def format_date_slash(date: date) -> str:
    formatted_date = date.strftime("%Y/%m/%d")
    
    return formatted_date