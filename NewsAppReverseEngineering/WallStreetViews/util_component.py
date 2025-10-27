import datetime as dt


def time_is_up(hr=6, m=0):
    delta = dt.timedelta(minutes=59)
    datetime_obj_lower_bound = dt.datetime.now() - delta
    datetime_obj_upper_bound = dt.datetime.now() + delta
    desired_time = dt.datetime.now().replace(hour=hr, minute=m)
    if datetime_obj_lower_bound < desired_time < datetime_obj_upper_bound:
        return True
    else:
        return False

