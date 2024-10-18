import requests
from urllib.request import urlopen
import json
from util import get_day

NUM_SHOWN_SLOTS = 3
GID = 23067
LID = 2552
headers = {
    "Referer": "https://umd.libcal.com/spaces?lid=2552&gid=23067&c=0"
}

def retrieve_data():
    payload = {
        "lid": LID,
        "gid": GID,
        "eid": -1, #eid corresponds with room
        "seat": 0,
        "seatId": 0,
        "zone": 0,
        "start": get_day(),
        "end": get_day(day_offset=1),
        "pageIndex": 0,
        "pageSize": 18
    }
    
    r = requests.post('https://umd.libcal.com/spaces/availability/grid', params=payload, headers=headers)
    all_slots = r.json()["slots"]
    # print(all_slots)

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
            # print(block)
            if(block["start"] < requirements["earliest-start"]):
                block["start"] = requirements["earliest-start"]
            fit_min_duration = subtract_time(block) >= requirements["min-duration"]
            fit_start_time = block["end"] > requirements["earliest-start"]
            # print(block, fit_min_duration, fit_start_time)
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
    
    hour_value -= hour_carryover
    output = ("0" + str(hour_value)) if hour_value < 10 else str(hour_value)
    output += ":" + ("0" + str(min_value) if min_value < 10 else str(min_value))
    output += ":" + ("0" + str(sec_value)) if sec_value < 10 else str(sec_value)
    return output

def sort_slots(slots):
    # print(slots)
    # print(sorted(slots, key=lambda x: (x["start"] + " " + reverse_duration(x["duration"]))))
    return sorted(slots, key=lambda x: (x["start"] + " " + reverse_duration(x["duration"])))

def reverse_duration(duration):
    split = duration.split(":")
    duration = f"{99-int(split[0])}:{99-int(split[1])}:{split[2]}"
    # print(duration)
    return duration

def find_slots(requirements):
    available_slots = retrieve_data()
    # print(available_slots)
    fitting_slots = fit_requirements(available_slots, requirements)
    sorted_slots = sort_slots(fitting_slots)
    return sorted_slots[:NUM_SHOWN_SLOTS]

def find_checksum(slot):
    base_url = 'https://umd.libcal.com/spaces/availability/booking/add'
    payload = {
        "add[eid]": slot['itemId'],
        "add[gid]": GID,
        'add[lid]': LID,
        "add[start]": slot['start'],
        "add[checksum]": slot['checksum'],
        "lid": LID,
        "gid": GID,
        "start": get_day(),
        "end": get_day(day_offset=1) 
    }
    r = requests.post(base_url, params=payload, headers=headers)
    json = r.json()
    return json['bookings'][0]['checksum']

def make_booking(user_data, slot):
    payload = user_data
    payload["q16114"] = user_data["school_uid"]
    payload['method'] = 11

    booking_data = {
        "id": 1,
        "eid": slot['itemId'],
        "seat_id": 0,
        "gid": GID,
        "lid": LID,
        "start": slot['start'],
        "end": slot['end'],
        "checksum": find_checksum(slot),
    }
    print(slot["checksum"])
    print(find_checksum(slot))
    booking_str = "[{" + ",".join(f"\"{k}\":{v if isinstance(v, (int)) else '\"'+str(v)+'\"'}" for k,v in booking_data.items()) + "}]"
    print(booking_str)
    payload['bookings'] = booking_str
    #[{"id":1,"eid":86501,"seat_id":0,"gid":23067,"lid":2552,"start":"2024-10-18 15:30:00","end":"2024-10-18 16:00:00","checksum":"053eca29ddb26bd8b954917df9279c77"}]

    payload.pop('uid')
    payload.pop('school_uid')

    base_url = 'https://umd.libcal.com/ajax/space/book'
    payload_str = "?" + "&".join("%s=%s" % (k,v) for k,v in payload.items())
    
    session = requests.Session()
    r = requests.Request('POST', base_url, headers=headers)
    p = r.prepare()
    p.url += payload_str
    resp = session.send(p)

    print(resp.url)
    return resp.status_code
    

if __name__ == '__main__':
    reqs = { #then find the soonest time
        "earliest-start": "2024-10-18 10:00:00", #hard
        "min-duration": "01:00:00" #hard h:m:s
    } # sort by start then duration?

    slots = find_slots(reqs)

