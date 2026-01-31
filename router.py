# router.py

from datetime import datetime
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

from controllers.reports import get_enrollment_report


# Clinic controllers
from controllers.patients import (
    get_all_patients,
    get_patient,
    create_patient,
    update_patient,
    delete_patient,
)

from controllers.doctors import (
    get_all_doctors,
    get_doctor,
    create_doctor,
    update_doctor,
    delete_doctor,
)

from controllers.appointments import (
    get_all_appointments,
    get_appointment,
    create_appointment,
    update_appointment,
    delete_appointment,
)

from controllers.invoices import (
    get_all_invoices,
    get_invoice,
    create_invoice,
    update_invoice,
    delete_invoice,
)

from core.static import serve_static
from core.responses import send_404, send_json
from core.middleware import add_cors_headers


# -------------------------------
# UI ROUTER (SPA shell + static)
# -------------------------------

FRONTEND_ROUTES = {
    "/", "/home",
    "/reports/enrollments",
    "/docs/flow", "/docs",
    "/profiles",
    # Clinic pages
    "/patients", "/doctors", "/appointments",
}

def handle_ui_routes(handler, path):
    # Exact SPA routes
    if path in FRONTEND_ROUTES:
        serve_static(handler, "frontend/pages/index.html")
        return True

    # Allow /something.html to map to SPA routes too
    if path.endswith(".html"):
        stripped = path.replace(".html", "")
        if stripped in FRONTEND_ROUTES:
            serve_static(handler, "frontend/pages/index.html")
            return True

    # Serve assets at /assets/... -> frontend/assets/...
    if path.startswith("/assets/"):
        serve_static(handler, "frontend" + path)
        return True

    # Serve anything under /frontend/ directly
    if path.startswith("/frontend/"):
        serve_static(handler, path.lstrip("/"))
        return True

    if path == "/openapi.yaml":
        serve_static(handler, "openapi.yaml")
        return True

    # Dynamic SPA routes (profiles pages)
    # e.g. /profiles/1 should still load index.html and let the SPA router decide
    if path.startswith("/profiles/"):
        serve_static(handler, "frontend/pages/index.html")
        return True

    return False


# -------------------------------
# Helpers
# -------------------------------

def _last_path_id_or_404(handler, path):
    """
    Extract the last path segment and ensure it's a number.
    If it's not a number, return None after sending 404 (no crash).
    """
    last = path.split("/")[-1]
    if not last.isdigit():
        send_404(handler)
        return None
    return int(last)


# -------------------------------
# MAIN ROUTER CLASS
# -------------------------------

class StudentRouter(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        add_cors_headers(self)
        self.end_headers()

    # ---------------------------
    # READ (GET)
    # ---------------------------
    def do_GET(self):
        path = urlparse(self.path).path

        # 1) UI routes first (SPA + static)
        if handle_ui_routes(self, path):
            return


        # ---------------------------
        # REPORTS (JOIN)
        # ---------------------------
        if path == "/api/reports/enrollments":
            return get_enrollment_report(self)

        # Clinic reports
        if path == "/api/reports/appointments":
            # Lazy import to avoid circular if necessary
            from database.queries import appointment_report
            return send_json(self, 200, appointment_report())

        # ---------------------------
        # PATIENTS
        # ---------------------------
        if path == "/api/patients":
            return get_all_patients(self)

        if path.startswith("/api/patients/"):
            patient_id = _last_path_id_or_404(self, path)
            if patient_id is None:
                return
            return get_patient(self, patient_id)

        # ---------------------------
        # DOCTORS
        # ---------------------------
        if path == "/api/doctors":
            return get_all_doctors(self)

        if path.startswith("/api/doctors/"):
            doctor_id = _last_path_id_or_404(self, path)
            if doctor_id is None:
                return
            return get_doctor(self, doctor_id)

        # ---------------------------
        # APPOINTMENTS
        # ---------------------------
        if path == "/api/appointments":
            return get_all_appointments(self)

        if path.startswith("/api/appointments/"):
            appointment_id = _last_path_id_or_404(self, path)
            if appointment_id is None:
                return
            return get_appointment(self, appointment_id)

        # ---------------------------
        # INVOICES
        # ---------------------------
        if path == "/api/invoices":
            return get_all_invoices(self)

        if path.startswith("/api/invoices/"):
            invoice_id = _last_path_id_or_404(self, path)
            if invoice_id is None:
                return
            return get_invoice(self, invoice_id)

        # If the path doesn't belong to the API or static assets, serve the SPA
        # This helps deep-linking like /profiles/123 work even when the server only
        # sees the direct request (typical in some deployment setups).
        if not path.startswith("/api/") and not path.startswith("/assets/") and not path.startswith("/frontend/") and path != "/openapi.yaml":
            serve_static(self, "frontend/pages/index.html")
            return

        return send_404(self)

    # ---------------------------
    # CREATE (POST)
    # ---------------------------
    def do_POST(self):
        path = urlparse(self.path).path


        # ---------------------------
        # PATIENTS
        # ---------------------------
        if path == "/api/patients":
            return create_patient(self)

        # ---------------------------
        # DOCTORS
        # ---------------------------
        if path == "/api/doctors":
            return create_doctor(self)

        # ---------------------------
        # APPOINTMENTS
        # ---------------------------
        if path == "/api/appointments":
            return create_appointment(self)

        # ---------------------------
        # INVOICES
        # ---------------------------
        if path == "/api/invoices":
            return create_invoice(self)

        return send_404(self)

    # ---------------------------
    # UPDATE (PUT)
    # ---------------------------
    def do_PUT(self):
        path = urlparse(self.path).path

        # ---------------------------
        # PATIENTS
        # ---------------------------
        if path.startswith("/api/patients/"):
            patient_id = _last_path_id_or_404(self, path)
            if patient_id is None:
                return
            return update_patient(self, patient_id)

        # ---------------------------
        # DOCTORS
        # ---------------------------
        if path.startswith("/api/doctors/"):
            doctor_id = _last_path_id_or_404(self, path)
            if doctor_id is None:
                return
            return update_doctor(self, doctor_id)

        # ---------------------------
        # APPOINTMENTS
        # ---------------------------
        if path.startswith("/api/appointments/"):
            appointment_id = _last_path_id_or_404(self, path)
            if appointment_id is None:
                return
            return update_appointment(self, appointment_id)

        # ---------------------------
        # INVOICES
        # ---------------------------
        if path.startswith("/api/invoices/"):
            invoice_id = _last_path_id_or_404(self, path)
            if invoice_id is None:
                return
            return update_invoice(self, invoice_id)

        return send_404(self)

    # ---------------------------
    # DELETE (DELETE)
    # ---------------------------
    def do_DELETE(self):
        path = urlparse(self.path).path


        # ---------------------------
        # PATIENTS
        # ---------------------------
        if path.startswith("/api/patients/"):
            patient_id = _last_path_id_or_404(self, path)
            if patient_id is None:
                return
            return delete_patient(self, patient_id)

        # ---------------------------
        # DOCTORS
        # ---------------------------
        if path.startswith("/api/doctors/"):
            doctor_id = _last_path_id_or_404(self, path)
            if doctor_id is None:
                return
            return delete_doctor(self, doctor_id)

        # ---------------------------
        # APPOINTMENTS
        # ---------------------------
        if path.startswith("/api/appointments/"):
            appointment_id = _last_path_id_or_404(self, path)
            if appointment_id is None:
                return
            return delete_appointment(self, appointment_id)

        # ---------------------------
        # INVOICES
        # ---------------------------
        if path.startswith("/api/invoices/"):
            invoice_id = _last_path_id_or_404(self, path)
            if invoice_id is None:
                return
            return delete_invoice(self, invoice_id)

        return send_404(self)

    def log_message(self, format, *args):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [Server] {format % args}")