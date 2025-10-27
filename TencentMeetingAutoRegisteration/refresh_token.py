import requests

cookies = {
}

headers = {
}

json_data = {
    'refresh_token': 0,
}

response = requests.post(
    'https://meeting.tencent.com/wemeet-webapi/v2/account/login/refresh-token',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"refresh_token":0}'

# NOTE: check this file/request on developer tool
