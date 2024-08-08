from fastapi import FastAPI
from routers import slack, develop
import logging

app = FastAPI()

app.include_router(slack.router)
app.include_router(develop.router)
