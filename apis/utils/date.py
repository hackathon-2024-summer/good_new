from datetime import date
import datetime
import jpholiday
from routers.slack import logger

def format_date_slash(date: date) -> str:
    formatted_date = date.strftime("%Y/%m/%d")
    
    return formatted_date

def valid_date() -> bool:
    today = datetime.date.today()
    weekday = today.weekday()  # 0(月曜日)から6(日曜日)が取得できる

    if weekday >= 5 or jpholiday.is_holiday(today):
        logger.warning("土日祝日のため、質問を送信しません")
        return False

    return True
    