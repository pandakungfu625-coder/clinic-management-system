# services/course_service.py
# Business logic for courses (no HTTP here)

from database.queries import (
    courses_get_all,
    courses_get_one,
    courses_create,
    courses_update,
    courses_delete,
)

def service_get_all():
    return courses_get_all()

def service_get_one(course_id):
    return courses_get_one(course_id)

def service_create(data):
    return courses_create(data)

def service_update(course_id, data):
    return courses_update(course_id, data)

def service_delete(course_id):
    return courses_delete(course_id)