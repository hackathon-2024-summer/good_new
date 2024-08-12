import logging
from fastapi import FastAPI
from routers import slack, develop
from slack_schedule.question import question
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler


# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

job_defaults = {"coalesce": False, "max_instances": 3, "misfire_grace_time": 3600}


@asynccontextmanager
async def lifespan(app: FastAPI):
    global scheduler
    # 非同期処理のためBackgroundSchedulerから変更
    scheduler = AsyncIOScheduler(job_defaults=job_defaults)
    scheduler.add_job(question, "cron", hour=17, minute=0)
    # scheduler.add_job(question, "interval", minutes=1)
    scheduler.start()
    logger.info("Scheduler started")

    yield

    if scheduler:
        scheduler.shutdown()
        logger.info("Scheduler shut down")


app = FastAPI(lifespan=lifespan)
app.include_router(slack.router)
app.include_router(develop.router)

