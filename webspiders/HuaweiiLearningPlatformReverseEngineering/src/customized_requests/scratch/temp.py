

a = {'code': 200, 'message': '操作成功！', 'data': [{'applicationId': ''}]}


def get_val_of_key_in_response(dictionary, target="resourceApplyId"):
    if dictionary is None:
        return None
    elif isinstance(dictionary, dict):
        if target in dictionary.keys() and dictionary.get(target) is not None:
            return dictionary.get(target)
        for k, v in dictionary.items():
            if type(v) in [dict, list]:
                return_val = get_val_of_key_in_response(v, target)
                if return_val is not None:
                    return return_val
        return None
    elif isinstance(dictionary, list):
        for ele in dictionary:
            return_val = get_val_of_key_in_response(ele, target)
            if return_val is not None:
                return return_val
        return None
    else:
        return None


print(get_val_of_key_in_response(a, "title"))
