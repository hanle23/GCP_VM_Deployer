from typing import Union
import requests
import json
import os

__all__ = ["get_student_list",
           "get_students_id",
           "get_student_id_txt"]


def get_student_list() -> json:
    url = ""
    response_API = requests.get(url)
    assert response_API.status_code == 200, "No response from URL"
    return response_API.json()


def get_students_id() -> json:
    students_id = []
    student_list = get_student_list()
    for student in student_list:
        students_id.append(student.get("person_number"))
    return students_id


def get_student_id_txt(file_name: str) -> list:
    student_list = []
    path = os.path.dirname(__file__)
    full_path = path + "\\data\\" + file_name
    open_file = open(full_path)
    student_list = open_file.read().split()
    open_file.close()
    return student_list
