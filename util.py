from datetime import datetime, timedelta

def get_day(day_offset = 0):
    time = datetime.now() + timedelta(days=day_offset) 
    return time.strftime("%Y-%m-%d")