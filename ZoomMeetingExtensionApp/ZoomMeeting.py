from time import time
import json
import requests
import jwt

API_KEY = ""
API_SEC = ""


def generate_token():
    token = jwt.encode(
        {'iss': API_KEY, 'exp': time() + 5000},
        API_SEC,
        algorithm="HS256"
    )
    return token


jsonmeeting_details = {"topic": "Python Zoom Meeting", "type": 2,  # Scheduled meeting
                       "start_time": "2023-06-14T10:00:00",  # Use your desired date and time
                       "duration": "45",  # Duration in minutes
                       "timezone": "America/New_York", "agenda": "Discuss Zoom API Integration",
                       "settings": {"host_video": True, "participant_video": True, "join_before_host": False,
                                    "mute_upon_entry": True, "watermark": False, "audio": "voip",
                                    "auto_recording": "none"}}

def create_meeting():
    headers = {
        "authorization": "Bearer " + generate_token(),
        "content-type": "application/json"
    }
    r = requests.post(
        f"https://api.zoom.us/v2/users/me/meetings",
        headers=headers,
        data=json.dumps(jsonmeeting_details)
    )
    return r.json()

create_meeting()
