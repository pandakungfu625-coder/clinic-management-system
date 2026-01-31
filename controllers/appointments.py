import json
from core.responses import send_json, send_404
from core.request import parse_json_body
from services.appointment_service import (
    service_get_all,
    service_get_one,
    service_create,
    service_update,
    service_delete,
)


def get_all_appointments(handler):
    return send_json(handler, 200, service_get_all())


def get_appointment(handler, appointment_id):
    appt = service_get_one(appointment_id)
    return send_json(handler, 200, appt) if appt else send_404(handler)


def create_appointment(handler):
    data = parse_json_body(handler)
    new_appt = service_create(data)
    return send_json(handler, 201, new_appt)


def update_appointment(handler, appointment_id):
    data = parse_json_body(handler)
    updated = service_update(appointment_id, data)
    return send_json(handler, 200, updated) if updated else send_404(handler)


def delete_appointment(handler, appointment_id):
    deleted = service_delete(appointment_id)
    return send_json(handler, 200, {"deleted": True}) if deleted else send_404(handler)
