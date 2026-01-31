# controllers/enrollments.py
# Handlers are responsible for dealing with HTTP details (headers, body, methods)

from core.responses import send_json, send_404
from core.request import parse_json_body
from services.enrollment_service import (
    service_get_all,
    service_get_one,
    service_create,
    service_delete
)

def get_all_enrollments(handler):
    return send_json(handler, 200, service_get_all())

def get_enrollment(handler, enrollment_id):
    enrollment = service_get_one(enrollment_id)
    return send_json(handler, 200, enrollment) if enrollment else send_404(handler)

def create_enrollment(handler):
    data = parse_json_body(handler)
    new_enrollment = service_create(data)
    return send_json(handler, 201, new_enrollment)

def delete_enrollment(handler, enrollment_id):
    deleted = service_delete(enrollment_id)
    return send_json(handler, 200, {"deleted": True}) if deleted else send_404(handler)