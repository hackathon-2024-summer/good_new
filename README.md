# ngrokでlocalhostのバックエンドを公開し、Slack Appと連携させる

## Slack App

Slack AppとはSlack ワークスペースで実行するアプリケーションをbotと呼び、そのbotが検知するイベントとアクションを許可するもの。
公開されたhttps URLでバックエンドと接続するため、ローカル開発でのSlackワークスペースと本番環境でのSlackワークスペースを分離しなければならない。
開発中のSlack Appバックエンドの動作を確認するには本番環境にデプロイせざるを得ず、誰かが動作確認していると他のメンバーは待つしかない。

## バックエンドを公開するngrok

1. nginxと似たサーバーで、https付きで公開する機能を持っている。
2. 以下サイトにアクセスし、アカウントを作る。
   <https://ngrok.com/>
3. Your Authtokenのページで与えられたトークンをコピーし、.envのNGROK_AUTH_TOKENで指定する。
4. docker-compose.ymlにてngrokとfastapiを接続する。
5. docker compose -f "docker-compose.yml" up -d --build でngrokコンテナとfastapiコンテナを起動する。
6. ローカルのWebブラウザで <http://localhost:4040/inspect/http> にアクセスする。
7. 表示されたURLにアクセスするとバックエンドが公開される。
   No requests to display yet
   To get started, make a request to one of your tunnel URLs
   <https://hoge-222-229-40-231.ngrok-free.app>
8. このアドレスをSlack Appで使う。

## Slack Appの設定

自分のローカル環境で開発するためにSlackのワークスペースを作成しておく。
<https://www.pci-sol.com/business/service/product/blog/lets-make-slack-app/> を参考に設定する。

1. Slackのワークスペースを開き、左サイドバーから「アプリを追加する」を選択
2. 右上の「Appディレクトリ」を押下
3. 右上の「ビルド」を押下
4. 右上の「Your App」を押下
5. 「Create an App」を押下
6. 「From scratch」を選択
7. App Nameにアプリ名、「Pick a workspace to develop your app in:」でアプリを導入したいワークスペース名を選択する
8. 開いた画面にある「Bots」を押下
9. 「Review Scopes to Add」を押下
10. 以下のScopeを追加
    - channels:history
    - chat:write
    - groups:history
    - im:history
    - im:read
    - im:write
11. 左サイドバーから「App Home」を選択
12. 「App Display Name」で「Edit」を押下
13. 「Display Name(Bot Name)」にボット名、「Default username」に適当なユーザ名を入力し、「Add」を押下
14. 「Show Tabs」にある「Messages Tab」をオンにし、「Allow users to send Slash commands and messages from the messages tab」のチェックボックスをオンにする
15. 左サイドバーから「Install App」を選択し、「Install to Workspace」を押下
16. 「許可する」を押下
17. 左サイドバーから「OAuth & Permissions」を選択し、「Bot User OAuth Token」をコピーし、メモしておく
18. 左サイドバーから「Basic Information」を選択し、「Signing Secret」項目の「Show」を押下し表示させたのち、内容をコピーし、メモしておく
19. .envのSLACK_BOT_TOKENに17、SLACK_SIGNING_SECRETに18のトークンを設定する。
20. 左サイドバーから「Event Subscriptions」を選択
21. Enable Events」を「On」にし、「Request URL」にngrokで公開したバックエンドのURL(イベントハンドラを指す)を指定
    <https://hoge-222-229-40-231.ngrok-free.app/slack/events>
22. 下部の「Subscribe to bot events」タブ内で以下3つのイベントを追加
    - message.channels
    - message.groups
    - message.im
23. 上部に黄色で以下のメッセージが表示されるので、メッセージ内の「reinstall your app」を押下
24. 「許可する」を押下
25. Botを招待したいチャンネル名をクリック
26. 「インテグレーション」タブから「アプリを追加する」を押下
27. 作成したアプリの「追加」を押下
28. 追加したチャンネル内でメッセージやDMを投稿すると、アプリがオウム返ししてくれることを確認
