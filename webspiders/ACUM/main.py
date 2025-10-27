import requests
import time

url = 'https://adum.fr/ajax/candidatures/ed_by_etab.pl?mat=%s&entite=etab'
headers = {
}

school_codes = ['195', '62', '295', '135', '184', '281', '282', '280', '283', '257', '194', '328', '196', '197', '288',
                '188', '71', '76', '102', '276', '296', '327', '202', '284', '241', '65', '261', '189', '317', '209',
                '323', '22', '190', '133', '213', '325', '322', '39', '293', '38', '93', '299', '21', '265', '275',
                '43', '4', '90', '54', '83', '320', '14', '298', '256', '318', '48', '326', '273', '35', '29', '319',
                '305', '304', '300', '308', '310', '306', '302', '311', '312', '307', '315', '303', '247', '245', '246',
                '331']


# given one school code, get the subschool code
def get_subschool_codes(school_code) -> list:
    global url
    url_cp = url
    url_cp = url_cp % school_code
    res = requests.get(url_cp, headers=headers)
    # print(res.status_code, "\n----\n", res.json())
    res_json = res.json()
    subschool_li = res_json.get('data', None)
    subschool_codes = []
    if subschool_li is not None:
        for subschool in subschool_li:
            subschool_code = subschool.get('val')
            subschool_codes.append(subschool_code)
    return subschool_codes


# given the school code together with the subschool code, get the projects
def get_project_page(school_code, subschool_code) -> str:
    from project_page_info_config import url as project_url, data as req_data, headers as req_headers
    req_data = req_data % (school_code, subschool_code)
    res = requests.post(data=req_data, url=project_url, headers=req_headers)
    with open(f"French_phd_positions_ACUM/{school_code}_{subschool_code}.html", 'w') as fo:
        fo.write(res.text)
    time.sleep(3)


for school_code in school_codes:
    subschool_codes = get_subschool_codes(school_code)
    print(school_code, subschool_codes)
    if len(subschool_codes) == 0:
        subschool_code = ""
        get_project_page(school_code, subschool_code)
        continue

    for subschool_code in subschool_codes:
        try:
            get_project_page(school_code, subschool_code)
        except Exception:
            pass

    time.sleep(3)

