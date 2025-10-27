from get_data_from_database import *
import json

seven_len = get_data_table_len("seven")
eight_len = get_data_table_len("eight")
nine_len = get_data_table_len("nine")
ten_len = get_data_table_len("ten")

length = {
    "seven": seven_len,
    "eight": eight_len,
    "nine": nine_len,
    "ten": ten_len
}
print(length)

with open("len.json", 'w') as outfi:
    json.dump(length, outfi)