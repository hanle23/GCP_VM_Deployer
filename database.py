import mysql.connector
from mysql.connector import errorcode
import databaseconfig as cfg


def connect():
    try:
        database = mysql.connector.connect(
            host=cfg.mysql["host"], user=cfg.mysql["user"], password=cfg.mysql["password"], database=cfg.mysql["database"])
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        return database


def add():
    pass


def close(database):
    return database.close()
