
from punchcard import register_attendance
"""
research center location：(
        20.2638000, 
        100.6322350
        )
"""


# register_attendance()

import datetime
import time

# print(datetime.datetime.now().hour)

if __name__ == "__main__":
    while True:
        current_hr = datetime.datetime.now().hour
        current_day = datetime.datetime.now().day
        # if current_hr == 22 and current_day == 18:
        if current_hr == 22 or current_hr == 19 or current_hr == 7:
            print(datetime.datetime.now())
            register_attendance()
            time.sleep(60 * 60)
            # break
        else:
            print("Sleeping for 30 minutes...")
            time.sleep(60 * 30)
