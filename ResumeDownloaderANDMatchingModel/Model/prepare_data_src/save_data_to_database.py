import mysql.connector
from private_vars import *
from components import *


def command_executor(comm):
    cnx = mysql.connector.connect(
        user=user,
        password=password,
        host="localhost",
        database="train_cv_position_rawdata"
    )

    cursor = cnx.cursor()
    cursor.execute(comm)

    result = cursor.fetchall()

    cursor.close()
    cnx.close()
    return result


clean_tables()

save_data_pairs_in_json("../data/7.json")
save_data_pairs_in_json("../data/8.json")
save_data_pairs_in_json("../data/9.json")
save_data_pairs_in_json("../data/10.json")
