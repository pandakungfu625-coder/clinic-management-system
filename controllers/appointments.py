# controllers/appointments.py
# DEPRECATED: appointments endpoints renamed to billing and now forward to invoices.
# See controllers/billing.py and services/billing_service.py

import json
from core.responses import send_json


def get_all_appointments(handler):
    return send_json(handler, 410, {"error": "appointments endpoints replaced by /api/billing"})


def get_appointment(handler, appointment_id):
    return send_json(handler, 410, {"error": "appointments endpoints replaced by /api/billing"})


def create_appointment(handler):
    return send_json(handler, 410, {"error": "appointments endpoints replaced by /api/billing"})


def update_appointment(handler, appointment_id):
    return send_json(handler, 410, {"error": "appointments endpoints replaced by /api/billing"})


def delete_appointment(handler, appointment_id):
    return send_json(handler, 410, {"error": "appointments endpoints replaced by /api/billing"})
