# ルートの.envの修正
- FastAPIのポート番号は80。ALBがそのように設定されている。
- MYSQL_HOSTをDockerコンテナ名からRDSインスタンスのエンドポイントに書き換える。
    MYSQL_HOST=aws-and-infra-rdsa.・・・
- MYSQL_PORTをRDSインスタンスに書き換える。3306はMySQLのデフォルト値
    PORT_MYSQL_FAST=・・・
- MYSQL_USERをCDFTKの.env　RDS_USERと一致させる。
- MYSQL_PASSWORDをCDFTKの.env　RRDS_PASSWORDと一致させる。

# バックエンドの.envは削除すること
- Dockerfileは自分のフォルダから上方に.envを探していき、該当する環境変数が最初に見つかれば採用する。つまり、バックエンドのMYSQL_HOSTがDockerコンテナのままなので、RDSに接続できない。(Slack Appの場合、関係なし)

# docker-compose.ymlの修正
- MySQLコンテナの箇所を消去

# docker_softclear.shの修正
- docker composeをdocker-composeに変更

# Slack Appのバックエンドではnginxを使わない。

RDSやphpMyAdminを公開するわけにはいかない。EC2インスタンスにSSMでリモート接続できるものだけがアクセスする。

ssmで接続しているlocalhostのVSCode→統合ターミナル→PORTSタブ→Foward a Portを押す→phpMyAdminコンテナのポート番号(例4081)を入力→ブラウザでlocalhost:4081にアクセスする


