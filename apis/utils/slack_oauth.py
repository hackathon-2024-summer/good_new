import logging
import os
import time
from datetime import datetime
from logging import Logger
from typing import Optional
from uuid import uuid4

from sqlalchemy import and_, desc, Table, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from slack_sdk.oauth.installation_store import Bot, Installation
from slack_sdk.oauth.installation_store.async_installation_store import (
    AsyncInstallationStore,
)
from slack_sdk.oauth.state_store.async_state_store import AsyncOAuthStateStore
from slack_sdk.oauth.installation_store.sqlalchemy import SQLAlchemyInstallationStore
from slack_sdk.oauth.state_store.sqlalchemy import SQLAlchemyOAuthStateStore

from db_session import ASYNC_DB_URL

# https://github.com/slackapi/bolt-python/blob/v1.1.1/examples/sqlalchemy/async_oauth_app.py
# 上記コードより、DB接続の非同期対応をdatabases→AsyncSessionへ変更

class AsyncSQLAlchemyInstallationStore(AsyncInstallationStore):
    client_id: str
    engine: any
    session_factory: any
    metadata: MetaData
    installations: Table
    bots: Table

    def __init__(
        self,
        client_id: str,
        database_url: str,
        logger: Logger = logging.getLogger(__name__),
    ):
        self.client_id = client_id
        self.engine = create_async_engine(database_url, echo=True)
        self.session_factory = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )
        self.metadata = MetaData()
        self.installations = SQLAlchemyInstallationStore.build_installations_table(
            metadata=self.metadata,
            table_name=SQLAlchemyInstallationStore.default_installations_table_name,
        )
        self.bots = SQLAlchemyInstallationStore.build_bots_table(
            metadata=self.metadata,
            table_name=SQLAlchemyInstallationStore.default_bots_table_name,
        )
        self._logger = logger

    @property
    def logger(self) -> Logger:
        return self._logger

    async def async_save(self, installation: Installation):
        async with self.session_factory() as session:
            async with session.begin():
                i = installation.to_dict()
                i["client_id"] = self.client_id
                await session.execute(self.installations.insert().values(**i))
                b = installation.to_bot().to_dict()
                b["client_id"] = self.client_id
                await session.execute(self.bots.insert().values(**b))

    async def async_find_bot(
        self, *, enterprise_id: Optional[str], team_id: Optional[str], is_enterprise_install: Optional[bool] = False
    ) -> Optional[Bot]:
        # is_enterprise_installは元のコードには引数として入っていなかったが、設定しないとエラーになるため追加。
        async with self.session_factory() as session:
            c = self.bots.c
            query = (
                self.bots.select()
                .where(and_(c.enterprise_id == enterprise_id, c.team_id == team_id))
                .order_by(desc(c.installed_at))
                .limit(1)
            )
            result = await session.execute(query)
            row = result.fetchone()
            if row:
                return Bot(
                    app_id=row.app_id,
                    enterprise_id=row.enterprise_id,
                    team_id=row.team_id,
                    bot_token=row.bot_token,
                    bot_id=row.bot_id,
                    bot_user_id=row.bot_user_id,
                    bot_scopes=row.bot_scopes,
                    installed_at=row.installed_at,
                )
            else:
                return None


class AsyncSQLAlchemyOAuthStateStore(AsyncOAuthStateStore):
    engine: any
    session_factory: any
    expiration_seconds: int
    metadata: MetaData
    oauth_states: Table

    def __init__(
        self,
        *,
        expiration_seconds: int,
        database_url: str,
        logger: Logger = logging.getLogger(__name__),
    ):
        self.expiration_seconds = expiration_seconds
        self.engine = create_async_engine(database_url, echo=True)
        self.session_factory = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )
        self.metadata = MetaData()
        self.oauth_states = SQLAlchemyOAuthStateStore.build_oauth_states_table(
            metadata=self.metadata,
            table_name=SQLAlchemyOAuthStateStore.default_table_name,
        )
        self._logger = logger

    @property
    def logger(self) -> Logger:
        return self._logger

    async def async_issue(self) -> str:
        state: str = str(uuid4())
        now = datetime.utcfromtimestamp(time.time() + self.expiration_seconds)
        async with self.session_factory() as session:
            async with session.begin():
                await session.execute(self.oauth_states.insert().values(state=state, expire_at=now))
            return state

    async def async_consume(self, state: str) -> bool:
        try:
            async with self.session_factory() as session:
                async with session.begin():
                    c = self.oauth_states.c
                    query = self.oauth_states.select().where(
                        and_(c.state == state, c.expire_at > datetime.utcnow())
                    )
                    result = await session.execute(query)
                    row = result.fetchone()
                    self.logger.debug(f"consume's query result: {row}")
                    if row:
                        await session.execute(
                            self.oauth_states.delete().where(c.id == row.id)
                        )
                        return True
            return False
        except Exception as e:
            message = f"Failed to find any persistent data for state: {state} - {e}"
            self.logger.warning(message)
            return False


# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


installation_store = AsyncSQLAlchemyInstallationStore(
    client_id=os.environ["SLACK_CLIENT_ID"], database_url=ASYNC_DB_URL, logger=logger,
)
oauth_state_store = AsyncSQLAlchemyOAuthStateStore(
    expiration_seconds=300, database_url=ASYNC_DB_URL, logger=logger,
)

# slack_oauthに必要なテーブルの確認・作成
async def init_slack_oauth():
    try:
        async with installation_store.engine.begin() as conn:
            await conn.execute("SELECT 1")
    except Exception:
        async with installation_store.engine.begin() as conn:
            await conn.run_sync(installation_store.metadata.create_all)
            await conn.run_sync(oauth_state_store.metadata.create_all)

