from sqlalchemy import Column, String, DateTime, Boolean, func
from database.base import Base
import uuid


# emailの重複を禁止し、uuidでtokenを作る。emailで作るとcookie解析でバレる。
class User(Base):
    __tablename__ = "users"  # テーブル名 __tablename__はsqlalchemyの特別な変数
    __table_args__ = {"extend_existing": True}  # 既存テーブルの再定義を認める。
    # 新しいレコードが挿入される際に、lambdaで指定する関数の出力をデフォルト値として使う
    id = Column(
        String(36),
        nullable=False,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    email = Column(String(256), nullable=False, unique=True, index=True)
    password = Column(String(256), nullable=False)
    username = Column(String(15), nullable=False, index=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    is_active = Column(Boolean, nullable=False, default=True)

    # printで表示するための関数
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username}, password={self.password}, created_at={self.created_at}, updated_at={self.updated_at}, is_active={self.is_active})>"

    def __str__(self):
        return f"User(id={self.id}, email={self.email}, username={self.username}, password={self.password}, created_at={self.created_at}, updated_at={self.updated_at}, is_active={self.is_active})"
