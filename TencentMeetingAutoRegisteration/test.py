import requests
from config import *

response = requests.post(
    'https://meeting.tencent.com/wemeet-tapi/wemeet/manage_service/comm/v1/schedule',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"create_from":9,"security_component_code":""}'
#response = requests.post(
#    'https://meeting.tencent.com/wemeet-tapi/wemeet/manage_service/comm/v1/schedule?c_app_id=',
#    cookies=cookies,
#    headers=headers,
#    data=data,
#)

with open("res.json", 'w') as fi:
    import json
    json.dump(response.json(), fi)