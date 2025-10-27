import requests


def register_attendance():
    with requests.Session() as s:
        headers = {

        }

        data = ''

        s.post('https://abc.xxxxxx.com/xxxxxxx/LoginWithSF', headers=headers, data=data, verify=False)
        params = {
            'numType': '2',
            'users': '000000',
        }
        s.get("https://abc.xxxxxx.com/xxxxxxx/ProxyForText/mservice/person/personInfoByW3account", params=params)
        json_data = {
            'locale': 'cn',
            'employeeNumber': '000000',
            'deviceId': 'ED7CCF7E816A',
            'deviceType': '0',
        }
        s.get('https://abc.xxxxxx.com/xxxxxxx/ProxyForText/mattend-new/service/getrecord', json=json_data
              , verify=False)

        params = {
            'comVer': '1077',
            'allowBreak': 'true',
            'method': 'postMap',
        }

        data = {
            'installParas': '{"paras":[{"appId":"com.xxxxxx.works.h5.common","ver":"1077"}',
        }

        s.post(
            'https://abc.xxxxxx.com/xxxxxxx/ProxyForText/westore/services/hwworks/store/checkVersions/3/com.xxxxxx.works/16.7.1/1/513',
            params=params,
            data=data, verify=False
        )

        json_data = {
            'lastUpdateDate': '2000-01-01 00:00:00',
        }

        s.post(
            'https://abc.xxxxxx.com/xxxxxxx/ProxyForText/mcontact/services/userbehavior/safeBrowserConfig/listBrowserByLastDate',
            json=json_data, verify=False
        )

        params = {
            'validateUser': 'false',
        }

        json_data = {
            'locale': 'cn',
            'deviceModel': 'iPhone10,3',
        }

        response = s.post(
            'https://abc.xxxxxx.com/xxxxxxx/ProxyForText/abcbm-new/rest/mattend/punchCard',
            params=params,
            json=json_data, verify=False
        )
        print(response.status_code)
        print("*" * 10)
        print(response.text)
        # print("*" * 10)
        # print(response.content)


register_attendance()
