import requests
import json
url = ""


def get_student_list():
    response_API = requests.get(url)
    assert response_API.status_code == 200, "No response from URL"
    return response_API.json()


def get_students_id():
    students_id = []
    student_list = get_student_list()
    for student in student_list:
        students_id.append(student.get("person_number"))
    return students_id
