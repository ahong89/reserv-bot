GID = 23067
LID = 2552
slot = {
    'itemId': 86443,
    'start': '2024-10-18 10:00:00',
    'end': '2042-10-18 12:00:00',
    "checksum": '9e89eea551b593a3d0a075c5315c0d37'
}

booking_data = {
        "id": 1,
        "eid": slot['itemId'],
        "seat_id": 0,
        "gid": GID,
        "lid": LID,
        "start": slot['start'],
        "end": slot['end'],
        "checksum": slot['checksum'],
    }
booking_str = "[{" + ",".join(f"\"{k}\":{v if isinstance(v, (int)) else '\"'+str(v)+'\"'}" for k,v in booking_data.items()) + "}]"
print(booking_str)