from routers.slack import slack_app, logger

# users https://api.slack.com/methods/users.list

# Slack APIから全ユーザーを取得し、Botと削除済みユーザーを除外して返す
async def get_slack_users(token):
    data = await slack_app.client.users_list(token=token)

    # APIレスポンス全体を出力
    logger.debug(f"Slack API response: {data}")

    # レスポンスの中身をチェック
    if not data.get("ok"):
        logger.error(f"Slack API error: {data.get('error')}")
        return "Slack usersの取得に失敗しました"

    # ボットユーザーと削除済みユーザーを除外
    members = data.get("members", [])
    real_users = [
        user for user in members if not user.get("is_bot") and not (user.get("deleted"))
    ]

    return real_users