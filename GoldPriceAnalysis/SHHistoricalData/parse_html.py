from bs4 import BeautifulSoup


def get_data(htmlTxt):
    soup = BeautifulSoup(htmlTxt, features="html.parser")
    table = soup.find('table')
    trs = table.find("tbody").find_all('tr')
    data = []
    for tr in trs:
        tds = tr.find_all("td")
        tds = [td.text for td in tds]
        if tds[1] == "Au99.99":
            data.append(tds)
    return data


def get_head(htmlTxt):
    soup = BeautifulSoup(htmlTxt, features="html.parser")
    table = soup.find('table')
    thead = table.find("thead")
    ths = thead.find_all('th')
    ths = [th.text for th in ths]
    return ths

