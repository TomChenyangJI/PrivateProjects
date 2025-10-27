import sqlite3
import time
from contextlib import closing


def get_table_names(db_path: str =
                    "all_stocks.db"
                    ):
    with closing(sqlite3.connect(db_path)) as conn:
        with closing(conn.cursor()) as cursor:
            # conn = sqlite3.connect(db_path)
            # cursor = conn.cursor()
            command = f"""
            SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';
            """
            cursor.execute(command)
            data = cursor.fetchall()
            conn.commit()
    tables = [entry[0] for entry in data]
    return tables


def db_query_for_symbol(symbol: str, limit: int = 11, db_path: str =
                    "all_stocks.bk.db"
                    ):
    with closing(sqlite3.connect(db_path)) as conn:
        with closing(conn.cursor()) as cursor:
            # conn = sqlite3.connect(db_path)
            # cursor = conn.cursor()
            command = f"""
            SELECT * FROM `{symbol}` ORDER BY `date` desc limit {limit};
            """
            cursor.execute(command)
            data = cursor.fetchall()
            conn.commit()
    return data


def create_table(symbol: str, db_path: str =
"all_stocks.db"
                 ):
    """
        e.g.: # create_table("600900")
    """
    with closing(sqlite3.connect(db_path)) as conn:
        with closing(conn.cursor()) as cursor:
            # conn = sqlite3.connect(db_path)
            #
            # cursor = conn.cursor()
            command = f"""\
                create table if not exists `{symbol}` (
                    date TEXT PRIMARY KEY,
                    open_price REAL,
                    close_price REAL,
                    high REAL,
                    low REAL,
                    trade_amount INTEGER,
                    trade_capital REAL,
                    unknown_field REAL,
                    change_rate REAL,
                    abs_change_value REAL,
                    hand_change_rate REAL
                )
            """
            cursor.execute(command)

            conn.commit()
    # conn.close()

    # print(f"{symbol} table has been created into database: {db_path}")
    return


def insert_data_into_table(symbol: str, entries: list[tuple|list], db_path: str =
"all_stocks.db"
                           ):
    """
        this method is designed to insert history data into symbol tables
        e.g.:
            # insert_data_into_table("603119",
            #                        ["1990-12-19", 96.05, 99.98, 99.98, 95.79, 1260, 494000.00, 0.00, 0.00, 0.00, 0.00])
    """
    create_table(symbol, db_path)
    with closing(sqlite3.connect(db_path)) as conn:
        with closing(conn.cursor()) as cursor:
            # conn = sqlite3.connect(db_path)
            # cursor = conn.cursor()
            for entry in entries:
                command = f"""
                INSERT INTO `{symbol}` (date, open_price, close_price, high, low, trade_amount, trade_capital, unknown_field, change_rate, abs_change_value, hand_change_rate)
                VALUES ('{entry[0]}', {entry[1]}, {entry[2]}, {entry[3]}, {entry[4]}, {entry[5]}, {entry[6]}, {entry[7]}, {entry[8]}, {entry[9]}, {entry[10]});
            """
                cursor.execute(command)
            conn.commit()
            # conn.close()

    print(f"Entries have been inserted into table {symbol}")
    return


def query_data_from_table(symbol: str, db_path: str =
"all_stocks.db"
                          ):
    """
        e.g.:
            query_data_from_table("603119")
    """
    with closing(sqlite3.connect(db_path)) as conn:
        with closing(conn.cursor()) as cursor:
            # conn = sqlite3.connect(db_path)
            # cursor = conn.cursor()
            command = f"""
            SELECT * from `{symbol}`;
            """
            cursor.execute(command)
            data = cursor.fetchall()
            conn.commit()
    # conn.close()

    return data


def insert_latest_data_into_table(symbol: str, entry: tuple | list, db_path: str =
"all_stocks.db"
                           ):
    """
        this function is designed to insert one-day data into symbole database
        e.g.:
            # insert_data_into_table("603119",
            #                        ["1990-12-19", 96.05, 99.98, 99.98, 95.79, 1260, 494000.00, 0.00])
    """
    create_table(symbol, db_path)
    with closing(sqlite3.connect(db_path)) as conn:
        with closing(conn.cursor()) as cursor:
            # conn = sqlite3.connect(db_path)
            # cursor = conn.cursor()
            command = f"""
            INSERT INTO `{symbol}` (date, open_price, close_price, high, low, trade_amount, trade_capital, hand_change_rate)
            VALUES ('{entry[0]}', {entry[1]}, {entry[2]}, {entry[3]}, {entry[4]}, {entry[5]}, {entry[6]}, {entry[7]});
        """
            cursor.execute(command)
            conn.commit()
    # conn.close()

    print(f"{entry} has been inserted into table {symbol}")
    return
