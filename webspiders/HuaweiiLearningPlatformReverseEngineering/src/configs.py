PROJECT_BASE_DIRECTORY = "~/PythonWorkspaces/Space1/web_spider_test/image_downloader"

config_edx_img = {
}

config_v1_img = {
    "cookies": {
    },
    "headers": {
    }
}

config_tiny_v1_img = {
    "cookies": {
    },
    "headers": {
    }
}

config_edx_v1_img = {
    "cookies": {
    },
    "headers": {
    }

}

config1 = {
    "cookies": {
    },
    "headers": {
    },
    "params": {
    }
}

config2 = {
    "cookies": {
    },
    "headers": {
    },
    "params": {
        'numType': '2',
        'users': '000000',
    }
}

config3 = {
    "cookies": {
    },
    "headers": {
    },
    "params": {
    }
}

config4 = {
    "cookies": {
    },
    "headers": {
    },
    "params": {
    }
}

config5 = {
    "cookies": {
    },
    "headers": {
    }
}

config6 = {
    "cookies": {
    },
    "headers": {
    }
}

config7 = {
    "cookies": {
    },
    "headers": {
    }
}

config8 = {
    "cookies": {
    },
    "headers": {
    }
}




Configs = [config1, config2, config3, config4, config5, config6, config7, config8]


def request_get(uri, config):
    import requests
    response = ""
    if config.get("cookies"):
        if config.get("headers"):
            if config.get("params"):
                response = requests.get(uri, cookies=config.get("cookies"),
                                        headers=config.get("headers"),
                                        params=config.get("params"), verify=False)
            else:
                response = requests.get(uri, cookies=config.get("cookies"),
                                        headers=config.get("headers"), verify=False)
        else:
            response = requests.get(uri, cookies=config.get("cookies"), verify=False)
    return response
