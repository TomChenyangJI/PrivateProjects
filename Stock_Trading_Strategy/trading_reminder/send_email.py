class EmailConfig:
    min_buffer = 59
    user_pass163 = ""
    weather_x_api_key = ""
    weather_api_key = ""  # the api for WeatherAPI website

    # mail info
    mail_host = "smtp.163.com"
    mail_user = "xyz@163.com"
    sender = "xyz@163.com"
    receivers = "xyz@163.com"

def send_info_to_user(msg_body="test", subject=""):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.header import Header

    receivers = EmailConfig.receivers
    mail_host = EmailConfig.mail_host
    mail_user = EmailConfig.mail_user
    sender = EmailConfig.sender
    # subject = EmailConfig.subject
    mail_pass = EmailConfig.user_pass163

    # msg = MIMEText(msg_body, 'plain', 'utf-8')
    msg = MIMEMultipart("alternative")
    msg['From'] = mail_user
    msg['To'] = receivers

    msg['Subject'] = Header(subject, 'utf-8')
    part = MIMEText(msg_body, "html")
    msg.attach(part)
    # Send the email
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, msg.as_string())
        print(f"Email {subject} has been sent.")
    except Exception as e:
        print(f"Failed to send email: {e}")