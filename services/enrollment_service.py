# services/enrollment_service.py
# Business logic for enrollments (no HTTP here)

from database.queries import (
    enrollments_get_all,
    enrollments_get_one,
    enrollments_create,
    enrollments_delete,
)

def service_get_all():
    return enrollments_get_all()

def service_get_one(enrollment_id):
    return enrollments_get_one(enrollment_id)

def service_create(data):
    return enrollments_create(data)

def service_delete(enrollment_id):
    return enrollments_delete(enrollment_id)