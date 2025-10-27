

def format_cookies(cookie_file='./cookies.txt'):
    with open(cookie_file, 'r') as fi:
        s = fi.read().strip()
    s = s.strip()
    li = s.split(";")
    cookies = {}
    for ele in li:
        tmp = ele.split("=")
        if len(tmp) == 2:
            cookies[tmp[0].strip()] = tmp[1].strip()
    print(cookies)
    return cookies

# format_cookies()
