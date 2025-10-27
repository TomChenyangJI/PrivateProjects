import os
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from News.WallStreetViews.config import paper_params, headers
from News.WallStreetViews.util_component import *

def create_section(i: list):
    section = "<table style='border: 1px solid purple;'>"
    for ele in i:
        piece = f"""
    <tr style='border: 1px solid purple;'>
        <td style='border: 1px solid purple;'>{ele[0]}</th>
        <td style='border: 1px solid purple;'><a href="{ele[1]}"><small>Link</small></a></td>
    </tr>
            """
        section += piece
    section += "</table>"
    return section


def get_html_for_email(chars_in_titles, chars_in_contents):
    base = "<h3>First Priority</h3>%s<h3>Second Priority</h3>%s"
    section = create_section(chars_in_titles)
    section2 = create_section(chars_in_contents)
    html_content = base % (section, section2)
    return html_content


def send_info_to_user(msg_body="test", subject_component="", subject=""):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.header import Header
    from News.WallStreetViews.config import EmailConfig
    receivers = EmailConfig.receivers
    mail_host = EmailConfig.mail_host
    mail_user = EmailConfig.mail_user
    sender = EmailConfig.sender
    user_pass163 = EmailConfig.user_pass163
    subject = EmailConfig.subject
    mail_pass = user_pass163

    # msg = MIMEText(msg_body, 'plain', 'utf-8')
    msg = MIMEMultipart("alternative")
    msg['From'] = mail_user
    msg['To'] = receivers
    subject = (subject + subject_component) if not subject else subject
    msg['Subject'] = Header(subject, 'utf-8')
    part = MIMEText(msg_body, "html")
    msg.attach(part)
    # Send the email
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, msg.as_string())
        print("Latest News has been sent via email.")
    except Exception as e:
        print(f"Failed to send email: {e}")


def get_paper_api_uri(uri_id):
    base_uri = 'https://api-one-wscn.awtmt.com/apiv1/content/articles/'
    return base_uri + uri_id


def get_all_uris(obj: dict):
    uris = []
    items = obj.get("data").get('items')
    for item in items:
        uri = item.get('resource').get('uri')
        uris.append(uri)

        # display_time = item.get('resource').get('display_time')
        # display_time = time.ctime(display_time)
    return uris


def get_paper_content(obj: dict):
    content = obj.get('data').get('content')
    soup = BeautifulSoup(content, features="html.parser")
    return soup.text


def get_paper_title(obj: dict):
    title = obj.get('data').get('title')
    soup = BeautifulSoup(title, features="html.parser")
    return soup.text


def get_paper_display_time(obj: dict):
    display_time = obj.get('data').get('display_time')  # this is timestamp
    temp = datetime.fromtimestamp(int(display_time)).strftime("%Y/%m/%d")
    return display_time


def get_date(display_time):
    temp = datetime.fromtimestamp(int(display_time)).strftime("%Y/%m/%d")
    return str(temp)

# print(datetime.strptime("2025/03/31 10:00:00", "%Y/%m/%d %H:%M:%S").timestamp())


def get_timestamp(d_str: str, default_format='%Y/%m/%d %H:%M:%S'):
    # get time stamp from formatted str
    return datetime.strptime(d_str, default_format).timestamp()


def download_all_papers(obj: dict):
    chars = "跌超"
    chars_in_titles = []
    chars_in_contents = []
    uris = get_all_uris(obj)
    for uri in uris:
        time.sleep(1)
        try:
            pieces = uri.split('/')
            uri_id = pieces[-1]
            api_uri = get_paper_api_uri(uri_id)
            res = requests.get(api_uri, params=paper_params, headers=headers)
            print(api_uri)
            content = get_paper_content(res.json())
            title = get_paper_title(res.json())
            if chars in title:
                paper_uri = 'https://wallstreetcn.com/articles/' + uri_id
                chars_in_titles.append([title, paper_uri])

            if chars in content:
                paper_uri = 'https://wallstreetcn.com/articles/' + uri_id
                if [title, paper_uri] not in chars_in_titles:
                    chars_in_contents.append([title, paper_uri])
            title = title.replace("/", " ")
            display_time = get_paper_display_time(res.json())  # this is for dirs
            dir = "news/" + get_date(display_time)
            os.makedirs(dir, exist_ok=True)
            with open(f'{dir}/{title}.txt', "w") as fi:
                fi.write(content)
        except Exception as e:
            print(e)

    # send email to user
    if chars_in_titles or chars_in_contents:
        html_content = get_html_for_email(chars_in_titles, chars_in_contents)
        send_info_to_user(html_content, " " + str(datetime.fromtimestamp(time.time()).strftime("%Y/%m/%d")))

# download_all_papers(obj)


