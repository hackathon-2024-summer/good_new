from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from apis.database.contents import Content
import os

# 接続情報
host = os.getenv("MYSQL_HOST_FAST")
port = int(os.getenv("PORT_MYSQL_FAST"))
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
db = os.getenv("MYSQL_DB_FAST")

# SQLAlchemyエンジンを作成
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")
print(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")

# セッションを作成
SessionLocal = Session(engine)

# データを挿入する関数
def insert_data():
    # データのインスタンスを作成
    contents_data1 = [
        Content(team_id='T07EBDGAKY6', user_id='U07EQ3NDUM3', content_date='2024-08-08', content='ミスドの新作っぽいドーナツが美味しかった :doughnut: '),
        Content(team_id='T07EBDGAKY6', user_id='U07EQ3NDUH6', content_date='2024-08-06', content='晴れていて、洗濯物がよく乾きました！ :sunny:'),
        Content(team_id='T07EBDGAKY6', user_id='U07EQ5KDUY2', content_date='2024-08-10', content='話題のうまとまハンバーグを食べました！'),
    ]

    contents_data2 = [
        Content(team_id='T07EBDGAKY6', user_id='U07EQ5KDUT1', content='保険の見直しのついでに外食しました！'),
        Content(team_id='T07EBDGAKY6', user_id='U07EQ5KDUS4', content='布団を干しました！'),
        Content(team_id='T07EBDGAKY6', user_id='U07EQ3NDUM3', content='久しぶりに地元の友達とおしゃべりしました :raised_hands: '),
        Content(team_id='T07EBDGAKY6', user_id='U07EQ5KDUD8', content='久しぶりに息子と食事に行きました！'),
        Content(team_id='T07EBDGAKY6', user_id='U07EQ5KDUS4', content='実家で飼っている犬のドライブご満悦写真が送られてきました。かわいい :dog2: '),
        Content(team_id='T07EBDGAKY6', user_id='U07EQ5KDUY2', content='東京都から価格高騰給付金（paypay)が10万円分来てました:crying_cat_face:'),
        Content(team_id='T07EBDGAKY6', user_id='U07EQ3NDUU5', content='朝寝坊してよく眠りました :sleeping: '),
        Content(team_id='T07EBDGAKY6', user_id='U07EQ5KDUT1', content='壊れていたエアコンが直りました！'),
        Content(team_id='T07EBDGAKY6', user_id='U07EQ5KDUT1', content='東京のオフ会に参加しました！'),
        Content(team_id='T07EBDGAKY6', user_id='U07EQ5KDUJ7', content='明日は土曜日。久々にたくさん睡眠時間が取れる…！！'),
        Content(team_id='T07EBDGAKY6', user_id='U07EQ3NDUM3', content='買ったピーマンが一部茶色がかってたので大丈夫かなと思って検索したら、熟している途中なので問題ないらしいです。初めて知りました :bell_pepper'),
        Content(team_id='T07EBDGAKY6', user_id='U07EQ5KDUS4', content='懐かしくてつい買った甘露飴がおいしい :candy: '),
    ]

    # トランザクション処理
    try:
        # データベースに追加
        for content in contents_data1 + contents_data2:
            SessionLocal.add(content)
        
        # コミットして変更を反映
        SessionLocal.commit()
        print("データが挿入されました。")
    
    except Exception as e:
        # 何らかのエラーが発生した場合、ロールバック
        SessionLocal.rollback()
        print(f"エラーが発生しました: {e}")
    
    finally:
        # セッションを閉じる
        SessionLocal.close()

# データを挿入
insert_data()
