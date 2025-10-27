headers = {
}

params = {
    'accept': 'article,topic,live,ad,chart',
    'limit': '100',
    'cursor': '',
    'action': 'upglide',
}

paper_params = {
    'extract': '0',
    'accept_theme': 'theme,premium-theme',
}


class EmailConfig:
    min_buffer = 59
    user_pass163 = ""
    weather_x_api_key = ""
    weather_api_key = ""  # the api for WeatherAPI website

    # mail info
    mail_host = "smtp.163.com"
    mail_user = "xxxxxxx@163.com"
    sender = "xxxxxxx@163.com"
    receivers = "xxxxxxx@163.com"

    subject = ''
