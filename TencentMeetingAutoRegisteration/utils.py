from datetime import datetime
import base64
from config import *
#
# base64_string ="=="
# # base64_bytes = base64_string.encode("ascii")
# #
# # sample_string_bytes = base64.b64decode(base64_bytes)
# # sample_string = sample_string_bytes.decode("ascii")
# sample_string = base64.b64decode(base64_string)
# print(sample_string.decode("utf-8"))


def gen_encoded_str(s):
    return base64.b64encode(s.encode("utf-8"))


def parse_encoded_s(e_url):
    """
    filename: 9186.911b99fd.chunk.js
    function:
    function Ge(e) {
            void 0 === e && (e = "");
            try {
                return E.S ? Buffer.from(e, "base64").toString() : decodeURIComponent(escape(window.atob(e)))
            } catch (t) {
                return e
            }
        }
    """
    return base64.b64decode(e_url).decode('utf-8')

# print(parse_encoded_url(""))
# print(parse_encoded_url("=="))
# print(datetime.fromtimestamp(1743399000))
# print(datetime.strptime('2025-03-31 13:30:00', '%Y-%m-%d %H:%M:%S').timestamp())


def get_formatted_date_from_timestamp(st):
    return datetime.fromtimestamp(st)


def get_timestamp_from_formatted_date(f_date):
    return int(datetime.strptime(f_date, '%Y-%m-%d %H:%M:%S').timestamp())

# print(get_formatted_date_from_timestamp(1743688501))

with open("res.json", 'r') as fi:
    import json
    con = json.load(fi)

encoded_url = con['url']
meeting_code = con['meeting_code']
print(parse_encoded_s(encoded_url))
print(meeting_code)


def transfer_meeting_code(c):
    return c[:3] + "-" + c[3:6] + "-" + c[6:]


def gen_post_data(start_time, end_time):
    s = get_timestamp_from_formatted_date(start_time)
    e = get_timestamp_from_formatted_date(end_time)
    json_data['begin_time'] = s
    json_data['end_time'] = e
    return json_data
