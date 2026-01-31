import json
from core.responses import send_json, send_404
from core.request import parse_json_body
from services.invoice_service import (
    service_get_all,
    service_get_one,
    service_create,
    service_update,
    service_delete,
)


def get_all_invoices(handler):
    return send_json(handler, 200, service_get_all())


def get_invoice(handler, invoice_id):
    inv = service_get_one(invoice_id)
    return send_json(handler, 200, inv) if inv else send_404(handler)


def create_invoice(handler):
    data = parse_json_body(handler)
    new_inv = service_create(data)
    return send_json(handler, 201, new_inv)


def update_invoice(handler, invoice_id):
    data = parse_json_body(handler)
    updated = service_update(invoice_id, data)
    return send_json(handler, 200, updated) if updated else send_404(handler)


def delete_invoice(handler, invoice_id):
    deleted = service_delete(invoice_id)
    return send_json(handler, 200, {"deleted": True}) if deleted else send_404(handler)
