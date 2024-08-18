from routers.slack import slack_app, logger
from slack_apis.users import get_slack_users

# conversations https://api.slack.com/apis/conversations-api

async def get_target_slack_channel(channel_name: str, token: str):
    data = await slack_app.client.conversations_list(token=token)
    
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
        if channel.get('name') == channel_name:
            target_channel = channel
            break
    
    if target_channel:
        return target_channel
    
    # 雑談チャンネルがない場合はチャンネルを作成する
    created_channel = await create_slack_channle(channel_name="雑談", is_private=False, token=token)
    return created_channel

async def create_slack_channle(channel_name: str, is_private: bool, token: str):
    data = await slack_app.client.conversations_create(
        token=token,
        name=channel_name,  # チャンネル名
        is_private=is_private  # パブリックチャンネルにする場合はFalse
    )

    # APIレスポンス全体を出力
    logger.debug(f"Slack API response: {data}")

    # レスポンスの中身をチェック
    if not data.get("ok"):
        logger.error(f"Slack API error: {data.get('error')}")
        return "Slack channelの作成に失敗しました"
    
    # userを作成したチャンネルに招待する
    users = await get_slack_users(token)
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
            token=token,
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