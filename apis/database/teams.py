from sqlalchemy import Column, String
from database.base import Base

class Team(Base):
    __tablename__ = "teams"  # テーブル名 __tablename__はsqlalchemyの特別な変数
    __table_args__ = {"extend_existing": True}  # 既存テーブルの再定義を認める。    
    
    team_id = Column(String(255), primary_key=True)
    access_token = Column(String(255), nullable=False)
    
