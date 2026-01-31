# Contains business logic (validation, processing, rules)
# Does NOT know about HTTP — only works with Python data

from database.queries import (
    students_get_all,
    students_get_one,
    students_create,
    students_update,
    students_delete,
)

def service_get_all():
    return students_get_all()

def service_get_one(student_id):
    return students_get_one(student_id)

def service_create(data):
    return students_create(data)

def service_update(student_id, data):
    return students_update(student_id, data)

def service_delete(student_id):
    return students_delete(student_id)