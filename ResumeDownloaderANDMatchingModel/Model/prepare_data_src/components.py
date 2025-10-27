from config import *
import json
import os
import mysql.connector
from private_vars import *


def insert_data_command(comm):
    cnx = mysql.connector.connect(user='root', database='train_cv_position_rawdata', password=password)
    cursor = cnx.cursor()

    cursor.execute(comm)

    cnx.commit()

    cursor.close()
    cnx.close()


def clean_tables():
    cnx = mysql.connector.connect(user='root', database='train_cv_position_rawdata', password=password)
    cursor = cnx.cursor()

    cursor.execute("delete from train_cv_position_rawdata.seven;")
    cursor.execute("delete from train_cv_position_rawdata.eight;")
    cursor.execute("delete from train_cv_position_rawdata.nine;")
    cursor.execute("delete from train_cv_position_rawdata.ten;")

    cnx.commit()

    cursor.close()
    cnx.close()


def read_cv_data(file):
    with open(file, "r") as infi:
        lines = infi.readlines()
        lines = lines[8:]
        lines = [line.strip() for line in lines]

    content = "\n".join(lines)
    content = content.replace("\"", "'")
    return str(content)


def read_overview_data(file):
    with open(file, "r") as infi:
        lines = infi.readlines()
        lines = lines[1:]
        lines = [line.strip() for line in lines]
        content = "\n".join(lines)
    content = content.replace("\"", "'")

    return content


def format_file_path(file, parent="../../Files"):
    content = os.path.join(parent, file) + ".txt"
    return content


def get_table_name(json_file):
    keys = json_table_map.keys()
    for key in keys:
        if key in json_file:
            return json_table_map.get(key)

def save_data_pairs_in_json(json_file):
    print(json_file)
    with open(json_file, "r") as infi:
        table_name = get_table_name(json_file)
        obj = json.load(infi)
        for pair in obj:
            try:
                cv_file, overview_file = pair
                cv_file, overview_file = format_file_path(cv_file), format_file_path(overview_file)
                cv = read_cv_data(cv_file)
                overview = read_overview_data(overview_file)
                comm = f'INSERT INTO train_cv_position_rawdata.{table_name} (cv, position_overview) VALUES ( "' + cv + '", ' + f'\"{overview}\"' +');'
                insert_data_command(comm)
            except Exception as e:
                print(e)
                continue

