
cookies = {
}

headers = {
}

from utils import *
json_data = {
    'create_from': 9,
    'meeting_type': 0,
    'creator_time_zone': '+0800',
    'recurring_rule': {
        'recurring_type': 0,
        'until_type': 0,
        'until_times': 7,
        'version': 0,
        'until_date': 1743955199,
        'recurring_days': 127,
        'recurring_step': 0,
    },
    'water_mark': 0,
    'water_mark_type': 0,
    'begin_time': get_timestamp_from_formatted_date("2025-03-31 14:30:00"),
    'end_time': get_timestamp_from_formatted_date("2025-03-31 15:00:00"),
    'join_network_limit': 0,
    'allow_unmute_by_self': 1,
    'play_prompt_to_other_on_join': 0,
    'auto_in_waiting_room': 1,
    'allow_in_before_host': 2,
    'admission_type': 0,
    'join_permission': 0,
    'audio_watermark': 0,
    'location': '',
    'password': '',
    'host_list': [],
    'invite_list': [],
    'invite_list_big': [],
    'big_room_limit': 100,
    'capacity_card_id': '',
    'media_set_type': 0,
    'auto_record_type': 0,
    'virtual_background': None,
    'screenshot_state': 1,
    'is_anonymous': 0,
    'meeting_room_list': [],
    'auto_consume_promotion_card': False,
    'allow_multi_device': 1,
    'usr_opt_multi_device': False,
    'meeting_extra_cfg_info': {
        'str_auto_trans': 'CAA=',
    },
    'mute_on_join': 0,
    'auto_mute_by_member_count_switch': 1,
    'host_key': '',
    'ms_meeting_id': '7c6041ede03780b',
    'doc_info': {
        'doc_upload_permission': 2,
        'doc_list_info': [],
    },
    'time_zone': 'QXNpYS9TaGFuZ2hhaQ==',
    'subject': '6YKj5Lq6LeesrOS4gOasoee6v+S4iuayn+mAmuS8muiurg==',
    'check_meeting_conflict': 3,
    'create_type': 0,
    'enroll_pay_type': 0,
    'ignore_real_name_verify': 0,
    'support_secondary_verify': True,
    'security_component_code': '',
}


# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"support_secondary_verify":true,"security_component_code":""}'
#response = requests.post(
#    '',
#    cookies=cookies,
#    headers=headers,
#    data=data,
#)