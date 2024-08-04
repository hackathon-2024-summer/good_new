from datetime import date
import uuid
from sqlalchemy import Column, String, Date, Boolean
from database.base import Base

class Content(Base):
    __tablename__ = "contents"  # テーブル名 __tablename__はsqlalchemyの特別な変数
    __table_args__ = {"extend_existing": True}  # 既存テーブルの再定義を認める。
    
    # 新しいレコードが挿入される際に、lambdaで指定する関数の出力をデフォルト値として使う
    # id, content_date, is_deliveredは登録時にDB側でデフォルト値が入る
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    team_id = Column(String(255), nullable=False)
    user_id = Column(String(255), nullable=False)
    content_date = Column(Date, nullable=False, index=True, default=date.today())
    content = Column(String(255), nullable=False)
    is_delivered = Column(Boolean, nullable=False, default=False)
