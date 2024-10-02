import requests
import json

def retrieve_data():
    payload = {
        "lid": 2552,
        "gid": 23067,
        "eid": -1, #eid corresponds with room
        "seat": 0,
        "seatId": 0,
        "zone": 0,
        "start": "2024-10-01",
        "end": "2024-10-02",
        "pageIndex": 0,
        "pageSize": 18
    }
    headers = {
        "Referer": "https://umd.libcal.com/spaces?lid=2552&gid=23067&c=0"
    }
    r = requests.post('https://umd.libcal.com/spaces/availability/grid', params=payload, headers=headers)
    all_slots = r.json()["slots"]

    available_slots = {}
    for slot in all_slots:
        if "className" not in slot.keys():
            if slot["itemId"] in available_slots.keys():
                if available_slots[slot["itemId"]][-1]["end"] == slot["start"]:
                    available_slots[slot["itemId"]][-1]["end"] = slot["end"]
                else: 
                    available_slots[slot["itemId"]].append(slot)
            else:
                available_slots[slot["itemId"]] = [slot]

    return available_slots

def fit_requirements(available, requirements):
    best_fit = []
    for roomId in available.keys():
        for block in available[roomId]:
            fit_min_duration = subtract_time(block) >= requirements["min-duration"]
            fit_start_time = block["start"] >= requirements["earliest-start"]
            if fit_min_duration and fit_start_time:
                block["duration"] = subtract_time(block)
                best_fit.append(block)
    return best_fit
                
def parse_time(slot_time):
    day_time = slot_time.split(" ")
    day = day_time[0].split("-")
    time = day_time[1].split(":")
    output = {
        "year": int(day[0]),
        "month": int(day[1]),
        "day": int(day[2]),
        "hour": 24 if time[0] == "00" else int(time[0]),
        "min": int(time[1]),
        "sec": int(time[2])
    }
    return output

def compare_slot(slot1, slot2):
    if slot1["start"] > slot2["start"]:
        return slot2
    elif slot2["start"] > slot1["start"]:
        return slot1
    else:
        return slot1
    
def subtract_time(period):
    start_parsed = parse_time(period["start"])
    end_parsed = parse_time(period["end"])
    hour_value = end_parsed["hour"] - start_parsed["hour"]
    min_value = end_parsed["min"] - start_parsed["min"]
    sec_value = end_parsed["sec"] - start_parsed["sec"]

    #implementing hour carryover lmaoooo not minute tho
    hour_carryover = 0
    if(min_value < 0):
        hour_carryover = 1
        min_value += 60
    
    output = ("0" + str(hour_value - hour_carryover)) if hour_value - hour_carryover < 10 else str(hour_value - hour_carryover)
    output += ":" + ("0" + str(min_value) if min_value < 10 else str(min_value))
    output += ":" + ("0" + str(sec_value)) if sec_value < 10 else str(sec_value)
    return output

def sort_slots(slots):
    return sorted(slots, key=lambda x: (x["start"] + " " + x["duration"]))

if __name__ == '__main__':
    available_slots = retrieve_data()
    print(available_slots)
    reqs = { #then find the soonest time
        "earliest-start": "2024-10-01 20:00:00", #hard
        "min-duration": "01:00:00" #hard h:m:s
    } # sort by start then duration?

    fitting_slots = fit_requirements(available_slots, reqs)
    sorted_slots = sort_slots(fitting_slots)

