from datetime import date, datetime, timedelta
import mysql.connector


def insert_data_command(comm):
    cnx = mysql.connector.connect(user='root', database='train_cv_position_rawdata', password="*******")
    cursor = cnx.cursor()

    cursor.execute(comm)

    cnx.commit()

    cursor.close()
    cnx.close()

comm = "INSERT INTO seven "\
                   "(cv, position_overview) "\
                   "VALUES (3, 2)"
insert_data_command(comm)
# insert_data_command(("INSERT INTO seven "
#                    "(cv, position_overview) "
#                    "VALUES (%s, %s)"), ('Geert', 'Vanderkelen'))
