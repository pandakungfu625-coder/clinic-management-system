# controllers/courses.py
# Handlers are responsible for dealing with HTTP details (headers, body, methods)

from core.responses import send_json, send_404
from core.request import parse_json_body
from services.course_service import (
    service_get_all,
    service_get_one,
    service_create,
    service_update,
    service_delete
)

def get_all_courses(handler):
    return send_json(handler, 200, service_get_all())

def get_course(handler, course_id):
    course = service_get_one(course_id)
    return send_json(handler, 200, course) if course else send_404(handler)

def create_course(handler):
    data = parse_json_body(handler)
    new_course = service_create(data)
    return send_json(handler, 201, new_course)

def update_course(handler, course_id):
    data = parse_json_body(handler)
    updated = service_update(course_id, data)
    return send_json(handler, 200, updated) if updated else send_404(handler)

def delete_course(handler, course_id):
    deleted = service_delete(course_id)
    return send_json(handler, 200, {"deleted": True}) if deleted else send_404(handler)