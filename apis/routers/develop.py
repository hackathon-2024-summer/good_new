# developは、DB接続等の動作確認のためのエンドポイントをまとめています（本番環境では不要です）

from typing import Annotated
from fastapi import APIRouter, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db_session import get_db
from schemas.develop import AddContentRequest, ContentResponse
from database.contents import Content

router = APIRouter(tags=["Develop"])

DbDependency = Annotated[AsyncSession, Depends(get_db)]


@router.get("/")
def read_root():
    return {"Hello": "Slack App Backend!"}

# contentsを登録する
@router.post(
    "/develop/contents", response_model=ContentResponse, status_code=status.HTTP_201_CREATED
    )
async def add_content(db: DbDependency, request: AddContentRequest):
    # データ作成（id, content_date, is_deliveredは登録時にDB側でデフォルト値が入る）
    new_content = Content(
        team_id = request.team_id,
        user_id = request.user_id,
        content = request.content,
    )
    # DBへ追加
    db.add(new_content)
    await db.commit()
    # DBデータでリフレッシュ（DB側で設定されたid, content_date, is_deliveredも取得）
    await db.refresh(new_content)
    # response_modelでバリデーションしてreturn
    return ContentResponse.model_validate(new_content)


# 特定のteam_idを持つcontentsの一覧を取得する
@router.get(
    "/develop/contents/team/{team_id}", response_model=list[ContentResponse], status_code=status.HTTP_200_OK
    )
async def get_contents(db: DbDependency, team_id):
    # select()内の項目が複数の場合はdb.execute…を使う。
    # （scalarsは最初の項目しか取得できないため）
    result = await db.scalars(select(Content).filter(Content.team_id == team_id))
    contents = result.all()

    return contents
