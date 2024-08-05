from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
server = os.getenv("MYSQL_HOST_FAST")
port = os.getenv("PORT_MYSQL_FAST")
db = os.getenv("MYSQL_DB_FAST")

ASYNC_DB_URL = f"mysql+aiomysql://{user}:{password}@{server}:{port}/{db}"

async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

async def get_db():
    async with async_session() as session:
        yield session