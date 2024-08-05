from fastapi import FastAPI
from routers import slack, develop
import logging

app = FastAPI()

app.include_router(slack.router)
app.include_router(develop.router)

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
