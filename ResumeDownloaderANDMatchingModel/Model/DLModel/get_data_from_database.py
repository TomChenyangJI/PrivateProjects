import mysql.connector
from web_spider_test.get_resumes.Model.prepare_data_src.private_vars import *


def execute_command(comm):
    cnx = mysql.connector.connect(user='root', database='train_cv_position_rawdata', password=password)
    cursor = cnx.cursor()

    cursor.execute(comm)
    result = cursor.fetchall()
    cnx.commit()

    cursor.close()
    cnx.close()

    return result


def get_data_table_len(scheme):
    comm = f"select count(*) from {scheme};"
    result = execute_command(comm)
    return result[0][0]


# comm1 = "select * from seven limit 0, 100;"
# data = execute_command(comm1)
# for entry in data:
#     cv, overview = entry  # one sample

