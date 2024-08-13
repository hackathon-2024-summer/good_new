import logging
from fastapi import FastAPI
from routers import slack, develop
from slack_schedule.question import question
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from slack_schedule.update_question import update_question_to_user
import asyncio

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

job_defaults = {"coalesce": False, "max_instances": 3, "misfire_grace_time": 3600}

# chat_updateメソッド用辞書…送信したメッセージ情報を保存
sent_messages = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    global scheduler
    # 非同期処理のためBackgroundSchedulerから変更
    scheduler = AsyncIOScheduler(job_defaults=job_defaults)
    scheduler.add_job(
        lambda: asyncio.run(question(sent_messages)), "cron", hour=14, minute=0
    )
    # scheduler.add_job(question, "interval", minutes=1) # 検証用
    scheduler.add_job(
        lambda: asyncio.run(update_question_to_user(sent_messages)),
        "cron",
        hour=0,
        minute=0,
    )
    scheduler.start()
    logger.info("Scheduler started")

    yield

    if scheduler:
        scheduler.shutdown()
        logger.info("Scheduler shut down")


app = FastAPI(lifespan=lifespan)
app.include_router(slack.router)
app.include_router(develop.router)
