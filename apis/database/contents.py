from datetime import date
from sqlalchemy import Column, String, Date, Boolean
from database.base import Base

class Content(Base):
    __tablename__ = "contents"  # テーブル名 __tablename__はsqlalchemyの特別な変数
    __table_args__ = {"extend_existing": True}  # 既存テーブルの再定義を認める。

    id = Column(String(36), primary_key=True)
    team_id = Column(String(255), nullable=False)
    user_id = Column(String(255), nullable=False)
    content_date = Column(Date, nullable=False, index=True, default=date.today())
    content = Column(String(255), nullable=False)
    is_delivered = Column(Boolean, nullable=False, default=False)
