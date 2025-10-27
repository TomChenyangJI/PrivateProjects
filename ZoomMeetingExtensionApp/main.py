import requests
from requests.auth import HTTPBasicAuth
from config import *


def request_access_token():
    # ref docu: https://developers.zoom.us/docs/integrations/oauth/
    api_url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={account_id}"
    res = requests.post(api_url, auth=HTTPBasicAuth(client_id, client_secret))
    return res.json()  # access_token


# print(request_access_token())


def create_a_meeting():
    url = f"https://api.zoom.us/v2/users/{email}/meetings"
    token = request_access_token().get("access_token")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

create_a_meeting()
