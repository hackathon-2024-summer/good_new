from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import logging

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="templates")

router = APIRouter(tags=["Pages"])

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)