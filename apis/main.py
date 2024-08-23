import logging
from fastapi import FastAPI, Request
from routers import slack, page
from repository.slack_oauth import init_slack_oauth
from slack_schedule.question import question
from slack_schedule.delivery import delivery
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi.staticfiles import StaticFiles


# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

job_defaults = {"coalesce": False, "max_instances": 3, "misfire_grace_time": 3600}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # slack_oauthに必要なテーブルの確認・作成
    await init_slack_oauth()

    # スケジュールの追加と起動
    global scheduler
    # 非同期処理のためBackgroundSchedulerから変更
    scheduler = AsyncIOScheduler(job_defaults=job_defaults)
    scheduler.add_job(question, "cron", hour=14, minute=0)
    # scheduler.add_job(question, "interval", minutes=1) # 検証用
    scheduler.add_job(delivery, "cron", hour=16, minute=0)
    # scheduler.add_job(delivery, "interval", minutes=1) # 検証用
    scheduler.start()
    logger.info("Scheduler started")

    yield

    if scheduler:
        scheduler.shutdown()
        logger.info("Scheduler shut down")


app = FastAPI(lifespan=lifespan)

# 静的ファイルをマウント
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

app.include_router(slack.router)
app.include_router(page.router)
