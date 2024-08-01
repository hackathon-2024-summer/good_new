1.slackでワークスペースを作る。

2.api.slack.comでtokenをFrom Scratchで取得。
Basic InformationタブにApp ID, Client ID, Client Secret, Signin Secretが明記されている。

3.OAuth & Permissionsで許容するアクションをtokenに紐付ける。紐付けたのは以下。

reactions:write

機能: 絵文字リアクションの追加・編集
用途: ユーザーの投稿に自動でリアクションを付けるなど


commands

機能: スラッシュコマンドの追加
用途: カスタムコマンドを作成し、ユーザーが簡単に機能を呼び出せるようにする


chat:write

機能: メッセージの送信
用途: ボットからユーザーや channel にメッセージを送信する


files:write

機能: ファイルのアップロード、編集、削除
用途: 自動的にファイルを共有したり、ユーザーのリクエストに応じてファイルを操作する


channels:read

機能: パブリックチャンネルの基本情報の閲覧
用途: チャンネルリストの取得や、特定のチャンネルの情報を確認する


im:history

機能: ダイレクトメッセージの履歴閲覧
用途: ユーザーとボットの1対1の会話履歴にアクセスする


app_mentions:read

機能: アプリへのメンションの閲覧
用途: アプリが呼び出された際のコンテキストを理解し、適切に応答する


users:read

機能: ワークスペース内のユーザー情報の閲覧
用途: ユーザーのプロフィール情報を取得し、パーソナライズされた応答を提供する

4.App HomeタブのYour App's Presense in SlackでBotのDisplay NameとDefault Nameを入力。半角のみで使える記号は限られる。不正文字を入力すると弾かれるが、全角は受け付けてしまい名無しで登録されてしまう。






# good_new
# good_new
