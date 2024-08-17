from datetime import date

def format_date_slash(date: date) -> str:
    formatted_date = date.strftime("%Y/%m/%d")
    
    return formatted_date