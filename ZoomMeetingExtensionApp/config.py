account_id = "***********"
client_id = "***********"
client_secret = "***********"
token = '***********.***********.***********-***********'
email = "***********@gmail.com"
payload = {
    "agenda": "Testing API",
    "default_password": False,
    "duration": 30,
    "password": "***********",
    "pre_schedule": False,
    "recurrence": {
        "end_date_time": "2025-04-02T15:59:00Z",
        "end_times": 7,
        "monthly_day": 1,
        "monthly_week": 1,
        "monthly_week_day": 1,
        "repeat_interval": 1,
        "type": 1,
        "weekly_days": "1"
    },  # doesnt work at all, this is only  for type 8 meeting
    "schedule_for": email,
    "settings": {
        "additional_data_center_regions": ["TY"],
        "allow_multiple_devices": True,
        # "alternative_hosts": email,
        "alternative_hosts_email_notification": False,
        "approval_type": 2,
        "approved_or_denied_countries_or_regions": {
            "approved_list": ["US", "CN"],
            # "denied_list": ["CA"],
            "enable": True,
            "method": "approve"
        },
        # "audio": "telephony",
        "audio_conference_info": "test",
        "authentication_domains": "gmail.com",
        "authentication_exception": [
            {
                "email": email,
                "name": "Tom xxx xxx"
            }
        ],
        # "authentication_option": "***********",
        "auto_recording": "cloud",
        "breakout_room": {
            "enable": True,
            "rooms": [
                {
                    "name": "room1",
                    "participants": [email]
                }
            ]
        },
        "calendar_type": 1,
        "close_registration": False,
        "cn_meeting": False,
        "contact_email": email,
        "contact_name": "Tom xxx xxx",
        "email_notification": True,
        "encryption_type": "enhanced_encryption",
        "focus_mode": True,
        # "global_dial_in_countries": ["US"],
        "host_video": True,
        "host_audio": True,
        "in_meeting": False,
        "jbh_time": 0,
        "join_before_host": False,
        "question_and_answer": {
            "enable": True,
            "allow_submit_questions": True,
            "allow_anonymous_questions": True,
            "question_visibility": "all",
            "attendees_can_comment": True,
            "attendees_can_upvote": True
        },
        "language_interpretation": {
            "enable": True,
            "interpreters": [
                {
                    "email": email,
                    "languages": "US,FR",
                    "interpreter_languages": "English,French"
                }
            ]
        },
        "sign_language_interpretation": {
            "enable": True,
            "interpreters": [
                {
                    "email": email,
                    "sign_language": "American"
                }
            ]
        },
        "meeting_authentication": True,
        "meeting_invitees": [{ "email": email }],
        "mute_upon_entry": False,
        "participant_video": False,
        "private_meeting": False,
        "registrants_confirmation_email": True,
        "registrants_email_notification": True,
        "registration_type": 1,
        "show_share_button": True,
        "use_pmi": False,
        "waiting_room": False,
        "watermark": False,
        "host_save_video_order": True,
        "alternative_host_update_polls": True,
        "internal_meeting": False,
        "continuous_meeting_chat": {
            "enable": True,
            "auto_add_invited_external_users": True,
            "auto_add_meeting_participants": True,
            "who_is_added": "all_users"
        },
        "participant_focused_meeting": False,
        "push_change_to_calendar": False,
        "resources": [
            {
                "resource_type": "whiteboard",
                "resource_id": "***********",
                "permission_level": "editor"
            }
        ],
        "auto_start_meeting_summary": False,
        "who_will_receive_summary": 1,
        "auto_start_ai_companion_questions": False,
        "who_can_ask_questions": 1,
        "device_testing": False,
        "allow_host_control_participant_mute_state": False,
        "disable_participant_video": False
    },
    "start_time": "2025-03-29T07:32:55Z",
    "template_id": "***********+***********==",
    "timezone": "China/Shanghai",
    "topic": "My Meeting",
    "tracking_fields": [
        {
            "field": "field1",
            "value": "value1"
        }
    ],
    "type": 2
}