#!/bin/bash
source ./.env

while :; do
    echo "Checking if MySQL is up on port ${PORT_MYSQL_FAST}"
    python create_db.py
    if [ $? -eq 0 ]; then
        break
    else
        echo "MySQL is not up. Sleep for 5 seconds then check again."
        sleep 5
    fi
done
sleep 5

# 開発段階でalembicの履歴を残す意義は薄いので、dockerコンテナを立ち上げる度に消去する。
# migrationファイルでデータベースの構成を更新・復旧させることを確約しながら進めるのが理想だが、非常に手間がかかる。
# 特にデータベースにデータが残った状態で更新させようとすると、周到にmigrationファイルを作る必要があるため
# dockerコンテナの運用となじまない。

if [ -d "./apis/alembic" ]; then
    rm -rf ./apis/alembic
    rm ./apis/alembic.ini
fi

# FastAPIのソースファイルができるフォルダに移動
cd apis
# alembic.iniを新規作成
# alembicはPythonのマイグレーションツールでデータベースのconfigを更新・復旧するためのライブラリ。
# sqlalchemyと併用される。sqlalchemyはPythonのORMでクラスとデータベース操作を繋げる。
alembic init alembic
# データベース接続URLを環境変数から生成
DATABASE_URL="mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@${MYSQL_HOST_FAST}:${PORT_MYSQL_FAST}/${MYSQL_DB_FAST}"

# 生成されたalembic.iniをsedコマンドで編集。sqlalchemyが参照するpathを追記。
# docker-compose.ymlのVOLUMESでコンテナ内外が繋がるので、ローカルにできたalembic.iniに接続URLが残るので、間違ってアップロードしないこと。
sed -i "s|sqlalchemy.url = .*|sqlalchemy.url = ${DATABASE_URL}|" /home/appuser/back/alembic.ini

# env.pyの初期ファイルはsqlalchemyが参照するBaseクラスのpathが明記されている。それをapisフォルダにコピー。
# Baseクラスがあるフォルダに__init__.pyを置くこと。Baseクラスを継承したクラスを全てデータベースに構築するため。
cp ../env.py ./alembic/env.py

# migration
alembic revision --autogenerate -m "migration by build.sh"
alembic upgrade head
chown -R appuser:appgroup alembic
chown appuser:appgroup alembic.ini

# コンテナ新規起動時にデータを挿入したい場合、insert_db.pyを作ってここで実行。
# 接続URL・SQL文・接続インスタンスを作り、execute(text(sql文))を実行する。
python ../insert_db.py

uvicorn main:app --reload --host 0.0.0.0 --port ${PORT_FAST} --log-level info
#--log-levelはproductionでは不要

# tail -f /dev/null