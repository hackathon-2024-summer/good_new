# developは、DB接続等の動作確認のためのエンドポイントをまとめています（本番環境では不要です）

from datetime import date
from pydantic import BaseModel, Field, ConfigDict


class AddContentRequest(BaseModel):
    team_id: str = Field(examples=["ABCDE1"])
    user_id: str = Field(examples=["FGHIJ1"])
    content: str = Field(examples=["虹がきれいに見えました！"])


class ContentResponse(BaseModel):
    id: str = Field(examples=["KLMNO123"])
    team_id: str = Field(examples=["ABCDE1"])
    user_id: str = Field(examples=["FGHIJ1"])
    content_date: date = Field(examples=["2024-08-04"])
    content: str = Field(examples=["虹がきれいに見えました！"])
    is_delivered: bool = Field(examples=[False])

    model_config = ConfigDict(from_attributes=True)


