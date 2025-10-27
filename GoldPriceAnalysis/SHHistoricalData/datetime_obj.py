from datetime import datetime
from datetime import timedelta

# print(datetime.now().strftime('%Y-%m-%d'))
# delta = timedelta(days=30)
# current = datetime.now()
# current = current - delta
# print(current)

def get_date_params(d=None, c=0):
    delta = timedelta(days=29)
    if not d:
        current = datetime.now()
    else:
        current = d

    for i in range(c):
        current -= delta
    return current