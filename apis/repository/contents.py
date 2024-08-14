from database.contents import Content
from db_session import get_db
from sqlalchemy import func, select, update

class Contents:
    @staticmethod
    async def delivery() -> list[tuple[str, str, str]]:
        async for db in get_db():
            try:
                subquery = (
                    select(
                        Content.user_id,
                        func.min(Content.id).label("id")  # 各ユーザーの最初のコンテンツIDを取得
                    )
                    .filter(Content.is_delivered == False)
                    .group_by(Content.user_id)
                    .subquery()
                )

                result = await db.execute(
                    select(
                        Content.id,
                        Content.content,
                        Content.user_id,
                        Content.content_date
                    )
                    .join(subquery, Content.id == subquery.c.id)
                    .order_by(func.rand())  # ランダムな順序で取得
                    .limit(3)  # 3件取得
                )

                contents = result.fetchall()
                return contents
            
            except Exception as e:
                print(f"Error: {e}")
                return []
            

    @staticmethod
    async def updateDelivery(content_ids):
        async for db in get_db():
            try:
                # コンテンツIDリストに含まれる全てのコンテンツのis_deliveredフラグをTrueに更新
                await db.execute(
                    update(Content)
                    .where(Content.id.in_(content_ids))
                    .values(is_delivered=True)
                )
                await db.commit()  # 変更をコミット
            except Exception as e:
                await db.rollback()  # エラー発生時にはロールバック
                print(f"Error: {e}")
