from datetime import datetime
import mysql
from mysql.connector import errorcode
import databaseconfig as cfg


def connect() -> object:
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


def add(project_id: str, student_id: str, deploy_status: bool, zone_id: str, creation_time: datetime.date, changelog: str) -> None:
    connection = connect()
    my_cursor = connection.cursor()
    if not exist(project_id):
        query = "INSERT INTO student (project_id, student_id, deploy_status, zone_id, creation_date, changelog) VALUES (%s, %s, %d, ('SELECT zone_id FROM zone WHERE zone_name = %s'), %s, %s)"
        value = (project_id, student_id, deploy_status,
                 zone_id, creation_time, changelog)
        my_cursor.execute(query, value)
        connection.commit()
    else:
        query = "UPDATE student SET deploy_status = %d, zone_id = ('SELECT zone_id FROM zone WHERE zone_name = %s'), creation_time = %s, changelog = %s WHERE project_id = %s"
        value = (deploy_status, zone_id, creation_time, changelog, project_id)
        my_cursor.execute(query, value)
        connection.commit()


def exist(project_id: str) -> bool:
    connection = connect()
    my_cursor = connection.cursor()
    check_username = my_cursor.execute(
        'SELECT project_id FROM student WHERE project_id = %(project_id)s', (project_id))
    if check_username != 0:
        return False
    else:
        return True


def close(database) -> None:
    return database.close()
