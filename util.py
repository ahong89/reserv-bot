from datetime import datetime, timedelta

def get_day(day_offset = 0):
    time = datetime.now() + timedelta(days=day_offset) 
    return time.strftime("%Y-%m-%d")

def subtract_time(end_time, start_time):
    start_parsed = start_time.split(":")
    end_parsed = end_time.split(":")
    hour_value = int(end_parsed[0]) - int(start_parsed[0])
    min_value = int(end_parsed[1]) - int(start_parsed[1])
    sec_value = int(end_parsed[2]) - int(start_parsed[2])

    #implementing hour carryover lmaoooo not minute tho
    hour_carryover = 0
    if(min_value < 0):
        hour_carryover = 1
        min_value += 60
    
    hour_value -= hour_carryover
    output = ("0" + str(hour_value)) if hour_value < 10 else str(hour_value)
    output += ":" + ("0" + str(min_value) if min_value < 10 else str(min_value))
    output += ":" + ("0" + str(sec_value)) if sec_value < 10 else str(sec_value)
    return output